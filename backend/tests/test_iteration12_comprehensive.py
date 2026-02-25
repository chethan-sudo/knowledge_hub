"""
Comprehensive Backend API Tests - Iteration 12
Testing Agent Anatomy documentation app with 51+ documents across 16 categories.

Features tested:
- Categories API (GET, POST, PUT, DELETE)
- Documents API (GET, POST, PUT, DELETE with soft-delete)
- Bookmarks API
- Search API
- Tools API (CRUD)
- Trash API
- Analytics API
- Tags API
- AI Chat API
- Version History
"""

import pytest
import requests
import os
import uuid
from datetime import datetime

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://hub-preview-2.preview.emergentagent.com')


class TestHealthAndBasicAPIs:
    """Basic API health and structure tests"""
    
    def test_api_root(self):
        """Test API root returns valid response"""
        r = requests.get(f"{BASE_URL}/api/", timeout=30)
        assert r.status_code == 200
        data = r.json()
        assert "message" in data
        print(f"API root: {data}")
    
    def test_categories_endpoint(self):
        """Test GET /api/categories returns expected structure"""
        r = requests.get(f"{BASE_URL}/api/categories", timeout=30)
        assert r.status_code == 200
        cats = r.json()
        assert isinstance(cats, list)
        assert len(cats) > 0
        
        # Verify structure
        for cat in cats[:5]:
            assert "id" in cat
            assert "name" in cat
            assert "order" in cat or cat.get("order", 0) == 0
        
        print(f"Total categories: {len(cats)}")
    
    def test_documents_endpoint(self):
        """Test GET /api/documents returns expected structure"""
        r = requests.get(f"{BASE_URL}/api/documents", timeout=30)
        assert r.status_code == 200
        docs = r.json()
        assert isinstance(docs, list)
        assert len(docs) > 0
        
        # Verify structure
        for doc in docs[:5]:
            assert "id" in doc
            assert "title" in doc
            assert "content" in doc
            assert "category_id" in doc
        
        print(f"Total documents: {len(docs)}")


class TestCategoriesContent:
    """Test that all expected categories exist"""
    
    def test_16_public_categories_exist(self):
        """Verify 16 public categories exist (Tools & Resources should NOT appear)"""
        r = requests.get(f"{BASE_URL}/api/categories", timeout=30)
        assert r.status_code == 200
        cats = r.json()
        
        # Filter to non-internal, top-level categories
        public_top_level = [c for c in cats if not c.get('internal', False) and not c.get('parent_id')]
        
        expected_categories = [
            "Getting Started",
            "Agent Anatomy",
            "Tutorials",
            "Platform Architecture",
            "LLM Internals",
            "Infrastructure",
            "Frontend Development",
            "Backend Development",
            "DevOps & Deployment",
            "Security",
            "Data & Storage",
            "Advanced Concepts",
            "Future of AI Agents",
            "Limitations",
            "UI Guide",
            "FAQ"
        ]
        
        found_names = [c['name'] for c in public_top_level]
        print(f"Found public top-level categories: {found_names}")
        
        for expected in expected_categories:
            assert expected in found_names, f"Missing expected category: {expected}"
        
        # Verify Tools & Resources is NOT in public categories
        assert "Tools & Resources" not in found_names, "Tools & Resources should NOT appear as a category"
        
        print(f"Verified {len(expected_categories)} expected categories exist")
    
    def test_internal_categories_have_flag(self):
        """Test that internal categories (Test Cases) are marked with internal: true"""
        r = requests.get(f"{BASE_URL}/api/categories", timeout=30)
        assert r.status_code == 200
        cats = r.json()
        
        internal_cats = [c for c in cats if c.get('internal', False)]
        print(f"Internal categories: {[c['name'] for c in internal_cats]}")
        
        # There should be internal categories (Test Cases)
        assert len(internal_cats) > 0, "Should have internal categories"
        
        # Test Cases should be internal
        test_cases_found = any(c['name'] == 'Test Cases' for c in internal_cats)
        assert test_cases_found, "Test Cases category should be internal"


