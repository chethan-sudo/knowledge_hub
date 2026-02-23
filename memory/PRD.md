# Emergent Knowledge Hub - PRD

## Original Problem Statement
Build a comprehensive, Notion-style documentation website covering AI agent architecture, LLMs, and software development. Public access model with hardcoded admin user.

## Architecture
- **Frontend**: React (`App.js`) — sidebar, doc viewer, Markdown/Mermaid, AI chat, analytics
- **Backend**: FastAPI (`server.py`) — CRUD, search, AI chat, WebSocket collab, analytics
- **Database**: MongoDB
- **LLM**: Claude Sonnet 4.5 via emergentintegrations

## Content Status (Feb 2026)
- **45 total documents** (38 public + 7 internal test cases)
- **~145K characters** of general-purpose technical content
- **Zero** E1/Emergent-specific references in all public documents
- All content is universal — covers AI agent architecture, LLMs, and software development generically
- Categories: Getting Started (3), Tutorials (4), Platform Architecture (4), LLM Internals (4), Infrastructure (3), Frontend (2), Backend (3), DevOps (2), Security (2), Data & Storage (3), Advanced Concepts (3), Future (1), Limitations (1), UI Guide (1), FAQ (1)

## Pending
- **Access control**: Make the hub accessible only to Emergent employees (user requested, to be done after content is finalized)

## Backlog
- Refactor monolithic App.js and server.py
- PWA/Offline access
- Real-time notifications

## Authentication
MOCKED — Hardcoded admin user. No real login flow. Employee-only access needs auth implementation.
