# Emergent Knowledge Hub - PRD

## Stats: 37 documents, 46 categories, 14 unique cover images, 33 mermaid diagrams

## All Implemented Features
- [x] Notion-style UI with collapsible resizable sidebar, dark/light modes
- [x] 14 unique cover images, collapsible H2 sections, reading progress (doc pages only)
- [x] AI Chatbot (Claude Sonnet), full-text search, templates, tags, comments, versioning
- [x] Soft delete/restore with sidebar auto-refresh, public sharing, bookmarks
- [x] 33 mermaid diagrams with step-by-step flow explanations
- [x] P0: Real-time Collaborative Editing (WebSocket, presence, auto-save)
- [x] P1: Analytics Dashboard (views, searches, chatbot usage, activity)
- [x] Comprehensive QA fixes (iterations 8-10):
  - Delete confirmations (tool, document, permanent)
  - Sidebar auto-refresh after trash restore
  - Breadcrumb links clickable (navigate to home)
  - PDF export success/failure feedback
  - Inline italic markdown rendering
  - URLs auto-linked in markdown tables
  - Search snippets strip raw markdown (code blocks, pipes, bold markers)
  - Duplicate TOC entries deduplicated
  - Bookmark badge uses actual doc count (not stale IDs)
  - Analytics: "[Deleted document]" for orphaned views, title stored with views
  - Test data cleaned (search queries, tools, users, orphaned views)
  - Content fixes: E1 table header, Shadcn language, token count consistency

## Backlog
- P2: Slack/Discord Notifications
- Refactoring: Split monolithic App.js (~1700 lines) and server.py (~800 lines)
