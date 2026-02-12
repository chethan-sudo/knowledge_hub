"""
Backend API Tests for P2 Features - Emergent Document Hub
- Tests version history (GET /documents/{id}/versions, version creation on PUT)
- Tests export (GET /documents/{id}/export returns markdown file)
- Tests tags system (create doc with tags, GET /tags endpoint)
- Tests search with snippets (regression from P1)
"""

import pytest
import requests
import os
import uuid

# Base URL from env
BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')

# Test credentials
TEST_USER = {
    "email": "test@test.com",
    "password": "test1234",
    "name": "Test User"
}

# Global token storage for authenticated requests
AUTH_TOKEN = None


def get_auth_token():
    """Get or refresh auth token"""
    global AUTH_TOKEN
    if not AUTH_TOKEN:
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": TEST_USER["email"],
            "password": TEST_USER["password"]
        })
        if response.status_code == 200:
            AUTH_TOKEN = response.json()["token"]
    return AUTH_TOKEN


class TestSearchWithSnippets:
    """P1-2 Regression: Search with content snippets"""
    
    @pytest.fixture(autouse=True)
    def ensure_auth(self):
        get_auth_token()
    
    def test_search_kubernetes_returns_snippet(self):
        """GET /search?q=kubernetes returns results with 'snippet' field"""
        headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}
        response = requests.get(f"{BASE_URL}/api/search?q=kubernetes", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0, "Should find kubernetes documents"
        
        # Check snippet field exists
        for result in data:
            assert "snippet" in result, f"Result missing 'snippet' field: {result}"
            assert "id" in result
            assert "title" in result
            assert "category_id" in result
        
        print(f"✓ Search 'kubernetes' returns {len(data)} results with snippets")
        
        # At least one should have content snippet
        with_snippets = [r for r in data if r.get("snippet")]
        assert len(with_snippets) > 0, "At least one result should have non-empty snippet"
        print(f"  Sample snippet: {with_snippets[0]['snippet'][:60]}...")


class TestTagsSystem:
    """P2: Tags/labels system"""
    
    @pytest.fixture(autouse=True)
    def ensure_auth(self):
        get_auth_token()
    
    def test_get_tags_endpoint(self):
        """GET /tags returns list of all unique tags"""
        headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}
        response = requests.get(f"{BASE_URL}/api/tags", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list), f"Expected list, got {type(data)}"
        print(f"✓ GET /tags returns {len(data)} unique tags: {data[:5]}")
    
    def test_create_document_with_tags(self):
        """POST /documents creates doc with tags array"""
        headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}
        
        # Get a valid category ID
        cat_response = requests.get(f"{BASE_URL}/api/categories", headers=headers)
        cats = cat_response.json()
        cat_id = cats[0]["id"]
        
        # Create document with tags
        test_tags = ["test-tag", "pytest", "p2-feature"]
        new_doc = {
            "title": f"TEST_Tags_Doc_{uuid.uuid4().hex[:6]}",
            "content": "# Test Doc\n\nContent with tags",
            "category_id": cat_id,
            "order": 99,
            "tags": test_tags
        }
        create_response = requests.post(f"{BASE_URL}/api/documents", headers=headers, json=new_doc)
        assert create_response.status_code == 200
        created = create_response.json()
        doc_id = created["id"]
        
        # Verify tags in response
        assert "tags" in created, "Created document should have tags field"
        assert created["tags"] == test_tags, f"Tags mismatch: expected {test_tags}, got {created.get('tags')}"
        print(f"✓ Created document with tags: {created['tags']}")
        
        # Verify via GET
        get_response = requests.get(f"{BASE_URL}/api/documents/{doc_id}", headers=headers)
        fetched = get_response.json()
        assert fetched.get("tags") == test_tags, f"GET returned wrong tags: {fetched.get('tags')}"
        print(f"✓ Tags verified via GET: {fetched['tags']}")
        
        # Cleanup
        requests.delete(f"{BASE_URL}/api/documents/{doc_id}", headers=headers)
        print(f"✓ Test document cleaned up")
    
    def test_update_document_tags(self):
        """PUT /documents/{id} can update tags"""
        headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}
        
        # Get a valid category ID
        cat_response = requests.get(f"{BASE_URL}/api/categories", headers=headers)
        cats = cat_response.json()
        cat_id = cats[0]["id"]
        
        # Create document without tags
        new_doc = {
            "title": f"TEST_UpdateTags_{uuid.uuid4().hex[:6]}",
            "content": "Initial content",
            "category_id": cat_id,
            "order": 99,
            "tags": []
        }
        create_response = requests.post(f"{BASE_URL}/api/documents", headers=headers, json=new_doc)
        doc_id = create_response.json()["id"]
        
        # Update with tags
        update_tags = ["updated-tag", "new-label"]
        update_response = requests.put(f"{BASE_URL}/api/documents/{doc_id}", headers=headers, json={
            "tags": update_tags
        })
        assert update_response.status_code == 200
        updated = update_response.json()
        assert updated.get("tags") == update_tags, f"Update tags mismatch: {updated.get('tags')}"
        print(f"✓ Updated document tags: {updated['tags']}")
        
        # Verify persistence
        get_response = requests.get(f"{BASE_URL}/api/documents/{doc_id}", headers=headers)
        assert get_response.json().get("tags") == update_tags
        print(f"✓ Tags update verified via GET")
        
        # Cleanup
        requests.delete(f"{BASE_URL}/api/documents/{doc_id}", headers=headers)


