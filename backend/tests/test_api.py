"""
Backend API Tests for Emergent Document Hub
- Tests all auth endpoints (register, login, me)
- Tests categories and documents CRUD
- Tests bookmarks and search functionality
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

class TestHealthCheck:
    """Basic API health check"""
    
    def test_api_root(self):
        """API root endpoint returns 200"""
        response = requests.get(f"{BASE_URL}/api/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Emergent Document Hub API" in data["message"]
        print(f"✓ API root working: {data}")


class TestAuthentication:
    """Authentication endpoint tests"""
    
    def test_register_existing_user(self):
        """Registration returns 400 for existing user (expected)"""
        response = requests.post(f"{BASE_URL}/api/auth/register", json=TEST_USER)
        # User already exists from seeding
        assert response.status_code == 400
        data = response.json()
        assert "already registered" in data.get("detail", "").lower()
        print(f"✓ Register existing user returns 400 as expected")
    
    def test_register_new_user(self):
        """Registration works for new users"""
        unique_email = f"test_{uuid.uuid4().hex[:8]}@test.com"
        new_user = {
            "email": unique_email,
            "password": "testpass123",
            "name": "New Test User"
        }
        response = requests.post(f"{BASE_URL}/api/auth/register", json=new_user)
        assert response.status_code == 200
        data = response.json()
        assert "token" in data
        assert "user" in data
        assert data["user"]["email"] == unique_email
        print(f"✓ New user registration successful: {unique_email}")
    
    def test_login_success(self):
        """Login with valid credentials returns token"""
        global AUTH_TOKEN
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": TEST_USER["email"],
            "password": TEST_USER["password"]
        })
        assert response.status_code == 200
        data = response.json()
        assert "token" in data
        assert "user" in data
        assert data["user"]["email"] == TEST_USER["email"]
        AUTH_TOKEN = data["token"]
        print(f"✓ Login successful, token obtained")
    
    def test_login_invalid_credentials(self):
        """Login with invalid credentials returns 401"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": "nonexistent@test.com",
            "password": "wrongpassword"
        })
        assert response.status_code == 401
        print(f"✓ Invalid login returns 401")
    
    def test_get_me_authenticated(self):
        """GET /auth/me returns user info when authenticated"""
        global AUTH_TOKEN
        if not AUTH_TOKEN:
            pytest.skip("No auth token available")
        
        headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}
        response = requests.get(f"{BASE_URL}/api/auth/me", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "email" in data
        assert data["email"] == TEST_USER["email"]
        print(f"✓ GET /auth/me returns user: {data['email']}")
    
    def test_get_me_unauthenticated(self):
        """GET /auth/me returns 401 when not authenticated"""
        response = requests.get(f"{BASE_URL}/api/auth/me")
        assert response.status_code == 401
        print(f"✓ GET /auth/me without token returns 401")


class TestCategories:
    """Categories API tests"""
    
    @pytest.fixture(autouse=True)
    def ensure_auth(self):
        """Ensure we have auth token before tests"""
        global AUTH_TOKEN
        if not AUTH_TOKEN:
            response = requests.post(f"{BASE_URL}/api/auth/login", json={
                "email": TEST_USER["email"],
                "password": TEST_USER["password"]
            })
            if response.status_code == 200:
                AUTH_TOKEN = response.json()["token"]
    
    def test_get_categories(self):
        """GET /categories returns 34 categories"""
        global AUTH_TOKEN
        headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}
        response = requests.get(f"{BASE_URL}/api/categories", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 34, f"Expected 34 categories, got {len(data)}"
        print(f"✓ GET /categories returns {len(data)} categories")
    
    def test_categories_have_parent_structure(self):
        """Categories have proper parent-child structure"""
        global AUTH_TOKEN
        headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}
        response = requests.get(f"{BASE_URL}/api/categories", headers=headers)
        data = response.json()
        
        # Check parent categories (no parent_id)
        parents = [c for c in data if c.get("parent_id") is None]
        children = [c for c in data if c.get("parent_id") is not None]
        
        assert len(parents) == 10, f"Expected 10 parent categories, got {len(parents)}"
        assert len(children) == 24, f"Expected 24 child categories, got {len(children)}"
        print(f"✓ Categories structure: {len(parents)} parents, {len(children)} children")
    
    def test_create_category(self):
        """POST /categories creates new category"""
        global AUTH_TOKEN
        headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}
        new_cat = {
            "name": f"Test Category {uuid.uuid4().hex[:6]}",
            "icon": "FileText",
            "order": 99
        }
        response = requests.post(f"{BASE_URL}/api/categories", headers=headers, json=new_cat)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == new_cat["name"]
        assert "id" in data
        print(f"✓ Created category: {data['name']}")


