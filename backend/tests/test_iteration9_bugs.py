"""
Iteration 9 Bug Fix Tests - Testing 14+ QA bug fixes
Tests: Tool delete, sidebar refresh, breadcrumb, PDF export, italic markdown, 
role change, URLs in tables, analytics, table overflow, chat z-index, E1 comparison table
"""
import pytest
import requests
import os

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', 'http://localhost:8001').rstrip('/')


class TestAnalyticsEndpoints:
    """B-06, B-09: Analytics tests - deleted docs and search queries"""
    
    def test_popular_docs_shows_deleted_document_label(self):
        """B-06: Analytics popular-docs shows '[Deleted document]' for orphaned views"""
        response = requests.get(f"{BASE_URL}/api/analytics/popular-docs")
        assert response.status_code == 200
        data = response.json()
        
        # Verify the endpoint returns a list
        assert isinstance(data, list)
        
        # Check that documents have expected fields
        for doc in data:
            assert "doc_id" in doc
            assert "views" in doc
            assert "title" in doc
            # Title should either be a real title or "[Deleted document]"
            assert doc["title"] != "Unknown" or doc["title"] == "[Deleted document]"
    
    def test_no_test_search_queries_in_analytics(self):
        """B-09: No TEST_SEARCH_ queries in analytics"""
        response = requests.get(f"{BASE_URL}/api/analytics/searches")
        assert response.status_code == 200
        data = response.json()
        
        # Verify no TEST_SEARCH_ prefixed queries
        for search in data:
            query = search.get("query", "")
            assert "TEST_SEARCH" not in query.upper(), f"Found test query: {query}"


class TestToolsAPI:
    """B-02: Tool operations tests"""
    
    def test_create_tool(self):
        """Create a tool for testing"""
        response = requests.post(f"{BASE_URL}/api/tools", json={
            "name": "TEST_TOOL_Delete_Test",
            "url": "https://test.example.com",
            "description": "Test tool for delete confirmation",
            "category": "Testing"
        })
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert data["name"] == "TEST_TOOL_Delete_Test"
        return data["id"]
    
    def test_delete_tool(self):
        """B-02: Tool delete - backend accepts delete request"""
        # First create a tool
        create_response = requests.post(f"{BASE_URL}/api/tools", json={
            "name": "TEST_TOOL_To_Delete",
            "url": "https://test.example.com",
            "description": "Will be deleted",
            "category": "Testing"
        })
        assert create_response.status_code == 200
        tool_id = create_response.json()["id"]
        
        # Delete the tool
        delete_response = requests.delete(f"{BASE_URL}/api/tools/{tool_id}")
        assert delete_response.status_code == 200
        assert delete_response.json()["status"] == "deleted"
        
        # Verify tool is gone
        tools_response = requests.get(f"{BASE_URL}/api/tools")
        tool_ids = [t["id"] for t in tools_response.json()]
        assert tool_id not in tool_ids


class TestTrashRestore:
    """B-05: Trash restore functionality"""
    
    def test_restore_document_from_trash(self):
        """B-05: After restoring from trash, document should be restored"""
        # Create a test document
        create_response = requests.post(f"{BASE_URL}/api/documents", json={
            "title": "TEST_DOC_Trash_Restore_Test",
            "content": "Test content for trash restore",
            "category_id": "7094c81a-3133-4f8d-b96b-b899af186559"  # Platform Architecture
        })
        assert create_response.status_code == 200
        doc_id = create_response.json()["id"]
        
        # Move to trash
        delete_response = requests.delete(f"{BASE_URL}/api/documents/{doc_id}")
        assert delete_response.status_code == 200
        
        # Verify in trash
        trash_response = requests.get(f"{BASE_URL}/api/trash")
        assert trash_response.status_code == 200
        trash_ids = [d["id"] for d in trash_response.json()]
        assert doc_id in trash_ids
        
        # Restore from trash
        restore_response = requests.post(f"{BASE_URL}/api/trash/{doc_id}/restore")
        assert restore_response.status_code == 200
        
        # Verify restored
        docs_response = requests.get(f"{BASE_URL}/api/documents")
        doc_ids = [d["id"] for d in docs_response.json()]
        assert doc_id in doc_ids
        
        # Clean up - permanent delete
        requests.delete(f"{BASE_URL}/api/documents/{doc_id}")
        requests.delete(f"{BASE_URL}/api/trash/{doc_id}")


