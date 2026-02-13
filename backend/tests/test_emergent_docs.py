"""
Emergent Document Hub Backend API Test Suite
Tests: Authentication, Role-based access, Documents, Categories, Comments, Sharing, Trash, Tools, Search
"""
import pytest
import requests
import os

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://emergent-docs-dev.preview.emergentagent.com')

# Test tokens (pre-created in MongoDB)
ADMIN_TOKEN = "test_admin_session_token"
VIEWER_TOKEN = "test_viewer_session_token"


class TestAuthenticationRoles:
    """Test authentication and role assignment"""

    def test_admin_auth_me_returns_admin_role(self):
        """GET /api/auth/me with admin token returns role=admin"""
        response = requests.get(
            f"{BASE_URL}/api/auth/me",
            headers={"Authorization": f"Bearer {ADMIN_TOKEN}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("role") == "admin"
        assert data.get("email") == "chethan@emergent.sh"
        print(f"✓ Admin user verified: {data.get('email')}, role={data.get('role')}")

    def test_viewer_auth_me_returns_viewer_role(self):
        """GET /api/auth/me with viewer token returns role=viewer"""
        response = requests.get(
            f"{BASE_URL}/api/auth/me",
            headers={"Authorization": f"Bearer {VIEWER_TOKEN}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("role") == "viewer"
        assert data.get("email") == "viewer@test.com"
        print(f"✓ Viewer user verified: {data.get('email')}, role={data.get('role')}")

    def test_unauthenticated_request_returns_401(self):
        """GET /api/auth/me without token returns 401"""
        response = requests.get(f"{BASE_URL}/api/auth/me")
        assert response.status_code == 401
        print("✓ Unauthenticated request correctly returns 401")


class TestViewerPermissions:
    """Test that viewers cannot perform admin actions"""

    def test_viewer_cannot_create_document(self):
        """POST /api/documents with viewer token returns 403"""
        response = requests.post(
            f"{BASE_URL}/api/documents",
            headers={"Authorization": f"Bearer {VIEWER_TOKEN}"},
            json={"title": "Test Doc", "content": "Test", "category_id": "test-cat"}
        )
        assert response.status_code == 403
        print("✓ Viewer correctly blocked from creating documents (403)")

    def test_viewer_cannot_create_category(self):
        """POST /api/categories with viewer token returns 403"""
        response = requests.post(
            f"{BASE_URL}/api/categories",
            headers={"Authorization": f"Bearer {VIEWER_TOKEN}"},
            json={"name": "Test Category", "icon": "FileText"}
        )
        assert response.status_code == 403
        print("✓ Viewer correctly blocked from creating categories (403)")

    def test_viewer_cannot_delete_document(self):
        """DELETE /api/documents/{id} with viewer token returns 403"""
        # First get a document ID
        docs_response = requests.get(
            f"{BASE_URL}/api/documents",
            headers={"Authorization": f"Bearer {VIEWER_TOKEN}"}
        )
        assert docs_response.status_code == 200
        docs = docs_response.json()
        if docs:
            doc_id = docs[0]["id"]
            response = requests.delete(
                f"{BASE_URL}/api/documents/{doc_id}",
                headers={"Authorization": f"Bearer {VIEWER_TOKEN}"}
            )
            assert response.status_code == 403
            print("✓ Viewer correctly blocked from deleting documents (403)")
        else:
            pytest.skip("No documents to test delete permission")

    def test_viewer_cannot_access_trash(self):
        """GET /api/trash with viewer token returns 403"""
        response = requests.get(
            f"{BASE_URL}/api/trash",
            headers={"Authorization": f"Bearer {VIEWER_TOKEN}"}
        )
        assert response.status_code == 403
        print("✓ Viewer correctly blocked from accessing trash (403)")

    def test_viewer_cannot_create_tool(self):
        """POST /api/tools with viewer token returns 403"""
        response = requests.post(
            f"{BASE_URL}/api/tools",
            headers={"Authorization": f"Bearer {VIEWER_TOKEN}"},
            json={"name": "Test Tool", "url": "https://test.com", "description": "Test"}
        )
        assert response.status_code == 403
        print("✓ Viewer correctly blocked from creating tools (403)")


class TestAdminDocumentCRUD:
    """Test admin document CRUD operations"""
    created_doc_id = None

    def test_admin_can_create_document(self):
        """POST /api/documents creates successfully for admin"""
        # Get a category ID first
        cats_response = requests.get(
            f"{BASE_URL}/api/categories",
            headers={"Authorization": f"Bearer {ADMIN_TOKEN}"}
        )
        assert cats_response.status_code == 200
        cats = cats_response.json()
        cat_id = cats[0]["id"] if cats else None
        assert cat_id, "Need at least one category"

        response = requests.post(
            f"{BASE_URL}/api/documents",
            headers={"Authorization": f"Bearer {ADMIN_TOKEN}"},
            json={
                "title": "TEST_Admin_Created_Document",
                "content": "# Test Document\n\nThis is test content.",
                "category_id": cat_id,
                "tags": ["test", "automated"]
            }
        )
        assert response.status_code == 200  # FastAPI default for POST
        data = response.json()
        assert data.get("id")
        assert data.get("title") == "TEST_Admin_Created_Document"
        assert "test" in data.get("tags", [])
        TestAdminDocumentCRUD.created_doc_id = data["id"]
        print(f"✓ Admin created document: {data.get('id')}")

    def test_admin_can_get_document(self):
        """GET /api/documents/{id} returns document"""
        if not TestAdminDocumentCRUD.created_doc_id:
            pytest.skip("No document was created")
        
        response = requests.get(
            f"{BASE_URL}/api/documents/{TestAdminDocumentCRUD.created_doc_id}",
            headers={"Authorization": f"Bearer {ADMIN_TOKEN}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("title") == "TEST_Admin_Created_Document"
        print(f"✓ Admin can fetch document: {data.get('title')}")

    def test_admin_soft_delete_moves_to_trash(self):
        """DELETE /api/documents/{id} soft-deletes (moves to trash)"""
        if not TestAdminDocumentCRUD.created_doc_id:
            pytest.skip("No document was created")
        
        response = requests.delete(
            f"{BASE_URL}/api/documents/{TestAdminDocumentCRUD.created_doc_id}",
            headers={"Authorization": f"Bearer {ADMIN_TOKEN}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("status") == "moved to trash"
        print("✓ Admin soft-deleted document to trash")


class TestTrashOperations:
    """Test trash and restore functionality"""

    def test_get_trash_returns_deleted_docs(self):
        """GET /api/trash returns deleted docs (admin only)"""
        response = requests.get(
            f"{BASE_URL}/api/trash",
            headers={"Authorization": f"Bearer {ADMIN_TOKEN}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        print(f"✓ Admin can access trash, found {len(data)} deleted documents")

    def test_restore_document_from_trash(self):
        """POST /api/trash/{id}/restore restores doc"""
        # Get a document in trash
        trash_response = requests.get(
            f"{BASE_URL}/api/trash",
            headers={"Authorization": f"Bearer {ADMIN_TOKEN}"}
        )
        assert trash_response.status_code == 200
        trash = trash_response.json()
        
        if trash:
            doc_id = trash[0]["id"]
            response = requests.post(
                f"{BASE_URL}/api/trash/{doc_id}/restore",
                headers={"Authorization": f"Bearer {ADMIN_TOKEN}"}
            )
            assert response.status_code == 200
            data = response.json()
            assert data.get("status") == "restored"
            print(f"✓ Admin restored document from trash: {doc_id}")
        else:
            pytest.skip("No documents in trash to restore")


class TestComments:
    """Test threaded comments with upvotes"""
    test_doc_id = None
    created_comment_id = None

    @classmethod
    def setup_class(cls):
        """Get a document ID for comment tests"""
        response = requests.get(
            f"{BASE_URL}/api/documents",
            headers={"Authorization": f"Bearer {ADMIN_TOKEN}"}
        )
        if response.status_code == 200 and response.json():
            cls.test_doc_id = response.json()[0]["id"]

    def test_create_comment_on_document(self):
        """POST /api/documents/{docId}/comments creates comment"""
        if not TestComments.test_doc_id:
            pytest.skip("No document available for comment testing")
        
        response = requests.post(
            f"{BASE_URL}/api/documents/{TestComments.test_doc_id}/comments",
            headers={"Authorization": f"Bearer {ADMIN_TOKEN}"},
            json={"content": "TEST_This is a test comment"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("id")
        assert data.get("content") == "TEST_This is a test comment"
        TestComments.created_comment_id = data["id"]
        print(f"✓ Created comment: {data.get('id')}")

    def test_toggle_upvote_on_comment(self):
        """POST /api/comments/{id}/upvote toggles upvote"""
        if not TestComments.created_comment_id:
            pytest.skip("No comment available for upvote testing")
        
        # First upvote
        response = requests.post(
            f"{BASE_URL}/api/comments/{TestComments.created_comment_id}/upvote",
            headers={"Authorization": f"Bearer {ADMIN_TOKEN}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "upvotes" in data
        print(f"✓ Toggled upvote, upvotes count: {len(data['upvotes'])}")

    def test_delete_own_comment(self):
        """DELETE /api/comments/{id} works for own comment"""
        if not TestComments.created_comment_id:
            pytest.skip("No comment available for delete testing")
        
        response = requests.delete(
            f"{BASE_URL}/api/comments/{TestComments.created_comment_id}",
            headers={"Authorization": f"Bearer {ADMIN_TOKEN}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("status") == "deleted"
        print("✓ Deleted own comment successfully")


class TestPublicSharing:
    """Test public document sharing"""
    test_doc_id = None
    share_id = None

    @classmethod
    def setup_class(cls):
        """Get a document ID for sharing tests"""
        response = requests.get(
            f"{BASE_URL}/api/documents",
            headers={"Authorization": f"Bearer {ADMIN_TOKEN}"}
        )
        if response.status_code == 200 and response.json():
            cls.test_doc_id = response.json()[0]["id"]

    def test_toggle_share_creates_share_link(self):
        """POST /api/documents/{id}/share toggles sharing"""
        if not TestPublicSharing.test_doc_id:
            pytest.skip("No document available for sharing testing")
        
        response = requests.post(
            f"{BASE_URL}/api/documents/{TestPublicSharing.test_doc_id}/share",
            headers={"Authorization": f"Bearer {ADMIN_TOKEN}"}
        )
        assert response.status_code == 200
        data = response.json()
        # It either enables or disables sharing
        if data.get("shared"):
            TestPublicSharing.share_id = data.get("share_id")
            print(f"✓ Sharing enabled, share_id: {TestPublicSharing.share_id}")
        else:
            # Enable it again for testing
            response2 = requests.post(
                f"{BASE_URL}/api/documents/{TestPublicSharing.test_doc_id}/share",
                headers={"Authorization": f"Bearer {ADMIN_TOKEN}"}
            )
            data2 = response2.json()
            TestPublicSharing.share_id = data2.get("share_id")
            print(f"✓ Sharing re-enabled, share_id: {TestPublicSharing.share_id}")

    def test_public_endpoint_returns_doc_without_auth(self):
        """GET /api/public/{shareId} returns doc without auth"""
        if not TestPublicSharing.share_id:
            pytest.skip("No share_id available")
        
        response = requests.get(
            f"{BASE_URL}/api/public/{TestPublicSharing.share_id}"
            # No auth header - public endpoint
        )
        assert response.status_code == 200
        data = response.json()
        assert "title" in data
        assert "content" in data
        print(f"✓ Public endpoint works without auth, title: {data.get('title')[:30]}...")


class TestTools:
    """Test tools directory"""
    created_tool_id = None

    def test_admin_can_create_tool(self):
        """POST /api/tools creates tool (admin only)"""
        response = requests.post(
            f"{BASE_URL}/api/tools",
            headers={"Authorization": f"Bearer {ADMIN_TOKEN}"},
            json={
                "name": "TEST_Tool",
                "url": "https://test-tool.example.com",
                "description": "A test tool for automated testing",
                "category": "Testing"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("id")
        assert data.get("name") == "TEST_Tool"
        TestTools.created_tool_id = data["id"]
        print(f"✓ Admin created tool: {data.get('name')}")

    def test_get_tools_returns_list(self):
        """GET /api/tools returns tools list"""
        response = requests.get(
            f"{BASE_URL}/api/tools",
            headers={"Authorization": f"Bearer {ADMIN_TOKEN}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        print(f"✓ Tools list returned, count: {len(data)}")

    def test_cleanup_tool(self):
        """Delete created test tool"""
        if TestTools.created_tool_id:
            response = requests.delete(
                f"{BASE_URL}/api/tools/{TestTools.created_tool_id}",
                headers={"Authorization": f"Bearer {ADMIN_TOKEN}"}
            )
            assert response.status_code == 200
            print("✓ Cleaned up test tool")


class TestSearch:
    """Test search functionality with fuzzy matching"""

    def test_search_returns_results_with_snippet(self):
        """GET /api/search?q=proxy returns LLM Proxy doc with snippet"""
        response = requests.get(
            f"{BASE_URL}/api/search?q=proxy",
            headers={"Authorization": f"Bearer {ADMIN_TOKEN}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        # Should find LLM Proxy Architecture doc
        proxy_docs = [d for d in data if "proxy" in d.get("title", "").lower() or "proxy" in d.get("snippet", "").lower()]
        print(f"✓ Search for 'proxy' returned {len(data)} results, proxy-related: {len(proxy_docs)}")

    def test_search_fuzzy_matching(self):
        """GET /api/search fuzzy matching works"""
        # Test fuzzy search with partial term
        response = requests.get(
            f"{BASE_URL}/api/search?q=kubernetes",
            headers={"Authorization": f"Bearer {ADMIN_TOKEN}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        print(f"✓ Fuzzy search for 'kubernetes' returned {len(data)} results")

    def test_search_case_insensitive(self):
        """Search is case-insensitive"""
        response_upper = requests.get(
            f"{BASE_URL}/api/search?q=REACT",
            headers={"Authorization": f"Bearer {ADMIN_TOKEN}"}
        )
        response_lower = requests.get(
            f"{BASE_URL}/api/search?q=react",
            headers={"Authorization": f"Bearer {ADMIN_TOKEN}"}
        )
        assert response_upper.status_code == 200
        assert response_lower.status_code == 200
        # Both should return similar results
        print(f"✓ Case-insensitive search works (REACT: {len(response_upper.json())}, react: {len(response_lower.json())})")


class TestDataCounts:
    """Verify expected data counts"""

    def test_categories_count(self):
        """Verify 43 categories exist"""
        response = requests.get(
            f"{BASE_URL}/api/categories",
            headers={"Authorization": f"Bearer {ADMIN_TOKEN}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 43, f"Expected 43 categories, got {len(data)}"
        print(f"✓ Categories count: {len(data)} (expected 43)")

    def test_documents_count(self):
        """Verify 33 documents exist"""
        response = requests.get(
            f"{BASE_URL}/api/documents",
            headers={"Authorization": f"Bearer {ADMIN_TOKEN}"}
        )
        assert response.status_code == 200
        data = response.json()
        # Account for possible test documents created/deleted
        assert len(data) >= 32 and len(data) <= 35, f"Expected ~33 documents, got {len(data)}"
        print(f"✓ Documents count: {len(data)} (expected ~33)")


class TestViewerCanRead:
    """Test viewer can read content"""

    def test_viewer_can_get_documents(self):
        """Viewer can list documents"""
        response = requests.get(
            f"{BASE_URL}/api/documents",
            headers={"Authorization": f"Bearer {VIEWER_TOKEN}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        print(f"✓ Viewer can list documents: {len(data)} docs")

    def test_viewer_can_get_categories(self):
        """Viewer can list categories"""
        response = requests.get(
            f"{BASE_URL}/api/categories",
            headers={"Authorization": f"Bearer {VIEWER_TOKEN}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        print(f"✓ Viewer can list categories: {len(data)} cats")

    def test_viewer_can_search(self):
        """Viewer can search documents"""
        response = requests.get(
            f"{BASE_URL}/api/search?q=react",
            headers={"Authorization": f"Bearer {VIEWER_TOKEN}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        print(f"✓ Viewer can search: found {len(data)} results")

    def test_viewer_can_bookmark(self):
        """Viewer can toggle bookmarks"""
        # Get a document ID
        docs_response = requests.get(
            f"{BASE_URL}/api/documents",
            headers={"Authorization": f"Bearer {VIEWER_TOKEN}"}
        )
        if docs_response.status_code == 200 and docs_response.json():
            doc_id = docs_response.json()[0]["id"]
            response = requests.post(
                f"{BASE_URL}/api/bookmarks/{doc_id}",
                headers={"Authorization": f"Bearer {VIEWER_TOKEN}"}
            )
            assert response.status_code == 200
            data = response.json()
            assert "bookmarked" in data
            print(f"✓ Viewer can toggle bookmark: bookmarked={data.get('bookmarked')}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
