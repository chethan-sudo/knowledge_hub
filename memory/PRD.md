# Emergent Document Hub - PRD

## Original Problem Statement
User wanted all knowledge about Emergent platform, LLMs, AI agents, infrastructure etc. converted into a Notion-like documentation website called "Emergent Document Hub" with light/dark mode, categories/subcategories, full CRUD, search, bookmarks, and comprehensive feature set.

## Architecture
- **Frontend**: React (single-file App.js) + Custom CSS (port 3000)
- **Backend**: FastAPI + Motor (port 8001)
- **Database**: MongoDB
- **Auth**: JWT-based (bcrypt + pyjwt)

## Core Requirements (All Completed)
- [x] Authentication (register/login with JWT)
- [x] Dark/Light mode toggle
- [x] Sidebar navigation with nested categories
- [x] Sidebar flattening (subcategories with 1 doc shown inline)
- [x] Document viewer with custom markdown rendering
- [x] Mermaid diagram rendering (22 documents with diagrams)
- [x] Code blocks with copy button
- [x] Table rendering
- [x] Table of contents per document
- [x] Breadcrumb navigation
- [x] Search dialog (Ctrl+K) with backend full-text search
- [x] Search results with content snippets
- [x] Bookmarks (toggle, bookmarks page)
- [x] CRUD for documents (create, read, update, delete)
- [x] Pre-seeded content (26 documents across 34 categories)
- [x] Content accuracy (E1 as orchestrator, not LLM)
- [x] System Architecture Overview document
- [x] Split-pane markdown editor with live preview
- [x] Category management UI (create, edit, delete)
- [x] Export documents as Markdown
- [x] Document version history
- [x] Tags/labels system
- [x] Keyboard navigation for sidebar (ArrowUp/Down)

## Key API Endpoints
- POST /api/auth/register, /api/auth/login, GET /api/auth/me
- GET/POST /api/categories, PUT/DELETE /api/categories/{id}
- GET/POST /api/documents, GET/PUT/DELETE /api/documents/{id}
- GET /api/documents/{id}/versions
- GET /api/documents/{id}/export
- GET/POST /api/bookmarks, POST /api/bookmarks/{id}
- GET /api/search?q=...
- GET /api/tags

## DB Collections
- users, categories, documents, bookmarks, doc_versions

## Backlog
- Drag-and-drop document reordering
- Collaborative editing (multi-user)
- Reading progress indicator
- Full-text search indexing (MongoDB text index)
- Document sharing via public links
