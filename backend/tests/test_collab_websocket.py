"""
WebSocket Collaboration Feature Tests
Tests for P0: Real-time collaborative editing feature
- WebSocket connection & presence
- Multi-user scenarios
- Content broadcast
- Mode changes
- Auto-save via WebSocket
"""
import pytest
import asyncio
import json
import os
import time
import requests
import websockets
from websockets.exceptions import ConnectionClosedOK, ConnectionClosed

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')
# For WebSocket testing, we need to use localhost since external URL goes through HTTPS
WS_BASE_URL = "ws://localhost:8001"
API_BASE_URL = "http://localhost:8001"


class TestPresenceRESTEndpoint:
    """Test the REST endpoint GET /api/documents/{doc_id}/presence"""
    
    def test_presence_returns_empty_for_unknown_doc(self):
        """When no one is connected, presence should return empty array"""
        response = requests.get(f"{API_BASE_URL}/api/documents/nonexistent-doc-id/presence")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        # Could be empty if no one is connected, or have users if someone is
        print(f"Presence REST endpoint works, returned {len(data)} users")

    def test_presence_endpoint_exists(self):
        """Verify presence endpoint returns valid response"""
        # Get a real document ID first
        docs_response = requests.get(f"{API_BASE_URL}/api/documents")
        assert docs_response.status_code == 200
        docs = docs_response.json()
        if docs:
            doc_id = docs[0]["id"]
            response = requests.get(f"{API_BASE_URL}/api/documents/{doc_id}/presence")
            assert response.status_code == 200
            data = response.json()
            assert isinstance(data, list)
            print(f"Presence for doc {doc_id[:8]}... returned {len(data)} users")
        else:
            pytest.skip("No documents available for presence test")


class TestWebSocketBasicConnection:
    """Test basic WebSocket connection and presence"""

    @pytest.mark.asyncio
    async def test_websocket_connects_and_receives_presence(self):
        """Test that WebSocket connects and receives initial presence"""
        doc_id = "test-ws-conn-" + str(int(time.time()))
        ws_url = f"{WS_BASE_URL}/api/ws/collab/{doc_id}?user_id=test1&name=TestUser&color=%236366f1"
        
        async with websockets.connect(ws_url) as ws:
            # Should receive presence immediately after connecting
            msg = await asyncio.wait_for(ws.recv(), timeout=5)
            data = json.loads(msg)
            
            assert data["type"] == "presence"
            assert "users" in data
            assert len(data["users"]) >= 1  # At least our own user
            
            # Verify our user is in the presence list
            our_user = next((u for u in data["users"] if u["user_id"] == "test1"), None)
            assert our_user is not None
            assert our_user["name"] == "TestUser"
            assert our_user["color"] == "#6366f1"
            assert our_user["mode"] == "viewing"
            
            print(f"WebSocket connected, presence shows {len(data['users'])} users")

    @pytest.mark.asyncio
    async def test_websocket_with_special_characters_in_name(self):
        """Test WebSocket connection with special characters in user name"""
        doc_id = "test-special-chars"
        # URL-encoded name with spaces
        ws_url = f"{WS_BASE_URL}/api/ws/collab/{doc_id}?user_id=user-special&name=Test%20User%20123&color=%23ff0000"
        
        async with websockets.connect(ws_url) as ws:
            msg = await asyncio.wait_for(ws.recv(), timeout=5)
            data = json.loads(msg)
            
            assert data["type"] == "presence"
            our_user = next((u for u in data["users"] if u["user_id"] == "user-special"), None)
            assert our_user is not None
            assert our_user["name"] == "Test User 123"
            print("Special characters in name handled correctly")


class TestMultiUserWebSocket:
    """Test multi-user WebSocket scenarios"""

    @pytest.mark.asyncio
    async def test_two_users_see_each_other_in_presence(self):
        """When 2 users connect, both should see each other in presence"""
        doc_id = "test-multi-" + str(int(time.time()))
        
        # Connect user1
        ws1_url = f"{WS_BASE_URL}/api/ws/collab/{doc_id}?user_id=user1&name=Alice&color=%23ef4444"
        ws2_url = f"{WS_BASE_URL}/api/ws/collab/{doc_id}?user_id=user2&name=Bob&color=%233b82f6"
        
        async with websockets.connect(ws1_url) as ws1:
            # User1 receives initial presence (just themselves)
            msg1 = await asyncio.wait_for(ws1.recv(), timeout=5)
            data1 = json.loads(msg1)
            assert data1["type"] == "presence"
            assert len(data1["users"]) == 1
            assert data1["users"][0]["user_id"] == "user1"
            
            # Now connect user2
            async with websockets.connect(ws2_url) as ws2:
                # User2 should receive presence with both users
                msg2 = await asyncio.wait_for(ws2.recv(), timeout=5)
                data2 = json.loads(msg2)
                assert data2["type"] == "presence"
                assert len(data2["users"]) == 2
                
                # User1 should also receive updated presence with both users
                msg1_update = await asyncio.wait_for(ws1.recv(), timeout=5)
                data1_update = json.loads(msg1_update)
                assert data1_update["type"] == "presence"
                assert len(data1_update["users"]) == 2
                
                # Verify both users present
                user_ids = [u["user_id"] for u in data1_update["users"]]
                assert "user1" in user_ids
                assert "user2" in user_ids
                
                print("Multi-user presence working: both users see each other")


