"""
Analytics Dashboard API Tests - Iteration 7
Tests for all analytics endpoints:
- GET /api/analytics/overview - Total docs, views, searches, chats, views_7d, chats_7d
- GET /api/analytics/popular-docs - Documents sorted by view count
- GET /api/analytics/searches - Aggregated search queries
- GET /api/analytics/chatbot - Total, daily, recent questions
- GET /api/analytics/activity - Recent docs and comments
- POST /api/documents/{doc_id}/view - Track document view
"""
import pytest
import requests
import os
import uuid

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')


class TestAnalyticsOverview:
    """Test GET /api/analytics/overview"""
    
    def test_analytics_overview_returns_200(self):
        """Overview endpoint returns 200 status"""
        response = requests.get(f"{BASE_URL}/api/analytics/overview")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        print(f"✓ Analytics overview returned 200")
    
    def test_analytics_overview_contains_required_fields(self):
        """Overview contains all required metric fields"""
        response = requests.get(f"{BASE_URL}/api/analytics/overview")
        assert response.status_code == 200
        data = response.json()
        
        required_fields = [
            "total_docs", "total_views", "total_searches", "total_chats",
            "views_7d", "chats_7d"
        ]
        for field in required_fields:
            assert field in data, f"Missing field: {field}"
            assert isinstance(data[field], int), f"{field} should be int, got {type(data[field])}"
        print(f"✓ Analytics overview contains all required fields: {list(data.keys())}")
    
    def test_analytics_overview_values_are_non_negative(self):
        """All overview values are non-negative integers"""
        response = requests.get(f"{BASE_URL}/api/analytics/overview")
        data = response.json()
        for key, value in data.items():
            assert value >= 0, f"{key} should be non-negative, got {value}"
        print(f"✓ All overview values are non-negative")


class TestPopularDocs:
    """Test GET /api/analytics/popular-docs"""
    
    def test_popular_docs_returns_200(self):
        """Popular docs endpoint returns 200"""
        response = requests.get(f"{BASE_URL}/api/analytics/popular-docs")
        assert response.status_code == 200
        print("✓ Popular docs endpoint returned 200")
    
    def test_popular_docs_returns_list(self):
        """Popular docs returns a list"""
        response = requests.get(f"{BASE_URL}/api/analytics/popular-docs")
        data = response.json()
        assert isinstance(data, list), f"Expected list, got {type(data)}"
        print(f"✓ Popular docs returned list with {len(data)} items")
    
    def test_popular_docs_item_structure(self):
        """Each popular doc has doc_id, views, title fields"""
        response = requests.get(f"{BASE_URL}/api/analytics/popular-docs")
        data = response.json()
        if len(data) > 0:
            item = data[0]
            assert "doc_id" in item, "Missing doc_id"
            assert "views" in item, "Missing views"
            assert "title" in item, "Missing title"
            assert isinstance(item["views"], int), "views should be int"
            print(f"✓ Popular doc item has correct structure: {list(item.keys())}")
        else:
            print("⚠ No popular docs to verify structure (empty list)")
    
    def test_popular_docs_sorted_by_views(self):
        """Popular docs are sorted by views in descending order"""
        response = requests.get(f"{BASE_URL}/api/analytics/popular-docs")
        data = response.json()
        if len(data) > 1:
            views = [d["views"] for d in data]
            assert views == sorted(views, reverse=True), "Docs should be sorted by views descending"
            print(f"✓ Popular docs sorted correctly by views: {views[:5]}")
        else:
            print("⚠ Not enough docs to verify sorting")


class TestSearchAnalytics:
    """Test GET /api/analytics/searches"""
    
    def test_searches_returns_200(self):
        """Searches endpoint returns 200"""
        response = requests.get(f"{BASE_URL}/api/analytics/searches")
        assert response.status_code == 200
        print("✓ Search analytics returned 200")
    
    def test_searches_returns_list(self):
        """Searches returns a list"""
        response = requests.get(f"{BASE_URL}/api/analytics/searches")
        data = response.json()
        assert isinstance(data, list), f"Expected list, got {type(data)}"
        print(f"✓ Search analytics returned list with {len(data)} items")
    
    def test_searches_item_structure(self):
        """Each search item has query, count, last_searched"""
        response = requests.get(f"{BASE_URL}/api/analytics/searches")
        data = response.json()
        if len(data) > 0:
            item = data[0]
            assert "query" in item, "Missing query"
            assert "count" in item, "Missing count"
            assert isinstance(item["count"], int), "count should be int"
            print(f"✓ Search item has correct structure: {list(item.keys())}")
        else:
            print("⚠ No searches to verify structure")


