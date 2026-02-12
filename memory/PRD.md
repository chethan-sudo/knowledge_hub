# Emergent Document Hub - PRD

## Original Problem Statement
Notion-like documentation website called "Emergent Document Hub" with comprehensive features for managing AI/platform documentation. Admin (chethan@emergent.sh) has full CRUD; viewers can read + comment.

## Architecture
- **Frontend**: React + Custom CSS (port 3000)
- **Backend**: FastAPI + Motor (port 8001)
- **Database**: MongoDB (users, user_sessions, categories, documents, doc_versions, comments, bookmarks, tools)
- **Auth**: Emergent-managed Google OAuth with session cookies

## All Implemented Features
- [x] Google OAuth login (Emergent-managed)
- [x] Admin/Viewer role system (chethan@emergent.sh = admin)
- [x] Dark/Light mode toggle
- [x] Sidebar navigation with nested categories + flattening
- [x] Inline search bar (not modal) with fuzzy/case-insensitive matching + snippets
- [x] Mermaid diagram rendering with expand/fullscreen
- [x] PDF export (renders Mermaid as images)
- [x] Document version history
- [x] Tags/labels system
- [x] Keyboard navigation (ArrowUp/Down)
- [x] Soft delete + Trash with admin restore
- [x] Threaded comments with upvotes and replies
- [x] Public document sharing (shareable links)
- [x] Tools & Resources directory (admin-managed)
- [x] Category management UI (admin-only)
- [x] Bookmarks
- [x] Breadcrumb navigation
- [x] Table of contents
- [x] Pre-seeded content: 33 documents, 43 categories
- [x] Test Cases category (6 sub-categories, comprehensive QA suite)
- [x] LLM Proxy Architecture document
- [x] Code blocks with copy button, tables, markdown rendering

## Key API Endpoints
- POST /api/auth/session (Google OAuth exchange)
- GET /api/auth/me, POST /api/auth/logout
- GET/POST /api/categories, PUT/DELETE /api/categories/{id}
- GET/POST /api/documents, GET/PUT/DELETE /api/documents/{id}
- GET /api/documents/{id}/versions
- GET/POST /api/documents/{id}/comments
- POST /api/comments/{id}/upvote, DELETE /api/comments/{id}
- POST /api/documents/{id}/share, GET /api/public/{shareId}
- GET/POST /api/tools, PUT/DELETE /api/tools/{id}
- GET /api/trash, POST /api/trash/{id}/restore, DELETE /api/trash/{id}
- GET/POST /api/bookmarks, POST /api/bookmarks/{id}
- GET /api/search?q=..., GET /api/tags

## Backlog
- Drag-and-drop document reordering
- Collaborative editing (multi-user)
- Reading progress indicator
- Document sharing with specific users/groups