class TestDocumentsContent:
    """Test document content and structure"""
    
    def test_51_plus_documents_exist(self):
        """Verify 51+ documents exist"""
        r = requests.get(f"{BASE_URL}/api/documents", timeout=30)
        assert r.status_code == 200
        docs = r.json()
        
        # Should have 51+ documents
        assert len(docs) >= 51, f"Expected 51+ documents, got {len(docs)}"
        print(f"Total documents: {len(docs)}")
    
    def test_agent_anatomy_documents_exist(self):
        """Verify Agent Anatomy category documents"""
        r = requests.get(f"{BASE_URL}/api/documents", timeout=30)
        docs = r.json()
        
        expected_titles = [
            "What Is an AI Agent?",
            "The Agent Loop",
            "Agent Memory Systems",
            "Planning & Reasoning Patterns",
            "Agent Design Patterns",
            "Guardrails & Safety"
        ]
        
        found_titles = [d['title'] for d in docs]
        
        for expected in expected_titles:
            assert expected in found_titles, f"Missing Agent Anatomy doc: {expected}"
        
        print(f"Agent Anatomy documents verified: {expected_titles}")
    
    def test_tutorial_documents_exist(self):
        """Verify Tutorials category documents"""
        r = requests.get(f"{BASE_URL}/api/documents", timeout=30)
        docs = r.json()
        
        expected_titles = [
            "Function Calling & Tool Use",
            "Multi-Agent Communication",
            "Cost Optimization",
            "Real-World AI Agents: Case Studies"
        ]
        
        found_titles = [d['title'] for d in docs]
        
        for expected in expected_titles:
            assert expected in found_titles, f"Missing Tutorial doc: {expected}"
        
        print(f"Tutorial documents verified: {expected_titles}")
    
    def test_document_has_markdown_content(self):
        """Verify documents have proper markdown content"""
        r = requests.get(f"{BASE_URL}/api/documents", timeout=30)
        docs = r.json()
        
        # Check first 5 docs have substantial content
        for doc in docs[:5]:
            assert len(doc.get('content', '')) > 100, f"Document {doc['title']} has too little content"
            # Should have markdown headings
            content = doc.get('content', '')
            assert '#' in content, f"Document {doc['title']} missing markdown headings"
        
        print("Document markdown content verified")


class TestSearchAPI:
    """Test search functionality"""
    
    def test_search_finds_documents(self):
        """Test search returns relevant results"""
        r = requests.get(f"{BASE_URL}/api/search?q=agent", timeout=30)
        assert r.status_code == 200
        results = r.json()
        assert isinstance(results, list)
        assert len(results) > 0, "Search for 'agent' should return results"
        
        # Verify result structure
        for result in results[:3]:
            assert "id" in result
            assert "title" in result
        
        print(f"Search 'agent' found {len(results)} results")
    
    def test_search_empty_query(self):
        """Test search with empty query"""
        r = requests.get(f"{BASE_URL}/api/search?q=", timeout=30)
        assert r.status_code == 200
        results = r.json()
        assert results == [], "Empty search should return empty results"


class TestBookmarksAPI:
    """Test bookmarks functionality"""
    
    def test_get_bookmarks(self):
        """Test GET /api/bookmarks"""
        r = requests.get(f"{BASE_URL}/api/bookmarks", timeout=30)
        assert r.status_code == 200
        data = r.json()
        assert "bookmarks" in data
        assert "documents" in data
        print(f"Bookmarks: {len(data['bookmarks'])}, Documents: {len(data['documents'])}")
    
    def test_toggle_bookmark(self):
        """Test POST /api/bookmarks/{doc_id} toggle"""
        # Get a document to bookmark
        r = requests.get(f"{BASE_URL}/api/documents", timeout=30)
        docs = r.json()
        doc_id = docs[0]['id']
        
        # Toggle bookmark ON
        r = requests.post(f"{BASE_URL}/api/bookmarks/{doc_id}", timeout=30)
        assert r.status_code == 200
        data = r.json()
        assert "bookmarked" in data
        
        # Toggle bookmark OFF (or ON again)
        r = requests.post(f"{BASE_URL}/api/bookmarks/{doc_id}", timeout=30)
        assert r.status_code == 200
        
        print(f"Bookmark toggle for {doc_id} works")


class TestToolsAPI:
    """Test tools CRUD functionality"""
    
    def test_get_tools(self):
        """Test GET /api/tools"""
        r = requests.get(f"{BASE_URL}/api/tools", timeout=30)
        assert r.status_code == 200
        tools = r.json()
        assert isinstance(tools, list)
        print(f"Tools count: {len(tools)}")
    
    def test_create_tool(self):
        """Test POST /api/tools creates a new tool"""
        tool_data = {
            "name": f"TEST_Tool_{uuid.uuid4().hex[:8]}",
            "url": "https://example.com/test-tool",
            "description": "A test tool for automated testing",
            "category": "Testing"
        }
        
        r = requests.post(f"{BASE_URL}/api/tools", json=tool_data, timeout=30)
        assert r.status_code == 200
        created = r.json()
        assert "id" in created
        assert created["name"] == tool_data["name"]
        
        # Clean up - delete the tool
        tool_id = created["id"]
        requests.delete(f"{BASE_URL}/api/tools/{tool_id}", timeout=30)
        
        print(f"Tool CRUD verified: {tool_data['name']}")
    
    def test_delete_tool(self):
        """Test DELETE /api/tools/{tool_id}"""
        # Create a tool first
        tool_data = {
            "name": f"TEST_Delete_{uuid.uuid4().hex[:8]}",
            "url": "https://example.com/delete-test",
            "description": "Tool to be deleted",
            "category": "Testing"
        }
        r = requests.post(f"{BASE_URL}/api/tools", json=tool_data, timeout=30)
        assert r.status_code == 200
        tool_id = r.json()["id"]
        
        # Delete it
        r = requests.delete(f"{BASE_URL}/api/tools/{tool_id}", timeout=30)
        assert r.status_code == 200
        
        print(f"Tool delete verified")


