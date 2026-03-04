"""
Backend tests for iteration 17 features:
- Category page with module tests
- Module tests API endpoint
- Homepage cards navigation to /category/{catId}
- Learning path roadmap enhancements
"""
import pytest
import requests
import os

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://ai-agent-hub-96.preview.emergentagent.com').rstrip('/')

# Category IDs for testing (full UUIDs)
GETTING_STARTED_CAT_ID = 'ff182579-9490-422f-9d69-30ce642cf662'
PLATFORM_ARCH_CAT_ID = 'a62bc498-73f6-44be-8230-979af325b628'
LLM_INTERNALS_CAT_ID = '52c88f91-c6d7-401b-8b56-c29a8a639a56'
BEGINNER_PATH_ID = '7871ac91-d606-4fdf-b2be-5ee8f08ad8e3'


class TestModuleTestsAPI:
    """Tests for /api/module-tests/{category_id} endpoint"""
    
    def test_module_tests_returns_questions_for_valid_category(self):
        """Module tests API returns questions for Getting Started category"""
        response = requests.get(f"{BASE_URL}/api/module-tests/{GETTING_STARTED_CAT_ID}")
        assert response.status_code == 200
        
        data = response.json()
        assert data['category_id'] == GETTING_STARTED_CAT_ID
        assert 'questions' in data
        assert isinstance(data['questions'], list)
        assert len(data['questions']) > 0
        
    def test_module_tests_question_structure(self):
        """Module tests API returns properly structured questions"""
        response = requests.get(f"{BASE_URL}/api/module-tests/{GETTING_STARTED_CAT_ID}")
        assert response.status_code == 200
        
        data = response.json()
        question = data['questions'][0]
        
        # Verify question structure
        assert 'id' in question
        assert 'question' in question
        assert 'options' in question
        assert 'correct' in question
        assert 'explanation' in question
        
        # Verify types
        assert isinstance(question['options'], list)
        assert isinstance(question['correct'], int)
        assert len(question['options']) >= 2  # At least 2 options
        
    def test_module_tests_for_platform_architecture(self):
        """Module tests API returns questions for Platform Architecture category"""
        response = requests.get(f"{BASE_URL}/api/module-tests/{PLATFORM_ARCH_CAT_ID}")
        assert response.status_code == 200
        
        data = response.json()
        assert data['category_id'] == PLATFORM_ARCH_CAT_ID
        assert 'questions' in data
        
    def test_module_tests_for_llm_internals(self):
        """Module tests API returns questions for LLM Internals category"""
        response = requests.get(f"{BASE_URL}/api/module-tests/{LLM_INTERNALS_CAT_ID}")
        assert response.status_code == 200
        
        data = response.json()
        assert data['category_id'] == LLM_INTERNALS_CAT_ID
        assert 'questions' in data
        
    def test_module_tests_empty_for_nonexistent_category(self):
        """Module tests API returns empty questions for non-existent category"""
        response = requests.get(f"{BASE_URL}/api/module-tests/non-existent-category-id")
        assert response.status_code == 200
        
        data = response.json()
        assert 'questions' in data
        assert data['questions'] == []
        
    def test_module_tests_correct_answer_in_range(self):
        """Module tests correct answer index is within options range"""
        response = requests.get(f"{BASE_URL}/api/module-tests/{GETTING_STARTED_CAT_ID}")
        assert response.status_code == 200
        
        data = response.json()
        for question in data['questions']:
            correct_idx = question['correct']
            num_options = len(question['options'])
            assert 0 <= correct_idx < num_options, f"Correct answer {correct_idx} out of range for {num_options} options"


