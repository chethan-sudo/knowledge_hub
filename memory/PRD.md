# Emergent Knowledge Hub - PRD

## Architecture
- Frontend: React + Custom CSS (port 3000)
- Backend: FastAPI + Motor (port 8001)  
- Database: MongoDB
- Auth: Email/password with JWT-style session tokens (localStorage)
- AI: Claude Sonnet 4.5 via Emergent LLM Key

## Auth
- Register: POST /api/auth/register (email, name, password)
- Login: POST /api/auth/login (email, password) → returns token
- Token stored in localStorage, sent as Authorization: Bearer header
- Admin: chethan@emergent.sh (password: admin123)
- Viewer: any other registered user

## All Implemented Features (36 docs, 46 categories)
- [x] Email/password auth with register/login
- [x] Admin/Viewer roles, Invite system, Settings page
- [x] System Architecture (DB, Jobs, Audits, Metadata, ENV, Tools, Subagents, LLM Proxy)
- [x] Limitations & Constraints category
- [x] UI Guide category
- [x] AI Agent test cases (15 TCs)
- [x] Mermaid diagrams with scoped expand button
- [x] AI Chatbot (Claude Sonnet)
- [x] Document templates (5 types), Tags with suggestions + cloud
- [x] Resizable sidebar, inline search, dark/light mode
- [x] Soft delete + Trash, version history, threaded comments
- [x] Public sharing, PDF export, bookmarks, keyboard nav
- [x] Reading progress bar

## Backlog
- Drag-and-drop document reordering
- Mermaid chart explanations
- Collaborative editing