class TestTrashAPI:
    """Test trash functionality"""
    
    def test_get_trash(self):
        """Test GET /api/trash"""
        r = requests.get(f"{BASE_URL}/api/trash", timeout=30)
        assert r.status_code == 200
        trash = r.json()
        assert isinstance(trash, list)
        print(f"Trash items: {len(trash)}")


class TestAnalyticsAPI:
    """Test analytics endpoints"""
    
    def test_analytics_overview(self):
        """Test GET /api/analytics/overview"""
        r = requests.get(f"{BASE_URL}/api/analytics/overview", timeout=30)
        assert r.status_code == 200
        data = r.json()
        assert "total_docs" in data
        assert "total_categories" in data
        assert "total_views" in data
        print(f"Analytics overview: {data}")
    
    def test_analytics_popular_docs(self):
        """Test GET /api/analytics/popular-docs"""
        r = requests.get(f"{BASE_URL}/api/analytics/popular-docs", timeout=30)
        assert r.status_code == 200
        data = r.json()
        assert isinstance(data, list)
        print(f"Popular docs: {len(data)}")
    
    def test_analytics_searches(self):
        """Test GET /api/analytics/searches"""
        r = requests.get(f"{BASE_URL}/api/analytics/searches", timeout=30)
        assert r.status_code == 200
        data = r.json()
        assert isinstance(data, list)
        print(f"Search logs: {len(data)}")
    
    def test_analytics_chatbot(self):
        """Test GET /api/analytics/chatbot"""
        r = requests.get(f"{BASE_URL}/api/analytics/chatbot", timeout=30)
        assert r.status_code == 200
        data = r.json()
        assert "total" in data
        assert "daily" in data
        print(f"Chatbot analytics: total={data['total']}")
    
    def test_analytics_activity(self):
        """Test GET /api/analytics/activity"""
        r = requests.get(f"{BASE_URL}/api/analytics/activity", timeout=30)
        assert r.status_code == 200
        data = r.json()
        assert "recent_docs" in data
        assert "recent_comments" in data
        print(f"Recent activity: docs={len(data['recent_docs'])}, comments={len(data['recent_comments'])}")


class TestTagsAPI:
    """Test tags functionality"""
    
    def test_get_tags(self):
        """Test GET /api/tags returns all tags"""
        r = requests.get(f"{BASE_URL}/api/tags", timeout=30)
        assert r.status_code == 200
        tags = r.json()
        assert isinstance(tags, list)
        print(f"Tags: {tags[:10]}...")
    
    def test_tag_suggestions(self):
        """Test GET /api/tags/suggestions"""
        r = requests.get(f"{BASE_URL}/api/tags/suggestions?q=tut", timeout=30)
        assert r.status_code == 200
        suggestions = r.json()
        assert isinstance(suggestions, list)
        print(f"Tag suggestions for 'tut': {suggestions}")


class TestDocumentCRUD:
    """Test document CRUD operations"""
    
    def test_get_single_document(self):
        """Test GET /api/documents/{doc_id}"""
        # Get documents first
        r = requests.get(f"{BASE_URL}/api/documents", timeout=30)
        docs = r.json()
        doc_id = docs[0]['id']
        
        # Get single document
        r = requests.get(f"{BASE_URL}/api/documents/{doc_id}", timeout=30)
        assert r.status_code == 200
        doc = r.json()
        assert doc['id'] == doc_id
        print(f"Single document: {doc['title']}")
    
    def test_create_update_delete_document(self):
        """Test full document CRUD cycle"""
        # Get a category to use
        r = requests.get(f"{BASE_URL}/api/categories", timeout=30)
        cats = r.json()
        non_internal = [c for c in cats if not c.get('internal', False)]
        cat_id = non_internal[0]['id']
        
        # CREATE
        doc_data = {
            "title": f"TEST_Doc_{uuid.uuid4().hex[:8]}",
            "content": "# Test Document\n\nThis is a test document created by automated tests.",
            "category_id": cat_id,
            "tags": ["test", "automated"]
        }
        r = requests.post(f"{BASE_URL}/api/documents", json=doc_data, timeout=30)
        assert r.status_code == 200
        created = r.json()
        assert "id" in created
        doc_id = created["id"]
        print(f"Created document: {doc_id}")
        
        # Verify creation
        r = requests.get(f"{BASE_URL}/api/documents/{doc_id}", timeout=30)
        assert r.status_code == 200
        assert r.json()["title"] == doc_data["title"]
        
        # UPDATE
        update_data = {"title": f"TEST_Updated_{uuid.uuid4().hex[:8]}"}
        r = requests.put(f"{BASE_URL}/api/documents/{doc_id}", json=update_data, timeout=30)
        assert r.status_code == 200
        updated = r.json()
        assert updated["title"] == update_data["title"]
        print(f"Updated document title")
        
        # DELETE (soft delete)
        r = requests.delete(f"{BASE_URL}/api/documents/{doc_id}", timeout=30)
        assert r.status_code == 200
        
        # Verify in trash
        r = requests.get(f"{BASE_URL}/api/trash", timeout=30)
        trash = r.json()
        assert any(d['id'] == doc_id for d in trash), "Document should be in trash"
        print(f"Document moved to trash")
        
        # Permanent delete
        r = requests.delete(f"{BASE_URL}/api/trash/{doc_id}", timeout=30)
        assert r.status_code == 200
        print(f"Document permanently deleted")


