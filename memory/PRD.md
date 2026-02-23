# Emergent Knowledge Hub - PRD

## Original Problem Statement
Build and refine "Emergent Knowledge Hub," a comprehensive, Notion-style documentation website for the Emergent platform. Key features include a resizable sidebar, light/dark modes, Markdown/Mermaid rendering, a Claude Sonnet-powered AI chatbot, full-text search, and document management. The application operates on a public, no-login model, with all write operations using a hardcoded default admin user.

## Architecture
- **Frontend**: React (monolithic `App.js`) with dark/light theme, resizable sidebar, Markdown/Mermaid rendering
- **Backend**: FastAPI (monolithic `server.py`) with MongoDB, WebSocket collaboration, analytics
- **Database**: MongoDB (`test_database`)
- **LLM**: Claude Sonnet 4.5 via emergentintegrations (Emergent LLM Key)
- **Key Libraries**: react-markdown, remark-gfm, mermaid, html2canvas, jsPDF, websockets

## Core Features (Implemented)
- Notion-style dashboard with category navigation
- Resizable sidebar with keyboard navigation
- Document viewer with Markdown/Mermaid rendering
- AI chatbot (Claude Sonnet 4.5)
- Full-text search with snippets
- Real-time collaborative editing (WebSocket)
- Analytics dashboard
- Tools & Resources page
- Bookmarks, Trash, Settings pages
- Reading progress indicator, scroll-spy TOC
- Document export (PDF)
- Tag filtering
- Light/dark mode

## Content
All documentation managed in `backend/seed_data.py` covering: Platform Architecture, LLM Internals, Infrastructure, Frontend/Backend Dev, DevOps, Security, Data & Storage, Advanced Concepts, Future of AI Agents, Limitations, UI Guide, FAQ, and internal Test Cases.

## Key DB Schema
- `users`: {email, name, role, avatar}
- `documents`: {id, title, content, category_id, author_id, deleted, tags, ...}
- `categories`: {id, name, icon, order, parent_id, internal}
- `tools`: {name, url, description, category}
- `doc_views`, `search_logs`, `chat_messages`: analytics collections

## What's Implemented (as of Feb 2026)
- All core features listed above
- 25+ bug fixes from comprehensive QA report
- Real-time collaboration via WebSocket
- Analytics dashboard with metrics
- Extensive content with FAQ section
- Delete confirmation for resources
- Cold start loading screen with auto-retry
- Internal categories hidden from public sidebar/homepage
- Consistent table formatting across all test case documents

## Backlog
- **P2**: Further content enhancement with more examples
- **P2**: Real-time notifications (Slack/Discord)
- **Backlog**: PWA/Offline access
- **Backlog**: Refactor monolithic App.js and server.py into modular components/routes

## Authentication
MOCKED - Hardcoded admin user (admin@emergent.sh). No real login flow.

## 3rd Party Integrations
- Claude Sonnet 4.5 (Text) via emergentintegrations + Emergent LLM Key
- OpenAI GPT Image 1 (cover images) via Emergent LLM Key