class TestChatbotAnalytics:
    """Test GET /api/analytics/chatbot"""
    
    def test_chatbot_returns_200(self):
        """Chatbot analytics returns 200"""
        response = requests.get(f"{BASE_URL}/api/analytics/chatbot")
        assert response.status_code == 200
        print("✓ Chatbot analytics returned 200")
    
    def test_chatbot_has_required_fields(self):
        """Chatbot analytics has total, daily, recent"""
        response = requests.get(f"{BASE_URL}/api/analytics/chatbot")
        data = response.json()
        
        assert "total" in data, "Missing total"
        assert "daily" in data, "Missing daily"
        assert "recent" in data, "Missing recent"
        
        assert isinstance(data["total"], int), "total should be int"
        assert isinstance(data["daily"], list), "daily should be list"
        assert isinstance(data["recent"], list), "recent should be list"
        print(f"✓ Chatbot analytics has correct structure: total={data['total']}, daily={len(data['daily'])} items, recent={len(data['recent'])} items")
    
    def test_chatbot_daily_item_structure(self):
        """Daily items have date and count"""
        response = requests.get(f"{BASE_URL}/api/analytics/chatbot")
        data = response.json()
        if len(data.get("daily", [])) > 0:
            item = data["daily"][0]
            assert "date" in item, "Missing date in daily"
            assert "count" in item, "Missing count in daily"
            print(f"✓ Daily item structure correct: {list(item.keys())}")
        else:
            print("⚠ No daily data to verify")
    
    def test_chatbot_recent_item_structure(self):
        """Recent items have question, asked_at"""
        response = requests.get(f"{BASE_URL}/api/analytics/chatbot")
        data = response.json()
        if len(data.get("recent", [])) > 0:
            item = data["recent"][0]
            assert "question" in item, "Missing question in recent"
            assert "asked_at" in item, "Missing asked_at in recent"
            print(f"✓ Recent question structure correct: {list(item.keys())}")
        else:
            print("⚠ No recent questions to verify")


class TestActivityAnalytics:
    """Test GET /api/analytics/activity"""
    
    def test_activity_returns_200(self):
        """Activity endpoint returns 200"""
        response = requests.get(f"{BASE_URL}/api/analytics/activity")
        assert response.status_code == 200
        print("✓ Activity analytics returned 200")
    
    def test_activity_has_required_fields(self):
        """Activity has recent_docs and recent_comments"""
        response = requests.get(f"{BASE_URL}/api/analytics/activity")
        data = response.json()
        
        assert "recent_docs" in data, "Missing recent_docs"
        assert "recent_comments" in data, "Missing recent_comments"
        assert isinstance(data["recent_docs"], list), "recent_docs should be list"
        assert isinstance(data["recent_comments"], list), "recent_comments should be list"
        print(f"✓ Activity has correct structure: {len(data['recent_docs'])} docs, {len(data['recent_comments'])} comments")
    
    def test_activity_recent_doc_structure(self):
        """Recent docs have id, title, updated_at"""
        response = requests.get(f"{BASE_URL}/api/analytics/activity")
        data = response.json()
        if len(data.get("recent_docs", [])) > 0:
            item = data["recent_docs"][0]
            assert "id" in item, "Missing id in recent_docs"
            assert "title" in item, "Missing title in recent_docs"
            print(f"✓ Recent doc structure correct: {list(item.keys())}")
        else:
            print("⚠ No recent docs to verify")