class TestDocuments:
    """Documents API tests"""
    
    @pytest.fixture(autouse=True)
    def ensure_auth(self):
        """Ensure we have auth token before tests"""
        global AUTH_TOKEN
        if not AUTH_TOKEN:
            response = requests.post(f"{BASE_URL}/api/auth/login", json={
                "email": TEST_USER["email"],
                "password": TEST_USER["password"]
            })
            if response.status_code == 200:
                AUTH_TOKEN = response.json()["token"]
    
    def test_get_documents(self):
        """GET /documents returns 26 documents"""
        global AUTH_TOKEN
        headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}
        response = requests.get(f"{BASE_URL}/api/documents", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 26, f"Expected 26 documents, got {len(data)}"
        print(f"✓ GET /documents returns {len(data)} documents")
    
    def test_documents_have_mermaid_content(self):
        """At least 22 documents contain mermaid diagrams"""
        global AUTH_TOKEN
        headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}
        response = requests.get(f"{BASE_URL}/api/documents", headers=headers)
        data = response.json()
        
        mermaid_count = sum(1 for d in data if "```mermaid" in d.get("content", ""))
        assert mermaid_count >= 22, f"Expected 22+ docs with mermaid, got {mermaid_count}"
        print(f"✓ {mermaid_count} documents have mermaid diagrams")
    
    def test_get_single_document(self):
        """GET /documents/{id} returns specific document"""
        global AUTH_TOKEN
        headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}
        
        # First get list to get a valid ID
        list_response = requests.get(f"{BASE_URL}/api/documents", headers=headers)
        docs = list_response.json()
        doc_id = docs[0]["id"]
        
        response = requests.get(f"{BASE_URL}/api/documents/{doc_id}", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == doc_id
        print(f"✓ GET single document: {data['title']}")
    
    def test_document_crud_flow(self):
        """Full CRUD flow: Create -> Read -> Update -> Delete"""
        global AUTH_TOKEN
        headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}
        
        # Get a valid category ID first
        cat_response = requests.get(f"{BASE_URL}/api/categories", headers=headers)
        cats = cat_response.json()
        cat_id = cats[0]["id"]
        
        # CREATE
        new_doc = {
            "title": f"TEST_Doc_{uuid.uuid4().hex[:6]}",
            "content": "# Test Document\n\nThis is test content.",
            "category_id": cat_id,
            "order": 99
        }
        create_response = requests.post(f"{BASE_URL}/api/documents", headers=headers, json=new_doc)
        assert create_response.status_code == 200
        created = create_response.json()
        doc_id = created["id"]
        assert created["title"] == new_doc["title"]
        print(f"✓ CREATE document: {doc_id}")
        
        # READ
        read_response = requests.get(f"{BASE_URL}/api/documents/{doc_id}", headers=headers)
        assert read_response.status_code == 200
        read_data = read_response.json()
        assert read_data["title"] == new_doc["title"]
        print(f"✓ READ document verified")
        
        # UPDATE
        update_payload = {"title": f"UPDATED_{new_doc['title']}"}
        update_response = requests.put(f"{BASE_URL}/api/documents/{doc_id}", headers=headers, json=update_payload)
        assert update_response.status_code == 200
        updated = update_response.json()
        assert "UPDATED_" in updated["title"]
        print(f"✓ UPDATE document: {updated['title']}")
        
        # Verify update persisted
        verify_response = requests.get(f"{BASE_URL}/api/documents/{doc_id}", headers=headers)
        assert verify_response.json()["title"] == updated["title"]
        print(f"✓ UPDATE verified via GET")
        
        # DELETE
        delete_response = requests.delete(f"{BASE_URL}/api/documents/{doc_id}", headers=headers)
        assert delete_response.status_code == 200
        print(f"✓ DELETE document")
        
        # Verify deletion
        verify_delete = requests.get(f"{BASE_URL}/api/documents/{doc_id}", headers=headers)
        assert verify_delete.status_code == 404
        print(f"✓ DELETE verified - document not found")