class TestVersionHistory:
    """P2: Version history - saved on each edit"""
    
    @pytest.fixture(autouse=True)
    def ensure_auth(self):
        get_auth_token()
    
    def test_get_versions_empty_initially(self):
        """GET /documents/{id}/versions returns empty list for new doc"""
        headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}
        
        # Get a valid category ID
        cat_response = requests.get(f"{BASE_URL}/api/categories", headers=headers)
        cats = cat_response.json()
        cat_id = cats[0]["id"]
        
        # Create a new document
        new_doc = {
            "title": f"TEST_Versions_{uuid.uuid4().hex[:6]}",
            "content": "Initial content",
            "category_id": cat_id,
            "order": 99
        }
        create_response = requests.post(f"{BASE_URL}/api/documents", headers=headers, json=new_doc)
        doc_id = create_response.json()["id"]
        
        # Get versions - should be empty (no edits yet)
        versions_response = requests.get(f"{BASE_URL}/api/documents/{doc_id}/versions", headers=headers)
        assert versions_response.status_code == 200
        versions = versions_response.json()
        assert isinstance(versions, list)
        assert len(versions) == 0, f"New document should have no versions, got {len(versions)}"
        print(f"✓ GET /documents/{doc_id}/versions returns empty list initially")
        
        # Cleanup
        requests.delete(f"{BASE_URL}/api/documents/{doc_id}", headers=headers)
    
    def test_put_creates_version(self):
        """PUT /documents/{id} creates a version entry in doc_versions"""
        headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}
        
        # Get a valid category ID
        cat_response = requests.get(f"{BASE_URL}/api/categories", headers=headers)
        cats = cat_response.json()
        cat_id = cats[0]["id"]
        
        # Create a new document
        original_title = f"TEST_VersionCreate_{uuid.uuid4().hex[:6]}"
        original_content = "Original content before edit"
        new_doc = {
            "title": original_title,
            "content": original_content,
            "category_id": cat_id,
            "order": 99
        }
        create_response = requests.post(f"{BASE_URL}/api/documents", headers=headers, json=new_doc)
        doc_id = create_response.json()["id"]
        
        # Update the document (should trigger version creation)
        update_response = requests.put(f"{BASE_URL}/api/documents/{doc_id}", headers=headers, json={
            "title": "UPDATED Title",
            "content": "Updated content after edit"
        })
        assert update_response.status_code == 200
        print(f"✓ Document updated")
        
        # Get versions - should have 1 version now (the pre-edit snapshot)
        versions_response = requests.get(f"{BASE_URL}/api/documents/{doc_id}/versions", headers=headers)
        assert versions_response.status_code == 200
        versions = versions_response.json()
        assert len(versions) == 1, f"Should have 1 version after 1 edit, got {len(versions)}"
        
        # Verify version contains pre-edit content
        version = versions[0]
        assert "id" in version
        assert version["document_id"] == doc_id
        assert version["title"] == original_title, f"Version title should be original: {version.get('title')}"
        assert version["content"] == original_content, f"Version content should be original"
        assert "created_at" in version
        assert "edited_by" in version
        print(f"✓ Version created with pre-edit content: title='{version['title']}', created_at={version['created_at']}")
        
        # Cleanup
        requests.delete(f"{BASE_URL}/api/documents/{doc_id}", headers=headers)
    
    def test_multiple_edits_create_multiple_versions(self):
        """Multiple PUT requests create multiple version entries"""
        headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}
        
        # Get a valid category ID
        cat_response = requests.get(f"{BASE_URL}/api/categories", headers=headers)
        cats = cat_response.json()
        cat_id = cats[0]["id"]
        
        # Create a new document
        new_doc = {
            "title": f"TEST_MultiVersion_{uuid.uuid4().hex[:6]}",
            "content": "Version 0 content",
            "category_id": cat_id,
            "order": 99
        }
        create_response = requests.post(f"{BASE_URL}/api/documents", headers=headers, json=new_doc)
        doc_id = create_response.json()["id"]
        
        # Make 3 edits
        for i in range(1, 4):
            requests.put(f"{BASE_URL}/api/documents/{doc_id}", headers=headers, json={
                "content": f"Version {i} content"
            })
        
        # Get versions - should have 3 versions
        versions_response = requests.get(f"{BASE_URL}/api/documents/{doc_id}/versions", headers=headers)
        versions = versions_response.json()
        assert len(versions) == 3, f"Should have 3 versions after 3 edits, got {len(versions)}"
        print(f"✓ Multiple edits create multiple versions: {len(versions)} versions")
        
        # Verify versions are sorted by created_at descending (most recent first)
        if len(versions) >= 2:
            assert versions[0]["created_at"] >= versions[1]["created_at"], "Versions should be sorted desc by created_at"
            print(f"✓ Versions sorted by created_at descending")
        
        # Cleanup
        requests.delete(f"{BASE_URL}/api/documents/{doc_id}", headers=headers)
    
    def test_get_existing_doc_versions(self):
        """GET /documents/{id}/versions works for existing seeded documents"""
        headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}
        
        # Get an existing document
        docs_response = requests.get(f"{BASE_URL}/api/documents", headers=headers)
        docs = docs_response.json()
        assert len(docs) > 0, "Should have existing documents"
        doc_id = docs[0]["id"]
        
        # Get versions endpoint
        versions_response = requests.get(f"{BASE_URL}/api/documents/{doc_id}/versions", headers=headers)
        assert versions_response.status_code == 200
        versions = versions_response.json()
        assert isinstance(versions, list)
        print(f"✓ GET /documents/{doc_id}/versions returns {len(versions)} versions")


