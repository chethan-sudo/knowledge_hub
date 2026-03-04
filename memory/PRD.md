# Agent Anatomy - PRD

## Overview
Production-ready AI agent education platform. 58 docs, 16+ categories, interactive learning.

## All Features
- Document viewer: Markdown, Mermaid, code blocks, TOC, reading time, timestamps
- Version history with restore
- Keyword auto-linking (skips current doc)
- Related documents, Next/Previous navigation
- Interactive quizzes per document (2-4 questions each)
- **Module-level tests**: 11 category quizzes with 2-5 questions each
- 4 learning path final assessments with downloadable PDF certificates
- **Category pages** (/category/{catId}): Document list + module test overview
- 4 learning paths: Beginner, Builder, LLM Foundations, Practitioner
- **Enhanced animated roadmap**: progress-filling connection line, pulse animation on next step
- Staggered step card entrance animations
- Collapsible quiz (Take Quiz button, minimize with X)
- Full-text search with Ctrl+K
- Bookmarks, Trash (restore only), Tools page
- AI Chatbot (Claude Sonnet)
- Analytics dashboard
- Light/dark mode, mobile responsive
- Print / Save as PDF (window.print with @media print CSS)
- Downloadable PDF certificates via jsPDF
- 404 page, Error boundary
- Comments with owner-only delete
- Draft auto-save to localStorage for new pages

## Content
58 public documents, 282K+ chars, zero platform-specific references
All content is general AI agent architecture knowledge
11 module tests across categories

## Auth
MOCKED - Hardcoded admin

## Completed (March 4, 2026)
- Fixed PDF export: replaced broken html2canvas+jsPDF with window.print() + @media print CSS
- Added downloadable PDF certificates using jsPDF programmatic generation
- Added Printer and Award icons, removed html2canvas dependency
- **NEW: Category Pages** — Clicking home cards navigates to /category/{catId} with numbered doc list + module test
- **NEW: Module Tests** — 11 interactive quizzes across categories (Getting Started, Platform Architecture, LLM Internals, Infrastructure, Backend Dev, Frontend Dev, Security, Data & Storage, Advanced Concepts, DevOps, Tutorials)
- **NEW: Enhanced Roadmap Animations** — Progress line fills as steps complete, pulse on next step, staggered step card animations
- All previous bug fixes verified (Start Again, Tool Delete, Editor Nav, Drafts)

## Upcoming Tasks
- (P2) Codebase Refactoring: Split App.js and server.py into modules
- (P2) "Trace a Request" simulator for architecture visualization
- (P3) Real-time Notifications
- (Backlog) Offline/PWA
- (Backlog) Real authentication (login system)
