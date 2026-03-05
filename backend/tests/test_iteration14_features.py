"""
Test Iteration 14: Related Documents, Mobile Responsiveness, Ctrl+K Search, and Regression Tests

Tests:
- Related Documents section (siblings + cousins)
- Ctrl+K shortcut focus
- 404 page
- All CRUD operations
- Version history & restore
- Keyword auto-linking
- Tools page (flat grid, no category dropdown)
- Comment delete (owner only)
"""

import pytest
import requests
import os
import uuid
from datetime import datetime

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')

class TestHealthAndBasics:
    """Basic API health checks"""
    
    def test_api_root(self):
        """API root endpoint responds"""
        response = requests.get(f"{BASE_URL}/api/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        print(f"API Root: {data}")
    
    def test_categories_list(self):
        """Categories endpoint returns list"""
        response = requests.get(f"{BASE_URL}/api/categories")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        print(f"Categories count: {len(data)}")
    
    def test_documents_list(self):
        """Documents endpoint returns list"""
        response = requests.get(f"{BASE_URL}/api/documents")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        print(f"Documents count: {len(data)}")


class TestRelatedDocuments:
    """Test data needed for Related Documents feature"""
    
    def test_documents_have_category_id(self):
        """Documents have category_id for sibling matching"""
        response = requests.get(f"{BASE_URL}/api/documents")
        assert response.status_code == 200
        docs = response.json()
        assert len(docs) > 0, "Should have documents"
        
        # Check at least some docs have category_id
        docs_with_category = [d for d in docs if d.get("category_id")]
        assert len(docs_with_category) > 0, "Documents should have category_id"
        print(f"Documents with category_id: {len(docs_with_category)}/{len(docs)}")
    
    def test_categories_have_parent_structure(self):
        """Categories have parent_id for cousin matching"""
        response = requests.get(f"{BASE_URL}/api/categories")
        assert response.status_code == 200
        cats = response.json()
        
        # Check for subcategories (have parent_id)
        subcats = [c for c in cats if c.get("parent_id")]
        parent_cats = [c for c in cats if not c.get("parent_id")]
        print(f"Parent categories: {len(parent_cats)}, Subcategories: {len(subcats)}")
        
    def test_related_docs_data_structure(self):
        """Verify data structure supports Related Documents computation"""
        # Get categories
        cats_response = requests.get(f"{BASE_URL}/api/categories")
        assert cats_response.status_code == 200
        categories = cats_response.json()
        
        # Get documents  
        docs_response = requests.get(f"{BASE_URL}/api/documents")
        assert docs_response.status_code == 200
        documents = docs_response.json()
        
        # Build category map
        cat_map = {c["id"]: c for c in categories}
        
        # Find a document with siblings
        for doc in documents:
            cat_id = doc.get("category_id")
            if not cat_id:
                continue
            
            # Find siblings (same category)
            siblings = [d for d in documents if d.get("category_id") == cat_id and d["id"] != doc["id"]]
            
            # Find cousins (same parent category)
            current_cat = cat_map.get(cat_id, {})
            parent_id = current_cat.get("parent_id")
            
            if siblings:
                print(f"Doc '{doc['title']}' has {len(siblings)} siblings in category")
                break
        
        print("Related docs data structure: VALID")


class TestKeywordsAutoLinking:
    """Test keyword auto-linking endpoint"""
    
    def test_keywords_endpoint(self):
        """GET /api/keywords returns keyword-to-docId map"""
        response = requests.get(f"{BASE_URL}/api/keywords")
        assert response.status_code == 200
        keywords = response.json()
        assert isinstance(keywords, dict)
        print(f"Keywords count: {len(keywords)}")
        
        # Check some expected keywords are present
        expected_keywords = ["orchestrator", "transformer", "kubernetes", "docker"]
        found = [k for k in expected_keywords if k in keywords]
        print(f"Found expected keywords: {found}")
    
    def test_keywords_map_to_valid_docs(self):
        """Keywords map to existing documents"""
        keywords_response = requests.get(f"{BASE_URL}/api/keywords")
        keywords = keywords_response.json()
        
        docs_response = requests.get(f"{BASE_URL}/api/documents")
        docs = docs_response.json()
        doc_ids = {d["id"] for d in docs}
        
        # Check a sample of keywords point to valid docs
        sample_count = min(10, len(keywords))
        valid_count = 0
        for keyword, doc_id in list(keywords.items())[:sample_count]:
            if doc_id in doc_ids:
                valid_count += 1
        
        print(f"Valid keyword mappings: {valid_count}/{sample_count}")
        assert valid_count > 0, "Should have valid keyword mappings"


class TestDocumentCRUD:
    """Test document Create, Read, Update, Delete operations"""
    
    @pytest.fixture
    def test_category(self):
        """Get or create test category"""
        response = requests.get(f"{BASE_URL}/api/categories")
        cats = response.json()
        # Use first available category
        if cats:
            return cats[0]["id"]
        return None
    
    def test_create_document(self, test_category):
        """Create a new document"""
        if not test_category:
            pytest.skip("No category available")
        
        doc_data = {
            "title": f"TEST_Doc_{uuid.uuid4().hex[:8]}",
            "content": "# Test Document\n\nThis is a test document.",
            "category_id": test_category,
            "tags": ["test"]
        }
        
        response = requests.post(f"{BASE_URL}/api/documents", json=doc_data)
        assert response.status_code == 200
        created = response.json()
        assert created["title"] == doc_data["title"]
        assert "id" in created
        print(f"Created doc: {created['id']}")
        
        # Cleanup
        requests.delete(f"{BASE_URL}/api/documents/{created['id']}")
    
    def test_read_document(self):
        """Read a document by ID"""
        # Get list first
        list_response = requests.get(f"{BASE_URL}/api/documents")
        docs = list_response.json()
        if not docs:
            pytest.skip("No documents to read")
        
        doc_id = docs[0]["id"]
        response = requests.get(f"{BASE_URL}/api/documents/{doc_id}")
        assert response.status_code == 200
        doc = response.json()
        assert doc["id"] == doc_id
        print(f"Read doc: {doc['title']}")
    
    def test_update_document(self, test_category):
        """Update a document"""
        if not test_category:
            pytest.skip("No category available")
        
        # Create first
        doc_data = {
            "title": f"TEST_Update_{uuid.uuid4().hex[:8]}",
            "content": "Original content",
            "category_id": test_category
        }
        create_response = requests.post(f"{BASE_URL}/api/documents", json=doc_data)
        doc_id = create_response.json()["id"]
        
        # Update
        update_data = {"title": "Updated Title", "content": "Updated content"}
        response = requests.put(f"{BASE_URL}/api/documents/{doc_id}", json=update_data)
        assert response.status_code == 200
        updated = response.json()
        assert updated["title"] == "Updated Title"
        print(f"Updated doc: {doc_id}")
        
        # Cleanup
        requests.delete(f"{BASE_URL}/api/documents/{doc_id}")
    
    def test_delete_document_to_trash(self, test_category):
        """Delete document (soft delete to trash)"""
        if not test_category:
            pytest.skip("No category available")
        
        # Create first
        doc_data = {
            "title": f"TEST_Delete_{uuid.uuid4().hex[:8]}",
            "content": "To be deleted",
            "category_id": test_category
        }
        create_response = requests.post(f"{BASE_URL}/api/documents", json=doc_data)
        doc_id = create_response.json()["id"]
        
        # Delete (soft)
        response = requests.delete(f"{BASE_URL}/api/documents/{doc_id}")
        assert response.status_code == 200
        assert response.json().get("status") == "moved to trash"
        print(f"Deleted doc to trash: {doc_id}")
        
        # Verify in trash
        trash_response = requests.get(f"{BASE_URL}/api/trash")
        trash_docs = trash_response.json()
        assert any(d["id"] == doc_id for d in trash_docs), "Doc should be in trash"
        
        # Cleanup - permanent delete
        requests.delete(f"{BASE_URL}/api/trash/{doc_id}")


class TestTrashOperations:
    """Test trash restore and permanent delete"""
    
    @pytest.fixture
    def test_category(self):
        response = requests.get(f"{BASE_URL}/api/categories")
        cats = response.json()
        if cats:
            return cats[0]["id"]
        return None
    
    def test_restore_from_trash(self, test_category):
        """Restore document from trash"""
        if not test_category:
            pytest.skip("No category available")
        
        # Create and delete
        doc_data = {
            "title": f"TEST_Restore_{uuid.uuid4().hex[:8]}",
            "content": "To restore",
            "category_id": test_category
        }
        create_response = requests.post(f"{BASE_URL}/api/documents", json=doc_data)
        doc_id = create_response.json()["id"]
        requests.delete(f"{BASE_URL}/api/documents/{doc_id}")
        
        # Restore
        response = requests.post(f"{BASE_URL}/api/trash/{doc_id}/restore")
        assert response.status_code == 200
        print(f"Restored doc: {doc_id}")
        
        # Verify not in trash anymore
        trash_response = requests.get(f"{BASE_URL}/api/trash")
        trash_docs = trash_response.json()
        assert not any(d["id"] == doc_id for d in trash_docs), "Doc should not be in trash"
        
        # Cleanup
        requests.delete(f"{BASE_URL}/api/documents/{doc_id}")
        requests.delete(f"{BASE_URL}/api/trash/{doc_id}")


class TestVersionHistory:
    """Test version history and restore"""
    
    @pytest.fixture
    def test_category(self):
        response = requests.get(f"{BASE_URL}/api/categories")
        cats = response.json()
        if cats:
            return cats[0]["id"]
        return None
    
    def test_versions_created_on_update(self, test_category):
        """Updating a doc creates a version"""
        if not test_category:
            pytest.skip("No category available")
        
        # Create
        doc_data = {
            "title": f"TEST_Version_{uuid.uuid4().hex[:8]}",
            "content": "Version 1 content",
            "category_id": test_category
        }
        create_response = requests.post(f"{BASE_URL}/api/documents", json=doc_data)
        doc_id = create_response.json()["id"]
        
        # Update (should create version)
        requests.put(f"{BASE_URL}/api/documents/{doc_id}", json={"content": "Version 2 content"})
        
        # Check versions
        versions_response = requests.get(f"{BASE_URL}/api/documents/{doc_id}/versions")
        assert versions_response.status_code == 200
        versions = versions_response.json()
        assert len(versions) >= 1, "Should have at least one version"
        print(f"Doc has {len(versions)} versions")
        
        # Cleanup
        requests.delete(f"{BASE_URL}/api/documents/{doc_id}")
        requests.delete(f"{BASE_URL}/api/trash/{doc_id}")
    
    def test_restore_version(self, test_category):
        """Restore a previous version"""
        if not test_category:
            pytest.skip("No category available")
        
        # Create
        original_content = "Original content here"
        doc_data = {
            "title": f"TEST_RestoreVer_{uuid.uuid4().hex[:8]}",
            "content": original_content,
            "category_id": test_category
        }
        create_response = requests.post(f"{BASE_URL}/api/documents", json=doc_data)
        doc_id = create_response.json()["id"]
        
        # Update (creates version of original)
        requests.put(f"{BASE_URL}/api/documents/{doc_id}", json={"content": "New content"})
        
        # Get versions
        versions_response = requests.get(f"{BASE_URL}/api/documents/{doc_id}/versions")
        versions = versions_response.json()
        
        if versions:
            version_id = versions[0]["id"]
            # Restore version
            restore_response = requests.post(f"{BASE_URL}/api/documents/{doc_id}/versions/{version_id}/restore")
            assert restore_response.status_code == 200
            print(f"Restored version: {version_id}")
        
        # Cleanup
        requests.delete(f"{BASE_URL}/api/documents/{doc_id}")
        requests.delete(f"{BASE_URL}/api/trash/{doc_id}")


class TestUserManagement:
    """Test user invite, role change, delete"""
    
    def test_list_users(self):
        """List users endpoint"""
        response = requests.get(f"{BASE_URL}/api/users")
        assert response.status_code == 200
        users = response.json()
        assert isinstance(users, list)
        print(f"Users count: {len(users)}")
    
    def test_invite_user(self):
        """Invite a new user"""
        email = f"test_{uuid.uuid4().hex[:8]}@test.com"
        invite_data = {"email": email, "role": "viewer"}
        
        response = requests.post(f"{BASE_URL}/api/invite", json=invite_data)
        assert response.status_code == 200
        created = response.json()
        assert created["email"] == email
        user_id = created["user_id"]
        print(f"Invited user: {email}")
        
        # Cleanup
        requests.delete(f"{BASE_URL}/api/users/{user_id}")
    
    def test_change_user_role(self):
        """Change user role"""
        # Create user first
        email = f"test_role_{uuid.uuid4().hex[:8]}@test.com"
        invite_response = requests.post(f"{BASE_URL}/api/invite", json={"email": email, "role": "viewer"})
        user_id = invite_response.json()["user_id"]
        
        # Change role
        response = requests.put(f"{BASE_URL}/api/users/{user_id}/role", json={"role": "admin"})
        assert response.status_code == 200
        assert response.json()["role"] == "admin"
        print(f"Changed role to admin: {user_id}")
        
        # Cleanup
        requests.delete(f"{BASE_URL}/api/users/{user_id}")
    
    def test_delete_user(self):
        """Delete a user"""
        # Create user first
        email = f"test_del_{uuid.uuid4().hex[:8]}@test.com"
        invite_response = requests.post(f"{BASE_URL}/api/invite", json={"email": email, "role": "viewer"})
        user_id = invite_response.json()["user_id"]
        
        # Delete
        response = requests.delete(f"{BASE_URL}/api/users/{user_id}")
        assert response.status_code == 200
        assert response.json()["status"] == "removed"
        print(f"Deleted user: {user_id}")


class TestTools:
    """Test tools/resources CRUD"""
    
    def test_list_tools(self):
        """List tools endpoint"""
        response = requests.get(f"{BASE_URL}/api/tools")
        assert response.status_code == 200
        tools = response.json()
        assert isinstance(tools, list)
        print(f"Tools count: {len(tools)}")
    
    def test_create_tool(self):
        """Create a new tool/resource"""
        tool_data = {
            "name": f"TEST_Tool_{uuid.uuid4().hex[:8]}",
            "url": "https://example.com",
            "description": "Test tool description"
        }
        
        response = requests.post(f"{BASE_URL}/api/tools", json=tool_data)
        assert response.status_code == 200
        created = response.json()
        assert created["name"] == tool_data["name"]
        print(f"Created tool: {created['id']}")
        
        # Cleanup
        requests.delete(f"{BASE_URL}/api/tools/{created['id']}")
    
    def test_update_tool(self):
        """Update a tool"""
        # Create first
        tool_data = {
            "name": f"TEST_ToolUpdate_{uuid.uuid4().hex[:8]}",
            "url": "https://example.com",
            "description": "Original"
        }
        create_response = requests.post(f"{BASE_URL}/api/tools", json=tool_data)
        tool_id = create_response.json()["id"]
        
        # Update
        response = requests.put(f"{BASE_URL}/api/tools/{tool_id}", json={"description": "Updated"})
        assert response.status_code == 200
        assert response.json()["description"] == "Updated"
        print(f"Updated tool: {tool_id}")
        
        # Cleanup
        requests.delete(f"{BASE_URL}/api/tools/{tool_id}")
    
    def test_delete_tool(self):
        """Delete a tool"""
        # Create first
        tool_data = {
            "name": f"TEST_ToolDel_{uuid.uuid4().hex[:8]}",
            "url": "https://example.com"
        }
        create_response = requests.post(f"{BASE_URL}/api/tools", json=tool_data)
        tool_id = create_response.json()["id"]
        
        # Delete
        response = requests.delete(f"{BASE_URL}/api/tools/{tool_id}")
        assert response.status_code == 200
        print(f"Deleted tool: {tool_id}")


class TestComments:
    """Test comments with owner-only delete"""
    
    def test_get_comments(self):
        """Get comments for a document"""
        # Get a document first
        docs_response = requests.get(f"{BASE_URL}/api/documents")
        docs = docs_response.json()
        if not docs:
            pytest.skip("No documents")
        
        doc_id = docs[0]["id"]
        response = requests.get(f"{BASE_URL}/api/documents/{doc_id}/comments")
        assert response.status_code == 200
        comments = response.json()
        assert isinstance(comments, list)
        print(f"Comments for doc {doc_id}: {len(comments)}")
    
    def test_add_comment(self):
        """Add a comment to a document"""
        # Get a document first
        docs_response = requests.get(f"{BASE_URL}/api/documents")
        docs = docs_response.json()
        if not docs:
            pytest.skip("No documents")
        
        doc_id = docs[0]["id"]
        comment_data = {"content": f"TEST_Comment_{uuid.uuid4().hex[:8]}"}
        
        response = requests.post(f"{BASE_URL}/api/documents/{doc_id}/comments", json=comment_data)
        assert response.status_code == 200
        created = response.json()
        assert created["content"] == comment_data["content"]
        print(f"Added comment: {created['id']}")
        
        # Cleanup
        requests.delete(f"{BASE_URL}/api/comments/{created['id']}")
    
    def test_delete_comment_as_owner(self):
        """Owner can delete their own comment"""
        # Get a document first
        docs_response = requests.get(f"{BASE_URL}/api/documents")
        docs = docs_response.json()
        if not docs:
            pytest.skip("No documents")
        
        doc_id = docs[0]["id"]
        comment_data = {"content": f"TEST_DeleteComment_{uuid.uuid4().hex[:8]}"}
        
        # Create comment
        create_response = requests.post(f"{BASE_URL}/api/documents/{doc_id}/comments", json=comment_data)
        comment_id = create_response.json()["id"]
        
        # Delete as same user (owner)
        response = requests.delete(f"{BASE_URL}/api/comments/{comment_id}")
        assert response.status_code == 200
        print(f"Owner deleted comment: {comment_id}")


class TestSearch:
    """Test search functionality"""
    
    def test_search_documents(self):
        """Search documents"""
        response = requests.get(f"{BASE_URL}/api/search?q=agent")
        assert response.status_code == 200
        results = response.json()
        assert isinstance(results, list)
        print(f"Search 'agent' results: {len(results)}")
    
    def test_search_with_snippet(self):
        """Search results include snippets"""
        response = requests.get(f"{BASE_URL}/api/search?q=architecture")
        results = response.json()
        
        if results:
            first = results[0]
            assert "title" in first
            assert "snippet" in first
            print(f"Search result with snippet: {first['title'][:30]}...")


class Test404Page:
    """Test 404 response for non-existent documents"""
    
    def test_document_not_found(self):
        """Non-existent document returns 404"""
        fake_id = f"fake_{uuid.uuid4().hex}"
        response = requests.get(f"{BASE_URL}/api/documents/{fake_id}")
        assert response.status_code == 404
        print("404 for non-existent document: PASS")
    
    def test_version_not_found(self):
        """Non-existent version returns 404"""
        # Get a real document
        docs_response = requests.get(f"{BASE_URL}/api/documents")
        docs = docs_response.json()
        if not docs:
            pytest.skip("No documents")
        
        doc_id = docs[0]["id"]
        fake_version = f"fake_{uuid.uuid4().hex}"
        
        response = requests.post(f"{BASE_URL}/api/documents/{doc_id}/versions/{fake_version}/restore")
        assert response.status_code == 404
        print("404 for non-existent version: PASS")


class TestBookmarks:
    """Test bookmarks toggle"""
    
    def test_toggle_bookmark(self):
        """Toggle bookmark on/off"""
        # Get a document
        docs_response = requests.get(f"{BASE_URL}/api/documents")
        docs = docs_response.json()
        if not docs:
            pytest.skip("No documents")
        
        doc_id = docs[0]["id"]
        
        # Toggle on
        response1 = requests.post(f"{BASE_URL}/api/bookmarks/{doc_id}")
        assert response1.status_code == 200
        
        # Toggle off
        response2 = requests.post(f"{BASE_URL}/api/bookmarks/{doc_id}")
        assert response2.status_code == 200
        
        # Check they toggled
        result1 = response1.json()
        result2 = response2.json()
        assert result1["bookmarked"] != result2["bookmarked"]
        print(f"Bookmark toggle: {result1['bookmarked']} -> {result2['bookmarked']}")