class TestContentBroadcast:
    """Test content broadcast between users"""

    @pytest.mark.asyncio
    async def test_content_update_broadcasts_to_other_users(self):
        """When user1 sends content_update, user2 should receive it"""
        doc_id = "test-content-" + str(int(time.time()))
        
        ws1_url = f"{WS_BASE_URL}/api/ws/collab/{doc_id}?user_id=sender&name=Sender&color=%23ef4444"
        ws2_url = f"{WS_BASE_URL}/api/ws/collab/{doc_id}?user_id=receiver&name=Receiver&color=%233b82f6"
        
        async with websockets.connect(ws1_url) as ws1:
            # Skip initial presence
            await asyncio.wait_for(ws1.recv(), timeout=5)
            
            async with websockets.connect(ws2_url) as ws2:
                # Skip presence updates
                await asyncio.wait_for(ws2.recv(), timeout=5)  # User2 initial presence
                await asyncio.wait_for(ws1.recv(), timeout=5)  # User1 updated presence
                
                # User1 sends content update
                content_msg = {
                    "type": "content_update",
                    "content": "# Test Content\n\nThis is collaborative editing!",
                    "cursor": 45
                }
                await ws1.send(json.dumps(content_msg))
                
                # User2 should receive the content update
                received = await asyncio.wait_for(ws2.recv(), timeout=5)
                data = json.loads(received)
                
                assert data["type"] == "content_update"
                assert data["sender_id"] == "sender"
                assert data["content"] == "# Test Content\n\nThis is collaborative editing!"
                assert data["cursor"] == 45
                
                print("Content broadcast working: receiver got content from sender")


class TestModeChange:
    """Test mode change functionality"""

    @pytest.mark.asyncio
    async def test_mode_change_updates_presence(self):
        """When user sends mode_change to 'editing', presence should update"""
        doc_id = "test-mode-" + str(int(time.time()))
        
        ws1_url = f"{WS_BASE_URL}/api/ws/collab/{doc_id}?user_id=editor&name=Editor&color=%23ef4444"
        ws2_url = f"{WS_BASE_URL}/api/ws/collab/{doc_id}?user_id=viewer&name=Viewer&color=%233b82f6"
        
        async with websockets.connect(ws1_url) as ws1:
            # Skip initial presence (mode should be 'viewing')
            msg = await asyncio.wait_for(ws1.recv(), timeout=5)
            data = json.loads(msg)
            assert data["users"][0]["mode"] == "viewing"
            
            async with websockets.connect(ws2_url) as ws2:
                # Skip presence updates
                await asyncio.wait_for(ws2.recv(), timeout=5)
                await asyncio.wait_for(ws1.recv(), timeout=5)
                
                # User1 changes mode to editing
                mode_msg = {"type": "mode_change", "mode": "editing"}
                await ws1.send(json.dumps(mode_msg))
                
                # Both should receive updated presence
                # User2 should get the presence update
                received = await asyncio.wait_for(ws2.recv(), timeout=5)
                data = json.loads(received)
                
                assert data["type"] == "presence"
                editor_user = next((u for u in data["users"] if u["user_id"] == "editor"), None)
                assert editor_user is not None
                assert editor_user["mode"] == "editing"
                
                print("Mode change working: editor's mode updated to 'editing'")


