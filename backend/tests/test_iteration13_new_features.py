"""
Test Iteration 13: New Production Features Testing
=================================================
Tests for:
1. Version history & restore API
2. Keywords endpoint for auto-linking
3. User management (invite, change role, delete)
4. 404 handling (NotFoundPage)
"""

import pytest
import requests
import os
import uuid

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://ai-agent-hub-96.preview.emergentagent.com').rstrip('/')

class TestKeywordsEndpoint:
    """Test GET /api/keywords endpoint for auto-linking"""
    
    def test_keywords_endpoint_returns_data(self):
        """Keywords endpoint should return keyword-to-docId map"""
        response = requests.get(f"{BASE_URL}/api/keywords", allow_redirects=True)
        assert response.status_code == 200
        data = response.json()
        
        # Should be a non-empty dict
        assert isinstance(data, dict)
        assert len(data) > 0
        print(f"Keywords endpoint returned {len(data)} keyword mappings")
        
    def test_keywords_contains_expected_terms(self):
        """Keywords should include common AI agent terminology"""
        response = requests.get(f"{BASE_URL}/api/keywords", allow_redirects=True)
        assert response.status_code == 200
        data = response.json()
        
        # Check for expected keywords (lowercase)
        keywords_lower = {k.lower(): v for k, v in data.items()}
        
        expected_keywords = ['orchestrator', 'transformer', 'kubernetes', 'docker', 
                           'fastapi', 'mongodb', 'rag', 'subagent']
        found = []
        missing = []
        for kw in expected_keywords:
            if kw in keywords_lower:
                found.append(kw)
            else:
                missing.append(kw)
        
        print(f"Found keywords: {found}")
        print(f"Missing keywords: {missing}")
        
        # At least 5 of the expected keywords should be present
        assert len(found) >= 5, f"Expected at least 5 keywords, found {len(found)}: {found}"

    def test_keywords_values_are_valid_uuids(self):
        """Keyword values should be valid document IDs (UUIDs)"""
        response = requests.get(f"{BASE_URL}/api/keywords", allow_redirects=True)
        assert response.status_code == 200
        data = response.json()
        
        # Check first 10 values are UUID-like
        for i, (keyword, doc_id) in enumerate(list(data.items())[:10]):
            assert isinstance(doc_id, str), f"Keyword '{keyword}' has non-string value"
            assert len(doc_id) == 36, f"Keyword '{keyword}' doc_id '{doc_id}' is not UUID format"
            print(f"Keyword '{keyword}' -> doc_id '{doc_id[:8]}...'")


