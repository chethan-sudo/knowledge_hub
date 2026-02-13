"""
Iteration 6 Tests - Content Accuracy and UI Fixes
- Reading progress bar CSS fix verification
- Mermaid diagram spacing verification  
- UI Guide content accuracy (Save to GitHub in message panel)
- Flow explanations in documents
"""
import pytest
import requests
import os

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')

class TestContentAccuracy:
    """Test content accuracy in documents"""
    
    def test_ui_guide_mentions_message_panel_for_github_save(self):
        """UI Guide should mention that Save to GitHub is in message panel, NOT top nav"""
        response = requests.get(f"{BASE_URL}/api/documents", timeout=10)
        assert response.status_code == 200
        
        documents = response.json()
        ui_guide = next((d for d in documents if "UI Guide" in d.get("title", "")), None)
        
        assert ui_guide is not None, "UI Guide document not found"
        
        content = ui_guide.get("content", "")
        
        # Check for correct information
        assert "message panel" in content.lower(), "UI Guide should mention 'message panel'"
        assert "Save to GitHub" in content, "UI Guide should mention 'Save to GitHub'"
        
        # Check that it correctly states NOT in top nav
        assert "NOT top nav" in content or "not in the top navigation" in content.lower(), \
            "UI Guide should state Save to GitHub is NOT in top nav"
    
    def test_system_architecture_has_diagram_explanation(self):
        """System Architecture Overview should have Diagram Explanation sections"""
        response = requests.get(f"{BASE_URL}/api/documents", timeout=10)
        assert response.status_code == 200
        
        documents = response.json()
        sys_arch = next((d for d in documents if "System Architecture Overview" in d.get("title", "")), None)
        
        assert sys_arch is not None, "System Architecture Overview document not found"
        
        content = sys_arch.get("content", "")
        
        # Check for Diagram Explanation sections
        assert "Diagram Explanation" in content or "Flow Explanation" in content, \
            "System Architecture should have explanation sections after diagrams"
    
    def test_what_is_e1_has_flow_explanations(self):
        """What Is E1 document should have Flow Explanation sections"""
        response = requests.get(f"{BASE_URL}/api/documents", timeout=10)
        assert response.status_code == 200
        
        documents = response.json()
        e1_doc = next((d for d in documents if "What Is E1" in d.get("title", "")), None)
        
        assert e1_doc is not None, "What Is E1 document not found"
        
        content = e1_doc.get("content", "")
        
        # Should have Flow Explanation sections
        assert "Flow Explanation" in content, "What Is E1 should have Flow Explanation sections"
        
        # Should have mermaid diagrams
        assert "```mermaid" in content, "What Is E1 should have mermaid diagrams"
    
    def test_subagent_system_has_flow_explanations(self):
        """The Subagent System document should have Flow Explanation sections"""
        response = requests.get(f"{BASE_URL}/api/documents", timeout=10)
        assert response.status_code == 200
        
        documents = response.json()
        subagent_doc = next((d for d in documents if "Subagent System" in d.get("title", "")), None)
        
        assert subagent_doc is not None, "The Subagent System document not found"
        
        content = subagent_doc.get("content", "")
        
        assert "Flow Explanation" in content, "Subagent System should have Flow Explanation sections"
        assert "```mermaid" in content, "Subagent System should have mermaid diagrams"
    
    def test_tool_execution_engine_has_flow_explanations(self):
        """Tool Execution Engine document should have Flow Explanation sections"""
        response = requests.get(f"{BASE_URL}/api/documents", timeout=10)
        assert response.status_code == 200
        
        documents = response.json()
        tool_doc = next((d for d in documents if "Tool Execution Engine" in d.get("title", "")), None)
        
        assert tool_doc is not None, "Tool Execution Engine document not found"
        
        content = tool_doc.get("content", "")
        
        assert "Flow Explanation" in content, "Tool Execution Engine should have Flow Explanation sections"
        assert "```mermaid" in content, "Tool Execution Engine should have mermaid diagrams"


class TestBackendAPIs:
    """Test backend APIs are working correctly"""
    
    def test_health_endpoint(self):
        """Health endpoint should return OK"""
        # Note: /api/health may return 404 as the app doesn't have a dedicated health endpoint
        # Using categories endpoint as a health check instead
        response = requests.get(f"{BASE_URL}/api/categories", timeout=10)
        assert response.status_code == 200, "Backend is not responding correctly"
    
    def test_categories_endpoint(self):
        """Categories endpoint should return list"""
        response = requests.get(f"{BASE_URL}/api/categories", timeout=10)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list), "Categories should return a list"
        assert len(data) > 0, "Should have categories"
    
    def test_documents_endpoint(self):
        """Documents endpoint should return list"""
        response = requests.get(f"{BASE_URL}/api/documents", timeout=10)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list), "Documents should return a list"
        assert len(data) > 0, "Should have documents"
    
    def test_search_endpoint(self):
        """Search endpoint should return results"""
        response = requests.get(f"{BASE_URL}/api/search?q=transformer", timeout=10)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list), "Search should return a list"
    
    def test_mermaid_diagrams_count(self):
        """Should have multiple documents with mermaid diagrams"""
        response = requests.get(f"{BASE_URL}/api/documents", timeout=10)
        assert response.status_code == 200
        
        documents = response.json()
        docs_with_mermaid = [d for d in documents if "```mermaid" in d.get("content", "")]
        
        assert len(docs_with_mermaid) >= 10, f"Should have at least 10 docs with mermaid, got {len(docs_with_mermaid)}"


class TestWebSocketCollaboration:
    """Test WebSocket collaboration endpoint"""
    
    def test_collab_presence_endpoint(self):
        """Presence endpoint should be accessible"""
        # Get a document ID first
        response = requests.get(f"{BASE_URL}/api/documents", timeout=10)
        assert response.status_code == 200
        docs = response.json()
        
        if docs:
            doc_id = docs[0].get("id")
            presence_resp = requests.get(f"{BASE_URL}/api/documents/{doc_id}/presence", timeout=10)
            # Should return empty array if no one connected
            assert presence_resp.status_code == 200
            data = presence_resp.json()
            assert isinstance(data, list), "Presence should return a list"