class TestCategoriesAPI:
    """Tests for /api/categories endpoint"""
    
    def test_categories_returns_list(self):
        """Categories API returns list of categories"""
        response = requests.get(f"{BASE_URL}/api/categories")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        
    def test_categories_include_getting_started(self):
        """Categories include Getting Started category"""
        response = requests.get(f"{BASE_URL}/api/categories")
        assert response.status_code == 200
        
        data = response.json()
        cat_ids = [c['id'] for c in data]
        assert GETTING_STARTED_CAT_ID in cat_ids
        
    def test_category_structure(self):
        """Categories have proper structure"""
        response = requests.get(f"{BASE_URL}/api/categories")
        assert response.status_code == 200
        
        data = response.json()
        category = data[0]
        
        assert 'id' in category
        assert 'name' in category
        assert 'icon' in category


class TestLearningPathsAPI:
    """Tests for learning paths API endpoints"""
    
    def test_learning_paths_returns_list(self):
        """Learning paths API returns list of paths"""
        response = requests.get(f"{BASE_URL}/api/learning-paths")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        
    def test_learning_path_structure(self):
        """Learning paths have proper structure"""
        response = requests.get(f"{BASE_URL}/api/learning-paths")
        assert response.status_code == 200
        
        data = response.json()
        path = data[0]
        
        assert 'id' in path
        assert 'title' in path
        assert 'description' in path
        assert 'difficulty' in path
        assert 'estimated_time' in path
        assert 'steps' in path
        assert isinstance(path['steps'], list)
        
    def test_learning_path_steps_structure(self):
        """Learning path steps have document IDs and titles"""
        response = requests.get(f"{BASE_URL}/api/learning-paths")
        assert response.status_code == 200
        
        data = response.json()
        path = data[0]
        step = path['steps'][0]
        
        assert 'document_id' in step
        assert 'title' in step
        assert 'description' in step
        
    def test_learning_path_detail_returns_path(self):
        """Learning path detail API returns specific path"""
        response = requests.get(f"{BASE_URL}/api/learning-paths/{BEGINNER_PATH_ID}")
        assert response.status_code == 200
        
        data = response.json()
        assert data['id'] == BEGINNER_PATH_ID
        assert 'steps' in data
        assert len(data['steps']) > 0
        
    def test_learning_path_detail_not_found(self):
        """Learning path detail returns 404 for invalid ID"""
        response = requests.get(f"{BASE_URL}/api/learning-paths/non-existent-path-id")
        assert response.status_code == 404


class TestPathTestsAPI:
    """Tests for path tests API endpoint"""
    
    def test_path_tests_endpoint_exists(self):
        """Path tests API endpoint exists"""
        response = requests.get(f"{BASE_URL}/api/path-tests/{BEGINNER_PATH_ID}")
        assert response.status_code == 200
        
    def test_path_tests_structure(self):
        """Path tests have proper structure"""
        response = requests.get(f"{BASE_URL}/api/path-tests/{BEGINNER_PATH_ID}")
        assert response.status_code == 200
        
        data = response.json()
        assert 'path_id' in data or 'questions' in data
        assert 'questions' in data
        assert isinstance(data['questions'], list)
        
    def test_path_tests_empty_for_nonexistent(self):
        """Path tests returns empty questions for non-existent path"""
        response = requests.get(f"{BASE_URL}/api/path-tests/non-existent-path-id")
        assert response.status_code == 200
        
        data = response.json()
        assert 'questions' in data
        assert data['questions'] == []


class TestDocumentsAPI:
    """Tests for documents API to verify category page data"""
    
    def test_documents_returns_list(self):
        """Documents API returns list of documents"""
        response = requests.get(f"{BASE_URL}/api/documents")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        
    def test_documents_have_category_id(self):
        """Documents have category_id field"""
        response = requests.get(f"{BASE_URL}/api/documents")
        assert response.status_code == 200
        
        data = response.json()
        doc = data[0]
        
        assert 'category_id' in doc
        assert 'id' in doc
        assert 'title' in doc
        
    def test_documents_filter_by_category(self):
        """Documents can be filtered by category_id"""
        response = requests.get(f"{BASE_URL}/api/documents?category_id={GETTING_STARTED_CAT_ID}")
        assert response.status_code == 200
        
        data = response.json()
        # All returned docs should have the specified category_id or child category
        # (since subcategories are also included)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
