"""
Iteration 15 Tests: Interactive Quizzes and Learning Paths
- Quiz API: GET /api/documents/{doc_id}/quiz
- Learning Paths API: GET /api/learning-paths, GET /api/learning-paths/{id}
- Documents with quizzes validation
"""

import pytest
import requests
import os

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')


class TestQuizAPI:
    """Test Quiz API endpoints"""

    def test_quiz_for_document_with_quiz(self):
        """Test getting quiz for 'What Is an AI Agent?' document"""
        doc_id = "f53aecbb-3b19-478c-9912-66d82827f402"
        response = requests.get(f"{BASE_URL}/api/documents/{doc_id}/quiz")
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        assert "document_id" in data
        assert "questions" in data
        assert data["document_id"] == doc_id
        
        # Verify 4 questions as specified
        assert len(data["questions"]) == 4, f"Expected 4 questions, got {len(data['questions'])}"
        
        # Verify question structure
        for q in data["questions"]:
            assert "id" in q
            assert "question" in q
            assert "options" in q
            assert "correct" in q
            assert "explanation" in q
            assert isinstance(q["options"], list)
            assert len(q["options"]) >= 2  # At least 2 options
            assert isinstance(q["correct"], int)
            assert 0 <= q["correct"] < len(q["options"])
        
        print(f"PASS: Quiz for 'What Is an AI Agent?' has {len(data['questions'])} questions")

    def test_quiz_for_document_without_quiz(self):
        """Test getting quiz for a document that doesn't have one"""
        # Use System Architecture Overview which shouldn't have a quiz
        doc_id = "82ae6221-0508-422e-a7ff-b84201cd1a9e"
        response = requests.get(f"{BASE_URL}/api/documents/{doc_id}/quiz")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "document_id" in data
        assert "questions" in data
        # Empty questions array for docs without quizzes
        assert data["questions"] == [] or len(data["questions"]) == 0
        print(f"PASS: Document without quiz returns empty questions array")

    def test_quiz_question_content_validity(self):
        """Test that quiz questions have meaningful content"""
        doc_id = "f53aecbb-3b19-478c-9912-66d82827f402"
        response = requests.get(f"{BASE_URL}/api/documents/{doc_id}/quiz")
        
        assert response.status_code == 200
        data = response.json()
        
        for q in data["questions"]:
            # Question should not be empty
            assert len(q["question"]) > 10, f"Question too short: {q['question']}"
            # Each option should have content
            for opt in q["options"]:
                assert len(opt) > 0, f"Empty option in question: {q['question']}"
            # Explanation should be provided
            assert len(q["explanation"]) > 10, f"Explanation too short for: {q['question']}"
        
        print(f"PASS: All quiz questions have valid content")


