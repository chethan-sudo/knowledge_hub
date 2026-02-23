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
- Document export (PDF), Tag filtering, Light/dark mode

## Content Structure (45 documents, 220K+ chars)

### New Categories (Feb 2026)
- **Getting Started** (3 docs): "Your First 10 Minutes", "How to Talk to E1", "Platform Glossary"
- **Tutorials** (4 docs): "Building a REST API", "Debugging a 500 Error", "Choosing the Right LLM", "MongoDB vs PostgreSQL"

### Existing Categories (enhanced)
- Platform Architecture, LLM Internals, Infrastructure, Frontend Dev, Backend Dev, DevOps, Security, Data & Storage, Advanced Concepts, Future of AI Agents, Limitations, UI Guide, FAQ, Tools & Resources

### Content Enhancement (all 7 areas completed)
1. Real code examples added to every document
2. Troubleshooting sections with problem/cause/solution tables
3. Real-world use case tutorials (CRUD API, debugging walkthrough)
4. Comparison & decision-making content (LLM comparison, MongoDB vs PostgreSQL)
5. All thin documents expanded from ~1K-3K to 5K-7K chars
6. Visual content: sequence diagrams, architecture diagrams, decision flowcharts
7. Getting Started onboarding guide with glossary

### Internal Categories (hidden from public)
- Test Cases (7 subcategories, marked `internal: true`)

## Key DB Schema
- `categories`: {id, name, icon, order, parent_id, internal}
- `documents`: {id, title, content, category_id, author_id, deleted, tags}
- `tools`: {name, url, description, category}
- `doc_views`, `search_logs`, `chat_messages`: analytics

## Backlog
- **P2**: Real-time notifications (Slack/Discord)
- **Backlog**: PWA/Offline access
- **Backlog**: Refactor monolithic App.js and server.py into modular components

## Authentication
MOCKED - Hardcoded admin user (admin@emergent.sh). No real login flow.

## 3rd Party Integrations
- Claude Sonnet 4.5 (Text) via emergentintegrations + Emergent LLM Key
- OpenAI GPT Image 1 (cover images) via Emergent LLM Key