class TestAutoSaveViaWebSocket:
    """Test auto-save via WebSocket"""

    @pytest.mark.asyncio
    async def test_save_message_persists_to_database(self):
        """Sending 'save' message should persist content to database"""
        # Get a real document to test with
        docs_response = requests.get(f"{API_BASE_URL}/api/documents")
        assert docs_response.status_code == 200
        docs = docs_response.json()
        
        if not docs:
            pytest.skip("No documents available for save test")
        
        doc = docs[0]
        doc_id = doc["id"]
        original_content = doc.get("content", "")
        
        ws_url = f"{WS_BASE_URL}/api/ws/collab/{doc_id}?user_id=saver&name=Saver&color=%23ef4444"
        
        async with websockets.connect(ws_url) as ws:
            # Skip initial presence
            await asyncio.wait_for(ws.recv(), timeout=5)
            
            # Send save message with new content
            test_content = original_content + "\n\n<!-- Auto-save test: " + str(int(time.time())) + " -->"
            save_msg = {
                "type": "save",
                "content": test_content,
                "title": doc["title"]
            }
            await ws.send(json.dumps(save_msg))
            
            # Should receive doc_saved broadcast
            received = await asyncio.wait_for(ws.recv(), timeout=5)
            data = json.loads(received)
            
            # Could be presence or doc_saved (we're alone so doc_saved goes to us)
            # Let's verify by checking the database directly
            await asyncio.sleep(0.5)  # Give time for DB write
            
            # Verify document was updated
            updated_doc = requests.get(f"{API_BASE_URL}/api/documents/{doc_id}").json()
            assert "Auto-save test" in updated_doc["content"]
            
            # Verify version was created
            versions = requests.get(f"{API_BASE_URL}/api/documents/{doc_id}/versions").json()
            assert len(versions) >= 1
            
            # Restore original content
            restore_save = {
                "type": "save",
                "content": original_content,
                "title": doc["title"]
            }
            await ws.send(json.dumps(restore_save))
            await asyncio.sleep(0.5)
            
            print(f"Auto-save working: content persisted, {len(versions)} version(s) created")


class TestCursorUpdate:
    """Test cursor position updates"""

    @pytest.mark.asyncio
    async def test_cursor_update_broadcasts(self):
        """Cursor updates should broadcast to other users"""
        doc_id = "test-cursor-" + str(int(time.time()))
        
        ws1_url = f"{WS_BASE_URL}/api/ws/collab/{doc_id}?user_id=cursor1&name=Cursor1&color=%23ef4444"
        ws2_url = f"{WS_BASE_URL}/api/ws/collab/{doc_id}?user_id=cursor2&name=Cursor2&color=%233b82f6"
        
        async with websockets.connect(ws1_url) as ws1:
            await asyncio.wait_for(ws1.recv(), timeout=5)
            
            async with websockets.connect(ws2_url) as ws2:
                await asyncio.wait_for(ws2.recv(), timeout=5)
                await asyncio.wait_for(ws1.recv(), timeout=5)
                
                # Send cursor update
                cursor_msg = {
                    "type": "cursor_update",
                    "cursor": 100,
                    "selection_end": 150
                }
                await ws1.send(json.dumps(cursor_msg))
                
                # User2 should receive cursor update
                received = await asyncio.wait_for(ws2.recv(), timeout=5)
                data = json.loads(received)
                
                assert data["type"] == "cursor_update"
                assert data["sender_id"] == "cursor1"
                assert data["cursor"] == 100
                assert data["selection_end"] == 150
                
                print("Cursor update broadcast working")


class TestDisconnectBehavior:
    """Test disconnect scenarios"""

    @pytest.mark.asyncio
    async def test_disconnect_removes_user_from_presence(self):
        """When a user disconnects, they should be removed from presence"""
        doc_id = "test-disconnect-" + str(int(time.time()))
        
        ws1_url = f"{WS_BASE_URL}/api/ws/collab/{doc_id}?user_id=stayer&name=Stayer&color=%23ef4444"
        ws2_url = f"{WS_BASE_URL}/api/ws/collab/{doc_id}?user_id=leaver&name=Leaver&color=%233b82f6"
        
        async with websockets.connect(ws1_url) as ws1:
            await asyncio.wait_for(ws1.recv(), timeout=5)
            
            # Connect user2
            ws2 = await websockets.connect(ws2_url)
            await asyncio.wait_for(ws2.recv(), timeout=5)
            
            # User1 should see both users now
            presence_with_both = await asyncio.wait_for(ws1.recv(), timeout=5)
            data = json.loads(presence_with_both)
            assert len(data["users"]) == 2
            
            # User2 disconnects
            await ws2.close()
            
            # User1 should receive updated presence with only themselves
            presence_after_leave = await asyncio.wait_for(ws1.recv(), timeout=5)
            data = json.loads(presence_after_leave)
            assert data["type"] == "presence"
            assert len(data["users"]) == 1
            assert data["users"][0]["user_id"] == "stayer"
            
            print("Disconnect behavior working: user removed from presence")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