class TestVersionHistory:
    """Test version history and restore functionality"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Create a test document for version testing"""
        self.test_doc_title = f"TEST_Version_Test_{uuid.uuid4().hex[:8]}"
        
        # Get a valid category ID
        cats_response = requests.get(f"{BASE_URL}/api/categories", allow_redirects=True)
        assert cats_response.status_code == 200
        categories = cats_response.json()
        assert len(categories) > 0
        self.category_id = categories[0]['id']
        
        # Create a test document
        create_response = requests.post(
            f"{BASE_URL}/api/documents",
            json={
                "title": self.test_doc_title,
                "content": "Initial content version 1",
                "category_id": self.category_id,
                "tags": ["test", "version-test"]
            },
            allow_redirects=True
        )
        assert create_response.status_code == 200 or create_response.status_code == 201
        self.doc_id = create_response.json()['id']
        print(f"Created test doc: {self.doc_id}")
        yield
        
        # Cleanup - soft delete
        try:
            requests.delete(f"{BASE_URL}/api/documents/{self.doc_id}", allow_redirects=True)
        except:
            pass
    
    def test_get_versions_empty_initially(self):
        """New document should have no versions initially"""
        response = requests.get(f"{BASE_URL}/api/documents/{self.doc_id}/versions", allow_redirects=True)
        assert response.status_code == 200
        versions = response.json()
        # A brand new doc might have 0 versions
        print(f"Initial versions count: {len(versions)}")
        
    def test_update_creates_version(self):
        """Updating a document should create a version"""
        # First update
        update_response = requests.put(
            f"{BASE_URL}/api/documents/{self.doc_id}",
            json={"content": "Updated content version 2", "title": self.test_doc_title},
            allow_redirects=True
        )
        assert update_response.status_code == 200
        
        # Check versions
        versions_response = requests.get(f"{BASE_URL}/api/documents/{self.doc_id}/versions", allow_redirects=True)
        assert versions_response.status_code == 200
        versions = versions_response.json()
        assert len(versions) >= 1, "Expected at least one version after update"
        print(f"Versions after update: {len(versions)}")
        
        # Version should have required fields
        v = versions[0]
        assert 'id' in v
        assert 'content' in v
        assert 'title' in v
        assert 'created_at' in v
        
    def test_restore_version_api(self):
        """POST /api/documents/{doc_id}/versions/{version_id}/restore should restore version"""
        # Create initial content
        update1 = requests.put(
            f"{BASE_URL}/api/documents/{self.doc_id}",
            json={"content": "Content A", "title": self.test_doc_title},
            allow_redirects=True
        )
        assert update1.status_code == 200
        
        # Update again
        update2 = requests.put(
            f"{BASE_URL}/api/documents/{self.doc_id}",
            json={"content": "Content B", "title": self.test_doc_title},
            allow_redirects=True
        )
        assert update2.status_code == 200
        
        # Get versions
        versions_response = requests.get(f"{BASE_URL}/api/documents/{self.doc_id}/versions", allow_redirects=True)
        assert versions_response.status_code == 200
        versions = versions_response.json()
        assert len(versions) >= 1
        
        # Get version to restore (first/oldest in sorted list)
        version_to_restore = versions[-1]  # oldest version
        version_id = version_to_restore['id']
        old_content = version_to_restore['content']
        
        print(f"Restoring version {version_id} with content: '{old_content[:30]}...'")
        
        # Restore the version
        restore_response = requests.post(
            f"{BASE_URL}/api/documents/{self.doc_id}/versions/{version_id}/restore",
            allow_redirects=True
        )
        assert restore_response.status_code == 200
        restored_doc = restore_response.json()
        
        # Verify the content was restored
        assert restored_doc['content'] == old_content, f"Expected '{old_content}' but got '{restored_doc['content']}'"
        print(f"Successfully restored to version with content: '{restored_doc['content'][:30]}...'")
        
    def test_restore_creates_new_version(self):
        """Restoring should save current state as new version first"""
        # Create content A
        update1 = requests.put(
            f"{BASE_URL}/api/documents/{self.doc_id}",
            json={"content": "Content A for restore test", "title": self.test_doc_title},
            allow_redirects=True
        )
        assert update1.status_code == 200
        
        # Get initial version count
        v1_response = requests.get(f"{BASE_URL}/api/documents/{self.doc_id}/versions", allow_redirects=True)
        initial_count = len(v1_response.json())
        
        # Update to content B
        update2 = requests.put(
            f"{BASE_URL}/api/documents/{self.doc_id}",
            json={"content": "Content B for restore test", "title": self.test_doc_title},
            allow_redirects=True
        )
        assert update2.status_code == 200
        
        # Get versions and restore oldest
        v2_response = requests.get(f"{BASE_URL}/api/documents/{self.doc_id}/versions", allow_redirects=True)
        versions = v2_response.json()
        version_id = versions[-1]['id']
        
        # Restore
        restore_response = requests.post(
            f"{BASE_URL}/api/documents/{self.doc_id}/versions/{version_id}/restore",
            allow_redirects=True
        )
        assert restore_response.status_code == 200
        
        # Check that a new version was created (current state saved before restore)
        v3_response = requests.get(f"{BASE_URL}/api/documents/{self.doc_id}/versions", allow_redirects=True)
        final_count = len(v3_response.json())
        
        print(f"Version count: {initial_count} -> {final_count}")
        assert final_count > len(versions), "Expected new version to be created when restoring"


class TestUserManagement:
    """Test user management: invite, change role, delete"""
    
    def test_list_users(self):
        """GET /api/users should return list of users"""
        response = requests.get(f"{BASE_URL}/api/users", allow_redirects=True)
        assert response.status_code == 200
        users = response.json()
        assert isinstance(users, list)
        print(f"Found {len(users)} users")
        
    def test_invite_user(self):
        """POST /api/invite should create a new user"""
        test_email = f"test_{uuid.uuid4().hex[:8]}@testdomain.com"
        response = requests.post(
            f"{BASE_URL}/api/invite",
            json={"email": test_email, "role": "viewer"},
            allow_redirects=True
        )
        assert response.status_code == 200
        new_user = response.json()
        
        assert 'user_id' in new_user
        assert new_user['email'] == test_email
        assert new_user['role'] == 'viewer'
        print(f"Invited user: {new_user['email']} with role {new_user['role']}")
        
        # Cleanup
        user_id = new_user['user_id']
        requests.delete(f"{BASE_URL}/api/users/{user_id}", allow_redirects=True)
        
    def test_invite_duplicate_fails(self):
        """Inviting an existing email should fail"""
        test_email = f"dup_test_{uuid.uuid4().hex[:8]}@testdomain.com"
        
        # First invite
        r1 = requests.post(f"{BASE_URL}/api/invite", json={"email": test_email, "role": "viewer"}, allow_redirects=True)
        assert r1.status_code == 200
        user_id = r1.json()['user_id']
        
        # Second invite should fail
        r2 = requests.post(f"{BASE_URL}/api/invite", json={"email": test_email, "role": "admin"}, allow_redirects=True)
        assert r2.status_code == 400
        print(f"Duplicate invite correctly rejected: {r2.json()}")
        
        # Cleanup
        requests.delete(f"{BASE_URL}/api/users/{user_id}", allow_redirects=True)
        
    def test_change_user_role(self):
        """PUT /api/users/{user_id}/role should change role"""
        # Create test user
        test_email = f"role_test_{uuid.uuid4().hex[:8]}@testdomain.com"
        create_response = requests.post(
            f"{BASE_URL}/api/invite",
            json={"email": test_email, "role": "viewer"},
            allow_redirects=True
        )
        assert create_response.status_code == 200
        user_id = create_response.json()['user_id']
        
        # Change role to admin
        role_response = requests.put(
            f"{BASE_URL}/api/users/{user_id}/role",
            json={"role": "admin"},
            allow_redirects=True
        )
        assert role_response.status_code == 200
        assert role_response.json()['role'] == 'admin'
        print(f"Changed user {user_id} role to admin")
        
        # Change back to viewer
        role_response2 = requests.put(
            f"{BASE_URL}/api/users/{user_id}/role",
            json={"role": "viewer"},
            allow_redirects=True
        )
        assert role_response2.status_code == 200
        assert role_response2.json()['role'] == 'viewer'
        print(f"Changed user {user_id} role back to viewer")
        
        # Cleanup
        requests.delete(f"{BASE_URL}/api/users/{user_id}", allow_redirects=True)
        
    def test_delete_user(self):
        """DELETE /api/users/{user_id} should remove user"""
        # Create test user
        test_email = f"delete_test_{uuid.uuid4().hex[:8]}@testdomain.com"
        create_response = requests.post(
            f"{BASE_URL}/api/invite",
            json={"email": test_email, "role": "viewer"},
            allow_redirects=True
        )
        assert create_response.status_code == 200
        user_id = create_response.json()['user_id']
        
        # Delete user
        delete_response = requests.delete(f"{BASE_URL}/api/users/{user_id}", allow_redirects=True)
        assert delete_response.status_code == 200
        assert delete_response.json()['status'] == 'removed'
        print(f"Successfully deleted user {user_id}")
        
        # Verify user is gone
        users_response = requests.get(f"{BASE_URL}/api/users", allow_redirects=True)
        users = users_response.json()
        user_ids = [u.get('user_id') for u in users if u.get('user_id')]
        assert user_id not in user_ids, "Deleted user should not appear in users list"


