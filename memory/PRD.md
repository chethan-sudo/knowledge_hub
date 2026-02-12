# Emergent Document Hub — PRD

## Original Problem Statement
User wanted all knowledge about Emergent platform, LLMs, AI agents, infrastructure etc. converted into a Notion-like documentation website called "Emergent Document Hub" with light/dark mode, categories/subcategories, full CRUD, search, bookmarks.

## Architecture
- **Frontend**: React + Tailwind CSS (port 3000)
- **Backend**: FastAPI + Motor (port 8001)
- **Database**: MongoDB
- **Auth**: JWT-based (bcrypt + pyjwt)

## User Personas
- Developers learning about AI agent architecture
- Technical users exploring LLM internals, Kubernetes, deployment pipelines
- Emergent platform users wanting reference documentation

## Core Requirements
- [x] Authentication (register/login with JWT)
- [x] Dark/Light mode toggle
- [x] Sidebar navigation with nested categories
- [x] Document viewer with markdown rendering
- [x] Code block syntax highlighting with copy button
- [x] Table rendering
- [x] Table of contents per document
- [x] Breadcrumb navigation
- [x] Search dialog (Ctrl+K)
- [x] Bookmarks (toggle, bookmarks page)
- [x] CRUD for documents (create, read, update, delete)
- [x] Pre-seeded content (25 documents across 34 categories)

## What's Been Implemented (Feb 2026)
- Full auth system with JWT
- 10 parent categories, 24 subcategories
- 25 pre-seeded documents covering: Platform Architecture, LLM Internals, Infrastructure, Frontend/Backend Development, DevOps, Security, Data Storage, Advanced Concepts, Future of AI
- Notion-like sidebar with collapsible nested navigation
- Search command palette
- Bookmark system
- Document editor with markdown
- Dark/Light theme with persistence

## Backlog
### P0 (Critical)
- None

### P1 (Important)
- Markdown preview in editor (split-pane)
- Full-text search with content snippets in results
- Drag-and-drop document reordering
- Category CRUD from UI

### P2 (Nice to have)
- Export documents as PDF/Markdown
- Collaborative editing (multi-user)
- Version history per document
- Tags/labels system
- Reading progress indicator
- Favorites vs Bookmarks separation
- Keyboard navigation for sidebar

## Next Tasks
1. Add markdown preview in editor
2. Add content snippets in search results
3. Add category management UI
4. Add document sharing/export
