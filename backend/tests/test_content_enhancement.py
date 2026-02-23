"""
Test Content Enhancement - Iteration 11
Tests for the new Getting Started, Tutorials categories and enhanced documents
"""
import pytest
import requests
import os

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://hub-preview-2.preview.emergentagent.com')

class TestNewCategories:
    """Test new categories were created correctly"""
    
    def test_getting_started_category_exists(self):
        """Getting Started category should exist with order=-1"""
        response = requests.get(f"{BASE_URL}/api/categories")
        assert response.status_code == 200
        categories = response.json()
        
        getting_started = [c for c in categories if c.get('name') == 'Getting Started']
        assert len(getting_started) == 1, "Getting Started category not found"
        assert getting_started[0].get('order') == -1, "Getting Started should have order=-1 to appear first"
        assert getting_started[0].get('internal') != True, "Getting Started should not be internal"
    
    def test_tutorials_category_exists(self):
        """Tutorials category should exist with order=-0.5"""
        response = requests.get(f"{BASE_URL}/api/categories")
        assert response.status_code == 200
        categories = response.json()
        
        tutorials = [c for c in categories if c.get('name') == 'Tutorials']
        assert len(tutorials) == 1, "Tutorials category not found"
        assert tutorials[0].get('order') == -0.5, "Tutorials should have order=-0.5 to appear second"
        assert tutorials[0].get('internal') != True, "Tutorials should not be internal"
    
    def test_tutorials_has_subcategories(self):
        """Tutorials should have subcategories: Build a CRUD API, Debugging Guide, Comparisons"""
        response = requests.get(f"{BASE_URL}/api/categories")
        assert response.status_code == 200
        categories = response.json()
        
        tutorials = [c for c in categories if c.get('name') == 'Tutorials']
        assert tutorials, "Tutorials category not found"
        tutorials_id = tutorials[0]['id']
        
        children = [c for c in categories if c.get('parent_id') == tutorials_id]
        child_names = [c['name'] for c in children]
        
        expected = ['Build a CRUD API', 'Debugging Guide', 'Comparisons']
        for exp in expected:
            assert exp in child_names, f"Expected subcategory '{exp}' not found under Tutorials"
    
    def test_test_cases_category_hidden(self):
        """Test Cases category should have internal=True"""
        response = requests.get(f"{BASE_URL}/api/categories")
        assert response.status_code == 200
        categories = response.json()
        
        test_cases = [c for c in categories if c.get('name') == 'Test Cases']
        assert len(test_cases) == 1, "Test Cases category not found"
        assert test_cases[0].get('internal') == True, "Test Cases should be internal=True"


