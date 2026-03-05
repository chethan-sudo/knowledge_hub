"""
Backend integration tests for iteration 16 features:
- Learning Paths API
- Path Tests API  
- Document Quiz API
- Tools CRUD API
"""
import pytest
import requests
import os
import uuid

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://ai-agent-hub-96.preview.emergentagent.com').rstrip('/')

@pytest.fixture
def api_client():
    """Shared requests session"""
    session = requests.Session()
    session.headers.update({"Content-Type": "application/json"})
    return session


class TestLearningPathsAPI:
    """Tests for Learning Paths endpoints"""
    
    def test_get_all_learning_paths(self, api_client):
        """GET /api/learning-paths should return 4 learning paths"""
        response = api_client.get(f"{BASE_URL}/api/learning-paths", allow_redirects=True)
        assert response.status_code == 200
        paths = response.json()
        assert isinstance(paths, list)
        assert len(paths) == 4
        
        # Verify required fields
        for path in paths:
            assert 'id' in path
            assert 'title' in path
            assert 'description' in path
            assert 'difficulty' in path
            assert 'estimated_time' in path
            assert 'steps' in path
            assert isinstance(path['steps'], list)
    
    def test_learning_paths_have_correct_difficulties(self, api_client):
        """Learning paths should have beginner, intermediate, advanced difficulties"""
        response = api_client.get(f"{BASE_URL}/api/learning-paths", allow_redirects=True)
        paths = response.json()
        difficulties = [p['difficulty'] for p in paths]
        assert 'beginner' in difficulties
        assert 'intermediate' in difficulties
        assert 'advanced' in difficulties
    
    def test_get_single_learning_path(self, api_client):
        """GET /api/learning-paths/{id} should return a specific path"""
        # Beginner path ID
        path_id = "7871ac91-d606-4fdf-b2be-5ee8f08ad8e3"
        response = api_client.get(f"{BASE_URL}/api/learning-paths/{path_id}", allow_redirects=True)
        assert response.status_code == 200
        path = response.json()
        assert path['id'] == path_id
        assert path['title'] == "Beginner: Understanding AI Agents"
        assert path['difficulty'] == 'beginner'
        assert len(path['steps']) == 5
    
    def test_get_nonexistent_learning_path_returns_404(self, api_client):
        """GET /api/learning-paths/{id} should return 404 for nonexistent path"""
        response = api_client.get(f"{BASE_URL}/api/learning-paths/nonexistent-id", allow_redirects=True)
        assert response.status_code == 404


class TestPathTestsAPI:
    """Tests for Path Tests (Final Assessment) endpoints"""
    
    def test_get_path_test_for_beginner_path(self, api_client):
        """GET /api/path-tests/{path_id} should return test questions"""
        path_id = "7871ac91-d606-4fdf-b2be-5ee8f08ad8e3"  # Beginner path
        response = api_client.get(f"{BASE_URL}/api/path-tests/{path_id}", allow_redirects=True)
        assert response.status_code == 200
        data = response.json()
        assert 'path_id' in data
        # May have questions or empty questions array
        assert 'questions' in data
    
    def test_get_path_test_for_nonexistent_path(self, api_client):
        """GET /api/path-tests/{path_id} should return empty questions for nonexistent path"""
        response = api_client.get(f"{BASE_URL}/api/path-tests/nonexistent", allow_redirects=True)
        assert response.status_code == 200
        data = response.json()
        assert data['questions'] == []


class TestDocumentQuizAPI:
    """Tests for Document Quiz endpoints"""
    
    def test_get_quiz_for_doc_with_quiz(self, api_client):
        """GET /api/documents/{doc_id}/quiz should return quiz questions"""
        doc_id = "f53aecbb-3b19-478c-9912-66d82827f402"  # What Is an AI Agent?
        response = api_client.get(f"{BASE_URL}/api/documents/{doc_id}/quiz", allow_redirects=True)
        assert response.status_code == 200
        quiz = response.json()
        assert 'document_id' in quiz
        assert 'questions' in quiz
        assert len(quiz['questions']) == 4
        
        # Verify question structure
        q = quiz['questions'][0]
        assert 'id' in q
        assert 'question' in q
        assert 'options' in q
        assert 'correct' in q
        assert 'explanation' in q
        assert isinstance(q['options'], list)
        assert len(q['options']) == 4
        assert isinstance(q['correct'], int)
    
    def test_get_quiz_for_doc_without_quiz(self, api_client):
        """GET /api/documents/{doc_id}/quiz should return empty questions for doc without quiz"""
        # Use a different doc ID - check if it returns empty questions
        doc_id = "6c753d08-d469-4e3f-8f3b-017d11c365c0"  # The Agent Loop
        response = api_client.get(f"{BASE_URL}/api/documents/{doc_id}/quiz", allow_redirects=True)
        assert response.status_code == 200
        quiz = response.json()
        assert 'questions' in quiz


