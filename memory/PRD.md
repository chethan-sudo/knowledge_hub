# Emergent Knowledge Hub - PRD

## Architecture
- Frontend: React + Custom CSS (port 3000)
- Backend: FastAPI + Motor (port 8001)  
- Database: MongoDB
- Auth: Emergent-managed Google OAuth
- AI: Claude Sonnet 4.5 via Emergent LLM Key

## All Implemented Features
- [x] Google OAuth, Admin/Viewer roles, Invite system
- [x] 36 documents, 46 categories (comprehensive coverage)
- [x] System Architecture with DB, Jobs, Audits, Metadata, Chat History, ENV, Tools, Subagents, LLM Proxy
- [x] Limitations & Constraints category
- [x] UI Guide category (every button/feature documented)
- [x] AI Agent test cases (TC-AGT-001 to TC-AGT-015)
- [x] Mermaid diagrams with proper expand (scoped CSS, small button)
- [x] Book logo for Knowledge Hub brand
- [x] AI Chatbot (Claude Sonnet) with improved context retrieval
- [x] Reading progress bar (gradient, 4px)
- [x] Document templates (5 types)
- [x] Tags with auto-suggestions + tag cloud filter
- [x] Resizable sidebar, inline search, dark/light mode
- [x] Soft delete + Trash, version history, comments with threads
- [x] Public sharing, PDF export, bookmarks, keyboard nav

## Backlog
- Drag-and-drop document reordering
- Mermaid chart explanations in content  
- Collaborative editing (presence indicators)
