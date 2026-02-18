# Emergent Knowledge Hub - PRD

## Stats: 37 documents, 46 categories, 14 unique cover images, 33 mermaid diagrams

## All Implemented Features
- [x] Notion-style UI with collapsible resizable sidebar, dark/light modes
- [x] 14 unique cover images per category
- [x] Collapsible H2 sections, Mermaid zoom controls, reading progress bar (doc pages only)
- [x] AI Chatbot (Claude Sonnet), full-text search, templates, tags, comments, versioning
- [x] Soft delete/restore with sidebar auto-refresh, public sharing, bookmarks
- [x] 33 mermaid diagrams with step-by-step flow explanations
- [x] P0: Real-time Collaborative Editing (WebSocket, presence, auto-save)
- [x] P1: Analytics Dashboard (views, searches, chatbot usage, activity)
- [x] Comprehensive QA bug fixes (iteration 9):
  - Tool/document/permanent delete confirmations
  - Sidebar auto-refresh after trash restore
  - Breadcrumb links functional (clickable, navigate to home)
  - PDF export success/failure feedback
  - Inline italic markdown rendering
  - URLs auto-linked in markdown tables
  - Role change confirmation alert
  - Analytics: "[Deleted document]" for orphaned views
  - Test data cleanup (search queries, tools, users, orphaned views)
  - Table/diagram overflow CSS fixes
  - E1 comparison table header fixed ("Capability")
  - Shadcn language label corrected

## Remaining Known Issues (from QA report)
- B-04: Bookmark badge counter can get out of sync after delete/restore cycles
- B-08: Server cold start shows empty state (infra-level)
- B-09: Duplicate TOC on custom-created pages
- B-23: Search snippets show raw markdown table formatting
- B-26: Tag filter pill persists visually after clear (functionally works)
- B-30: Test Cases category visible to all users (should be admin-only)
- S-01: Undo toast after soft delete suggestion
- S-15: Version history diff view

## Backlog
- P2: Slack/Discord Notifications
- Refactoring: Split monolithic App.js (~1700 lines) and server.py (~800 lines)