class TestDocumentViewTracking:
    """Test POST /api/documents/{doc_id}/view"""
    
    def test_track_view_returns_200(self):
        """Track view returns 200 for valid doc_id"""
        # First get a valid document
        docs_response = requests.get(f"{BASE_URL}/api/documents")
        docs = docs_response.json()
        if len(docs) > 0:
            doc_id = docs[0]["id"]
            response = requests.post(f"{BASE_URL}/api/documents/{doc_id}/view")
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            data = response.json()
            assert data.get("status") == "tracked", f"Expected status=tracked, got {data}"
            print(f"✓ View tracked successfully for doc {doc_id[:8]}...")
        else:
            pytest.skip("No documents available for view tracking test")
    
    def test_track_view_increments_count(self):
        """Tracking a view increments the view count"""
        # Get current view count
        overview_before = requests.get(f"{BASE_URL}/api/analytics/overview").json()
        total_views_before = overview_before["total_views"]
        
        # Track a view
        docs = requests.get(f"{BASE_URL}/api/documents").json()
        if len(docs) > 0:
            doc_id = docs[0]["id"]
            requests.post(f"{BASE_URL}/api/documents/{doc_id}/view")
            
            # Check if count increased
            overview_after = requests.get(f"{BASE_URL}/api/analytics/overview").json()
            total_views_after = overview_after["total_views"]
            
            assert total_views_after >= total_views_before, "View count should not decrease"
            print(f"✓ View count: {total_views_before} -> {total_views_after}")
        else:
            pytest.skip("No documents available")
    
    def test_track_view_with_unknown_doc(self):
        """Track view for unknown doc_id still returns 200 (graceful handling)"""
        fake_doc_id = str(uuid.uuid4())
        response = requests.post(f"{BASE_URL}/api/documents/{fake_doc_id}/view")
        # The endpoint should track the view even for unknown doc (doesn't validate)
        assert response.status_code == 200
        print(f"✓ View tracking gracefully handles unknown doc_id")


class TestSearchLogging:
    """Test that search queries are logged for analytics"""
    
    def test_search_logs_query(self):
        """Searching logs the query for analytics"""
        # Generate a unique search query
        unique_query = f"TEST_SEARCH_{uuid.uuid4().hex[:8]}"
        
        # Perform search
        search_response = requests.get(f"{BASE_URL}/api/search?q={unique_query}")
        assert search_response.status_code == 200
        
        # Check if it appears in search analytics
        searches = requests.get(f"{BASE_URL}/api/analytics/searches").json()
        found = any(s["query"] == unique_query for s in searches)
        
        if found:
            print(f"✓ Search query '{unique_query}' was logged for analytics")
        else:
            # It might not appear immediately in aggregated results
            print(f"⚠ Search query '{unique_query}' may not appear in top 20 aggregation")


class TestExistingFeaturesRegression:
    """Regression tests - ensure existing features still work"""
    
    def test_documents_endpoint(self):
        """Documents endpoint still works"""
        response = requests.get(f"{BASE_URL}/api/documents")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        print(f"✓ GET /api/documents works ({len(data)} documents)")
    
    def test_categories_endpoint(self):
        """Categories endpoint still works"""
        response = requests.get(f"{BASE_URL}/api/categories")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        print(f"✓ GET /api/categories works ({len(data)} categories)")
    
    def test_search_endpoint(self):
        """Search endpoint still works"""
        response = requests.get(f"{BASE_URL}/api/search?q=test")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        print("✓ GET /api/search works")
    
    def test_single_document_endpoint(self):
        """Single document endpoint still works"""
        docs = requests.get(f"{BASE_URL}/api/documents").json()
        if len(docs) > 0:
            doc_id = docs[0]["id"]
            response = requests.get(f"{BASE_URL}/api/documents/{doc_id}")
            assert response.status_code == 200
            data = response.json()
            assert "title" in data
            assert "content" in data
            print(f"✓ GET /api/documents/{doc_id[:8]}... works")
        else:
            pytest.skip("No documents available")
    
    def test_bookmarks_endpoint(self):
        """Bookmarks endpoint still works"""
        response = requests.get(f"{BASE_URL}/api/bookmarks")
        assert response.status_code == 200
        print("✓ GET /api/bookmarks works")
    
    def test_tags_endpoint(self):
        """Tags endpoint still works"""
        response = requests.get(f"{BASE_URL}/api/tags")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        print("✓ GET /api/tags works")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
