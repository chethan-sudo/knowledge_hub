"""Test content fixes for iteration 8 - comprehensive content review fixes."""

import pytest
import requests
import os

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://ai-agent-hub-96.preview.emergentagent.com')

class TestCategoriesAndDocuments:
    """Test category and document counts after seed data update."""
    
    def test_total_categories_count(self):
        """Verify 46 categories exist after re-seed."""
        response = requests.get(f"{BASE_URL}/api/categories")
        assert response.status_code == 200
        categories = response.json()
        assert len(categories) == 46, f"Expected 46 categories, got {len(categories)}"
    
    def test_total_documents_count(self):
        """Verify 37 documents exist after re-seed."""
        response = requests.get(f"{BASE_URL}/api/documents")
        assert response.status_code == 200
        documents = response.json()
        assert len(documents) == 37, f"Expected 37 documents, got {len(documents)}"
    
    def test_tools_resources_category_exists(self):
        """Verify Tools & Resources category exists."""
        response = requests.get(f"{BASE_URL}/api/categories")
        assert response.status_code == 200
        categories = response.json()
        tools_cat = [c for c in categories if c.get('name') == 'Tools & Resources']
        assert len(tools_cat) == 1, "Tools & Resources category not found"
    
    def test_tools_resources_has_document(self):
        """Verify Tools & Resources category has 1 document (not 0)."""
        response = requests.get(f"{BASE_URL}/api/categories")
        assert response.status_code == 200
        categories = response.json()
        tools_cat = [c for c in categories if c.get('name') == 'Tools & Resources'][0]
        tools_cat_id = tools_cat['id']
        
        response = requests.get(f"{BASE_URL}/api/documents")
        assert response.status_code == 200
        documents = response.json()
        tools_docs = [d for d in documents if d.get('category_id') == tools_cat_id]
        assert len(tools_docs) >= 1, "Tools & Resources should have at least 1 document"
        
        # Verify it's the Essential Tools & Resources doc
        essential_tools_doc = [d for d in tools_docs if 'Essential Tools' in d.get('title', '')]
        assert len(essential_tools_doc) == 1, "Essential Tools & Resources document not found"


class TestContentAccuracyFixes:
    """Test specific content accuracy fixes mentioned in the review."""
    
    def test_debug_panel_token_count(self):
        """Verify Debug Panel doc says ~15,000 tokens (not ~10,000)."""
        response = requests.get(f"{BASE_URL}/api/documents")
        assert response.status_code == 200
        documents = response.json()
        
        debug_doc = [d for d in documents if 'Debug Panel' in d.get('title', '')]
        assert len(debug_doc) == 1, "Debug Panel document not found"
        
        content = debug_doc[0].get('content', '')
        assert '15,000' in content, "Debug Panel should reference ~15,000 tokens, not ~10,000"
        assert '10,000' not in content, "Debug Panel should NOT reference ~10,000 tokens"
    
    def test_transformers_layer_count(self):
        """Verify How Transformers Work says 32-128 layers (not x96)."""
        response = requests.get(f"{BASE_URL}/api/documents")
        assert response.status_code == 200
        documents = response.json()
        
        transformer_doc = [d for d in documents if 'Transformers' in d.get('title', '')]
        assert len(transformer_doc) == 1, "How Transformers Work document not found"
        
        content = transformer_doc[0].get('content', '')
        assert '32-128' in content, "Transformers doc should reference 32-128 layers"
        assert 'x96' not in content, "Transformers doc should NOT reference x96"
    
    def test_autogen_production_ready(self):
        """Verify AutoGen is marked as Production-ready (not research-oriented)."""
        response = requests.get(f"{BASE_URL}/api/documents")
        assert response.status_code == 200
        documents = response.json()
        
        agent_doc = [d for d in documents if 'Agent Framework' in d.get('title', '')]
        assert len(agent_doc) == 1, "Agent Framework Landscape document not found"
        
        content = agent_doc[0].get('content', '')
        assert 'AutoGen' in content, "Agent Framework doc should mention AutoGen"
        assert 'Production-ready' in content, "AutoGen should be marked as Production-ready"
    
    def test_ui_guide_rollback_location(self):
        """Verify UI Guide describes Rollback as being in message panel/chat area."""
        response = requests.get(f"{BASE_URL}/api/documents")
        assert response.status_code == 200
        documents = response.json()
        
        ui_doc = [d for d in documents if 'UI Guide' in d.get('title', '')]
        assert len(ui_doc) == 1, "Complete UI Guide document not found"
        
        content = ui_doc[0].get('content', '').lower()
        assert 'rollback' in content, "UI Guide should mention Rollback"
        assert 'message panel' in content or 'chat area' in content, \
            "UI Guide should describe Rollback location as message panel/chat area"
    
    def test_mongodb_has_mermaid_diagram(self):
        """Verify MongoDB Document Model page has a mermaid diagram."""
        response = requests.get(f"{BASE_URL}/api/documents")
        assert response.status_code == 200
        documents = response.json()
        
        mongo_doc = [d for d in documents if 'MongoDB' in d.get('title', '')]
        assert len(mongo_doc) == 1, "MongoDB Document Model document not found"
        
        content = mongo_doc[0].get('content', '')
        assert '```mermaid' in content, "MongoDB doc should contain a mermaid diagram"


class TestAnalyticsEndpoints:
    """Test analytics endpoints still work correctly."""
    
    def test_analytics_overview(self):
        """Verify analytics overview endpoint works."""
        response = requests.get(f"{BASE_URL}/api/analytics/overview")
        assert response.status_code == 200
        data = response.json()
        assert 'total_docs' in data
        assert 'total_views' in data
        assert 'total_searches' in data
    
    def test_analytics_popular_docs(self):
        """Verify popular docs endpoint works."""
        response = requests.get(f"{BASE_URL}/api/analytics/popular-docs")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_analytics_searches(self):
        """Verify search queries endpoint works."""
        response = requests.get(f"{BASE_URL}/api/analytics/searches")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
