# Emergent Knowledge Hub - PRD

## Architecture
- Frontend: React + Custom CSS (port 3000)
- Backend: FastAPI + Motor (port 8001)  
- Database: MongoDB
- Auth: Emergent Google OAuth + localStorage token + cookie fallback
- AI: Claude Sonnet 4.5 via Emergent LLM Key

## All Implemented Features (36 docs, 46 categories)
- [x] Google OAuth with dual auth (localStorage token + cookie)
- [x] Admin/Viewer roles, Invite system, Settings page
- [x] Comprehensive System Architecture (DB, Jobs, Audits, Metadata, Chat History, ENV, Tools, Subagents, LLM Proxy)
- [x] Limitations & Constraints category
- [x] UI Guide category (every button documented)
- [x] AI Agent test cases (TC-AGT-001 to TC-AGT-015)
- [x] Mermaid diagrams with scoped CSS expand button (no size inheritance)
- [x] Book logo for Knowledge Hub brand
- [x] AI Chatbot with improved context (5 docs, 4000 chars each)
- [x] Reading progress bar (4px gradient with glow)
- [x] Document templates (5 types), Tags with suggestions + cloud filter
- [x] Resizable sidebar, inline search, dark/light mode
- [x] Soft delete + Trash, version history, threaded comments
- [x] Public sharing, PDF export, bookmarks, keyboard nav
- [x] Dynamic CORS middleware for credential support

## Backlog
- Drag-and-drop document reordering
- Mermaid chart explanations in content
- Collaborative editing (presence indicators)
