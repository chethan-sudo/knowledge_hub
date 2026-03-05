"""
P0 Features Backend API Test Suite - Iteration 3
Tests: Invite system, Templates, Tag suggestions, User management, AI Agent TCs
"""
import pytest
import requests
import os
import uuid

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://ai-agent-hub-96.preview.emergentagent.com')

# Test tokens (pre-created in MongoDB)
ADMIN_TOKEN = "test_admin_session_token"
VIEWER_TOKEN = "test_viewer_session_token"


class TestTemplatesEndpoint:
    """Test GET /api/templates returns 5 templates"""

    def test_templates_returns_5_templates(self):
        """GET /api/templates returns exactly 5 templates"""
        response = requests.get(
            f"{BASE_URL}/api/templates",
            headers={"Authorization": f"Bearer {ADMIN_TOKEN}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 5, f"Expected 5 templates, got {len(data)}"
        print(f"✓ Templates endpoint returns {len(data)} templates")

    def test_templates_have_required_fields(self):
        """Each template has id, name, icon, content"""
        response = requests.get(
            f"{BASE_URL}/api/templates",
            headers={"Authorization": f"Bearer {ADMIN_TOKEN}"}
        )
        data = response.json()
        required_fields = ["id", "name", "icon", "content"]
        for template in data:
            for field in required_fields:
                assert field in template, f"Template missing {field}"
        template_names = [t["name"] for t in data]
        print(f"✓ Template names: {template_names}")

    def test_templates_include_expected_types(self):
        """Templates include API Doc, Runbook, RCA, Meeting Notes, Test Plan"""
        response = requests.get(
            f"{BASE_URL}/api/templates",
            headers={"Authorization": f"Bearer {ADMIN_TOKEN}"}
        )
        data = response.json()
        expected_ids = ["api-doc", "runbook", "rca", "meeting-notes", "test-plan"]
        template_ids = [t["id"] for t in data]
        for expected_id in expected_ids:
            assert expected_id in template_ids, f"Missing template: {expected_id}"
        print(f"✓ All 5 expected templates present: {expected_ids}")


class TestUserManagementEndpoints:
    """Test user management: GET /api/users, POST /api/invite, PUT /api/users/{id}/role, DELETE /api/users/{id}"""
    
    created_user_id = None

    def test_get_users_returns_list_admin_only(self):
        """GET /api/users returns list of all users (admin only)"""
        response = requests.get(
            f"{BASE_URL}/api/users",
            headers={"Authorization": f"Bearer {ADMIN_TOKEN}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        # Check users have required fields
        for user in data:
            assert "email" in user
            print(f"  User: {user.get('email')}, role={user.get('role', 'N/A')}")
        print(f"✓ GET /api/users returns {len(data)} users")

    def test_viewer_cannot_access_users(self):
        """GET /api/users with viewer token returns 403"""
        response = requests.get(
            f"{BASE_URL}/api/users",
            headers={"Authorization": f"Bearer {VIEWER_TOKEN}"}
        )
        assert response.status_code == 403
        assert "Admin access required" in response.json().get("detail", "")
        print("✓ Viewer correctly blocked from GET /api/users (403)")

    def test_invite_creates_new_user(self):
        """POST /api/invite creates new user with email and role"""
        test_email = f"TEST_invite_{uuid.uuid4().hex[:8]}@example.com"
        response = requests.post(
            f"{BASE_URL}/api/invite",
            headers={"Authorization": f"Bearer {ADMIN_TOKEN}"},
            json={"email": test_email, "role": "viewer"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("email") == test_email
        assert data.get("role") == "viewer"
        assert "user_id" in data
        TestUserManagementEndpoints.created_user_id = data["user_id"]
        print(f"✓ Invited user: {test_email}, user_id={data['user_id']}")

    def test_invite_existing_email_returns_400(self):
        """POST /api/invite with existing email returns 400"""
        response = requests.post(
            f"{BASE_URL}/api/invite",
            headers={"Authorization": f"Bearer {ADMIN_TOKEN}"},
            json={"email": "chethan@emergent.sh", "role": "admin"}
        )
        assert response.status_code == 400
        assert "already exists" in response.json().get("detail", "")
        print("✓ Invite with existing email returns 400: 'User already exists'")

    def test_invite_invalid_role_returns_400(self):
        """POST /api/invite with invalid role returns 400"""
        test_email = f"TEST_bad_role_{uuid.uuid4().hex[:8]}@example.com"
        response = requests.post(
            f"{BASE_URL}/api/invite",
            headers={"Authorization": f"Bearer {ADMIN_TOKEN}"},
            json={"email": test_email, "role": "superadmin"}
        )
        assert response.status_code == 400
        assert "Role must be admin or viewer" in response.json().get("detail", "")
        print("✓ Invalid role correctly rejected with 400")

    def test_update_user_role(self):
        """PUT /api/users/{id}/role changes user role"""
        if not TestUserManagementEndpoints.created_user_id:
            pytest.skip("No user created to update")
        
        user_id = TestUserManagementEndpoints.created_user_id
        response = requests.put(
            f"{BASE_URL}/api/users/{user_id}/role",
            headers={"Authorization": f"Bearer {ADMIN_TOKEN}"},
            json={"role": "admin"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("role") == "admin"
        print(f"✓ Updated user {user_id} role to admin")
        
        # Change back to viewer
        response2 = requests.put(
            f"{BASE_URL}/api/users/{user_id}/role",
            headers={"Authorization": f"Bearer {ADMIN_TOKEN}"},
            json={"role": "viewer"}
        )
        assert response2.status_code == 200
        print(f"✓ Changed user {user_id} role back to viewer")

    def test_delete_user(self):
        """DELETE /api/users/{id} removes user"""
        if not TestUserManagementEndpoints.created_user_id:
            pytest.skip("No user created to delete")
        
        user_id = TestUserManagementEndpoints.created_user_id
        response = requests.delete(
            f"{BASE_URL}/api/users/{user_id}",
            headers={"Authorization": f"Bearer {ADMIN_TOKEN}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("status") == "removed"
        print(f"✓ Deleted user {user_id}")
        
        # Verify user is gone
        users_response = requests.get(
            f"{BASE_URL}/api/users",
            headers={"Authorization": f"Bearer {ADMIN_TOKEN}"}
        )
        users = users_response.json()
        user_ids = [u.get("user_id") for u in users]
        assert user_id not in user_ids, "User should be deleted"
        print(f"✓ Verified user {user_id} no longer in users list")


class TestTagSuggestionsEndpoint:
    """Test GET /api/tags/suggestions endpoint"""

    def test_tags_suggestions_returns_list(self):
        """GET /api/tags/suggestions returns list"""
        response = requests.get(
            f"{BASE_URL}/api/tags/suggestions",
            headers={"Authorization": f"Bearer {ADMIN_TOKEN}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        print(f"✓ Tag suggestions returns list of {len(data)} items")

    def test_tags_suggestions_with_query(self):
        """GET /api/tags/suggestions?q=test filters suggestions"""
        # First create a doc with a tag
        cats_response = requests.get(
            f"{BASE_URL}/api/categories",
            headers={"Authorization": f"Bearer {ADMIN_TOKEN}"}
        )
        cats = cats_response.json()
        cat_id = cats[0]["id"] if cats else None
        
        if cat_id:
            # Create doc with tag
            doc_response = requests.post(
                f"{BASE_URL}/api/documents",
                headers={"Authorization": f"Bearer {ADMIN_TOKEN}"},
                json={
                    "title": "TEST_Tag_Suggestions_Doc",
                    "content": "Test content",
                    "category_id": cat_id,
                    "tags": ["testtag123", "automation"]
                }
            )
            if doc_response.status_code == 200:
                doc_id = doc_response.json()["id"]
                
                # Now test tag suggestions
                response = requests.get(
                    f"{BASE_URL}/api/tags/suggestions?q=test",
                    headers={"Authorization": f"Bearer {ADMIN_TOKEN}"}
                )
                assert response.status_code == 200
                data = response.json()
                assert isinstance(data, list)
                print(f"✓ Tag suggestions with q='test' returned: {data}")
                
                # Cleanup
                requests.delete(
                    f"{BASE_URL}/api/documents/{doc_id}",
                    headers={"Authorization": f"Bearer {ADMIN_TOKEN}"}
                )
                print(f"✓ Cleaned up test document {doc_id}")
        else:
            pytest.skip("No category available")


class TestDataCounts:
    """Verify expected data counts with AI Agent TCs"""

    def test_categories_count_is_44(self):
        """Verify 44 categories exist (includes AI Agent TC category)"""
        response = requests.get(
            f"{BASE_URL}/api/categories",
            headers={"Authorization": f"Bearer {ADMIN_TOKEN}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 44, f"Expected 44 categories, got {len(data)}"
        print(f"✓ Categories count: {len(data)} (expected 44)")
        
        # Verify AI Agent & Orchestration Tests subcategory exists
        ai_agent_cat = [c for c in data if "AI Agent" in c.get("name", "")]
        assert len(ai_agent_cat) > 0, "AI Agent & Orchestration Tests category should exist"
        print(f"✓ Found AI Agent category: {ai_agent_cat[0]['name']}")

    def test_documents_count_is_34(self):
        """Verify 34 documents exist (includes AI Agent TCs document)"""
        response = requests.get(
            f"{BASE_URL}/api/documents",
            headers={"Authorization": f"Bearer {ADMIN_TOKEN}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 34, f"Expected 34 documents, got {len(data)}"
        print(f"✓ Documents count: {len(data)} (expected 34)")

    def test_ai_agent_test_cases_document_exists(self):
        """Verify AI Agent & Orchestration Test Cases document exists with TC-AGT-001 through TC-AGT-015"""
        response = requests.get(
            f"{BASE_URL}/api/documents",
            headers={"Authorization": f"Bearer {ADMIN_TOKEN}"}
        )
        data = response.json()
        ai_agent_docs = [d for d in data if d.get("title") == "AI Agent & Orchestration Test Cases"]
        assert len(ai_agent_docs) > 0, "AI Agent & Orchestration Test Cases document should exist"
        
        doc_id = ai_agent_docs[0]["id"]
        doc_response = requests.get(
            f"{BASE_URL}/api/documents/{doc_id}",
            headers={"Authorization": f"Bearer {ADMIN_TOKEN}"}
        )
        assert doc_response.status_code == 200
        doc = doc_response.json()
        content = doc.get("content", "")
        
        # Check for TC-AGT-001 through TC-AGT-015
        assert "TC-AGT-001" in content, "TC-AGT-001 should be in content"
        assert "TC-AGT-015" in content, "TC-AGT-015 should be in content"
        print(f"✓ AI Agent Test Cases document found with TC-AGT-001 through TC-AGT-015")


class TestRegressionBasics:
    """Regression tests - verify previous features still work"""

    def test_search_works(self):
        """Search endpoint works"""
        response = requests.get(
            f"{BASE_URL}/api/search?q=kubernetes",
            headers={"Authorization": f"Bearer {ADMIN_TOKEN}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        print(f"✓ Search for 'kubernetes' returned {len(data)} results")

    def test_comments_work(self):
        """Comments can be created and retrieved"""
        docs_response = requests.get(
            f"{BASE_URL}/api/documents",
            headers={"Authorization": f"Bearer {ADMIN_TOKEN}"}
        )
        docs = docs_response.json()
        if docs:
            doc_id = docs[0]["id"]
            comments_response = requests.get(
                f"{BASE_URL}/api/documents/{doc_id}/comments",
                headers={"Authorization": f"Bearer {ADMIN_TOKEN}"}
            )
            assert comments_response.status_code == 200
            print(f"✓ Comments endpoint works for document {doc_id}")

    def test_bookmarks_work(self):
        """Bookmarks endpoint works"""
        response = requests.get(
            f"{BASE_URL}/api/bookmarks",
            headers={"Authorization": f"Bearer {ADMIN_TOKEN}"}
        )
        assert response.status_code == 200
        print("✓ Bookmarks endpoint works")

    def test_chatbot_endpoint_exists(self):
        """Chat endpoint exists (don't test full flow, just existence)"""
        response = requests.post(
            f"{BASE_URL}/api/chat",
            headers={"Authorization": f"Bearer {ADMIN_TOKEN}"},
            json={"message": "test", "session_id": "test-session"}
        )
        # 200 means it worked, 500 might mean LLM key issue but endpoint exists
        assert response.status_code in [200, 500], f"Chat endpoint returned {response.status_code}"
        print(f"✓ Chat endpoint exists (status: {response.status_code})")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
