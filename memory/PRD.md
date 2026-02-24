# Agent Anatomy - PRD

## Original Problem Statement
Build a comprehensive documentation website covering AI agent architecture, LLMs, and software development. Notion-style UI with sidebar, Markdown/Mermaid rendering, AI chatbot, search.

## Content Status (Feb 2026)
- **45 public documents**, ~240K characters
- **Zero** platform-specific references — all content is universal
- **7 new core agent docs** added: What Is an AI Agent?, The Agent Loop, Memory Systems, Planning & Reasoning, Design Patterns, Guardrails & Safety, Error Recovery

### Module Structure (17 categories, 45 docs)
1. Getting Started (4) — What Is an AI Agent?, First AI Coding Session, Communicating with Agents, Glossary
2. Tutorials (4) — REST API, Debugging 500, Choosing LLM, MongoDB vs PostgreSQL
3. Agent Anatomy (6) — Agent Loop, Memory Systems, Planning & Reasoning, Design Patterns, Guardrails & Safety, Error Recovery
4. Platform Architecture (4) — System Architecture, Orchestrator, Subagents, Tool Engine
5. LLM Internals (4) — Transformers, Training, Tokens, LLM Proxy
6. Infrastructure (3) — Kubernetes, Docker, Hot Reload
7. Frontend (2) — React, Browser Rendering
8. Backend (3) — FastAPI, MongoDB, Auth
9. DevOps (2) — Deployment, Git
10. Security (2) — Rate Limiting, SSL/CORS
11. Data & Storage (3) — Sessions, Assets, Observability
12. Advanced (3) — RAG, Frameworks, Prompt Engineering
13. Future of AI Agents (1)
14. Tools & Resources (1)
15. Limitations (1)
16. UI Guide (1)
17. FAQ (1)

## Pending — Batch 2 (Technical gaps)
- Function Calling Deep Dive
- Structured Outputs
- Fine-Tuning vs Prompting vs RAG
- Multi-Agent Communication (A2A, MCP)
- Evaluation & Observability
- Cost Optimization Strategies
- Real-World Agent Examples (Devin, Claude Code, Cursor)

## Pending — Batch 3 (Category reorg + dedup)
- Restructure categories to match recommended structure
- Deduplicate Universal Key, tool calling content
- Fix any remaining model name inaccuracies

## Pending — Features
- Employee-only access control (auth)
- Codebase refactoring (App.js, server.py)
- Interactive features (quizzes, learning paths, request tracing)

## Authentication
MOCKED — Hardcoded admin user. No real login flow.