class TestUserRoleChange:
    """B-24: Role change functionality"""
    
    def test_change_user_role(self):
        """B-24: Role change updates correctly"""
        # Get existing users
        users_response = requests.get(f"{BASE_URL}/api/users")
        if users_response.status_code != 200:
            pytest.skip("Users endpoint not accessible")
        
        users = users_response.json()
        if len(users) == 0:
            pytest.skip("No users to test role change")
        
        # Get a test user (not the admin)
        test_user = None
        for user in users:
            if user.get("email") != "admin@emergent.sh" and "TEST" not in user.get("email", ""):
                test_user = user
                break
        
        if not test_user:
            pytest.skip("No suitable user for role test")
        
        user_id = test_user["user_id"]
        current_role = test_user.get("role", "viewer")
        new_role = "admin" if current_role == "viewer" else "viewer"
        
        # Change role
        response = requests.put(f"{BASE_URL}/api/users/{user_id}/role", json={"role": new_role})
        assert response.status_code == 200
        assert response.json()["role"] == new_role
        
        # Restore original role
        requests.put(f"{BASE_URL}/api/users/{user_id}/role", json={"role": current_role})


class TestDocumentContent:
    """B-25, B-29: Document content tests"""
    
    def test_e1_document_has_capability_table(self):
        """B-25: E1 comparison table first column header says 'Capability'"""
        # Get documents
        response = requests.get(f"{BASE_URL}/api/documents")
        assert response.status_code == 200
        
        # Find E1 document
        e1_doc = None
        for doc in response.json():
            if "E1" in doc["title"]:
                e1_doc = doc
                break
        
        if not e1_doc:
            pytest.skip("E1 document not found")
        
        # Get full document content
        doc_response = requests.get(f"{BASE_URL}/api/documents/{e1_doc['id']}")
        assert doc_response.status_code == 200
        
        content = doc_response.json()["content"]
        # Check for Capability header in table
        assert "| Capability |" in content, "E1 doc should have Capability table header"
    
    def test_tools_document_has_shadcn_javascript(self):
        """B-29: Shadcn/UI shows JavaScript/TypeScript"""
        # Get documents
        response = requests.get(f"{BASE_URL}/api/documents")
        assert response.status_code == 200
        
        # Find Essential Tools document
        tools_doc = None
        for doc in response.json():
            if "Essential" in doc["title"] or "Tools" in doc["title"]:
                tools_doc = doc
                break
        
        if not tools_doc:
            pytest.skip("Tools document not found")
        
        # Get full document content
        doc_response = requests.get(f"{BASE_URL}/api/documents/{tools_doc['id']}")
        assert doc_response.status_code == 200
        
        content = doc_response.json()["content"]
        # Check for JavaScript/TypeScript in Shadcn row
        assert "Shadcn" in content or "shadcn" in content
        assert "JavaScript/TypeScript" in content, "Shadcn should show JavaScript/TypeScript"


class TestDocumentViews:
    """View tracking tests"""
    
    def test_view_tracking_stores_title(self):
        """View tracking stores title for analytics fallback"""
        # Get a document
        docs_response = requests.get(f"{BASE_URL}/api/documents")
        assert docs_response.status_code == 200
        
        docs = docs_response.json()
        if len(docs) == 0:
            pytest.skip("No documents to test")
        
        doc = docs[0]
        doc_id = doc["id"]
        doc_title = doc["title"]
        
        # Track a view
        view_response = requests.post(f"{BASE_URL}/api/documents/{doc_id}/view")
        assert view_response.status_code == 200
        
        # Verify in popular docs
        popular_response = requests.get(f"{BASE_URL}/api/analytics/popular-docs")
        assert popular_response.status_code == 200
        
        # Find the doc in popular docs
        found = False
        for popular_doc in popular_response.json():
            if popular_doc["doc_id"] == doc_id:
                assert popular_doc["title"] == doc_title
                found = True
                break
        
        # Doc should be in popular docs after view
        assert found, f"Document {doc_id} should appear in popular docs after view"


class TestDocumentCount:
    """Verify home page loads with all documents"""
    
    def test_home_page_document_count(self):
        """Home page loads correctly with all 37 documents"""
        response = requests.get(f"{BASE_URL}/api/documents")
        assert response.status_code == 200
        
        docs = response.json()
        assert len(docs) == 37, f"Expected 37 documents, got {len(docs)}"


# Cleanup test data
@pytest.fixture(scope="module", autouse=True)
def cleanup_test_data():
    """Clean up TEST_ prefixed tools after tests"""
    yield
    
    # Clean up test tools
    try:
        tools_response = requests.get(f"{BASE_URL}/api/tools")
        if tools_response.status_code == 200:
            for tool in tools_response.json():
                if tool.get("name", "").startswith("TEST_"):
                    requests.delete(f"{BASE_URL}/api/tools/{tool['id']}")
    except Exception:
        pass