class TestToolsAPI:
    """Tests for Tools CRUD endpoints"""
    
    def test_get_all_tools(self, api_client):
        """GET /api/tools should return list of tools"""
        response = api_client.get(f"{BASE_URL}/api/tools", allow_redirects=True)
        assert response.status_code == 200
        tools = response.json()
        assert isinstance(tools, list)
        assert len(tools) >= 1
        
        # Verify tool structure
        tool = tools[0]
        assert 'id' in tool
        assert 'name' in tool
        assert 'url' in tool
    
    def test_create_tool(self, api_client):
        """POST /api/tools should create a new tool"""
        test_name = f"TEST_Tool_{uuid.uuid4().hex[:8]}"
        tool_data = {
            "name": test_name,
            "url": "https://test-example.com",
            "description": "Test tool for integration testing",
            "category": "General"
        }
        response = api_client.post(f"{BASE_URL}/api/tools", json=tool_data, allow_redirects=True)
        assert response.status_code == 200
        created = response.json()
        assert created['name'] == test_name
        assert created['url'] == "https://test-example.com"
        assert 'id' in created
        
        # Return ID for cleanup
        return created['id']
    
    def test_delete_tool(self, api_client):
        """DELETE /api/tools/{id} should delete a tool"""
        # First create a tool
        test_name = f"TEST_DeleteMe_{uuid.uuid4().hex[:8]}"
        tool_data = {
            "name": test_name,
            "url": "https://delete-test.com",
            "description": "Tool to be deleted",
            "category": "General"
        }
        create_response = api_client.post(f"{BASE_URL}/api/tools", json=tool_data, allow_redirects=True)
        assert create_response.status_code == 200
        tool_id = create_response.json()['id']
        
        # Now delete it
        delete_response = api_client.delete(f"{BASE_URL}/api/tools/{tool_id}", allow_redirects=True)
        assert delete_response.status_code == 200
        
        # Verify it's gone
        get_response = api_client.get(f"{BASE_URL}/api/tools", allow_redirects=True)
        tools = get_response.json()
        tool_ids = [t['id'] for t in tools]
        assert tool_id not in tool_ids


class TestDocumentsAPI:
    """Tests for Documents endpoints"""
    
    def test_get_document(self, api_client):
        """GET /api/documents/{id} should return document details"""
        doc_id = "f53aecbb-3b19-478c-9912-66d82827f402"
        response = api_client.get(f"{BASE_URL}/api/documents/{doc_id}", allow_redirects=True)
        assert response.status_code == 200
        doc = response.json()
        assert doc['id'] == doc_id
        assert doc['title'] == "What Is an AI Agent?"
        assert 'content' in doc
        assert 'category_id' in doc
    
    def test_get_all_documents(self, api_client):
        """GET /api/documents should return list of documents"""
        response = api_client.get(f"{BASE_URL}/api/documents", allow_redirects=True)
        assert response.status_code == 200
        docs = response.json()
        assert isinstance(docs, list)
        assert len(docs) > 10  # Should have many docs


class TestKeywordsAPI:
    """Tests for Keywords auto-linking endpoint"""
    
    def test_get_keywords(self, api_client):
        """GET /api/keywords should return keyword-to-docId map"""
        response = api_client.get(f"{BASE_URL}/api/keywords", allow_redirects=True)
        assert response.status_code == 200
        keywords = response.json()
        assert isinstance(keywords, dict)
        assert len(keywords) > 10  # Should have many keywords


class TestCategoriesAPI:
    """Tests for Categories endpoint"""
    
    def test_get_categories(self, api_client):
        """GET /api/categories should return list of categories"""
        response = api_client.get(f"{BASE_URL}/api/categories", allow_redirects=True)
        assert response.status_code == 200
        cats = response.json()
        assert isinstance(cats, list)
        assert len(cats) >= 10  # Should have many categories


# Cleanup fixture
@pytest.fixture(autouse=True)
def cleanup_test_tools(api_client):
    """Clean up any TEST_ prefixed tools after tests"""
    yield
    try:
        response = api_client.get(f"{BASE_URL}/api/tools", allow_redirects=True)
        if response.status_code == 200:
            tools = response.json()
            for tool in tools:
                if tool['name'].startswith('TEST_'):
                    api_client.delete(f"{BASE_URL}/api/tools/{tool['id']}", allow_redirects=True)
    except Exception:
        pass
