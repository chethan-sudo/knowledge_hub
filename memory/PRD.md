# Emergent Knowledge Hub - PRD

## Original Problem Statement
Notion-like documentation website renamed to "Emergent Knowledge Hub" with comprehensive features. Admin (chethan@emergent.sh) has full CRUD; viewers can read + comment. AI-powered chatbot for doc Q&A.

## Architecture
- **Frontend**: React + Custom CSS (port 3000)
- **Backend**: FastAPI + Motor (port 8001)
- **Database**: MongoDB
- **Auth**: Emergent-managed Google OAuth with session cookies
- **AI**: Claude Sonnet 4.5 via Emergent LLM Key (emergentintegrations)

## All Implemented Features
- [x] Google OAuth login (Emergent-managed)
- [x] Admin/Viewer role system (chethan@emergent.sh = admin)
- [x] Dark/Light mode (no yellow mermaid bg in either)
- [x] Resizable sidebar with drag handle
- [x] Sidebar categories expanded by default (show all docs)
- [x] Inline search with category + document results, ESC to close
- [x] Fuzzy/case-insensitive search with heading matches
- [x] Mermaid diagrams - larger inline, expand to 90vw modal with H+V scroll
- [x] PDF export with html2canvas
- [x] Document version history
- [x] Tags/labels system
- [x] Keyboard navigation (ArrowUp/Down)
- [x] Soft delete + Trash with admin restore
- [x] Threaded comments with upvotes and replies
- [x] Public document sharing (modal dialog flow)
- [x] Tools & Resources directory (admin-managed)
- [x] Category management UI (admin-only)
- [x] Bookmarks
- [x] Breadcrumb navigation
- [x] Table of contents
- [x] Reading progress indicator
- [x] AI Chatbot (Claude Sonnet) for doc Q&A
- [x] Test Cases category (6 sub-categories)
- [x] LLM Proxy Architecture document
- [x] 33 documents, 43 categories

## Backlog
- Invite system (email-based with role checkboxes)
- Document templates for new pages
- Tags improvement (suggestions, cloud, filter)
- Drag-and-drop document reordering
- AI agent test cases (detailed TC format)
