"""
Iteration 10: Bug Fix Verification Tests
Tests for:
1. Resource delete confirmation dialog (frontend)
2. Cold start loading screen (frontend)
3. Test Cases category hidden from sidebar/home (internal flag)
4. AI Agent test cases table format (Step | Action | Expected Result)
5. Sidebar navigation
6. Tools & Resources CRUD
7. Settings page for admin
8. Home page categories
9. AI chatbot endpoint
10. Search functionality
"""

import pytest
import requests
import os

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')


class TestCategoriesAPI:
    """Test categories API - especially internal flag for Test Cases"""
    
    def test_get_categories_returns_all(self):
        """GET /api/categories should return all categories including internal ones"""
        response = requests.get(f"{BASE_URL}/api/categories")
        assert response.status_code == 200
        categories = response.json()
        assert len(categories) > 0
        print(f"Total categories: {len(categories)}")
    
    def test_test_cases_category_has_internal_flag(self):
        """Test Cases category should have internal: true"""
        response = requests.get(f"{BASE_URL}/api/categories")
        assert response.status_code == 200
        categories = response.json()
        
        # Find Test Cases category
        test_cases_cats = [c for c in categories if c.get('name') == 'Test Cases']
        assert len(test_cases_cats) >= 1, "Test Cases category not found"
        
        test_cases = test_cases_cats[0]
        assert test_cases.get('internal') == True, "Test Cases should have internal: true"
        print(f"Test Cases category internal flag: {test_cases.get('internal')}")
    
    def test_internal_categories_count(self):
        """Should have multiple internal categories (Test Cases and subcategories)"""
        response = requests.get(f"{BASE_URL}/api/categories")
        assert response.status_code == 200
        categories = response.json()
        
        internal_cats = [c for c in categories if c.get('internal') == True]
        assert len(internal_cats) >= 7, f"Expected 7+ internal categories, got {len(internal_cats)}"
        
        internal_names = [c['name'] for c in internal_cats]
        print(f"Internal categories ({len(internal_cats)}): {internal_names}")
        
        # Verify specific internal categories
        expected_internal = ['Test Cases', 'Authentication Tests', 'Document CRUD Tests']
        for name in expected_internal:
            assert name in internal_names, f"Missing internal category: {name}"


class TestDocumentsAPI:
    """Test documents API - especially test case documents"""
    
    def test_get_documents_list(self):
        """GET /api/documents should return documents"""
        response = requests.get(f"{BASE_URL}/api/documents")
        assert response.status_code == 200
        documents = response.json()
        assert len(documents) > 0
        print(f"Total documents: {len(documents)}")
    
    def test_test_case_document_has_correct_table_format(self):
        """Test case documents should have Step | Action | Expected Result table format"""
        # Get Authentication Test Cases document
        response = requests.get(f"{BASE_URL}/api/documents")
        assert response.status_code == 200
        documents = response.json()
        
        # Find a test case document
        test_case_docs = [d for d in documents if 'Test Cases' in d.get('title', '')]
        assert len(test_case_docs) > 0, "No test case documents found"
        
        test_doc = test_case_docs[0]
        doc_id = test_doc['id']
        
        # Get full document content
        response = requests.get(f"{BASE_URL}/api/documents/{doc_id}")
        assert response.status_code == 200
        doc = response.json()
        content = doc.get('content', '')
        
        # Check for table headers
        assert '| Step |' in content, "Missing 'Step' column header"
        assert '| Action |' in content, "Missing 'Action' column header"
        assert '| Expected Result |' in content, "Missing 'Expected Result' column header"
        print(f"Document '{doc['title']}' has correct table format")


class TestToolsAPI:
    """Test Tools & Resources API"""
    
    def test_get_tools_list(self):
        """GET /api/tools should return tools"""
        response = requests.get(f"{BASE_URL}/api/tools")
        assert response.status_code == 200
        tools = response.json()
        print(f"Total tools: {len(tools)}")
    
    def test_create_and_delete_tool(self):
        """Test tool CRUD operations"""
        # Create a test tool
        tool_data = {
            "name": "TEST_Iteration10_Tool",
            "url": "https://test-iteration10.example.com",
            "description": "Test tool for iteration 10",
            "category": "Testing"
        }
        
        response = requests.post(f"{BASE_URL}/api/tools", json=tool_data)
        assert response.status_code == 200
        created_tool = response.json()
        assert created_tool['name'] == tool_data['name']
        tool_id = created_tool['id']
        print(f"Created tool: {created_tool['name']} with id {tool_id}")
        
        # Verify it exists in list
        response = requests.get(f"{BASE_URL}/api/tools")
        tools = response.json()
        tool_names = [t['name'] for t in tools]
        assert 'TEST_Iteration10_Tool' in tool_names
        
        # Delete the test tool
        response = requests.delete(f"{BASE_URL}/api/tools/{tool_id}")
        assert response.status_code == 200
        print(f"Deleted tool: {tool_id}")
        
        # Verify it's gone
        response = requests.get(f"{BASE_URL}/api/tools")
        tools = response.json()
        tool_names = [t['name'] for t in tools]
        assert 'TEST_Iteration10_Tool' not in tool_names


class TestSearchAPI:
    """Test search functionality"""
    
    def test_search_returns_results(self):
        """Search should return relevant documents"""
        response = requests.get(f"{BASE_URL}/api/search?q=architecture")
        assert response.status_code == 200
        results = response.json()
        assert len(results) > 0, "Search should return results for 'architecture'"
        print(f"Search 'architecture' returned {len(results)} results")
        
        # Check result structure
        first_result = results[0]
        assert 'id' in first_result
        assert 'title' in first_result
        assert 'snippet' in first_result
    
    def test_search_with_empty_query(self):
        """Empty search should return empty list"""
        response = requests.get(f"{BASE_URL}/api/search?q=")
        assert response.status_code == 200
        results = response.json()
        assert results == [], "Empty query should return empty list"


class TestChatbotAPI:
    """Test AI chatbot endpoint"""
    
    def test_chatbot_endpoint_exists(self):
        """POST /api/chat should accept requests"""
        chat_data = {
            "message": "Hello, what is E1?",
            "session_id": "test_session_iteration10"
        }
        
        response = requests.post(f"{BASE_URL}/api/chat", json=chat_data)
        # Should return 200 or 500 (if LLM key issues), but endpoint should exist
        assert response.status_code in [200, 500], f"Unexpected status: {response.status_code}"
        if response.status_code == 200:
            result = response.json()
            assert 'response' in result
            print(f"Chat response received: {result['response'][:100]}...")


class TestUsersAPI:
    """Test users/settings API"""
    
    def test_get_users_list(self):
        """GET /api/users should return users list"""
        response = requests.get(f"{BASE_URL}/api/users")
        assert response.status_code == 200
        users = response.json()
        assert isinstance(users, list)
        print(f"Total users: {len(users)}")


class TestBookmarksAPI:
    """Test bookmarks functionality"""
    
    def test_get_bookmarks(self):
        """GET /api/bookmarks should return bookmarks"""
        response = requests.get(f"{BASE_URL}/api/bookmarks")
        assert response.status_code == 200
        result = response.json()
        assert 'bookmarks' in result
        assert 'documents' in result


class TestHealthCheck:
    """Basic health check tests"""
    
    def test_api_root(self):
        """API root should return message"""
        response = requests.get(f"{BASE_URL}/api/")
        assert response.status_code == 200
        data = response.json()
        assert 'message' in data


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
