# Emergent Knowledge Hub - PRD

## Stats: 37 documents, 47 categories, 14 unique cover images

## All Implemented Features
- [x] 14 unique cover images (2D illustrations, distinct per category)
- [x] Collapsible H2 sections with +/- toggle
- [x] Finshots-style circular reading progress (bottom-right, SVG circle with %)
- [x] Fixed sidebar (position: fixed, independent scroll)
- [x] Mermaid zoom controls (+/- reset in expanded view)
- [x] Mermaid text overlap fixed (shortened labels, 60/70px spacing)
- [x] Flow explanations added to 23 docs with mermaid diagrams
- [x] Complete QA Verification Guide (8,320 chars, DB verification, API testing, E2E scenarios)
- [x] All previous features (chatbot, templates, tags, search, etc.)
- [x] **P0: Real-time Collaborative Editing** (Feb 2026)
  - WebSocket-based real-time sync via `/api/ws/collab/{doc_id}`
  - Multi-user presence indicators (colored avatars showing who's viewing/editing)
  - Live content sync between editors with cursor preservation
  - Auto-save with 3-second debounce via WebSocket
  - "Live editing" banner in editor with connection status
  - Save status indicators (Saving... / Saved)
  - Anonymous user identity (random name + color stored in localStorage)
  - Auto-reconnect on WebSocket disconnect (2s retry)
  - Raw ASGI CORS middleware (replaced BaseHTTPMiddleware to support WebSocket)

## Architecture
- Backend: FastAPI (server.py) with WebSocket support
- Frontend: React (App.js) with useCollaboration hook
- Database: MongoDB
- LLM: Claude Sonnet via emergentintegrations (AI chatbot)
- No authentication (public access, default admin context)

## Key Endpoints
- REST: /api/documents, /api/categories, /api/search, /api/chat, /api/documents/{id}/presence
- WebSocket: /api/ws/collab/{doc_id} (query params: user_id, name, color)

## Backlog
- P1: Advanced analytics dashboard (views, search queries, chatbot usage)
- P2: Slack/Discord notifications on new comments/updates
- Backlog: Offline Access/PWA, Drag-and-drop document reordering
- Refactoring: Split monolithic App.js (~1400 lines) and server.py (~700 lines)
