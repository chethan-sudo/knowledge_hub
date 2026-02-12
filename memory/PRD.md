# Emergent Knowledge Hub - PRD

## Original Problem Statement
Notion-like documentation website "Emergent Knowledge Hub" with admin/viewer roles, AI chatbot, comprehensive QA test cases, and full document management.

## Architecture
- **Frontend**: React + Custom CSS (port 3000)
- **Backend**: FastAPI + Motor (port 8001)
- **Database**: MongoDB (users, user_sessions, categories, documents, doc_versions, comments, bookmarks, tools, chat_messages)
- **Auth**: Emergent-managed Google OAuth with session cookies
- **AI**: Claude Sonnet 4.5 via Emergent LLM Key

## All Implemented Features
- [x] Google OAuth login (Emergent-managed)
- [x] Admin/Viewer role system (chethan@emergent.sh = admin)
- [x] **Invite system** - Settings page with email invite, role picker, team management
- [x] Dark/Light mode (mermaid adapts to theme, no yellow)
- [x] Resizable sidebar with drag handle
- [x] Sidebar categories expanded by default
- [x] Inline search (category + doc results, ESC to close, fuzzy match)
- [x] Mermaid diagrams - larger inline, expand 90vw modal with H+V scroll
- [x] PDF export
- [x] Document version history
- [x] **Tags system** - auto-suggestions, tag cloud filter on home page
- [x] Keyboard navigation (ArrowUp/Down)
- [x] Soft delete + Trash with admin restore
- [x] Threaded comments with upvotes and replies
- [x] Public document sharing (modal dialog)
- [x] Tools & Resources directory (admin-managed)
- [x] Category management UI (admin-only)
- [x] **Document templates** - 5 pre-built (API Doc, Runbook, RCA, Meeting Notes, Test Plan)
- [x] Bookmarks, Breadcrumbs, TOC
- [x] Reading progress indicator
- [x] **AI Chatbot** (Claude Sonnet) for doc Q&A
- [x] **AI-Agent test cases** - 15 TCs with TC IDs, steps, expected results
- [x] LLM Proxy Architecture document
- [x] 34 documents, 44 categories

## API Endpoints
Auth: POST /api/auth/session, GET /api/auth/me, POST /api/auth/logout
Users: GET /api/users, POST /api/invite, PUT /api/users/{id}/role, DELETE /api/users/{id}
Categories: GET/POST /api/categories, PUT/DELETE /api/categories/{id}
Documents: GET/POST /api/documents, GET/PUT/DELETE /api/documents/{id}
Versions: GET /api/documents/{id}/versions
Comments: GET/POST /api/documents/{id}/comments, POST /api/comments/{id}/upvote, DELETE /api/comments/{id}
Sharing: POST /api/documents/{id}/share, GET /api/public/{shareId}
Tools: GET/POST /api/tools, PUT/DELETE /api/tools/{id}
Trash: GET /api/trash, POST /api/trash/{id}/restore, DELETE /api/trash/{id}
Bookmarks: GET/POST /api/bookmarks, POST /api/bookmarks/{id}
Search: GET /api/search?q=...
Tags: GET /api/tags, GET /api/tags/suggestions?q=...
Templates: GET /api/templates
Chat: POST /api/chat, GET /api/chat/history/{session_id}

## Backlog (P1)
- Drag-and-drop document reordering
- Mermaid chart explanations in content
- Collaborative editing (presence indicators)
