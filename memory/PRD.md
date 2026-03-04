# Agent Anatomy - PRD

## Overview
Production-ready AI agent education platform. 58 docs, 16 categories, interactive learning.

## All Features
- Document viewer: Markdown, Mermaid, code blocks, TOC, reading time, timestamps
- Version history with restore
- Keyword auto-linking (skips current doc)
- Related documents, Next/Previous navigation
- Interactive quizzes: 51+ docs with 2-4 questions each
- 5 module-level final tests (24 questions)
- 4 learning path final assessments with completion certificates
- Downloadable PDF certificates via jsPDF
- 4 learning paths: Beginner, Builder, LLM Foundations, Practitioner
- Animated roadmap with progress tracking
- "Back to Learning Path" navigation from docs
- Collapsible quiz (Take Quiz button, minimize with X)
- Full-text search with Ctrl+K
- Bookmarks, Trash (restore only), Tools page
- AI Chatbot (Claude Sonnet)
- Analytics dashboard
- Light/dark mode, mobile responsive
- Print / Save as PDF (window.print with @media print CSS)
- 404 page, Error boundary
- Comments with owner-only delete
- Draft auto-save to localStorage for new pages

## Content
58 public documents, 282K+ chars, zero platform-specific references
All content is general AI agent architecture knowledge

## Auth
MOCKED - Hardcoded admin

## Completed (March 4, 2026)
- Fixed PDF export: replaced broken html2canvas+jsPDF with window.print() + @media print CSS
- Added downloadable PDF certificates using jsPDF programmatic generation
- Added Printer and Award icons
- Removed html2canvas dependency
- All 4 previous bug fixes verified (Start Again, Tool Delete, Editor Nav, Drafts)

## Upcoming Tasks
- (P1) Module-Level Tests UI: Build frontend for category/module final tests
- (P1) Interactive Learning Enhancements: Better roadmap animations
- (P2) Codebase Refactoring: Split App.js and server.py into modules
- (P3) Real-time Notifications
- (Backlog) Offline/PWA