class TestBookmarks:
    """Bookmarks API tests"""
    
    @pytest.fixture(autouse=True)
    def ensure_auth(self):
        """Ensure we have auth token before tests"""
        global AUTH_TOKEN
        if not AUTH_TOKEN:
            response = requests.post(f"{BASE_URL}/api/auth/login", json={
                "email": TEST_USER["email"],
                "password": TEST_USER["password"]
            })
            if response.status_code == 200:
                AUTH_TOKEN = response.json()["token"]
    
    def test_get_bookmarks(self):
        """GET /bookmarks returns bookmarks list"""
        global AUTH_TOKEN
        headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}
        response = requests.get(f"{BASE_URL}/api/bookmarks", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert "bookmarks" in data
        assert "documents" in data
        print(f"✓ GET /bookmarks: {len(data['bookmarks'])} bookmarks")
    
    def test_toggle_bookmark(self):
        """POST /bookmarks/{doc_id} toggles bookmark status"""
        global AUTH_TOKEN
        headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}
        
        # Get a document ID
        docs_response = requests.get(f"{BASE_URL}/api/documents", headers=headers)
        doc_id = docs_response.json()[0]["id"]
        
        # Toggle bookmark (add)
        toggle1 = requests.post(f"{BASE_URL}/api/bookmarks/{doc_id}", headers=headers)
        assert toggle1.status_code == 200
        bookmark_state1 = toggle1.json()["bookmarked"]
        print(f"✓ Toggle bookmark (state: {bookmark_state1})")
        
        # Toggle again (should flip)
        toggle2 = requests.post(f"{BASE_URL}/api/bookmarks/{doc_id}", headers=headers)
        assert toggle2.status_code == 200
        bookmark_state2 = toggle2.json()["bookmarked"]
        assert bookmark_state1 != bookmark_state2, "Bookmark should toggle between states"
        print(f"✓ Toggle bookmark again (state: {bookmark_state2})")


class TestSearch:
    """Search API tests"""
    
    @pytest.fixture(autouse=True)
    def ensure_auth(self):
        """Ensure we have auth token before tests"""
        global AUTH_TOKEN
        if not AUTH_TOKEN:
            response = requests.post(f"{BASE_URL}/api/auth/login", json={
                "email": TEST_USER["email"],
                "password": TEST_USER["password"]
            })
            if response.status_code == 200:
                AUTH_TOKEN = response.json()["token"]
    
    def test_search_documents(self):
        """GET /search?q=... returns matching documents"""
        global AUTH_TOKEN
        headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}
        
        # Search for "kubernetes"
        response = requests.get(f"{BASE_URL}/api/search?q=kubernetes", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0, "Should find documents matching 'kubernetes'"
        print(f"✓ Search 'kubernetes': {len(data)} results")
    
    def test_search_agent(self):
        """Search for 'agent' returns results"""
        global AUTH_TOKEN
        headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}
        
        response = requests.get(f"{BASE_URL}/api/search?q=agent", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0, "Should find documents matching 'agent'"
        print(f"✓ Search 'agent': {len(data)} results")
    
    def test_search_short_query_returns_empty(self):
        """Search with <2 chars returns empty"""
        global AUTH_TOKEN
        headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}
        
        response = requests.get(f"{BASE_URL}/api/search?q=a", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data == [], "Short query should return empty"
        print(f"✓ Short search query returns empty")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