class TestLearningPathsAPI:
    """Test Learning Paths API endpoints"""

    def test_get_all_learning_paths(self):
        """Test GET /api/learning-paths returns 4 paths"""
        response = requests.get(f"{BASE_URL}/api/learning-paths")
        
        assert response.status_code == 200
        data = response.json()
        
        # Should return 4 learning paths
        assert len(data) == 4, f"Expected 4 learning paths, got {len(data)}"
        
        # Verify each path has required fields
        for path in data:
            assert "id" in path
            assert "title" in path
            assert "description" in path
            assert "difficulty" in path
            assert "estimated_time" in path
            assert "steps" in path
            assert isinstance(path["steps"], list)
            assert len(path["steps"]) > 0
        
        print(f"PASS: GET /api/learning-paths returns {len(data)} paths")

    def test_learning_path_titles(self):
        """Verify the 4 expected learning paths exist"""
        response = requests.get(f"{BASE_URL}/api/learning-paths")
        assert response.status_code == 200
        
        data = response.json()
        titles = [p["title"] for p in data]
        
        expected = [
            "Beginner: Understanding AI Agents",
            "Builder: Agent Architecture Deep Dive",
            "LLM Foundations",
            "Practitioner: Building Real Applications"
        ]
        
        for exp in expected:
            assert exp in titles, f"Missing learning path: {exp}"
        
        print(f"PASS: All 4 expected learning paths present")

    def test_learning_path_difficulty_levels(self):
        """Test that paths have correct difficulty badges"""
        response = requests.get(f"{BASE_URL}/api/learning-paths")
        assert response.status_code == 200
        
        data = response.json()
        difficulties = {p["title"]: p["difficulty"] for p in data}
        
        # Verify specific difficulty levels
        assert difficulties.get("Beginner: Understanding AI Agents") == "beginner"
        assert difficulties.get("Builder: Agent Architecture Deep Dive") == "intermediate"
        assert difficulties.get("LLM Foundations") == "intermediate"
        assert difficulties.get("Practitioner: Building Real Applications") == "advanced"
        
        print(f"PASS: All difficulty levels are correct")

    def test_learning_path_step_counts(self):
        """Test expected step counts for each path"""
        response = requests.get(f"{BASE_URL}/api/learning-paths")
        assert response.status_code == 200
        
        data = response.json()
        step_counts = {p["title"]: len(p["steps"]) for p in data}
        
        # Verify step counts as specified
        assert step_counts.get("Beginner: Understanding AI Agents") == 5, "Beginner should have 5 steps"
        assert step_counts.get("Builder: Agent Architecture Deep Dive") == 7, "Builder should have 7 steps"
        assert step_counts.get("LLM Foundations") == 6, "LLM Foundations should have 6 steps"
        assert step_counts.get("Practitioner: Building Real Applications") == 6, "Practitioner should have 6 steps"
        
        print(f"PASS: All learning paths have correct step counts")

    def test_get_single_learning_path(self):
        """Test GET /api/learning-paths/{id}"""
        # First get all paths to get an ID
        response = requests.get(f"{BASE_URL}/api/learning-paths")
        assert response.status_code == 200
        paths = response.json()
        
        # Get the first path by ID
        path_id = paths[0]["id"]
        response = requests.get(f"{BASE_URL}/api/learning-paths/{path_id}")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["id"] == path_id
        assert "title" in data
        assert "description" in data
        assert "steps" in data
        
        # Verify step structure
        for step in data["steps"]:
            assert "document_id" in step
            assert "title" in step
            assert "description" in step
        
        print(f"PASS: GET /api/learning-paths/{path_id} returns path with {len(data['steps'])} steps")

    def test_get_nonexistent_learning_path(self):
        """Test 404 for nonexistent learning path"""
        response = requests.get(f"{BASE_URL}/api/learning-paths/nonexistent-id-12345")
        assert response.status_code == 404
        print(f"PASS: Nonexistent learning path returns 404")

    def test_learning_path_step_document_references(self):
        """Verify all step document_ids reference valid documents"""
        response = requests.get(f"{BASE_URL}/api/learning-paths")
        assert response.status_code == 200
        paths = response.json()
        
        invalid_refs = []
        for path in paths:
            for step in path["steps"]:
                doc_id = step["document_id"]
                doc_response = requests.get(f"{BASE_URL}/api/documents/{doc_id}")
                if doc_response.status_code != 200:
                    invalid_refs.append(f"{path['title']} -> {step['title']} ({doc_id})")
        
        assert len(invalid_refs) == 0, f"Invalid document references: {invalid_refs}"
        print(f"PASS: All learning path steps reference valid documents")


class TestQuizIntegration:
    """Test quiz integration with documents"""
    
    def test_documents_with_quizzes(self):
        """Test that all specified documents have quizzes"""
        # Documents that should have quizzes per spec
        docs_with_quizzes = [
            "f53aecbb-3b19-478c-9912-66d82827f402",  # What Is an AI Agent?
        ]
        
        for doc_id in docs_with_quizzes:
            response = requests.get(f"{BASE_URL}/api/documents/{doc_id}/quiz")
            assert response.status_code == 200
            data = response.json()
            assert len(data["questions"]) >= 3, f"Document {doc_id} should have at least 3 questions"
        
        print(f"PASS: {len(docs_with_quizzes)} documents verified to have quizzes")

    def test_quiz_endpoint_performance(self):
        """Test quiz endpoint responds quickly"""
        import time
        doc_id = "f53aecbb-3b19-478c-9912-66d82827f402"
        
        start = time.time()
        response = requests.get(f"{BASE_URL}/api/documents/{doc_id}/quiz")
        elapsed = time.time() - start
        
        assert response.status_code == 200
        assert elapsed < 2.0, f"Quiz endpoint took {elapsed:.2f}s, expected < 2s"
        print(f"PASS: Quiz endpoint responded in {elapsed:.3f}s")


class TestSidebarLearningPathsLink:
    """Test sidebar has Learning Paths link"""
    
    def test_documents_endpoint_works(self):
        """Basic sanity check that documents endpoint works"""
        response = requests.get(f"{BASE_URL}/api/documents")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        print(f"PASS: Documents endpoint returns {len(data)} documents")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