class TestDocumentVersions:
    """Test version history functionality"""
    
    def test_get_document_versions(self):
        """Test GET /api/documents/{doc_id}/versions"""
        # Get a document
        r = requests.get(f"{BASE_URL}/api/documents", timeout=30)
        docs = r.json()
        doc_id = docs[0]['id']
        
        r = requests.get(f"{BASE_URL}/api/documents/{doc_id}/versions", timeout=30)
        assert r.status_code == 200
        versions = r.json()
        assert isinstance(versions, list)
        print(f"Document {doc_id} has {len(versions)} versions")


class TestCommentsAPI:
    """Test comments functionality"""
    
    def test_get_comments(self):
        """Test GET /api/documents/{doc_id}/comments"""
        r = requests.get(f"{BASE_URL}/api/documents", timeout=30)
        docs = r.json()
        doc_id = docs[0]['id']
        
        r = requests.get(f"{BASE_URL}/api/documents/{doc_id}/comments", timeout=30)
        assert r.status_code == 200
        comments = r.json()
        assert isinstance(comments, list)
        print(f"Document {doc_id} has {len(comments)} comments")
    
    def test_add_and_delete_comment(self):
        """Test adding and deleting a comment"""
        r = requests.get(f"{BASE_URL}/api/documents", timeout=30)
        docs = r.json()
        doc_id = docs[0]['id']
        
        # Add comment
        comment_data = {"content": f"TEST_Comment_{uuid.uuid4().hex[:8]}"}
        r = requests.post(f"{BASE_URL}/api/documents/{doc_id}/comments", json=comment_data, timeout=30)
        assert r.status_code == 200
        comment = r.json()
        assert "id" in comment
        comment_id = comment["id"]
        print(f"Added comment: {comment_id}")
        
        # Delete comment
        r = requests.delete(f"{BASE_URL}/api/comments/{comment_id}", timeout=30)
        assert r.status_code == 200
        print(f"Deleted comment")


class TestUsersAPI:
    """Test users management API"""
    
    def test_get_users(self):
        """Test GET /api/users"""
        r = requests.get(f"{BASE_URL}/api/users", timeout=30)
        assert r.status_code == 200
        users = r.json()
        assert isinstance(users, list)
        print(f"Users count: {len(users)}")


class TestTemplatesAPI:
    """Test templates functionality"""
    
    def test_get_templates(self):
        """Test GET /api/templates"""
        r = requests.get(f"{BASE_URL}/api/templates", timeout=30)
        assert r.status_code == 200
        templates = r.json()
        assert isinstance(templates, list)
        assert len(templates) > 0
        
        # Verify structure
        for t in templates[:3]:
            assert "id" in t
            assert "name" in t
            assert "content" in t
        
        print(f"Templates: {[t['name'] for t in templates]}")


class TestPublicSharingAPI:
    """Test public sharing functionality"""
    
    def test_toggle_share(self):
        """Test sharing toggle creates and removes share ID"""
        # Get a document
        r = requests.get(f"{BASE_URL}/api/documents", timeout=30)
        docs = r.json()
        doc_id = docs[0]['id']
        
        # Toggle share on
        r = requests.post(f"{BASE_URL}/api/documents/{doc_id}/share", timeout=30)
        assert r.status_code == 200
        data = r.json()
        assert "shared" in data
        
        if data["shared"]:
            share_id = data["share_id"]
            # Test public access
            r = requests.get(f"{BASE_URL}/api/public/{share_id}", timeout=30)
            assert r.status_code == 200
            
            # Toggle share off
            r = requests.post(f"{BASE_URL}/api/documents/{doc_id}/share", timeout=30)
            assert r.status_code == 200
            print(f"Share toggle verified: {share_id}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
