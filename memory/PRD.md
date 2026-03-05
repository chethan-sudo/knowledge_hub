# Agent Anatomy - PRD

## Overview
Production-ready AI agent education platform. 58 docs, 16+ categories, interactive learning with gamified progress tracking.

## All Features
- Document viewer: Markdown, Mermaid, code blocks, TOC, reading time, timestamps
- Version history with restore
- Keyword auto-linking (skips current doc)
- Related documents, Next/Previous navigation
- Interactive quizzes per document (2-4 questions each)
- Module-level tests: 11 category quizzes with 2-5 questions each
- 4 learning path final assessments with downloadable PDF certificates
- Category pages (/category/{catId}): Document list + module test overview
- 4 learning paths: Beginner, Builder, LLM Foundations, Practitioner
- Enhanced animated roadmap: progress-filling connection line, pulse animation on next step
- **Knowledge Progress Dashboard** (/progress): Personal learning overview with SVG progress rings, overall mastery bar, achievement badges, recently read docs, learning path progress
- **Gamification**: 6 achievement badges (First Steps, Bookworm, Quiz Ace, Module Pro, Pathfinder, Halfway There), 4-tier level system (Newcomer, Explorer, Practitioner, Expert)
- **Progress tracking**: localStorage-based tracking for docs read, quizzes passed, module tests passed
- Collapsible quiz (Take Quiz button, minimize with X)
- Full-text search with Ctrl+K
- Bookmarks, Trash (restore only), Tools page
- AI Chatbot (Claude Sonnet)
- Analytics dashboard (admin)
- Light/dark mode, mobile responsive
- Print / Save as PDF (window.print with @media print CSS)
- Downloadable PDF certificates via jsPDF
- 404 page, Error boundary
- Comments with owner-only delete
- Draft auto-save to localStorage for new pages

## Content
58 public documents, 282K+ chars, zero platform-specific references
11 module tests across categories

## Auth
MOCKED - Hardcoded admin

## Completed (March 4, 2026)
- Fixed PDF export: window.print() + @media print CSS
- Downloadable PDF certificates via jsPDF
- Category Pages with module tests
- 11 module tests seeded
- Enhanced roadmap animations
- **Knowledge Progress Dashboard with gamification**:
  - 4 SVG progress rings (docs, quizzes, modules, paths)
  - Overall mastery bar with percentage
  - 4-tier level system
  - 6 achievement badges
  - Recently read docs
  - Learning path progress with clickable navigation

## Upcoming Tasks
- (P2) Codebase Refactoring: Split App.js and server.py into modules
- (P2) "Trace a Request" interactive simulator
- (P3) Real-time Notifications
- (Backlog) Offline/PWA
- (Backlog) Real authentication (login system)