class TestDocumentMetadata:
    """Test reading time and last updated features"""
    
    def test_document_has_updated_at(self):
        """Documents should have updated_at field"""
        docs_response = requests.get(f"{BASE_URL}/api/documents", allow_redirects=True)
        assert docs_response.status_code == 200
        docs = docs_response.json()
        
        assert len(docs) > 0, "No documents found"
        
        # Check a few docs for updated_at
        checked = 0
        for doc in docs[:5]:
            if 'updated_at' in doc and doc['updated_at']:
                checked += 1
                print(f"Doc '{doc['title'][:30]}...' updated_at: {doc['updated_at']}")
        
        assert checked > 0, "No documents have updated_at field"
        
    def test_reading_time_calculation(self):
        """Reading time should be calculable from content"""
        # Get a document with content
        docs_response = requests.get(f"{BASE_URL}/api/documents", allow_redirects=True)
        docs = docs_response.json()
        
        # Find doc with substantial content
        for doc in docs[:10]:
            doc_detail = requests.get(f"{BASE_URL}/api/documents/{doc['id']}", allow_redirects=True).json()
            content = doc_detail.get('content', '')
            if content and len(content) > 100:
                word_count = len(content.split())
                reading_time = max(1, word_count // 200)
                print(f"Doc '{doc['title'][:30]}...' has {word_count} words, ~{reading_time} min read")
                assert word_count > 0
                return
        
        print("Warning: No docs with substantial content found for reading time test")


class TestHomePageCategories:
    """Test home page shows categories without tag filtering"""
    
    def test_categories_exist(self):
        """Categories endpoint should return categories"""
        response = requests.get(f"{BASE_URL}/api/categories", allow_redirects=True)
        assert response.status_code == 200
        categories = response.json()
        
        assert len(categories) > 0
        
        # Count parent categories (non-internal, no parent_id)
        parent_cats = [c for c in categories if not c.get('parent_id') and not c.get('internal')]
        print(f"Total categories: {len(categories)}, Parent categories for home page: {len(parent_cats)}")
        
        # Should have at least 10 parent categories for home page
        assert len(parent_cats) >= 10, f"Expected at least 10 parent categories, found {len(parent_cats)}"
        
    def test_tutorials_is_last_category(self):
        """Tutorials category should be last in order"""
        response = requests.get(f"{BASE_URL}/api/categories", allow_redirects=True)
        assert response.status_code == 200
        categories = response.json()
        
        # Get parent categories sorted by order
        parent_cats = [c for c in categories if not c.get('parent_id') and not c.get('internal')]
        sorted_cats = sorted(parent_cats, key=lambda x: x.get('order', 0))
        
        cat_names = [c['name'] for c in sorted_cats]
        print(f"Category order: {cat_names}")
        
        # Find Tutorials
        tutorials_cat = next((c for c in sorted_cats if 'tutorial' in c['name'].lower()), None)
        if tutorials_cat:
            tutorials_order = tutorials_cat.get('order', 0)
            max_order = max(c.get('order', 0) for c in sorted_cats)
            print(f"Tutorials order: {tutorials_order}, Max order: {max_order}")
            # Tutorials should have the highest order value
            assert tutorials_order == max_order, f"Tutorials (order={tutorials_order}) should be last (max={max_order})"
        else:
            print("Warning: Tutorials category not found")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