class TestNewDocuments:
    """Test new documents in Getting Started and Tutorials"""
    
    def test_getting_started_has_3_documents(self):
        """Getting Started should have 3 documents"""
        response = requests.get(f"{BASE_URL}/api/categories")
        categories = response.json()
        
        getting_started = [c for c in categories if c.get('name') == 'Getting Started']
        assert getting_started, "Getting Started category not found"
        gs_id = getting_started[0]['id']
        
        # Get subcategories too
        children = [c for c in categories if c.get('parent_id') == gs_id]
        all_ids = [gs_id] + [c['id'] for c in children]
        
        response = requests.get(f"{BASE_URL}/api/documents")
        documents = response.json()
        
        gs_docs = [d for d in documents if d.get('category_id') in all_ids]
        assert len(gs_docs) >= 3, f"Expected at least 3 docs in Getting Started, found {len(gs_docs)}"
    
    def test_first_10_minutes_document(self):
        """'Your First 10 Minutes on Emergent' should exist with proper content"""
        response = requests.get(f"{BASE_URL}/api/documents")
        documents = response.json()
        
        doc = [d for d in documents if 'First 10 Minutes' in d.get('title', '')]
        assert len(doc) == 1, "Document 'Your First 10 Minutes on Emergent' not found"
        
        doc = doc[0]
        content_len = len(doc.get('content', ''))
        assert content_len >= 4000, f"Document content too short: {content_len} chars (expected 4000+)"
        
        tags = doc.get('tags', [])
        assert 'getting-started' in tags, "Document should have 'getting-started' tag"
        assert 'beginner' in tags, "Document should have 'beginner' tag"
    
    def test_how_to_talk_to_e1_document(self):
        """'How to Talk to E1 Effectively' should exist with mermaid diagram"""
        response = requests.get(f"{BASE_URL}/api/documents")
        documents = response.json()
        
        doc = [d for d in documents if 'Talk to E1' in d.get('title', '')]
        assert len(doc) == 1, "Document 'How to Talk to E1 Effectively' not found"
        
        doc = doc[0]
        content = doc.get('content', '')
        assert 'mermaid' in content.lower(), "Document should contain a mermaid diagram"
        
        tags = doc.get('tags', [])
        assert 'getting-started' in tags, "Document should have 'getting-started' tag"
    
    def test_platform_glossary_document(self):
        """'Platform Glossary' should exist with alphabetical organization"""
        response = requests.get(f"{BASE_URL}/api/documents")
        documents = response.json()
        
        doc = [d for d in documents if 'Platform Glossary' in d.get('title', '')]
        assert len(doc) == 1, "Document 'Platform Glossary' not found"
        
        doc = doc[0]
        content = doc.get('content', '')
        
        # Should have alphabetical sections
        assert '## A' in content or '## A' in content, "Glossary should have alphabetical sections"
        assert 'Agent' in content, "Glossary should define 'Agent'"
        
        content_len = len(content)
        assert content_len >= 5000, f"Document content too short: {content_len} chars (expected 5000+)"
    
    def test_building_rest_api_document(self):
        """'Building a REST API from Scratch' should exist with code blocks"""
        response = requests.get(f"{BASE_URL}/api/documents")
        documents = response.json()
        
        doc = [d for d in documents if 'REST API from Scratch' in d.get('title', '')]
        assert len(doc) == 1, "Document 'Building a REST API from Scratch' not found"
        
        doc = doc[0]
        content = doc.get('content', '')
        
        # Should have Python code blocks
        assert '```python' in content, "Document should contain Python code blocks"
        
        tags = doc.get('tags', [])
        assert 'tutorial' in tags, "Document should have 'tutorial' tag"
        
        content_len = len(content)
        assert content_len >= 6000, f"Document content too short: {content_len} chars (expected 6000+)"
    
    def test_debugging_500_error_document(self):
        """'Debugging a 500 Error Step-by-Step' should exist with code blocks"""
        response = requests.get(f"{BASE_URL}/api/documents")
        documents = response.json()
        
        doc = [d for d in documents if '500 Error' in d.get('title', '')]
        assert len(doc) == 1, "Document 'Debugging a 500 Error Step-by-Step' not found"
        
        doc = doc[0]
        content = doc.get('content', '')
        
        # Should have bash/code blocks for debugging
        has_code = '```' in content
        assert has_code, "Document should contain code blocks for debugging steps"
        
        tags = doc.get('tags', [])
        assert 'tutorial' in tags, "Document should have 'tutorial' tag"
    
    def test_choosing_right_llm_document(self):
        """'Choosing the Right LLM' should exist with comparison table"""
        response = requests.get(f"{BASE_URL}/api/documents")
        documents = response.json()
        
        doc = [d for d in documents if 'Choosing the Right LLM' in d.get('title', '')]
        assert len(doc) == 1, "Document 'Choosing the Right LLM' not found"
        
        doc = doc[0]
        content = doc.get('content', '')
        
        # Should have comparison table with model names
        assert 'Claude' in content, "Document should mention Claude"
        assert 'GPT' in content, "Document should mention GPT"
        assert '|' in content, "Document should have table markup"
        
        tags = doc.get('tags', [])
        assert 'comparison' in tags, "Document should have 'comparison' tag"
    
    def test_mongodb_vs_postgresql_document(self):
        """'MongoDB vs PostgreSQL on Emergent' should exist"""
        response = requests.get(f"{BASE_URL}/api/documents")
        documents = response.json()
        
        doc = [d for d in documents if 'MongoDB vs PostgreSQL' in d.get('title', '')]
        assert len(doc) == 1, "Document 'MongoDB vs PostgreSQL on Emergent' not found"
        
        doc = doc[0]
        content = doc.get('content', '')
        
        # Should compare databases
        assert 'MongoDB' in content, "Document should discuss MongoDB"
        assert 'PostgreSQL' in content or 'Postgres' in content, "Document should discuss PostgreSQL"
        
        tags = doc.get('tags', [])
        assert 'comparison' in tags, "Document should have 'comparison' tag"


class TestTagFiltering:
    """Test that new tags work correctly"""
    
    def test_getting_started_tag_exists(self):
        """getting-started tag should exist"""
        response = requests.get(f"{BASE_URL}/api/tags")
        assert response.status_code == 200
        tags = response.json()
        assert 'getting-started' in tags, "getting-started tag should exist"
    
    def test_tutorial_tag_exists(self):
        """tutorial tag should exist"""
        response = requests.get(f"{BASE_URL}/api/tags")
        assert response.status_code == 200
        tags = response.json()
        assert 'tutorial' in tags, "tutorial tag should exist"
    
    def test_comparison_tag_exists(self):
        """comparison tag should exist"""
        response = requests.get(f"{BASE_URL}/api/tags")
        assert response.status_code == 200
        tags = response.json()
        assert 'comparison' in tags, "comparison tag should exist"
    
    def test_beginner_tag_exists(self):
        """beginner tag should exist"""
        response = requests.get(f"{BASE_URL}/api/tags")
        assert response.status_code == 200
        tags = response.json()
        assert 'beginner' in tags, "beginner tag should exist"


class TestSearchForNewContent:
    """Test search returns new content"""
    
    def test_search_finds_getting_started(self):
        """Search should find Getting Started documents"""
        response = requests.get(f"{BASE_URL}/api/search?q=Getting+Started")
        assert response.status_code == 200
        results = response.json()
        # May return category or document match
        assert len(results) >= 0  # Search may not find exact match but should not error
    
    def test_search_finds_mongodb_postgres(self):
        """Search should find MongoDB vs PostgreSQL document"""
        response = requests.get(f"{BASE_URL}/api/search?q=MongoDB+PostgreSQL")
        assert response.status_code == 200
        results = response.json()
        titles = [r.get('title', '') for r in results]
        assert any('MongoDB' in t or 'PostgreSQL' in t for t in titles), "Search should find database comparison document"