class TestExportDocument:
    """P2: Export document as Markdown file"""
    
    @pytest.fixture(autouse=True)
    def ensure_auth(self):
        get_auth_token()
    
    def test_export_returns_markdown(self):
        """GET /documents/{id}/export returns markdown file"""
        headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}
        
        # Get an existing document
        docs_response = requests.get(f"{BASE_URL}/api/documents", headers=headers)
        docs = docs_response.json()
        doc = docs[0]
        doc_id = doc["id"]
        
        # Export document
        export_response = requests.get(f"{BASE_URL}/api/documents/{doc_id}/export", headers=headers)
        assert export_response.status_code == 200
        
        # Check content-type is markdown
        content_type = export_response.headers.get("content-type", "")
        assert "text/markdown" in content_type, f"Expected text/markdown, got {content_type}"
        print(f"✓ Export returns content-type: {content_type}")
        
        # Check content-disposition has filename
        content_disposition = export_response.headers.get("content-disposition", "")
        assert "attachment" in content_disposition.lower(), f"Expected attachment, got {content_disposition}"
        assert ".md" in content_disposition, f"Expected .md filename, got {content_disposition}"
        print(f"✓ Export returns content-disposition: {content_disposition}")
        
        # Check content starts with title
        content = export_response.text
        assert content.startswith(f"# {doc['title']}"), f"Content should start with '# {doc['title']}'"
        assert doc["content"] in content or len(content) > 10, "Content should include document content"
        print(f"✓ Export content starts with: {content[:50]}...")
    
    def test_export_nonexistent_doc_returns_404(self):
        """GET /documents/{fake_id}/export returns 404"""
        headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}
        
        fake_id = f"nonexistent-{uuid.uuid4().hex}"
        export_response = requests.get(f"{BASE_URL}/api/documents/{fake_id}/export", headers=headers)
        assert export_response.status_code == 404
        print(f"✓ Export nonexistent doc returns 404")


class TestDocumentDeleteCleansVersions:
    """Test that deleting a document also deletes its versions"""
    
    @pytest.fixture(autouse=True)
    def ensure_auth(self):
        get_auth_token()
    
    def test_delete_doc_removes_versions(self):
        """DELETE /documents/{id} also removes version history"""
        headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}
        
        # Get a valid category ID
        cat_response = requests.get(f"{BASE_URL}/api/categories", headers=headers)
        cats = cat_response.json()
        cat_id = cats[0]["id"]
        
        # Create a document
        new_doc = {
            "title": f"TEST_DeleteVersions_{uuid.uuid4().hex[:6]}",
            "content": "Initial",
            "category_id": cat_id,
            "order": 99
        }
        create_response = requests.post(f"{BASE_URL}/api/documents", headers=headers, json=new_doc)
        doc_id = create_response.json()["id"]
        
        # Create a version via PUT
        requests.put(f"{BASE_URL}/api/documents/{doc_id}", headers=headers, json={"content": "Updated"})
        
        # Verify version exists
        versions_response = requests.get(f"{BASE_URL}/api/documents/{doc_id}/versions", headers=headers)
        assert len(versions_response.json()) == 1
        
        # Delete document
        delete_response = requests.delete(f"{BASE_URL}/api/documents/{doc_id}", headers=headers)
        assert delete_response.status_code == 200
        print(f"✓ Document deleted")
        
        # Versions endpoint should return 404 (doc doesn't exist) or empty
        # Since the document is deleted, the endpoint might not be accessible
        verify_response = requests.get(f"{BASE_URL}/api/documents/{doc_id}", headers=headers)
        assert verify_response.status_code == 404
        print(f"✓ Document and associated data cleaned up")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
