"""
Test iteration 4 fixes:
1. 46 categories and 36 documents exist
2. System Architecture doc contains 'Database Layer', 'job_audits', 'Tool Registry', 'ENV'
3. Platform Limitations doc exists
4. Complete UI Guide doc exists  
5. POST /api/chat returns detailed response about system architecture
6. Limitations & Constraints category visible
7. UI Guide category visible
"""
import pytest
import requests
import os

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')
if not BASE_URL:
    BASE_URL = "http://localhost:8001"

# Test session token for admin
ADMIN_TOKEN = "test_admin_session_token"

@pytest.fixture
def admin_session():
    """Admin session with cookie authentication"""
    session = requests.Session()
    session.cookies.set("session_token", ADMIN_TOKEN)
    session.headers.update({"Content-Type": "application/json"})
    return session


class TestCategories:
    """Test category counts and new categories"""
    
    def test_categories_count_46(self, admin_session):
        """Backend should have 46 categories"""
        response = admin_session.get(f"{BASE_URL}/api/categories")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        categories = response.json()
        assert len(categories) == 46, f"Expected 46 categories, got {len(categories)}"
    
    def test_limitations_category_exists(self, admin_session):
        """Limitations & Constraints category should exist"""
        response = admin_session.get(f"{BASE_URL}/api/categories")
        assert response.status_code == 200
        categories = response.json()
        limitations = [c for c in categories if "Limitations" in c.get("name", "")]
        assert len(limitations) > 0, "Limitations & Constraints category not found"
        assert limitations[0]["name"] == "Limitations & Constraints"
    
    def test_ui_guide_category_exists(self, admin_session):
        """UI Guide category should exist"""
        response = admin_session.get(f"{BASE_URL}/api/categories")
        assert response.status_code == 200
        categories = response.json()
        ui_guide = [c for c in categories if "UI Guide" in c.get("name", "")]
        assert len(ui_guide) > 0, "UI Guide category not found"
        assert ui_guide[0]["name"] == "UI Guide"


class TestDocuments:
    """Test document counts and new documents"""
    
    def test_documents_count_36(self, admin_session):
        """Backend should have 36 documents"""
        response = admin_session.get(f"{BASE_URL}/api/documents")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        documents = response.json()
        assert len(documents) == 36, f"Expected 36 documents, got {len(documents)}"
    
    def test_platform_limitations_doc_exists(self, admin_session):
        """Platform Limitations document should exist"""
        response = admin_session.get(f"{BASE_URL}/api/documents")
        assert response.status_code == 200
        documents = response.json()
        limitations_doc = next((d for d in documents if "Platform Limitations" in d.get("title", "")), None)
        assert limitations_doc is not None, "Platform Limitations document not found"
    
    def test_complete_ui_guide_doc_exists(self, admin_session):
        """Complete UI Guide document should exist"""
        response = admin_session.get(f"{BASE_URL}/api/documents")
        assert response.status_code == 200
        documents = response.json()
        ui_guide_doc = next((d for d in documents if "Complete UI Guide" in d.get("title", "")), None)
        assert ui_guide_doc is not None, "Complete UI Guide document not found"


class TestSystemArchitecture:
    """Test System Architecture document content"""
    
    def test_system_arch_contains_database_layer(self, admin_session):
        """System Architecture doc should contain Database Layer section"""
        response = admin_session.get(f"{BASE_URL}/api/documents")
        assert response.status_code == 200
        documents = response.json()
        sys_arch = next((d for d in documents if "System Architecture" in d.get("title", "")), None)
        assert sys_arch is not None, "System Architecture Overview document not found"
        content = sys_arch.get("content", "")
        assert "Database Layer" in content, "Database Layer section not found in System Architecture"
    
    def test_system_arch_contains_job_audits(self, admin_session):
        """System Architecture doc should contain job_audits"""
        response = admin_session.get(f"{BASE_URL}/api/documents")
        assert response.status_code == 200
        documents = response.json()
        sys_arch = next((d for d in documents if "System Architecture" in d.get("title", "")), None)
        assert sys_arch is not None
        content = sys_arch.get("content", "")
        assert "job_audits" in content, "job_audits not found in System Architecture"
    
    def test_system_arch_contains_tool_registry(self, admin_session):
        """System Architecture doc should contain Tool Registry"""
        response = admin_session.get(f"{BASE_URL}/api/documents")
        assert response.status_code == 200
        documents = response.json()
        sys_arch = next((d for d in documents if "System Architecture" in d.get("title", "")), None)
        assert sys_arch is not None
        content = sys_arch.get("content", "")
        assert "Tool Registry" in content, "Tool Registry not found in System Architecture"
    
    def test_system_arch_contains_env(self, admin_session):
        """System Architecture doc should contain ENV section"""
        response = admin_session.get(f"{BASE_URL}/api/documents")
        assert response.status_code == 200
        documents = response.json()
        sys_arch = next((d for d in documents if "System Architecture" in d.get("title", "")), None)
        assert sys_arch is not None
        content = sys_arch.get("content", "")
        assert "ENV" in content, "ENV section not found in System Architecture"


class TestChatEndpoint:
    """Test AI chatbot endpoint with system architecture questions"""
    
    def test_chat_returns_response(self, admin_session):
        """POST /api/chat should return a response"""
        payload = {
            "message": "What is the system architecture?",
            "session_id": "test_iter4_session"
        }
        response = admin_session.post(f"{BASE_URL}/api/chat", json=payload, timeout=30)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        data = response.json()
        assert "response" in data, "Response should contain 'response' key"
        assert len(data["response"]) > 100, "Response should be substantial (>100 chars)"
    
    def test_chat_about_database_layer(self, admin_session):
        """Chat about database layer should return relevant info"""
        payload = {
            "message": "What collections are in the Database Layer?",
            "session_id": "test_iter4_db_session"
        }
        response = admin_session.post(f"{BASE_URL}/api/chat", json=payload, timeout=30)
        assert response.status_code == 200
        data = response.json()
        resp_text = data.get("response", "").lower()
        # Should mention MongoDB or database-related terms
        assert any(term in resp_text for term in ["mongodb", "database", "collection"]), \
            f"Chat should mention database terms, got: {resp_text[:200]}"


class TestRegression:
    """Regression tests for existing functionality"""
    
    def test_auth_me_endpoint(self, admin_session):
        """GET /api/auth/me should return user info"""
        response = admin_session.get(f"{BASE_URL}/api/auth/me")
        assert response.status_code == 200
        data = response.json()
        assert "user_id" in data
        assert "email" in data
        assert "role" in data
    
    def test_search_endpoint(self, admin_session):
        """GET /api/search should work"""
        response = admin_session.get(f"{BASE_URL}/api/search?q=kubernetes")
        assert response.status_code == 200
        results = response.json()
        assert isinstance(results, list)
    
    def test_bookmarks_endpoint(self, admin_session):
        """GET /api/bookmarks should return bookmarks"""
        response = admin_session.get(f"{BASE_URL}/api/bookmarks")
        assert response.status_code == 200
        data = response.json()
        assert "bookmarks" in data
        assert "documents" in data
    
    def test_templates_endpoint(self, admin_session):
        """GET /api/templates should return 5 templates"""
        response = admin_session.get(f"{BASE_URL}/api/templates")
        assert response.status_code == 200
        templates = response.json()
        assert len(templates) == 5, f"Expected 5 templates, got {len(templates)}"
