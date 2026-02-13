"""Seed data for Emergent Document Hub - Categories and Documents."""
from datetime import datetime, timezone
import uuid

def _id():
    return str(uuid.uuid4())

NOW = datetime.now(timezone.utc).isoformat()
SYSTEM_AUTHOR = "system"

# --- Category IDs ---
CAT_PLATFORM = _id()
CAT_LLM = _id()
CAT_INFRA = _id()
CAT_FRONTEND = _id()
CAT_BACKEND = _id()
CAT_DEVOPS = _id()
CAT_SECURITY = _id()
CAT_DATA = _id()
CAT_ADVANCED = _id()
CAT_FUTURE = _id()

# Sub-categories
SUB_E1 = _id()
SUB_AGENTS = _id()
SUB_TOOLS = _id()
SUB_TRANSFORMER = _id()
SUB_TRAINING = _id()
SUB_TOKENS = _id()
SUB_K8S = _id()
SUB_DOCKER = _id()
SUB_SUPERVISOR = _id()
SUB_REACT = _id()
SUB_BROWSER = _id()
SUB_FASTAPI = _id()
SUB_MONGODB = _id()
SUB_AUTH = _id()
SUB_DEPLOY = _id()
SUB_GIT = _id()
SUB_RATELIMIT = _id()
SUB_ENCRYPTION = _id()
SUB_SESSION = _id()
SUB_ASSETS = _id()
SUB_DEBUG = _id()
SUB_RAG = _id()
SUB_FRAMEWORKS = _id()
SUB_PROMPT = _id()

# New categories
CAT_TESTCASES = _id()
SUB_TC_AUTH = _id()
SUB_TC_DOCS = _id()
SUB_TC_SEARCH = _id()
SUB_TC_ADMIN = _id()
SUB_TC_EDGE = _id()
SUB_TC_PERF = _id()
SUB_TC_AGENT = _id()
CAT_TOOLS = _id()
SUB_LLM_PROXY = _id()
CAT_LIMITATIONS = _id()
CAT_UI_GUIDE = _id()

CATEGORIES = [
    {"id": CAT_PLATFORM, "name": "Platform Architecture", "icon": "Layers", "order": 0, "parent_id": None},
    {"id": SUB_E1, "name": "E1 Orchestrator", "icon": "Brain", "order": 0, "parent_id": CAT_PLATFORM},
    {"id": SUB_AGENTS, "name": "Agents & Subagents", "icon": "Users", "order": 1, "parent_id": CAT_PLATFORM},
    {"id": SUB_TOOLS, "name": "Tools & Execution", "icon": "Wrench", "order": 2, "parent_id": CAT_PLATFORM},

    {"id": CAT_LLM, "name": "LLM Internals", "icon": "Cpu", "order": 1, "parent_id": None},
    {"id": SUB_TRANSFORMER, "name": "Transformer Architecture", "icon": "Network", "order": 0, "parent_id": CAT_LLM},
    {"id": SUB_TRAINING, "name": "Training Pipeline", "icon": "GraduationCap", "order": 1, "parent_id": CAT_LLM},
    {"id": SUB_TOKENS, "name": "Tokens & Function Calling", "icon": "Hash", "order": 2, "parent_id": CAT_LLM},

    {"id": CAT_INFRA, "name": "Infrastructure", "icon": "Server", "order": 2, "parent_id": None},
    {"id": SUB_K8S, "name": "Kubernetes", "icon": "Container", "order": 0, "parent_id": CAT_INFRA},
    {"id": SUB_DOCKER, "name": "Docker & Containers", "icon": "Box", "order": 1, "parent_id": CAT_INFRA},
    {"id": SUB_SUPERVISOR, "name": "Hot Reload & Supervisor", "icon": "RefreshCw", "order": 2, "parent_id": CAT_INFRA},

    {"id": CAT_FRONTEND, "name": "Frontend Development", "icon": "Monitor", "order": 3, "parent_id": None},
    {"id": SUB_REACT, "name": "React Internals", "icon": "Atom", "order": 0, "parent_id": CAT_FRONTEND},
    {"id": SUB_BROWSER, "name": "Browser & Rendering", "icon": "Globe", "order": 1, "parent_id": CAT_FRONTEND},

    {"id": CAT_BACKEND, "name": "Backend Development", "icon": "Database", "order": 4, "parent_id": None},
    {"id": SUB_FASTAPI, "name": "FastAPI Internals", "icon": "Zap", "order": 0, "parent_id": CAT_BACKEND},
    {"id": SUB_MONGODB, "name": "MongoDB Deep Dive", "icon": "HardDrive", "order": 1, "parent_id": CAT_BACKEND},
    {"id": SUB_AUTH, "name": "Authentication", "icon": "Shield", "order": 2, "parent_id": CAT_BACKEND},

    {"id": CAT_DEVOPS, "name": "DevOps & Deployment", "icon": "Rocket", "order": 5, "parent_id": None},
    {"id": SUB_DEPLOY, "name": "Deployment Pipeline", "icon": "Upload", "order": 0, "parent_id": CAT_DEVOPS},
    {"id": SUB_GIT, "name": "Git & Rollback", "icon": "GitBranch", "order": 1, "parent_id": CAT_DEVOPS},

    {"id": CAT_SECURITY, "name": "Security", "icon": "Lock", "order": 6, "parent_id": None},
    {"id": SUB_RATELIMIT, "name": "Rate Limiting", "icon": "Gauge", "order": 0, "parent_id": CAT_SECURITY},
    {"id": SUB_ENCRYPTION, "name": "SSL/TLS & Encryption", "icon": "KeyRound", "order": 1, "parent_id": CAT_SECURITY},

    {"id": CAT_DATA, "name": "Data & Storage", "icon": "FolderOpen", "order": 7, "parent_id": None},
    {"id": SUB_SESSION, "name": "Session Lifecycle", "icon": "Timer", "order": 0, "parent_id": CAT_DATA},
    {"id": SUB_ASSETS, "name": "Asset Management", "icon": "Image", "order": 1, "parent_id": CAT_DATA},
    {"id": SUB_DEBUG, "name": "Debug Panel", "icon": "Bug", "order": 2, "parent_id": CAT_DATA},

    {"id": CAT_ADVANCED, "name": "Advanced Concepts", "icon": "Sparkles", "order": 8, "parent_id": None},
    {"id": SUB_RAG, "name": "RAG", "icon": "Search", "order": 0, "parent_id": CAT_ADVANCED},
    {"id": SUB_FRAMEWORKS, "name": "Agent Frameworks", "icon": "Blocks", "order": 1, "parent_id": CAT_ADVANCED},
    {"id": SUB_PROMPT, "name": "Prompt Engineering", "icon": "MessageSquare", "order": 2, "parent_id": CAT_ADVANCED},

    {"id": CAT_FUTURE, "name": "Future of AI Agents", "icon": "Telescope", "order": 9, "parent_id": None},

    {"id": CAT_TESTCASES, "name": "Test Cases", "icon": "Check", "order": 10, "parent_id": None},
    {"id": SUB_TC_AUTH, "name": "Authentication Tests", "icon": "Lock", "order": 0, "parent_id": CAT_TESTCASES},
    {"id": SUB_TC_DOCS, "name": "Document CRUD Tests", "icon": "FileText", "order": 1, "parent_id": CAT_TESTCASES},
    {"id": SUB_TC_SEARCH, "name": "Search & Navigation Tests", "icon": "Search", "order": 2, "parent_id": CAT_TESTCASES},
    {"id": SUB_TC_ADMIN, "name": "Admin & Permissions Tests", "icon": "Lock", "order": 3, "parent_id": CAT_TESTCASES},
    {"id": SUB_TC_EDGE, "name": "Edge Cases & Error Handling", "icon": "Sparkles", "order": 4, "parent_id": CAT_TESTCASES},
    {"id": SUB_TC_PERF, "name": "Performance & Stress Tests", "icon": "Rocket", "order": 5, "parent_id": CAT_TESTCASES},
    {"id": SUB_TC_AGENT, "name": "AI Agent & Orchestration Tests", "icon": "Cpu", "order": 6, "parent_id": CAT_TESTCASES},

    {"id": CAT_TOOLS, "name": "Tools & Resources", "icon": "Sparkles", "order": 11, "parent_id": None},

    {"id": SUB_LLM_PROXY, "name": "LLM Proxy", "icon": "Cpu", "order": 3, "parent_id": CAT_LLM},

    {"id": CAT_LIMITATIONS, "name": "Limitations & Constraints", "icon": "Lock", "order": 12, "parent_id": None},
    {"id": CAT_UI_GUIDE, "name": "UI Guide", "icon": "Monitor", "order": 13, "parent_id": None},
]

DOCUMENTS = [
    # ===== SYSTEM ARCHITECTURE OVERVIEW (new!) =====
    {
        "id": _id(), "title": "System Architecture Overview", "category_id": CAT_PLATFORM, "author_id": SYSTEM_AUTHOR,
        "created_at": NOW, "updated_at": NOW, "order": -1,
        "content": """# System Architecture Overview

A complete map of how the Emergent platform works — every component, every data flow, every service.

## End-to-End Flow

```mermaid
flowchart TD
    U[User] -->|message| FE[Frontend]
    FE -->|WebSocket| AS[Agent Service]
    AS -->|route + store| E1[E1 Orchestrator]
    E1 -->|reason| LLP[LLM Proxy]
    LLP -->|forward| LLM[LLM Provider]
    LLM -->|response| LLP
    LLP -->|tokens| E1
    E1 -->|tools| TE[Tool Engine]
    E1 -->|delegate| SA[Subagent]
    E1 -->|decides| DEC{Next?}
    DEC -->|continue| E1
    DEC -->|done| RESP[Response]
    TE -->|executes| POD[K8s Pod]
    SA -->|spawns LLM| SALLM[Subagent LLM]
    POD -->|result| E1
    SALLM -->|result| E1
    RESP --> FE
    FE -->|displays| U
    AS -->|stores| DB[(MongoDB)]
```

**Diagram Explanation:**

- **User**: The developer typing in the Emergent chat interface
- **Emergent Frontend**: React web app that provides the chat UI, file browser, and preview panel
- **Agent Service**: Python backend that receives messages, manages session state, and routes to E1. It also persists every message to MongoDB
- **E1 Orchestrator**: The core AI agent. NOT an LLM itself — it is a software system that uses an LLM for reasoning but makes its own decisions about what tools to call
- **LLM Proxy**: A reverse proxy that sits between E1 and all LLM providers. It routes requests, tracks token usage, enforces budget limits, and handles failover between providers
- **LLM Provider**: The actual AI model (Claude, GPT, Gemini) that generates text responses
- **Tool Engine**: Executes file operations, bash commands, screenshots, web searches inside the users Kubernetes pod
- **Subagent**: Specialized workers (testing, design, troubleshooting) that E1 delegates tasks to. Each subagent gets its own LLM instance
- **Decision**: After every LLM response, E1 decides whether to call more tools, delegate to a subagent, or send a final response to the user
- **K8s Pod**: The isolated Kubernetes container where the users code lives
- **MongoDB**: Stores everything — chat history, job audits, user data, session state

## Component Roles

| Component | What It Is | What It Does |
|-----------|-----------|-------------|
| **Frontend** | React web app | Chat UI, file browser, preview, code editor |
| **Agent Service** | Python backend | Routes messages, manages sessions, stores history |
| **E1 Orchestrator** | AI agent NOT an LLM | Decides what tools to call, when to delegate, when to respond |
| **LLM Proxy** | Reverse proxy | Routes LLM calls, tracks tokens, enforces budgets, failover |
| **LLM Provider** | Claude GPT Gemini | Generates text responses and reasoning |
| **Tool Execution Engine** | Container runtime | Runs bash, creates files, takes screenshots |
| **Subagents** | Specialist workers | Testing, design, troubleshooting, integration |
| **Kubernetes Pod** | Isolated container | User workspace with filesystem, DB, and services |
| **MongoDB** | Database | Stores everything: users, jobs, chat, metadata |

## Data Flow Diagram

```mermaid
flowchart TB
    subgraph User Layer
        BROWSER[Browser]
    end
    subgraph Frontend
        REACT[React App :3000]
    end
    subgraph Backend
        FASTAPI[FastAPI :8001]
    end
    subgraph Agent Layer
        AGENTSVC[Agent Service]
        E1_INST[E1 Instance]
        LLM_PROXY[LLM Proxy]
    end
    subgraph Storage
        MONGO[(MongoDB)]
        FS[Pod Filesystem]
        GIT[Git Repository]
    end
    subgraph External
        OPENAI[OpenAI]
        ANTHROPIC[Anthropic]
        GOOGLE[Google AI]
    end
    BROWSER --> REACT
    REACT --> FASTAPI
    FASTAPI --> MONGO
    BROWSER --> AGENTSVC
    AGENTSVC --> E1_INST
    AGENTSVC --> MONGO
    E1_INST --> LLM_PROXY
    E1_INST --> FS
    E1_INST --> GIT
    LLM_PROXY --> OPENAI
    LLM_PROXY --> ANTHROPIC
    LLM_PROXY --> GOOGLE
```

**Diagram Explanation:**

- **Browser**: Where the developer accesses Emergent. All interaction starts here
- **React App on port 3000**: The frontend that renders the chat interface, file browser, and preview panel. Communicates with both FastAPI (for the app being built) and Agent Service (for AI chat)
- **FastAPI on port 8001**: The backend server of the app being developed by the agent. E1 writes code here and the user previews it
- **Agent Service**: The orchestration backend. Receives chat messages from the browser via WebSocket, routes them to E1, and stores all history in MongoDB
- **E1 Instance**: A running instance of the E1 orchestrator. One per active job. Makes all decisions about tool calls and subagent delegation
- **LLM Proxy**: Mediates between E1 and external AI providers. Uses the Universal Key to authenticate, counts tokens for billing, and can fail over between OpenAI, Anthropic, and Google if one is down
- **MongoDB**: Central database storing users, sessions, jobs, audit trails, chat history, and metadata
- **Pod Filesystem**: The local filesystem inside the Kubernetes pod where project code lives
- **Git Repository**: Every change is auto-committed for rollback capability
- **OpenAI, Anthropic, Google**: External LLM providers that the proxy routes to based on which model E1 requests

## Database Layer

MongoDB stores ALL platform data:

| Collection | Purpose | Key Fields |
|------------|---------|-----------|
| **users** | User accounts | user_id, email, name, role |
| **user_sessions** | Auth sessions | session_token, user_id, expires_at |
| **jobs** | Agent job records | job_id, user_id, status, created_at |
| **job_audits** | Step-by-step audit trail | job_id, step_type, tool_name, input, output |
| **job_metadata** | Job configuration | job_id, model, system_prompt, tools_available |
| **chat_history** | Conversation messages | job_id, role, content, tool_calls |
| **env_variables** | Per-user ENV config | user_id, key, value |

## Jobs, Audits and Metadata

Every user interaction creates a Job:

- **Job**: A single agent session from user request to completion. Contains status (running, complete, failed), timestamps, and the user who initiated it
- **Job Audit**: Every single action E1 takes is logged. If E1 reads a file, that is an audit entry. If it calls bash, that is an audit entry. If it sends a message to the LLM, that is logged with the full prompt and response. This creates a complete traceable history
- **Job Metadata**: Records which LLM model was used, the version of the system prompt, which tools were available, and any constraints. This allows reproducing or debugging any job
- **Auto-commit**: After every significant file change, the system creates a git commit. This enables the rollback feature where users can revert to any previous state

## ENV and Configuration Tools

E1 can read and write environment variables:

| Tool | What It Does |
|------|-------------|
| **Read ENV** | View current environment variables from .env files |
| **Write ENV** | Set new variables, persisted across restarts |
| **Bash access** | Access env via os.environ in code |

Protected variables like MONGO_URL and REACT_APP_BACKEND_URL are pre-configured and must not be deleted. The frontend reads REACT_APP_BACKEND_URL to know where to send API calls. The backend reads MONGO_URL to connect to the database.

## Complete Tool Registry

| Tool | Category | What It Does |
|------|----------|-------------|
| create_file | File IO | Create new files with content at any path |
| view_file | File IO | Read file contents with line numbers for reference |
| search_replace | File IO | Edit existing files by finding and replacing exact text |
| view_bulk | File IO | Read multiple files at once for efficiency |
| glob_files | File IO | Find files matching patterns like **/*.py |
| insert_text | File IO | Insert new text at a specific line number |
| execute_bash | Execution | Run any shell command with 120 second timeout |
| screenshot_tool | Testing | Take browser screenshots via Playwright for visual verification |
| web_search | Research | Search the internet for documentation or solutions |
| crawl_tool | Research | Fetch and extract content from specific URLs |
| image_selector | Assets | Find stock photos from Unsplash and Pexels |
| image_generation | Assets | Generate custom images using AI models |
| lint_javascript | Quality | Run ESLint to check JavaScript and TypeScript for errors |
| lint_python | Quality | Run Ruff linter to check Python code for errors |
| analyze_file | Analysis | Use AI to analyze complex files for patterns and insights |
| extract_file | Analysis | Extract structured data from documents, images, or audio |
| ask_human | Interaction | Pause and ask the user for clarification or approval |

## Subagent Registry

| Subagent | Specialty | When E1 Delegates To It |
|----------|-----------|------------------------|
| testing_agent | QA and automated testing | After implementing features, to verify they work correctly with Playwright and API tests |
| design_agent | UI and UX design guidelines | When the user needs a polished frontend design, generates design_guidelines.json |
| troubleshoot_agent | Root cause analysis | When E1 is stuck in an error loop after 2+ failed attempts, provides fresh diagnostic perspective |
| integration_playbook | Third party API integration | When user needs Stripe, OpenAI, SendGrid etc. Provides verified step-by-step playbooks |
| expert_opinion | Architecture and code review | For complex design decisions, provides expert analysis of trade-offs |
| deployment_agent | Deployment debugging | When deployed app has issues, checks env vars, ports, and disk usage |
| support_agent | Platform help and queries | For questions about Emergent features, billing, GitHub integration, rollback etc. |

## Request Routing

All requests flow through Kubernetes Ingress:

| URL Pattern | Routes To | Purpose |
|------------|-----------|---------|
| /api/* | FastAPI on port 8001 | Backend API calls for the app being built |
| /* | React on port 3000 | Frontend pages of the app being built |
| WebSocket | Agent Service | Real time chat between user and E1 |

## The Orchestration Loop

E1 operates in a continuous loop until the task is complete:

1. **Receive** — Get user message or tool result
2. **Think** — Send full context (system prompt + history + tool results) to the LLM for reasoning
3. **Decide** — Parse the LLM response. If it contains tool calls, execute them. If it contains a subagent request, delegate. If it is a text response, send to user
4. **Act** — Execute the decided action (run bash, create file, call subagent)
5. **Log** — Record every action in the job audit trail with timestamps and full input/output
6. **Repeat** — If there is more work to do, go back to step 1 with the new context

## Key Architectural Principles

- **E1 is the orchestrator not an LLM.** It uses an LLM as its reasoning engine but E1 itself is the decision-making agent layer that chooses tools and manages workflow
- **LLMs are stateless.** The Agent Service maintains all conversation history and feeds it back with every call. The LLM has no memory between calls
- **Subagents are independent.** They have no memory of previous calls. E1 provides full context each time it delegates
- **Everything is containerized.** Each user gets an isolated Kubernetes pod with its own filesystem database and services. No user can access another users data
- **Auto-commit everything.** Every action creates a git checkpoint for rollback capability. Users can revert to any previous state for free
- **LLM Proxy mediates all AI calls.** Universal Key, cost tracking, rate limiting, and failover are all handled transparently by the proxy layer
- **MongoDB is the source of truth.** Jobs, audits, chat history, metadata, and user data all persist in MongoDB. Nothing is stored only in memory
"""

    },

    # ===== E1 ORCHESTRATOR =====
    {
        "id": _id(), "title": "What Is E1?", "category_id": SUB_E1, "author_id": SYSTEM_AUTHOR,
        "created_at": NOW, "updated_at": NOW, "order": 0,
        "content": """# What Is E1?

E1 is **not an LLM**. E1 is an **AI Agent** — a software orchestration system built by Emergent Labs that uses an LLM as one of its components. The distinction is critical.

## E1 vs an LLM

An LLM (like Claude or GPT) is a stateless text prediction model. Given input, it produces output. It cannot run code, read files, remember conversations, or take actions in the real world.

E1 is the **orchestration layer** that wraps around an LLM and gives it the ability to act:

```mermaid
flowchart TD
    subgraph E1["E1 (The Orchestrator)"]
        SP[System Prompt<br/>Rules & Workflow]
        TR[Tool Registry<br/>Available Actions]
        SR[Subagent Registry<br/>Specialist Workers]
        DL[Decision Layer<br/>What to do next]
        LLM_INT[LLM Engine<br/>Reasoning Only]
    end
    DL --> LLM_INT
    LLM_INT --> DL
    DL -->|invoke| TR
    DL -->|delegate| SR
    SP -->|governs| DL
```

**Flow Explanation — What is inside E1:**

- **What:** This diagram shows the internal architecture of E1 — it is NOT a single LLM but a multi-component software system
- **System Prompt (SP):** A massive set of rules and instructions (~15,000+ tokens) that governs E1's behavior. It defines coding guidelines, testing rules, tool usage patterns, and platform constraints. It tells E1 WHEN to ask the user, WHEN to use tools, and HOW to structure responses
- **Tool Registry (TR):** A catalog of all available tools (create_file, execute_bash, screenshot_tool, etc.). When E1 decides to act, it picks from this registry. Each tool has a defined schema (name, parameters, description) that the LLM uses to generate structured calls
- **Subagent Registry (SR):** A list of specialized agents (testing, design, troubleshoot, integration). E1 delegates to these when a task requires specialized expertise. Each subagent has its own LLM instance and tools
- **Decision Layer (DL):** The core logic loop. After every LLM response, the decision layer parses the output. If the LLM outputs a tool call, the decision layer routes it to the Tool Registry. If it outputs a subagent delegation, it routes to the Subagent Registry. If it outputs text, it sends it to the user
- **LLM Engine:** The actual language model (Claude Sonnet, GPT-5.2, etc.) used ONLY for reasoning. It receives the full context (system prompt + conversation history + tool results) and generates a response. It has no state between calls — the Decision Layer manages all state
- **Why this architecture?** Because LLMs alone cannot act. They can only generate text. E1 wraps the LLM with action capabilities, state management, and decision logic. This is what makes E1 an agent, not just a chatbot

| | LLM (Claude/GPT) | E1 (The Agent) |
|---|---|---|
| **Nature** | A model that generates text | A software system that acts |
| **Can run code?** | No | Yes, via tools |
| **Can read files?** | No | Yes, via tools |
| **Can call APIs?** | No | Yes, via subagents |
| **Has memory?** | No (stateless) | Yes (via Agent Service) |
| **Makes decisions?** | Generates suggestions | Actually picks and executes actions |
| **Has rules?** | Only what's in its prompt | Full system prompt + tool definitions |

## How E1 Makes Decisions

E1 follows a structured decision-making process governed by its system prompt:

```mermaid
flowchart TD
    MSG[User Message Received] --> FIRST{First message?}
    FIRST -->|Yes| ASK[Call ask_human<br/>Clarify requirements]
    FIRST -->|No| TYPE{What type of request?}
    TYPE -->|Platform question| SUPPORT[Delegate to support_agent]
    TYPE -->|New app| BUILD[Explore → Design → Build → Test]
    TYPE -->|Bug fix| DEBUG[Reproduce → Investigate → Fix → Test]
    TYPE -->|Existing code| MODIFY[Understand → Modify → Test]
    BUILD --> FINISH[Call finish with summary]
    DEBUG --> FINISH
    MODIFY --> FINISH
```

**Flow Explanation — E1 Decision Making:**

- **What:** This diagram shows exactly how E1 decides what to do when it receives a user message
- **First message check:** On the very FIRST message of a session, E1 MUST call ask_human to clarify requirements before doing anything else. This is a hard rule in the system prompt. Why? Because ambiguous instructions lead to wasted work and tokens
- **Platform question path:** If the user asks about Emergent capabilities (e.g., "Can I deploy to Vercel?"), E1 delegates to support_agent rather than trying to answer itself. Why? Because support_agent has specific knowledge about platform features, billing, and capabilities that E1 might get wrong
- **New app path (Explore, Design, Build, Test):** For new applications, E1 follows a strict sequence: (1) Explore the existing codebase if any, (2) Call design_agent for UI/UX guidelines if frontend is involved, (3) Build the code using tools, (4) Call testing_agent to verify. Each step must complete before the next begins
- **Bug fix path (Reproduce, Investigate, Fix, Test):** For bugs, E1 first reproduces the issue (runs the code, checks logs), then investigates (reads relevant files, checks git log for recent changes), then applies a fix, then tests. If stuck after 2+ attempts, E1 escalates to troubleshoot_agent
- **Modify path (Understand, Modify, Test):** For modifications to existing code, E1 reads the relevant files first (never edits blind), makes targeted changes using search_replace (not create_file with overwrite), then tests
- **Finish:** Every completed task ends with the finish tool, which provides a summary of what was done, what to test, and next steps
"""
    },

    # ===== AGENTS & SUBAGENTS =====
    {
        "id": _id(), "title": "The Subagent System", "category_id": SUB_AGENTS, "author_id": SYSTEM_AUTHOR,
        "created_at": NOW, "updated_at": NOW, "order": 0,
        "content": """# The Subagent System

## What Are Subagents?

Subagents are specialized AI agents that E1 delegates work to. Each has its own system prompt, LLM instance, and tools. They operate independently — E1 spawns them, they do their job, and return results.

```mermaid
flowchart TD
    E1[E1 Orchestrator] -->|"Test the app"| TA[Testing Agent]
    E1 -->|"Design the UI"| DA[Design Agent]
    E1 -->|"How to integrate Stripe?"| IA[Integration Expert]
    E1 -->|"Why is this crashing?"| TRA[Troubleshoot Agent]
    E1 -->|"Platform question"| SA[Support Agent]
    E1 -->|"Ready to deploy?"| DEP[Deployment Agent]
    TA -->|test report + git diff| E1
    DA -->|design_guidelines.json| E1
    IA -->|integration playbook| E1
    TRA -->|root cause + fix| E1
    SA -->|answer| E1
    DEP -->|validation report| E1
```

**Flow Explanation — Subagent Delegation:**

- **What:** This diagram shows every subagent E1 can delegate to and what each returns
- **When does E1 delegate?** E1 delegates when a task requires specialized expertise that is better handled by a focused agent with its own system prompt and tools
- **Testing Agent:** Called AFTER E1 implements features or fixes bugs. E1 sends the full problem statement, list of features to test, file references, and credentials. The testing agent writes and runs automated tests (Playwright for frontend, pytest for backend, curl for APIs), then returns a JSON test report at /app/test_reports/iteration_N.json plus any git diff of fixes it made. E1 MUST read this report and fix all issues before finishing
- **Design Agent:** Called BEFORE building UI. E1 sends the app type, target audience, and functionality list. The design agent returns design_guidelines.json with color palette, typography, spacing rules, and component styles. E1 follows these guidelines when writing frontend code
- **Integration Expert:** Called when the user needs third-party services (Stripe, OpenAI, SendGrid, etc.). Returns a verified playbook with exact code, required API keys, and setup steps. E1 MUST use this playbook rather than its own knowledge, because SDK versions change frequently
- **Troubleshoot Agent:** Called after E1 fails to fix a bug after 2+ attempts. Has READ-ONLY access to the codebase. Performs systematic root cause analysis in 10 steps or less. Returns diagnosis and recommended fixes that E1 then implements
- **Support Agent:** Called for platform questions (billing, GitHub, deployment capabilities). Returns accurate platform information. E1 passes the response directly to the user without modification
- **Deployment Agent:** Called when deployment fails. Checks for hardcoded env variables, port conflicts, disk issues, and reviews deployed app logs

## Subagent Details

| Subagent | When Invoked | Has Own Tools? | Returns |
|----------|-------------|----------------|---------|
| **Testing Agent** | After feature implementation | Yes (Playwright, curl, bash) | Test report JSON + git diff |
| **Design Agent** | Before building UI | Yes (image tools) | design_guidelines.json |
| **Integration Expert** | When 3rd party services needed | Yes (web search) | Integration playbook |
| **Troubleshoot Agent** | After 2+ failed fix attempts | Read-only access | Root cause + recommendations |
| **Support Agent** | For platform/capability questions | Limited | Text answer |
| **Deployment Agent** | Before/during deployment | Yes (log access) | Validation report |

## The Handoff Protocol

Subagents are **completely stateless**. They start fresh every time. E1 must package all relevant context into a single task description:

```mermaid
sequenceDiagram
    participant E1 as E1 Orchestrator
    participant AS as Agent Service
    participant SA as Subagent (e.g., Testing)
    E1->>AS: Call testing_agent with full context
    AS->>SA: Create new session + task
    SA->>SA: Own LLM + Own tools
    SA->>SA: Execute tests, take screenshots
    SA->>AS: Return results + test report
    AS->>E1: Results + git diff
    E1->>E1: Read report, fix bugs if needed
```

**Flow Explanation — The Handoff Protocol:**

- **What:** This sequence diagram shows the exact communication flow when E1 delegates to a subagent
- **Step 1 — E1 packages context:** E1 creates a detailed task description containing: the original problem statement, what has been implemented so far, file paths to reference, credentials needed, and what specifically to test or analyze. This is critical because subagents have ZERO memory of previous calls
- **Step 2 — Agent Service creates a session:** The Agent Service spawns a new, independent session for the subagent. This session has its own LLM instance, its own system prompt, and its own tool access. The subagent cannot see E1's conversation history
- **Step 3 — Subagent works independently:** The subagent uses its own LLM and tools to complete the task. For example, the testing agent writes test scripts, runs them via Playwright/pytest, captures screenshots, and fixes simple issues it finds
- **Step 4 — Results returned:** The subagent returns structured results (e.g., test report JSON) plus a git diff of any code changes it made. E1 receives both
- **Step 5 — E1 processes results:** E1 reads the test report, checks what the subagent changed (via git diff), and decides next steps. If tests failed, E1 fixes the bugs. If the subagent changed code, E1 reviews those changes
- **Why stateless?** Each subagent call is independent because subagents are specialized. They do one job well and return results. They don't need context from previous calls — E1 provides everything they need each time. This also means if E1 calls the same subagent twice, it must re-provide all context including what the first call already covered
"""
    },

    # ===== TOOLS & EXECUTION =====
    {
        "id": _id(), "title": "Tool Execution Engine", "category_id": SUB_TOOLS, "author_id": SYSTEM_AUTHOR,
        "created_at": NOW, "updated_at": NOW, "order": 0,
        "content": """# Tool Execution Engine

## What Are Tools?

Tools give E1 the ability to interact with the real world. The LLM inside E1 can only generate text — tools convert those text outputs into actual actions.

## Tool Execution Flow

```mermaid
flowchart TD
    E1[E1 decides to use a tool] -->|structured JSON| VAL[Agent Service validates]
    VAL -->|valid| ROUTE{Route by type}
    ROUTE -->|bash, files| CONT[Execute in Container]
    ROUTE -->|web search, crawl| EXT[External API]
    ROUTE -->|subagent| SPAWN[Spawn Subagent Session]
    CONT -->|result| STORE[Store in conversation DB]
    EXT -->|result| STORE
    SPAWN -->|result| STORE
    STORE -->|feed back| E1_2[E1 processes result]
    E1_2 -->|decides next| E1
```

**Flow Explanation — Tool Execution Flow:**

- **What:** This diagram shows exactly how a tool call travels from E1's decision to actual execution and back
- **Step 1 — E1 decides:** During the orchestration loop, the LLM generates a structured JSON tool call (e.g., `{"tool": "execute_bash", "command": "pip install flask"}`). E1's decision layer parses this from the LLM response
- **Step 2 — Validation:** The Agent Service validates the tool call against the tool registry. It checks that the tool exists, required parameters are present, and the call is well-formed. Invalid calls are rejected with an error message fed back to the LLM
- **Step 3 — Routing:** Valid calls are routed by type. Container tools (bash, file ops, screenshots) execute inside the user's Kubernetes pod. External API tools (web search, crawl) call external services. Subagent calls spawn new agent sessions
- **Step 4 — Execution:** The tool runs. Bash commands have a 120-second timeout for foreground execution. File operations are immediate. Screenshots launch a headless Chromium browser via Playwright. Web searches query search APIs
- **Step 5 — Storage:** Every tool result (stdout, stderr, exit code, file contents, screenshots) is stored in the conversation database. This creates the audit trail and ensures results persist if the session is interrupted
- **Step 6 — Feedback:** Results are fed back to E1 as part of the conversation context. The LLM sees the tool result and decides what to do next — call another tool, fix an error, or respond to the user
- **Why this matters:** This loop is how E1 actually builds software. Each iteration — think, act, observe — gets E1 closer to completing the task. A simple "create a todo app" might involve 50+ tool calls in this loop

## Available Tools

| Tool | Type | Purpose |
|------|------|---------|
| `execute_bash` | Container | Run shell commands |
| `create_file` | Container | Create new files |
| `search_replace` | Container | Edit existing files |
| `view_file` / `view_bulk` | Container | Read file contents |
| `glob_files` | Container | Find files by pattern |
| `web_search` | External API | Search the internet |
| `crawl_tool` | External API | Scrape web content |
| `screenshot_tool` | Container | Take webpage screenshots via Playwright |
| `lint_python` / `lint_javascript` | Container | Code quality checks |
| `analyze_file_tool` | External AI | AI-powered document analysis |

## Parallel vs Sequential Execution

```mermaid
flowchart LR
    subgraph Parallel["Safe to Parallelize"]
        F1[Create server.py]
        F2[Create App.js]
        F3[Create App.css]
    end
    subgraph Sequential["Must Be Sequential"]
        S1[Install package] --> S2[Import in code]
        S3[Edit .env] --> S4[Restart service]
    end
```

**Flow Explanation — Parallel vs Sequential:**

- **What:** This shows which tool operations E1 can safely run simultaneously vs which must wait for each other
- **Parallel (safe):** Creating multiple independent files (server.py, App.js, App.css) can happen in parallel because they don't depend on each other. Reading multiple files, running independent linters, or making independent API calls can also be parallelized. E1 is instructed to maximize parallel execution for speed
- **Sequential (must wait):** Installing a package MUST complete before importing it in code. Editing a .env file MUST complete before restarting the service that reads it. Creating a database table MUST complete before inserting data. E1 chains these with && in bash or waits for each tool call to complete before the next
- **Why this matters:** Parallel execution significantly speeds up development. If E1 needs to create 5 files, doing it in parallel takes 1 tool call round-trip instead of 5. But getting dependencies wrong (e.g., importing before installing) causes errors that waste time debugging
"""
    },

    # ===== LLM: TRANSFORMER =====
    {
        "id": _id(), "title": "How Transformers Work", "category_id": SUB_TRANSFORMER, "author_id": SYSTEM_AUTHOR,
        "created_at": NOW, "updated_at": NOW, "order": 0,
        "content": """# How Transformers Work

## The Pipeline

An LLM is a neural network that predicts the next token given all previous tokens.

```mermaid
flowchart LR
    A[Input Text] --> B[Tokenizer]
    B --> C[Embedding Layer]
    C --> D[Transformer Blocks x96]
    D --> E[Output Layer]
    E --> F[Next Token Probabilities]
    F --> G[Sampling]
    G --> H[Generated Token]
```

**Flow Explanation — The Transformer Pipeline:**

- **What:** This shows how text becomes a prediction, step by step, inside an LLM
- **Input Text:** The raw prompt — e.g., "Write a Python function that sorts a list." This includes the ENTIRE conversation history plus system prompt, not just the latest message
- **Tokenizer:** Splits text into subword tokens using a fixed vocabulary (~50K-100K tokens). "Hello world" becomes [464, 3797]. Each token is an integer ID. This is deterministic — the same text always produces the same tokens
- **Embedding Layer:** Converts each token ID into a dense vector (e.g., 4096 dimensions). Also adds positional encoding so the model knows token order (token 1 vs token 100). Without position encoding, the model would treat the input as a bag of words
- **Transformer Blocks (x96):** The core of the model. Each block has multi-head self-attention (tokens attend to each other to understand relationships) and a feed-forward network (where factual knowledge is stored as weights). Large models like Claude or GPT-4 have 96+ layers. Each layer refines the representation
- **Output Layer:** Maps the final hidden states to a probability distribution over all tokens in the vocabulary. E.g., after "The capital of France is", the token "Paris" has the highest probability
- **Sampling:** Selects the next token from the probability distribution. Temperature controls randomness (0 = always pick the most likely, 1.5 = more creative). Top-P and Top-K further constrain which tokens are considered
- **Generated Token:** The selected token is appended to the input, and the entire process repeats for the next token. This is called autoregressive generation — each token depends on all previous tokens

## Key Stages

### 1. Tokenization
Text is split into tokens (subwords). `"Hello world"` becomes `[464, 3797]`. Vocabulary is ~50,000-100,000 tokens. Rough rule: 1 token = ~4 characters.

### 2. Embedding + Positional Encoding
Each token maps to a dense vector (e.g., 4096 dimensions). Position encoding is added so the model knows token order.

### 3. Multi-Head Self-Attention
The core innovation. Each token computes how much to "attend" to every other token. Multiple heads capture different relationship types (syntax, semantics, position).

### 4. Feed-Forward Network
Each token processed through linear transformations. This is where factual knowledge is stored.

### 5. Output
Final hidden states map to a probability distribution over all tokens. Sampling selects the next token.

## Key Parameters

| Parameter | Controls | Example |
|-----------|----------|---------|
| **Temperature** | Randomness | 0=deterministic, 1.5=creative |
| **Top-P** | Probability cutoff | 0.9=consider top 90% likely tokens |
| **Top-K** | Candidate count | 50=only pick from top 50 tokens |
| **Max Tokens** | Response length | 4096=max output tokens |

## Multimodal LLMs

Modern LLMs can process images too. A Vision Encoder splits images into patches, converts to vectors, and feeds them alongside text tokens into the same transformer architecture.
"""
    },

    # ===== LLM: TRAINING =====
    {
        "id": _id(), "title": "LLM Training Stages", "category_id": SUB_TRAINING, "author_id": SYSTEM_AUTHOR,
        "created_at": NOW, "updated_at": NOW, "order": 0,
        "content": """# LLM Training Stages

## The Four Phases

```mermaid
flowchart TD
    P1["Phase 1: Pre-Training<br/>Trillions of tokens, next-token prediction<br/>Cost: $10M-$100M+"] --> P2["Phase 2: Instruction Tuning<br/>Human-curated Q&A pairs<br/>Learn to follow instructions"]
    P2 --> P3["Phase 3: RLHF / RLAIF<br/>Human or AI feedback<br/>Alignment: helpful, harmless, honest"]
    P3 --> P4["Phase 4: Tool Use Training<br/>Structured function calling<br/>JSON schema outputs"]
    P4 --> RESULT[Production Model]
```

**Flow Explanation — The Four Training Phases:**

- **What:** This shows the complete journey from raw neural network to production-ready LLM
- **Phase 1 — Pre-Training:** The model processes trillions of tokens from the internet (books, code, Wikipedia, forums). Objective: predict the next token. This is unsupervised — no human labels required. Takes months on thousands of GPUs. Cost: $10M-$100M+. Result: a base model that understands language patterns but is raw, unaligned, and may produce toxic or unhelpful output. Why so expensive? Because the model must see enough data to learn grammar, facts, reasoning patterns, and code structure
- **Phase 2 — Instruction Tuning:** Human annotators create thousands to millions of instruction-response pairs (e.g., "Summarize this article" → [good summary]). The model is fine-tuned on these. Result: a model that can follow instructions and format output properly. Without this phase, the base model would just autocomplete text rather than answer questions
- **Phase 3 — RLHF/RLAIF:** Reinforcement Learning from Human (or AI) Feedback. Humans rate model outputs as helpful/harmful/honest. A reward model is trained on these ratings. The LLM is then fine-tuned using reinforcement learning to maximize the reward. RLAIF uses AI judges instead of humans for scale. Result: a model that is helpful, harmless, and honest. This is what prevents the model from generating harmful content
- **Phase 4 — Tool Use Training:** Specific to agent-capable models. The model is trained on examples of structured function calls, JSON schemas, and multi-turn tool conversations. Result: a model that can output structured tool calls (e.g., `create_file(path="/app/server.py", content="...")`) instead of just text. This is what makes E1 possible — without this training, the LLM couldn't generate the structured JSON that E1's tool execution engine needs

### Phase 1: Pre-Training
Data from the entire internet — books, code, Wikipedia, documentation. Objective: predict the next token. Requires thousands of GPUs for months. Result: a base model that knows language but is raw and unaligned.

### Phase 2: Instruction Tuning
Human-curated instruction-response pairs teach the model to follow directions. Thousands to millions of examples. Result: model that can have conversations and format output.

### Phase 3: RLHF / RLAIF
**RLHF**: Humans rate outputs, train a reward model, fine-tune with reinforcement learning.
**RLAIF**: AI judges rate outputs — cheaper and more scalable.
Result: helpful, harmless, honest model.

### Phase 4: Tool Use Training
Specific to agent-capable models. Trained on examples of structured tool calls, JSON schemas, and multi-turn tool conversations. Result: model that can output structured function calls instead of just text.
"""
    },

    # ===== TOKENS & FUNCTION CALLING =====
    {
        "id": _id(), "title": "Token Economics & Billing", "category_id": SUB_TOKENS, "author_id": SYSTEM_AUTHOR,
        "created_at": NOW, "updated_at": NOW, "order": 0,
        "content": """# Token Economics & Billing

## What Are Tokens?

Tokens are chunks of text — roughly 4 characters or 0.75 words each. Both input and output tokens cost money.

## Why Costs Grow Over Time

The entire conversation history is sent with every LLM call. As the conversation grows, each call becomes more expensive:

| Message # | Approx Input Tokens | Relative Cost |
|-----------|-------------------|---------------|
| 1 | ~15K | 1x |
| 10 | ~60K | 4x |
| 20 | ~130K | 8.6x |
| 30 | ~190K | 12.6x |

## The Hidden Multiplier

One user message triggers **multiple** LLM calls (the tool loop). Plus each subagent call triggers its own LLM calls. A single "Build me a todo app" can consume 300-350K tokens total.

## Universal Key

Emergent's Universal Key works across OpenAI, Anthropic, and Google through a proxy:

```mermaid
flowchart LR
    APP[Your App] -->|universal key| PROXY[Emergent Proxy]
    PROXY -->|"model=gpt-5.2"| OAI[OpenAI]
    PROXY -->|"model=claude-sonnet"| ANT[Anthropic]
    PROXY -->|"model=gemini-flash"| GOO[Google]
    PROXY -->|deduct balance| BAL[(Your Balance)]
```

**Flow Explanation — Universal Key Flow:**

- **What:** This shows how one API key (the Universal Key) works across multiple AI providers
- **Your App:** Any code that needs LLM capabilities — your backend calling OpenAI for text generation, your app generating images, or E1 itself making LLM calls during development
- **Emergent Proxy:** A reverse proxy operated by Emergent that intercepts all LLM API calls. It authenticates using your Universal Key (sk-emergent-xxx), routes the request to the correct provider based on the model parameter, tracks token usage for billing, and handles failover if a provider is down
- **Provider Routing:** The proxy reads the model parameter. "gpt-5.2" routes to OpenAI. "claude-sonnet-4-5" routes to Anthropic. "gemini-3-flash" routes to Google. Your code uses the same SDK and key regardless of provider
- **Balance Deduction:** After each successful call, the proxy calculates the cost (input tokens x rate + output tokens x rate) and deducts from your balance. Different models have different per-token rates. You can view detailed usage breakdown in Profile > Universal Key
- **Why this exists:** Without the Universal Key, you would need separate API keys and billing accounts for each provider. The Universal Key simplifies this to one key, one balance. It also enables E1 to seamlessly switch between providers when needed
"""
    },

    # ===== KUBERNETES =====
    {
        "id": _id(), "title": "Kubernetes & Container Orchestration", "category_id": SUB_K8S, "author_id": SYSTEM_AUTHOR,
        "created_at": NOW, "updated_at": NOW, "order": 0,
        "content": """# Kubernetes & Container Orchestration

## Core Concepts

| Concept | Description |
|---------|-------------|
| **Pod** | Smallest unit. Your workspace = 1 pod |
| **Deployment** | Manages replica sets of identical pods |
| **Service** | Stable network endpoint for pods |
| **Ingress** | HTTP routing rules — the front door |
| **Secret** | Encrypted sensitive data |
| **PersistentVolume** | Storage that survives pod restarts |
| **Namespace** | Virtual cluster for user isolation |

## Ingress Routing

```mermaid
flowchart TD
    REQ[Browser Request] --> ING[Ingress Controller]
    ING -->|"path: /api/*"| BE["Backend :8001<br/>FastAPI"]
    ING -->|"path: /*"| FE["Frontend :3000<br/>React Dev Server"]
```

**Flow Explanation — Ingress Routing:**

- **What:** This shows how HTTP requests from the browser reach the correct service inside the Kubernetes pod
- **Browser Request:** Any request from the user's browser — viewing the app, calling an API, loading a CSS file
- **Ingress Controller:** The Kubernetes ingress acts as a reverse proxy. It examines the URL path of every incoming request and routes it to the correct internal service
- **Path /api/_ routes to Backend (port 8001):** Any URL starting with /api/ is forwarded to the FastAPI server running on port 8001 inside the pod. This is why every backend route MUST be prefixed with /api. Without it, the request hits the frontend instead, which returns HTML instead of JSON, causing confusing errors
- **Path /_ (everything else) routes to Frontend (port 3000):** All other requests go to the React development server on port 3000. This serves HTML pages, JavaScript bundles, CSS files, and static assets
- **Why this matters for developers:** This is the #1 source of routing bugs. If you define a backend route as `/users` instead of `/api/users`, the ingress sends it to React, which returns its index.html. The browser gets HTML when it expected JSON, causing parse errors. Always prefix backend routes with `/api`

## Multi-User Isolation

```mermaid
flowchart LR
    subgraph NS_A["User A Namespace"]
        POD_A["Pod A<br/>Backend + Frontend + MongoDB"]
    end
    subgraph NS_B["User B Namespace"]
        POD_B["Pod B<br/>Backend + Frontend + MongoDB"]
    end
    POD_A -.-|"NO ACCESS"| POD_B
```

**Flow Explanation — Multi-User Isolation:**

- **What:** This shows how Kubernetes isolates users from each other
- **User A Namespace:** Each user's workspace is deployed in its own Kubernetes namespace. A namespace is a virtual cluster boundary. Inside it, User A has their own pod containing a backend (FastAPI), frontend (React), and MongoDB instance
- **User B Namespace:** Completely separate namespace with its own pod and services. User B's data, code, environment variables, and database are entirely independent of User A
- **NO ACCESS:** Kubernetes network policies enforce that pods in different namespaces cannot communicate. User A cannot access User B's database, filesystem, or services. This is enforced at the network level, not just application level
- **Why this architecture:** Multi-tenant isolation is critical for a development platform. Users write and run arbitrary code. Without isolation, one user's buggy code could crash another user's services, or a malicious user could read another user's API keys
"""
    },

    # ===== DOCKER =====
    {
        "id": _id(), "title": "Docker & Container Fundamentals", "category_id": SUB_DOCKER, "author_id": SYSTEM_AUTHOR,
        "created_at": NOW, "updated_at": NOW, "order": 0,
        "content": """# Docker & Container Fundamentals

## Containers vs VMs

| Aspect | Virtual Machine | Container |
|--------|----------------|-----------|
| OS | Full OS with own kernel | Shares host kernel |
| Size | Gigabytes | Megabytes |
| Startup | Minutes | Seconds |
| Isolation | Hardware-level | Process-level |

## How Containers Work

Three Linux kernel features:
- **Namespaces**: PID, Network, Mount, User — each container thinks it's alone
- **Cgroups**: CPU, memory, I/O limits — prevents resource hogging
- **Overlay Filesystem**: Layered, shared base images — efficient storage

## Image Layers

```mermaid
flowchart BT
    L1["Layer 1: Ubuntu base<br/>(shared across containers)"] --> L2["Layer 2: Python 3.11<br/>(shared across Python apps)"]
    L2 --> L3["Layer 3: pip packages<br/>(requirements.txt)"]
    L3 --> L4["Layer 4: Your code<br/>(your application)"]
    L4 --> L5["Layer 5: Runtime<br/>(writable, container-specific)"]
```

**Flow Explanation — Docker Image Layers:**

- **What:** This shows how Docker images are built as a stack of layers, from bottom to top
- **Layer 1 (Ubuntu base):** The OS foundation. Shared across ALL containers that use Ubuntu. Downloaded once and cached. This is why Docker images are much smaller than VMs — multiple containers share this layer
- **Layer 2 (Python 3.11):** The runtime. Shared across all Python applications. Adding Python on top of Ubuntu creates a new layer without duplicating the Ubuntu layer
- **Layer 3 (pip packages):** Your dependencies from requirements.txt. This layer changes whenever you add or update a package. Docker caches this layer, so if requirements.txt hasn't changed, it skips rebuilding
- **Layer 4 (Your code):** Your application files. This changes frequently (every code edit). Because it's a separate layer, changing code only rebuilds this layer and above — not the entire image
- **Layer 5 (Runtime):** The writable layer that exists only during container execution. Log files, temp data, runtime state go here. This layer is destroyed when the container stops
- **Why layers matter:** Efficient rebuilds. If you only change your code (Layer 4), Docker reuses Layers 1-3 from cache. A rebuild that would take 10 minutes without layers takes 5 seconds with layers
"""
    },

    # ===== SUPERVISOR =====
    {
        "id": _id(), "title": "Hot Reload & Process Management", "category_id": SUB_SUPERVISOR, "author_id": SYSTEM_AUTHOR,
        "created_at": NOW, "updated_at": NOW, "order": 0,
        "content": """# Hot Reload & Process Management

## Supervisor

A process manager that starts services on boot, auto-restarts on crash, and manages logs.

## Hot Reload Flow

```mermaid
flowchart TD
    EDIT[E1 edits server.py] --> DETECT[File watcher detects change]
    DETECT -->|Backend| UV[uvicorn reloads Python modules<br/>~1-3 seconds]
    DETECT -->|Frontend| WP[Webpack recompiles module<br/>HMR swaps in browser<br/>~200ms-2s]
    UV --> LIVE1[New backend code live]
    WP --> LIVE2[New frontend code live<br/>State preserved]
```

**Flow Explanation — Hot Reload:**

- **What:** This shows how code changes become live without manually restarting services
- **E1 edits server.py:** When E1 uses create_file or search_replace to modify a Python or JavaScript file, the change is written to disk immediately
- **File watcher detects change:** Both the backend (uvicorn with WatchFiles) and frontend (webpack with HMR) have file watchers that monitor the filesystem for changes
- **Backend reload (uvicorn):** When a .py file changes, uvicorn detects it, stops the current Python process, re-imports all modules, and starts a new process. Takes 1-3 seconds. All in-memory state is lost (database state persists in MongoDB)
- **Frontend reload (Webpack HMR):** When a .js/.jsx/.css file changes, webpack recompiles only the changed module, sends it to the browser via WebSocket, and the browser hot-swaps the module WITHOUT a full page reload. React component state is preserved. Takes 200ms-2 seconds
- **Why this matters:** Hot reload means E1 doesn't need to restart services after every code change. This saves significant time during development. However, .env changes and new package installations DO require a manual restart via `sudo supervisorctl restart backend/frontend`

## When Restart IS Needed

| Change Type | Hot Reload Handles? | Manual Restart? |
|-------------|-------------------|-----------------|
| `.py` / `.js` code changes | Yes | No |
| CSS changes | Yes | No |
| `.env` file changes | No | **Yes** |
| New package installs | No | **Yes** |
| Config file changes | No | **Yes** |

```bash
sudo supervisorctl status           # Check all services
sudo supervisorctl restart backend  # Restart backend only
sudo supervisorctl restart frontend # Restart frontend only
```
"""
    },

    # ===== REACT =====
    {
        "id": _id(), "title": "React Virtual DOM & Hooks", "category_id": SUB_REACT, "author_id": SYSTEM_AUTHOR,
        "created_at": NOW, "updated_at": NOW, "order": 0,
        "content": """# React Virtual DOM & Hooks

## Reconciliation

```mermaid
flowchart LR
    SC[State Change] --> VDOM[New Virtual DOM]
    VDOM --> DIFF[Diff old vs new]
    DIFF --> MIN[Minimal update list]
    MIN --> REAL[Apply to Real DOM]
    REAL --> RENDER[Browser renders]
```

**Flow Explanation — React Reconciliation:**

- **What:** This shows how React efficiently updates the browser's DOM by comparing virtual DOMs
- **State Change:** Something triggers a re-render — user clicks a button, API data arrives, a timer fires. React creates a new Virtual DOM (a lightweight JavaScript object tree)
- **Diff:** React compares the new Virtual DOM with the previous one. It uses a heuristic O(n) algorithm that checks node types and keys. Different type = destroy and rebuild. Same type = update props only
- **Minimal update list:** The diff produces only the changes needed. If you update 1 item in a list of 100, React identifies that only 1 DOM node needs updating, not all 100
- **Apply to Real DOM:** React batches all changes and applies them in a single DOM update. This avoids the expensive reflow-repaint cycle for each individual change
- **Why this matters:** Direct DOM manipulation is slow. React's virtual DOM acts as a buffer, accumulating changes and applying them in the most efficient way possible. 100 state changes might result in only 3 real DOM updates

## Key Hooks

- **useState**: Component state, re-renders on change
- **useEffect**: Side effects (API calls, subscriptions), runs after render
- **useContext**: Shared state without prop drilling
- **useMemo**: Cache expensive calculations
- **useCallback**: Cache function references, prevent child re-renders
- **useRef**: Mutable reference, DOM access

## Component Lifecycle

**Mounting**: initialization → render → DOM update → useEffect (once)

**Updating**: setState/new props → render → diff → DOM update → useEffect (if deps changed)

**Unmounting**: useEffect cleanup → component removed
"""
    },

    # ===== BROWSER =====
    {
        "id": _id(), "title": "Browser Rendering & Network", "category_id": SUB_BROWSER, "author_id": SYSTEM_AUTHOR,
        "created_at": NOW, "updated_at": NOW, "order": 0,
        "content": """# Browser Rendering & Network

## Rendering Pipeline

```mermaid
flowchart TD
    HTML[Parse HTML] --> DOM[DOM Tree]
    CSS[Parse CSS] --> CSSOM[CSSOM Tree]
    DOM --> RT[Render Tree]
    CSSOM --> RT
    RT --> LAYOUT[Layout<br/>Calculate positions & sizes]
    LAYOUT --> PAINT[Paint<br/>Fill pixels]
    PAINT --> COMP[Composite<br/>Combine layers on GPU]
    COMP --> SCREEN[Pixels on Screen]
```

**Flow Explanation — Browser Rendering Pipeline:**

- **What:** This shows every step from receiving HTML to pixels appearing on screen
- **Parse HTML → DOM Tree:** The browser reads raw HTML and builds a tree of nodes (Document Object Model). Each HTML element becomes a node. This happens top-down, and can be blocked by synchronous scripts
- **Parse CSS → CSSOM Tree:** All CSS (external files, inline styles, browser defaults) is parsed into the CSS Object Model. Selectors are matched to DOM nodes. This must complete before rendering starts
- **Render Tree:** The DOM and CSSOM are combined. Only visible elements are included (display:none elements are excluded). Each node now has both its structure and computed styles
- **Layout:** The browser calculates the exact position and size of every element in pixels. This is also called "reflow." It must account for viewport size, font sizes, padding, margin, and flexbox/grid calculations. Expensive operation
- **Paint:** Fill each pixel with the correct color, text, images, borders, and shadows. Elements are painted in stacking order (z-index). This produces bitmap layers
- **Composite:** GPU combines the painted layers into the final image. Transforms and opacity changes happen here — which is why CSS transitions on `transform` and `opacity` are GPU-accelerated and cheap
- **Why this matters for performance:** Layout changes (width, position, font-size) trigger the full pipeline. Color changes skip layout. Transform/opacity changes skip both layout and paint, using only GPU compositing — making them the fastest visual changes

## Performance Cost of Changes

| Change Type | Triggers | Cost |
|-------------|----------|------|
| Layout (width, position) | Reflow + Repaint + Composite | **Expensive** |
| Appearance (color, bg) | Repaint + Composite | Moderate |
| Transform / Opacity | Composite only | **Cheap (GPU)** |

This is why transitions should target `transform` and `opacity` — they're GPU-accelerated.

## DNS to Response

```mermaid
sequenceDiagram
    Browser->>DNS: Resolve domain → IP
    Browser->>Server: TCP Handshake
    Browser->>Server: TLS Handshake (verify cert)
    Browser->>Server: HTTP Request
    Server->>Browser: HTTP Response
    Browser->>Browser: Parse + Render
```

**Flow Explanation — DNS to Response:**

- **What:** This shows every network step that happens when your browser loads a page
- **DNS Resolution:** The browser asks a DNS server to convert the domain name (e.g., myapp.emergentagent.com) into an IP address. This is cached after the first lookup. Takes 10-100ms for the first request
- **TCP Handshake:** A three-way handshake (SYN → SYN-ACK → ACK) establishes a reliable connection between browser and server. Takes one round-trip (~20-50ms)
- **TLS Handshake:** For HTTPS, the browser and server negotiate encryption. The server presents its SSL certificate. The browser verifies it against trusted authorities. They agree on encryption keys. Takes another 1-2 round-trips
- **HTTP Request:** The browser sends the actual request (GET /page, POST /api/data). Includes headers like Content-Type, Authorization, Cookie
- **HTTP Response:** The server processes the request and sends back the response with status code (200 OK, 404, 500), headers, and body (HTML, JSON, etc.)
- **Parse + Render:** The browser parses the response and renders it (see the rendering pipeline diagram above)
- **Subsequent requests:** Much faster because DNS is cached, the TCP connection is kept alive (HTTP keep-alive), and TLS is already established. First request: ~50-200ms. Subsequent: ~5-20ms
"""
    },

    # ===== FASTAPI =====
    {
        "id": _id(), "title": "FastAPI Request Lifecycle", "category_id": SUB_FASTAPI, "author_id": SYSTEM_AUTHOR,
        "created_at": NOW, "updated_at": NOW, "order": 0,
        "content": """# FastAPI Request Lifecycle

## Architecture

FastAPI = **Starlette** (ASGI framework) + **Pydantic** (data validation). Async by default, auto-generates OpenAPI docs.

## ASGI vs WSGI

**WSGI** (Flask): Synchronous, blocking, one request at a time per worker.
**ASGI** (FastAPI): Asynchronous, non-blocking, thousands of concurrent connections per worker.

## Request Flow

```mermaid
flowchart TD
    REQ[HTTP Request] --> UV[Uvicorn ASGI Server]
    UV --> MW[Middleware Stack<br/>CORS, Auth, Logging]
    MW --> ROUTE[Routing<br/>Match URL to handler]
    ROUTE --> DI[Dependency Injection<br/>Resolve deps like get_current_user]
    DI --> VALID[Pydantic Validation<br/>Type check all inputs]
    VALID --> HANDLER[Route Handler<br/>Your business logic]
    HANDLER --> SERIAL[Response Serialization<br/>Pydantic → JSON]
    SERIAL --> MW2[Middleware Reverse]
    MW2 --> RESP[HTTP Response]
```

**Flow Explanation — FastAPI Request Lifecycle:**

- **What:** This shows every stage an HTTP request passes through inside a FastAPI application
- **Uvicorn ASGI Server:** Receives the raw TCP connection and parses it into an ASGI event. Uvicorn is the server that actually listens on the port (8001). It handles concurrent connections using Python's asyncio event loop
- **Middleware Stack:** Each request passes through all registered middleware in order. CORS middleware adds Access-Control headers. Auth middleware validates tokens. Logging middleware records request details. Middleware can modify the request, reject it, or modify the response
- **Routing:** FastAPI matches the URL path and HTTP method to a registered route handler. /api/documents with GET matches `get_documents()`. Unmatched routes return 404
- **Dependency Injection:** Before the handler runs, FastAPI resolves all dependencies declared with Depends(). For example, `user=Depends(get_current_user)` calls `get_current_user()` and passes the result as the `user` parameter. Dependencies can themselves have dependencies, forming a tree
- **Pydantic Validation:** All request data (path params, query params, request body) is validated against Pydantic models. If a field is declared as `int` but receives a string, FastAPI returns 422 Unprocessable Entity with a detailed error message before your handler code even runs
- **Route Handler:** Your actual business logic executes. All I/O operations (database queries, HTTP calls) should be awaited to keep the event loop free for other requests
- **Response Serialization:** Pydantic models serialize the return value to JSON. ObjectId, datetime, and other non-JSON types must be handled explicitly or excluded
- **Middleware Reverse:** The response passes back through middleware in reverse order. CORS headers are added here

## Dependency Injection

FastAPI's most powerful feature. Dependencies are resolved automatically before your handler runs:

```python
async def get_current_user(token: str = Header()):
    return validate_and_fetch_user(token)

@app.get("/api/todos")
async def get_todos(user=Depends(get_current_user)):
    return await db.todos.find({"author": user["id"]})
```
"""
    },

    # ===== MONGODB =====
    {
        "id": _id(), "title": "MongoDB Document Model", "category_id": SUB_MONGODB, "author_id": SYSTEM_AUTHOR,
        "created_at": NOW, "updated_at": NOW, "order": 0,
        "content": """# MongoDB Document Model

## Document Database

Data stored as BSON (Binary JSON). No fixed schema. Documents in Collections, Collections in Databases.

## The ObjectId Problem

`ObjectId` is BSON, not JSON. `json.dumps({_id: ObjectId(...)})` will **crash** with `TypeError`.

**Fix 1**: Exclude `_id` — `db.find({}, {"_id": 0})`
**Fix 2**: Convert — `str(doc["_id"])`
**Fix 3**: Pydantic models with custom serializers

## Indexing

| Without Index | With Index |
|---------------|-----------|
| Scans every document | Jumps directly to matches |
| O(n) | O(log n) |
| Seconds on large collections | Milliseconds |

Always index fields you query frequently. Use compound indexes for multi-field queries. Use text indexes for search.
"""
    },

    # ===== AUTH =====
    {
        "id": _id(), "title": "JWT & OAuth Authentication", "category_id": SUB_AUTH, "author_id": SYSTEM_AUTHOR,
        "created_at": NOW, "updated_at": NOW, "order": 0,
        "content": """# JWT & OAuth Authentication

## JWT Flow

```mermaid
sequenceDiagram
    User->>Server: POST /login (email, password)
    Server->>Server: Verify credentials, create JWT
    Server->>User: Return JWT token
    User->>User: Store token (localStorage)
    User->>Server: GET /api/data (Authorization: Bearer token)
    Server->>Server: Verify signature, extract user
    Server->>User: Return data
```

**Flow Explanation — JWT Authentication Flow:**

- **What:** This shows how token-based authentication works from login to accessing protected resources
- **Step 1 — Login:** User submits email and password via POST /login. The server verifies credentials against the database (hashed password comparison)
- **Step 2 — Create JWT:** On successful login, the server creates a JSON Web Token containing the user ID, role, and expiration time. The token is signed with a secret key (JWT_SECRET in .env). The signature proves the token wasn't tampered with
- **Step 3 — Return token:** The JWT is sent back to the browser in the response body
- **Step 4 — Store token:** The browser stores the token in localStorage (or sessionStorage). This persists across page refreshes
- **Step 5 — Authenticated requests:** For every subsequent API call, the browser sends the token in the Authorization header: `Authorization: Bearer eyJhbG...`. The server extracts the token, verifies the signature, and extracts the user information
- **Step 6 — Return data:** If the token is valid and not expired, the server processes the request and returns data. If invalid or expired, it returns 401 Unauthorized
- **Why JWT?** Stateless authentication. The server doesn't need to store session data. The token itself contains all the information needed to identify the user. This scales better than session-based auth because any server can verify the token without checking a central session store

## OAuth 2.0 (Google Auth)

```mermaid
sequenceDiagram
    User->>App: Click "Sign in with Google"
    App->>Google: Redirect to Google login
    User->>Google: Enter credentials
    Google->>App: Redirect with auth code
    App->>Google: Exchange code for access token
    Google->>App: Access token
    App->>Google: Get user profile
    Google->>App: Email, name, picture
    App->>User: Create session, return JWT
```

**Flow Explanation — OAuth 2.0 Google Auth Flow:**

- **What:** This shows the OAuth 2.0 authorization code flow with Google, step by step
- **Step 1 — User clicks login:** User clicks "Sign in with Google" on your app. Your app redirects the browser to Google's OAuth consent page
- **Step 2 — Google login:** The user enters their Google credentials directly on Google's page. Your app NEVER sees the user's Google password
- **Step 3 — Authorization code:** After the user consents, Google redirects back to your app with a one-time authorization code in the URL
- **Step 4 — Exchange code for token:** Your backend (NOT the browser) sends this code to Google's token endpoint, along with your client_id and client_secret. Google verifies and returns an access token
- **Step 5 — Get user profile:** Your backend uses the access token to call Google's userinfo API. Google returns the user's email, name, and profile picture
- **Step 6 — Create session:** Your app creates a user record (if new) and generates a JWT session token. The user is now logged in
- **Why OAuth?** Security. The user's Google password never touches your app. You get a verified email (Google has already confirmed it). You get free 2FA (if the user has it enabled on Google). Users don't need to create yet another password
"""
    },

    # ===== DEPLOYMENT =====
    {
        "id": _id(), "title": "From Dev to Production", "category_id": SUB_DEPLOY, "author_id": SYSTEM_AUTHOR,
        "created_at": NOW, "updated_at": NOW, "order": 0,
        "content": """# From Dev to Production

## Deployment Pipeline

```mermaid
flowchart LR
    DEV[Development<br/>Preview URL] --> BUILD[Build Phase<br/>yarn build + pip freeze]
    BUILD --> DOCKER[Containerize<br/>Docker image]
    DOCKER --> PROVISION[Provision<br/>Compute + DB + SSL]
    PROVISION --> DEPLOY[Rolling Deploy<br/>Zero downtime]
    DEPLOY --> MONITOR[Monitor<br/>Logs + Metrics]
```

**Flow Explanation — Deployment Pipeline:**

- **What:** This shows the stages from development to production deployment
- **Development (Preview URL):** During development, your app runs on a preview URL (e.g., myapp.preview.emergentagent.com). This URL changes between sessions and is meant for testing only
- **Build Phase:** The frontend is compiled (yarn build creates optimized static files from React). The backend dependencies are frozen (pip freeze captures exact package versions). This ensures production uses the same versions as development
- **Containerize:** The application is packaged into a Docker image containing all code, dependencies, and runtime configuration. This image is immutable — the same image runs in any environment
- **Provision:** Cloud resources are allocated — compute (CPU/memory), database (MongoDB instance), SSL certificate (HTTPS), and DNS record (your domain name pointing to the server)
- **Rolling Deploy:** The new version is deployed without downtime using the rolling update strategy (see next diagram). Old and new versions temporarily run side by side
- **Monitor:** After deployment, logs, metrics (response times, error rates), and health checks are monitored to detect issues early

## Rolling Deployment (Zero Downtime)

```mermaid
flowchart TD
    S1["Step 1: Start new pod"] --> S2["Step 2: Health check passes"]
    S2 --> S3["Step 3: Route traffic to new pod"]
    S3 --> S4["Step 4: Drain old pod"]
    S4 --> S5["Step 5: Terminate old pod"]
```

**Flow Explanation — Rolling Deployment:**

- **What:** This shows how Kubernetes performs zero-downtime deployments
- **Step 1 — Start new pod:** A new pod with the updated code is created alongside the old one. Both run simultaneously
- **Step 2 — Health check:** Kubernetes sends readiness probes to the new pod. The pod must respond successfully (HTTP 200) before receiving traffic. If health checks fail, the deployment is rolled back automatically
- **Step 3 — Route traffic:** Once healthy, Kubernetes adds the new pod to the load balancer. New requests start going to both old and new pods
- **Step 4 — Drain old pod:** Kubernetes stops sending new requests to the old pod. In-flight requests are allowed to complete (typically 30-second grace period)
- **Step 5 — Terminate old pod:** Once all in-flight requests finish, the old pod is terminated and its resources are freed
- **Why rolling updates?** Users never experience downtime. If the new version has a bug that fails health checks, the old version keeps running and the deployment is automatically rolled back

## Deployment Options

| Option | Description |
|--------|-------------|
| **Emergent Native** | Managed production on Emergent infra |
| **GitHub Export** | Save to GitHub (from the message panel), then deploy to Vercel/Railway/AWS |
| **Code Download** | Download zip, self-host anywhere |
"""
    },

    # ===== GIT =====
    {
        "id": _id(), "title": "Git Internals & Rollback", "category_id": SUB_GIT, "author_id": SYSTEM_AUTHOR,
        "created_at": NOW, "updated_at": NOW, "order": 0,
        "content": """# Git Internals & Rollback

## Git Object Model

Everything is an object: **Blobs** (file content), **Trees** (directories), **Commits** (snapshots). Each commit is a complete snapshot, not a diff.

## Auto-Commits

Every E1 action creates a commit. Each is a rollback checkpoint.

## Rollback

```mermaid
flowchart LR
    C1[Commit 1] --> C2[Commit 2] --> C3[Commit 3] --> C4[Commit 4] --> C5["Commit 5<br/>(broken)"]
    C3 -.->|"ROLLBACK"| RESTORE["Restored State<br/>All files at Commit 3"]
```

**Flow Explanation — Git Rollback:**

- **What:** This shows how the rollback feature works using git commits as checkpoints
- **Commit chain:** Every significant action E1 takes creates an automatic git commit. These form a chain: Commit 1 → 2 → 3 → 4 → 5. Each commit is a complete snapshot of the entire codebase at that point in time
- **Rollback operation:** If Commit 5 introduces a bug, the user can rollback to Commit 3. The platform restores ALL files to exactly the state they were in at Commit 3
- **What IS rolled back:** Source code files (.py, .js, .css, .html), configuration files (.env, package.json, requirements.txt), project structure (folders, new files)
- **What is NOT rolled back:** MongoDB data (documents, users, collections remain as-is), conversation history with E1, git history itself (old commits are preserved)
- **Why the user should never use git reset:** E1 is instructed to never run `git reset` because the platform has special files (.emergent folder, .git config) that must be preserved. The Rollback feature handles these correctly. Users should use the Rollback button in the platform UI, which is free and instant
"""
    },

    # ===== RATE LIMITING =====
    {
        "id": _id(), "title": "Rate Limiting Layers", "category_id": SUB_RATELIMIT, "author_id": SYSTEM_AUTHOR,
        "created_at": NOW, "updated_at": NOW, "order": 0,
        "content": """# Rate Limiting Layers

## Three Layers of Protection

```mermaid
flowchart TD
    REQ[Incoming Request] --> L1{Layer 1: Infrastructure}
    L1 -->|blocked| R1[429 Too Many Requests]
    L1 -->|passed| L2{Layer 2: Application}
    L2 -->|blocked| R2[429 Rate Limited]
    L2 -->|passed| L3{Layer 3: LLM/Integration}
    L3 -->|blocked| R3[429 Budget Exceeded]
    L3 -->|passed| OK[Request Processed]
```

**Flow Explanation — Three-Layer Rate Limiting:**

- **What:** This shows the three levels of protection that prevent abuse and overuse
- **Layer 1 — Infrastructure:** At the Kubernetes ingress/load balancer level. Limits requests per IP address. Login endpoints get stricter limits to prevent brute-force password attacks. If blocked here, the request never reaches your application. Returns 429 Too Many Requests
- **Layer 2 — Application:** Inside your FastAPI application. Limits per-user and per-endpoint. For example, an API might allow 100 requests per minute per user. Expensive operations (search, file upload) get stricter limits than cheap ones (read a document). Uses token bucket or sliding window algorithms
- **Layer 3 — LLM/Integration:** At the Emergent proxy level. Checks Universal Key balance before each LLM call. Enforces provider-side rate limits (OpenAI, Anthropic have their own limits). Daily spending caps prevent runaway costs. If balance is depleted, LLM calls fail with a clear error message directing the user to add balance
- **Why three layers?** Defense in depth. Each layer catches different types of abuse. Infrastructure stops DDoS attacks. Application stops individual user abuse. LLM layer prevents cost overruns. A single layer would leave gaps

### Layer 1: Infrastructure
Per-IP limits at the ingress/load balancer. Login endpoints get stricter limits (brute force protection).

### Layer 2: Application
Per-user, per-endpoint limits in FastAPI. Token bucket or sliding window algorithm. Expensive operations get stricter limits.

### Layer 3: LLM/Integration
Universal Key balance checks, provider-side rate limits, daily spending caps. Auto-disable when balance depleted.
"""
    },

    # ===== SSL/TLS =====
    {
        "id": _id(), "title": "SSL/TLS & CORS", "category_id": SUB_ENCRYPTION, "author_id": SYSTEM_AUTHOR,
        "created_at": NOW, "updated_at": NOW, "order": 0,
        "content": """# SSL/TLS & CORS

## TLS Handshake

```mermaid
sequenceDiagram
    Client->>Server: ClientHello (supported ciphers)
    Server->>Client: ServerHello + Certificate
    Client->>Client: Verify certificate (trusted CA?)
    Client->>Server: Key Exchange
    Server->>Client: Key Exchange
    Note over Client,Server: Both derive shared secret
    Client->>Server: Encrypted HTTP Request
    Server->>Client: Encrypted HTTP Response
```

**Flow Explanation — TLS Handshake:**

- **What:** This shows how HTTPS encryption is established between browser and server
- **ClientHello:** The browser tells the server which encryption algorithms (ciphers) it supports and its TLS version
- **ServerHello + Certificate:** The server picks a cipher, sends its choice along with its SSL certificate (which contains the server's public key and is signed by a trusted Certificate Authority)
- **Certificate Verification:** The browser checks the certificate against its list of trusted CAs. If the certificate is expired, self-signed, or from an untrusted CA, the browser shows a security warning
- **Key Exchange:** Both sides exchange key material using Diffie-Hellman or similar algorithm. This allows them to derive a shared secret without ever sending the actual secret key over the network (even someone intercepting all messages cannot derive the shared secret)
- **Encrypted Communication:** All subsequent HTTP requests and responses are encrypted using the shared secret. Even if intercepted on the network, the data looks like random bytes
- **Why this matters:** Without TLS, anyone on the same network (coffee shop WiFi, corporate network) can read your API keys, passwords, and data in transit

## CORS

Browsers block cross-origin requests by default (Same-Origin Policy). Backend sends CORS headers to whitelist allowed origins. Without proper CORS configuration, your React frontend cannot call your FastAPI backend.

## Security Layers

1. **Network**: DDoS protection, WAF, SSL termination
2. **Kubernetes**: Network policies, pod isolation, RBAC
3. **Application**: JWT auth, input validation, security headers
4. **Data**: Encryption at rest, K8s Secrets, no secrets in code
"""
    },

    # ===== SESSION =====
    {
        "id": _id(), "title": "Session Lifecycle", "category_id": SUB_SESSION, "author_id": SYSTEM_AUTHOR,
        "created_at": NOW, "updated_at": NOW, "order": 0,
        "content": """# Session Lifecycle

## Phases

```mermaid
flowchart LR
    CREATE["1. Creation<br/>Pod provisioned"] --> ACTIVE["2. Active<br/>Building & chatting"]
    ACTIVE --> IDLE["3. Idle<br/>May hibernate"]
    IDLE --> RESUME["4. Resumption<br/>Wake on return"]
    IDLE --> EXPIRE["5. Expiry<br/>Cleanup"]
    RESUME --> ACTIVE
```

**Flow Explanation — Session Lifecycle:**

- **What:** This shows the complete lifecycle of a development session on the Emergent platform
- **1. Creation:** When a user starts a new project, Kubernetes provisions a dedicated pod. The pod contains backend (FastAPI), frontend (React dev server), and MongoDB. A project template is cloned, services are started, and a preview URL is assigned. This takes 15-30 seconds
- **2. Active:** The user and E1 are actively building. Messages are exchanged, tools are executed, code is written and tested. Every significant change is auto-committed to git for rollback. The preview URL is live and accessible
- **3. Idle:** When the user stops interacting. For minutes: everything keeps running. For hours: the container may hibernate (suspended state, wakes in 30-60 seconds). For days: the container may be stopped entirely (recreated in 1-3 minutes when the user returns). Code and data persist through git and MongoDB
- **4. Resumption:** User returns after idle period. The pod is recreated if stopped, services restart, the last git state is restored. It feels seamless — the user picks up where they left off
- **5. Expiry:** After extended inactivity, the container is fully terminated and resources are freed. Conversation history is preserved in MongoDB. Code is preserved if saved to GitHub. The pod can be recreated from git state if the user returns

### Creation
New session → K8s pod provisioned → project template cloned → services started → preview URL assigned.

### Active
Messages exchanged, tools executed, code built, tests run. Auto-committed to git at each step.

### Idle
- **Minutes**: Everything running
- **Hours**: Container may hibernate (wakes in 30-60s)
- **Days**: Container stopped (recreated in 1-3 min on return)

### Expiry
Container terminated, storage released. Conversation history preserved in DB. Code preserved if saved to GitHub.
"""
    },

    # ===== ASSETS =====
    {
        "id": _id(), "title": "Assets & File Processing", "category_id": SUB_ASSETS, "author_id": SYSTEM_AUTHOR,
        "created_at": NOW, "updated_at": NOW, "order": 0,
        "content": """# Assets & File Processing

## Asset Sources

1. **User Uploads**: Images, documents, code files via chat
2. **URL References**: Websites fetched via `crawl_tool`
3. **Tool-Generated**: Screenshots, test reports, design guidelines

## Processing Pipeline

```mermaid
flowchart TD
    UPLOAD[User uploads file] --> VAL[Validate type & size]
    VAL --> STORE[Store in cloud storage]
    STORE --> META[Save metadata in DB]
    META --> AVAIL[Available to E1]
    AVAIL -->|image| MULTI[Multimodal LLM sees it]
    AVAIL -->|document| EXTRACT[extract_file_tool]
    AVAIL -->|archive| BASH[bash: unzip + explore]
```

**Flow Explanation — Asset Processing Pipeline:**

- **What:** This shows how user-uploaded files are processed and made available to E1
- **Upload:** The user drags a file into the chat or uses the attachment button. Supported formats include images (.png, .jpg), documents (.pdf, .docx), code files (.py, .js), and archives (.zip)
- **Validation:** The system checks file type and size limits. Unsupported or oversized files are rejected with a clear error
- **Cloud Storage:** Valid files are uploaded to persistent cloud storage, generating a URL that persists beyond the session
- **Metadata:** File info (name, type, size, URL) is saved in the database and linked to the current job
- **Processing by type:** Images are sent to multimodal LLMs (Claude, GPT-4o) that can "see" and describe them. Documents are processed by extract_file_tool which extracts text, tables, and structured data. Archives are unzipped via bash, and E1 explores the contents
- **Why screenshots are low quality:** Screenshots taken by the screenshot_tool use quality=20 (80% compression). This saves significant tokens in the LLM context window. A full-quality screenshot could consume 10,000+ tokens; a compressed one uses ~2,000
"""
    },

    # ===== DEBUG =====
    {
        "id": _id(), "title": "Understanding the Debug Panel", "category_id": SUB_DEBUG, "author_id": SYSTEM_AUTHOR,
        "created_at": NOW, "updated_at": NOW, "order": 0,
        "content": """# Understanding the Debug Panel

## What Gets Captured

For every message: full LLM payload, tool calls with params/results/duration, token usage, and LLM reasoning.

## Why Debug Looks "The Same"

The system prompt (~10,000 tokens) is identical every time and dominates the view. Dynamic content (your messages, tool results) is there but buried.

| Part | Changes Between Messages? |
|------|--------------------------|
| System prompt | Same every time |
| Tool definitions | Same every time |
| Conversation history | **Grows** with each message |
| Your latest message | **Different** each time |
| Tool calls & results | **Different** each time |

The first 10,000 tokens look identical. Scroll past the system prompt to find the dynamic per-message content.
"""
    },

    # ===== RAG =====
    {
        "id": _id(), "title": "Retrieval Augmented Generation", "category_id": SUB_RAG, "author_id": SYSTEM_AUTHOR,
        "created_at": NOW, "updated_at": NOW, "order": 0,
        "content": """# Retrieval Augmented Generation

## The Problem

LLMs have frozen knowledge, can't access your private data, and may hallucinate.

## How RAG Works

```mermaid
flowchart TD
    subgraph Index["Indexing (once)"]
        DOCS[Your Documents] --> CHUNK[Split into chunks]
        CHUNK --> EMBED[Generate embeddings]
        EMBED --> VDB[(Vector Database)]
    end
    subgraph Query["Per Question"]
        Q[User Question] --> QEMB[Question embedding]
        QEMB --> SEARCH[Similarity search in VDB]
        SEARCH --> TOP[Top K relevant chunks]
        TOP --> PROMPT[Construct prompt with context]
        PROMPT --> LLM_Q[LLM generates grounded answer]
    end
```

**Flow Explanation — How RAG Works:**

- **What:** This shows how Retrieval Augmented Generation grounds LLM responses in actual data
- **Indexing Phase (done once):**
  - **Your Documents:** Company docs, knowledge base articles, code repositories — any text data the LLM should know about but doesn't have in its training data
  - **Split into chunks:** Documents are split into overlapping chunks (typically 500-1000 tokens each). Overlap ensures context isn't lost at chunk boundaries
  - **Generate embeddings:** Each chunk is converted into a vector (e.g., 1536 dimensions) using an embedding model. Semantically similar text produces similar vectors
  - **Vector Database:** Vectors are stored in a specialized database (Pinecone, Weaviate, FAISS) optimized for similarity search
- **Query Phase (per question):**
  - **User Question:** "What is the refund policy for enterprise plans?"
  - **Question embedding:** The question is converted into a vector using the same embedding model
  - **Similarity search:** The vector database finds the K chunks whose vectors are closest to the question vector (cosine similarity). These are the most relevant passages
  - **Construct prompt:** The retrieved chunks are inserted into the LLM prompt as context: "Based on the following information: [chunks], answer: [question]"
  - **Grounded answer:** The LLM generates an answer based on the actual retrieved documents, not its training data. This eliminates hallucination because the answer is grounded in real, retrievable text

## Embeddings

Text as vectors. Similar meaning = close in vector space.
- `"dog"` → [0.8, 0.2, 0.1] and `"puppy"` → [0.79, 0.21, 0.11] (close!)
- `"car"` → [0.1, 0.9, 0.3] (far away)

This is how semantic search works — find by meaning, not keywords.
"""
    },

    # ===== AGENT FRAMEWORKS =====
    {
        "id": _id(), "title": "Agent Framework Landscape", "category_id": SUB_FRAMEWORKS, "author_id": SYSTEM_AUTHOR,
        "created_at": NOW, "updated_at": NOW, "order": 0,
        "content": """# Agent Framework Landscape

## How E1 Compares

| Framework | Focus | vs E1 |
|-----------|-------|-------|
| **LangChain** | General LLM apps | E1 is more specialized |
| **CrewAI** | Multi-agent crews | Similar to E1's subagent architecture |
| **AutoGen** | Multi-agent conversations | More research-oriented |
| **OpenAI Assistants** | Managed agent service | Less customizable |
| **Anthropic MCP** | Standard tool protocol | Complementary to E1 |

## Key Difference

| Aspect | Framework Agents | E1 |
|--------|-----------------|-----|
| Purpose | General purpose building blocks | Coding-specialized complete system |
| Setup | You build the system | Pre-built and managed |
| Hosting | You host everything | Fully managed K8s |
| UI | No UI by default | Full chat interface |
| Container | No workspace | Full dev environment per user |
"""
    },

    # ===== PROMPT ENGINEERING =====
    {
        "id": _id(), "title": "Prompt Engineering Techniques", "category_id": SUB_PROMPT, "author_id": SYSTEM_AUTHOR,
        "created_at": NOW, "updated_at": NOW, "order": 0,
        "content": """# Prompt Engineering Techniques

## What Makes E1's System Prompt Effective

The system prompt is what transforms a generic LLM into E1. Same LLM + different prompt = completely different agent.

## Key Techniques

### 1. Role Definition
`"You are E1, the most powerful full-stack coding agent"` — clear identity and expertise level.

### 2. Structured Sections
XML tags (`<WORKFLOW>`, `<CRITICAL RULES>`) help the LLM parse and reference specific instruction sections.

### 3. Few-Shot Examples
Concrete examples like `data-testid="login-form-submit-button"` are more reliable than abstract descriptions.

### 4. Negative Instructions
`"NEVER delete initial keys from .env files"` — explicitly preventing common mistakes the LLM would otherwise make.

### 5. Self-Checking Prompts
`"Reflect: Are you making dark text on dark background?"` — the LLM reviews its own output before returning.

### 6. Priority Rules
`"Fix all bugs from high to low priority"` — resolves decision conflicts when multiple options exist.

## The Insight

The system prompt is a living document. It gets versioned, A/B tested, and gradually rolled out — just like any critical piece of software.
"""
    },

    # ===== FUTURE =====
    {
        "id": _id(), "title": "Where AI Agents Are Heading", "category_id": CAT_FUTURE, "author_id": SYSTEM_AUTHOR,
        "created_at": NOW, "updated_at": NOW, "order": 0,
        "content": """# Where AI Agents Are Heading

## Timeline

```mermaid
flowchart LR
    NOW["2026<br/>Text + tools, single-session"] --> NEAR["2027<br/>Persistent memory, proactive agents"]
    NEAR --> MID["2028-29<br/>Autonomous dev, self-improving"]
    MID --> FAR["2030+<br/>Natural language programming"]
```

**Flow Explanation — AI Agent Evolution Timeline:**

- **What:** This shows the projected evolution of AI agent capabilities over the next 5+ years
- **2026 (Current):** Agents like E1 work in single sessions — they receive text instructions, use tools (file ops, bash, search), and build software iteratively. Memory is limited to the current conversation. Each session starts fresh
- **2027 (Near):** Persistent memory means agents remember your preferences, coding style, and project context across sessions. Proactive agents monitor deployed apps, detect errors in logs, and fix them without being asked. Multi-agent collaboration means specialized agents (frontend, backend, DevOps) work as a coordinated team on the same project
- **2028-2029 (Medium):** Describe a SaaS product in natural language and receive a fully built, deployed, and tested application. Agents learn from all past sessions globally, continuously improving their coding patterns and error handling. Multimodal input means drawing wireframes on a whiteboard or describing features via voice
- **2030+ (Far):** The role of "developer" transforms into "director of AI agents." Humans define what to build (product management), agents handle the how (implementation). Applications self-maintain — automatically patching vulnerabilities, scaling infrastructure, and adapting to user feedback

## Near Future (2026-2027)
- **Persistent Memory**: Agents remember across sessions, learn your preferences
- **Proactive Agents**: Monitor apps, auto-fix bugs, suggest improvements without being asked
- **Multi-Agent Collaboration**: Frontend + Backend + DevOps agents working as a team

## Medium Future (2028-2029)
- **Autonomous Development**: Describe a SaaS in natural language → fully built and deployed
- **Self-Improving Agents**: Learn from past sessions globally, adapt to coding styles
- **Multimodal Input**: Draw on a whiteboard, voice commands, point-and-say

## Far Future (2030+)
- Humans as product managers, agents as the development team
- Natural language as the primary programming interface
- Self-maintaining, self-evolving applications
- The role of "developer" transforms into "director of AI agents"
"""
    },

    # ===== LLM PROXY =====
    {
        "id": _id(), "title": "LLM Proxy Architecture", "category_id": SUB_LLM_PROXY, "author_id": SYSTEM_AUTHOR,
        "created_at": NOW, "updated_at": NOW, "order": 0,
        "content": """# LLM Proxy Architecture

The LLM Proxy is one of the most critical infrastructure components in the Emergent platform. It sits between the E1 orchestrator and all external LLM providers, acting as a gateway, router, and cost controller.

## What Is the LLM Proxy?

The LLM Proxy is a reverse-proxy layer that intercepts every LLM API call made by E1 or any subagent. Instead of calling OpenAI, Anthropic, or Google directly, all requests route through this proxy.

```mermaid
flowchart LR
    E1[E1 Orchestrator] -->|API call| LP[LLM Proxy]
    SA[Subagents] -->|API call| LP
    LP -->|route| OAI[OpenAI GPT-5.2]
    LP -->|route| ANT[Anthropic Claude]
    LP -->|route| GEM[Google Gemini]
    LP -->|fallback| FB[Fallback Provider]
```

**Flow Explanation — LLM Proxy Architecture:**

- **What:** This shows the LLM Proxy as a central gateway between all Emergent agents and external AI providers
- **E1 Orchestrator:** The main agent making LLM calls for reasoning, code generation, and decision-making
- **Subagents:** Testing agent, design agent, troubleshoot agent — each makes their own LLM calls independently
- **LLM Proxy:** The single point through which ALL LLM traffic flows. It authenticates using the Universal Key, tracks token usage for billing, enforces rate limits, and handles provider selection
- **Provider routing:** Based on the model parameter in the request. "gpt-5.2" goes to OpenAI. "claude-sonnet-4-5" goes to Anthropic. "gemini-3-flash" goes to Google. The calling code doesn't need to know which provider — it just specifies the model
- **Fallback Provider:** If the primary provider is down or returns errors, the proxy automatically tries an alternative provider. This ensures E1 doesn't get stuck waiting for a provider that's experiencing outages
- **Why a centralized proxy?** Without it, every component would need its own API keys, billing logic, and error handling for each provider. The proxy centralizes all of this into one place, making it easier to manage, monitor, and scale

## Why a Proxy?

| Purpose | How It Works |
|---------|-------------|
| **Universal Key** | One API key works across all providers. Users don't need separate keys for OpenAI, Anthropic, Google |
| **Cost Tracking** | Every token is counted and attributed to a user, session, or organization |
| **Rate Limiting** | Prevents runaway loops from burning through budget |
| **Provider Routing** | Automatically selects the best provider based on model, latency, and availability |
| **Fallback Logic** | If OpenAI is down, automatically routes to an alternative provider |
| **Caching** | Identical prompts can return cached responses to save cost and latency |

## The Universal Key

The Universal Key (also called "Emergent LLM Key") is a single API key that the platform provides to every user. Under the hood, the LLM Proxy maps this key to the appropriate provider credentials.

- Users never handle raw OpenAI/Anthropic keys
- Balance is managed centrally via the user's account
- Auto top-up can be enabled to prevent service interruption
- Usage is tracked per-model, per-session, per-agent

## Request Flow

1. **E1 decides** to call an LLM (e.g., GPT-5.2 for code generation)
2. **Request hits LLM Proxy** with the Universal Key and model specification
3. **Proxy validates**: checks key, budget, rate limits
4. **Proxy routes**: selects the provider endpoint (OpenAI, Anthropic, etc.)
5. **Provider responds**: tokens streamed back through proxy
6. **Proxy logs**: records token counts, latency, cost, and metadata
7. **Response delivered** to E1 or subagent

```mermaid
sequenceDiagram
    participant E1 as E1 Orchestrator
    participant LP as LLM Proxy
    participant DB as Usage DB
    participant OAI as OpenAI
    E1->>LP: POST /chat/completions (Universal Key)
    LP->>LP: Validate key & budget
    LP->>DB: Log request start
    LP->>OAI: Forward to provider
    OAI-->>LP: Stream tokens
    LP->>DB: Log tokens & cost
    LP-->>E1: Stream response
```

**Flow Explanation — LLM Proxy Request Sequence:**

- **What:** This shows the exact sequence of events for a single LLM API call through the proxy
- **E1 sends request:** E1 makes a standard API call (POST /chat/completions) with the Universal Key as authentication and the model specification (e.g., gpt-5.2)
- **Proxy validates:** Checks that the Universal Key is valid, the user has sufficient balance, and rate limits haven't been exceeded. If any check fails, returns an error immediately without contacting the provider
- **Log request start:** The proxy logs the request metadata (timestamp, model, user, session) in the usage database before forwarding. This ensures even failed requests are tracked
- **Forward to provider:** The proxy translates the Universal Key to the actual provider API key and forwards the request to OpenAI (or whichever provider matches the model)
- **Stream tokens:** The provider generates tokens and streams them back. The proxy passes these through in real-time (streaming mode), so E1 doesn't have to wait for the complete response
- **Log tokens and cost:** After the response completes, the proxy counts input and output tokens, calculates cost using the model's rate card, and deducts from the user's balance
- **Why streaming?** Streaming reduces perceived latency. E1 can start processing the response before it's fully generated. For long responses (code generation), this can save 10-30 seconds of waiting

## Cost Attribution

Every LLM call is broken down into:
- **Input tokens**: The prompt sent to the model
- **Output tokens**: The response generated
- **Model multiplier**: Different models have different costs per token
- **Total cost**: Computed and deducted from user balance in real-time

## Provider Selection Logic

The proxy uses a priority system:
1. If the user specifies a model (e.g., `gpt-5.2`), route to that provider
2. If the provider is experiencing latency > threshold, try fallback
3. If a provider returns a 5xx error, automatic retry on alternate provider
4. If all providers fail, return a clear error to E1

## Caching Layer

- Exact-match cache: identical prompt + model + temperature = cached response
- Cache TTL: configurable per-use case (code gen vs. creative writing)
- Cache hit rate typically 5-15% for development workloads
- Reduces cost and latency for repetitive operations

## Rate Limiting

The proxy enforces multiple rate limit tiers:
- **Per-user**: Maximum requests per minute
- **Per-session**: Prevents infinite loops from burning budget
- **Per-organization**: Aggregate limits across all users
- **Global**: Platform-wide safety limits

## Key Budget Management

- Users can view usage in Profile -> Universal Key
- Add balance manually or enable auto top-up
- Budget alerts at configurable thresholds (50%, 80%, 95%)
- Hard stop when balance reaches zero (no negative balance)
"""
    },

    # ===== TEST CASES =====
    {
        "id": _id(), "title": "Authentication Test Cases", "category_id": SUB_TC_AUTH, "author_id": SYSTEM_AUTHOR,
        "created_at": NOW, "updated_at": NOW, "order": 0,
        "content": """# Authentication Test Cases

Comprehensive test suite for the Emergent platform authentication system.

## TC-AUTH-001: Google OAuth Login Flow

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Navigate to login page | Login page loads with "Sign in with Google" button |
| 2 | Click "Sign in with Google" | Redirects to Google OAuth consent screen |
| 3 | Select Google account | Redirects back to app with session_id in URL hash |
| 4 | App processes session_id | Session cookie set, user redirected to dashboard |
| 5 | Refresh the page | User remains logged in (session persists) |

## TC-AUTH-002: Session Persistence

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Login successfully | Session cookie set with 7-day expiry |
| 2 | Close browser tab | Session not lost |
| 3 | Open app in new tab | User auto-authenticated, no login required |
| 4 | Wait 7+ days | Session expires, redirect to login |

## TC-AUTH-003: Session Invalidation

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Login successfully | Dashboard loads |
| 2 | Click "Logout" | Session cookie deleted, redirect to login |
| 3 | Press browser back button | Login page shown, not dashboard |
| 4 | Try accessing /dashboard URL directly | Redirect to login |

## TC-AUTH-004: Multiple Device Login

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Login on Device A | Dashboard loads |
| 2 | Login on Device B (same account) | New session created, old session invalidated |
| 3 | Return to Device A | Redirect to login (old session expired) |

## TC-AUTH-005: API Authentication

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Call GET /api/auth/me without token | 401 Unauthorized |
| 2 | Call with valid session cookie | 200 with user data |
| 3 | Call with expired session | 401 Session expired |
| 4 | Call with invalid token | 401 Invalid session |

## TC-AUTH-006: Admin Role Assignment

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Login as chethan@emergent.sh | User role = "admin" |
| 2 | Login as any other email | User role = "viewer" |
| 3 | Admin sees edit/delete buttons | Buttons visible |
| 4 | Viewer does NOT see edit/delete | Buttons hidden |

## TC-AUTH-007: Protected Route Guard

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Navigate to /dashboard without auth | Redirect to /login |
| 2 | Navigate to /doc/{id} without auth | Redirect to /login |
| 3 | Navigate to /bookmarks without auth | Redirect to /login |
| 4 | Navigate to /login while authenticated | Redirect to /dashboard |
"""
    },
    {
        "id": _id(), "title": "Document CRUD Test Cases", "category_id": SUB_TC_DOCS, "author_id": SYSTEM_AUTHOR,
        "created_at": NOW, "updated_at": NOW, "order": 0,
        "content": """# Document CRUD Test Cases

## TC-DOC-001: Create Document (Admin)

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Login as admin | Dashboard loads |
| 2 | Click "New page" in sidebar | Editor opens with empty fields |
| 3 | Enter title "Test Document" | Title field populated |
| 4 | Select category from dropdown | Category selected |
| 5 | Type markdown content | Content appears in textarea |
| 6 | Check live preview panel | Preview renders markdown correctly |
| 7 | Add tags: "test", "qa" | Tags appear as pills |
| 8 | Click "Save" | Document saved, viewer opens |
| 9 | Verify in sidebar | Document appears under selected category |

## TC-DOC-002: Create Document (Viewer - Should Fail)

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Login as non-admin user | Dashboard loads |
| 2 | "New page" button should be hidden | Button not visible |
| 3 | POST /api/documents directly | 403 Admin access required |

## TC-DOC-003: Edit Document (Admin)

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Open existing document | Document viewer loads |
| 2 | Click edit (pencil) icon | Editor opens with pre-filled data |
| 3 | Modify title and content | Changes visible in editor |
| 4 | Check preview panel | Preview shows updated content |
| 5 | Click "Save" | Document updated |
| 6 | Check version history | Previous version saved |

## TC-DOC-004: Soft Delete Document

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Open document as admin | Document viewer loads |
| 2 | Click delete (trash) icon | Confirmation dialog appears |
| 3 | Confirm delete | Document moved to trash, not permanently deleted |
| 4 | Document disappears from sidebar | Not visible in main list |
| 5 | Check trash (admin) | Document appears in trash |

## TC-DOC-005: Restore from Trash

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Go to Trash page (admin) | Deleted documents listed |
| 2 | Click "Restore" on document | Document restored |
| 3 | Check sidebar | Document reappears in original category |
| 4 | Open document | Content intact |

## TC-DOC-006: Version History

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Edit a document and save | Version created |
| 2 | Click version history (clock) icon | Version panel opens |
| 3 | Click on a previous version | Document shows old content |
| 4 | Click "Back to current" | Current version restored |

## TC-DOC-007: Document Export (PDF)

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Open document with mermaid diagrams | Document renders correctly |
| 2 | Click export/download button | PDF generated |
| 3 | Open PDF | Mermaid diagrams rendered as images |
| 4 | Check formatting | Headers, lists, tables preserved |

## TC-DOC-008: Tags System

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Create document with tags "api", "testing" | Tags saved |
| 2 | View document | Tags displayed as colored pills |
| 3 | Edit document, remove "testing" tag | Tag removed |
| 4 | Save and verify | Only "api" tag remains |

## TC-DOC-009: Public Sharing

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Admin clicks share on document | Share link generated |
| 2 | Copy share URL | URL like /share/{id} |
| 3 | Open URL in incognito (no auth) | Document renders (read-only) |
| 4 | Admin disables sharing | Share link deactivated |
| 5 | Revisit old URL | 404 or "not shared" message |
"""
    },
    {
        "id": _id(), "title": "Search & Navigation Test Cases", "category_id": SUB_TC_SEARCH, "author_id": SYSTEM_AUTHOR,
        "created_at": NOW, "updated_at": NOW, "order": 0,
        "content": """# Search & Navigation Test Cases

## TC-SEARCH-001: Basic Search

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Click search in sidebar | Search input appears inline |
| 2 | Type "kubernetes" | Results appear with matching documents |
| 3 | Results show title + category + snippet | Content snippet with match highlighted |
| 4 | Click on result | Navigate to document |

## TC-SEARCH-002: Case-Insensitive Search

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Search "KUBERNETES" | Same results as "kubernetes" |
| 2 | Search "Kubernetes" | Same results |
| 3 | Search "kUbErNeTeS" | Same results |

## TC-SEARCH-003: Fuzzy / Partial Match

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Search "kubrnetes" (typo) | Still finds kubernetes documents |
| 2 | Search "auth" | Finds authentication, authorization docs |
| 3 | Search "trans" | Finds transformer architecture doc |

## TC-SEARCH-004: Multi-Word Search

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Search "session lifecycle" | Finds session lifecycle document |
| 2 | Search "react hooks" | Finds React Virtual DOM & Hooks doc |
| 3 | Search "rate limit" | Finds Rate Limiting document |

## TC-SEARCH-005: Content Search (Not Just Title)

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Search "FastAPI" | Finds docs that mention FastAPI in content |
| 2 | Check snippet | Snippet shows context around "FastAPI" match |
| 3 | Search "CORS" | Finds SSL/TLS & CORS and other docs mentioning CORS |

## TC-NAV-001: Sidebar Navigation

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Click category header | Expands/collapses subcategories |
| 2 | Click document in sidebar | Document loads in viewer |
| 3 | Active document highlighted in sidebar | Visual indicator |
| 4 | Click "Home" | Returns to category grid |

## TC-NAV-002: Keyboard Navigation

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Press Arrow Down | Moves to next document in sidebar |
| 2 | Press Arrow Up | Moves to previous document |
| 3 | Press Ctrl+K | Opens search |
| 4 | Press Escape | Closes search |

## TC-NAV-003: Breadcrumb Navigation

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Open nested document | Breadcrumb shows: Category > Subcategory > Document |
| 2 | Breadcrumb path is correct | Not showing wrong categories |

## TC-NAV-004: Mermaid Chart Expansion

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | View document with mermaid diagram | Diagram renders inline |
| 2 | Click expand/fullscreen button | Diagram opens in fullscreen modal |
| 3 | Diagram is zoomable/scrollable | Can see full detail |
| 4 | Click close or press Escape | Returns to document view |

## TC-NAV-005: Dark/Light Mode

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Toggle to light mode | All components switch to light theme |
| 2 | Toggle back to dark mode | All components switch to dark theme |
| 3 | Refresh page | Theme preference persists |
| 4 | Mermaid diagrams adapt to theme | Diagram colors change |
"""
    },
    {
        "id": _id(), "title": "Admin & Permissions Test Cases", "category_id": SUB_TC_ADMIN, "author_id": SYSTEM_AUTHOR,
        "created_at": NOW, "updated_at": NOW, "order": 0,
        "content": """# Admin & Permissions Test Cases

## TC-ADMIN-001: Admin CRUD Operations

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Login as chethan@emergent.sh | Role = admin, full UI visible |
| 2 | Create new category | Category created successfully |
| 3 | Edit category name | Name updated |
| 4 | Delete empty category | Category removed |
| 5 | Create new document | Document created |
| 6 | Edit existing document | Document updated, version saved |
| 7 | Delete document | Moved to trash |
| 8 | Restore from trash | Document restored |

## TC-ADMIN-002: Viewer Restrictions

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Login as non-admin | Role = viewer |
| 2 | Try to create document | Button hidden, API returns 403 |
| 3 | Try to edit document | Edit button hidden, API returns 403 |
| 4 | Try to delete document | Delete button hidden, API returns 403 |
| 5 | Try to manage categories | Button hidden, API returns 403 |
| 6 | Try to access trash | Not visible, API returns 403 |
| 7 | Can view documents | Full read access |
| 8 | Can bookmark documents | Bookmark works |
| 9 | Can comment on documents | Comment posted |
| 10 | Can search documents | Search works |

## TC-ADMIN-003: Tools Management

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Admin navigates to Tools page | Tools directory visible |
| 2 | Admin clicks "Add Tool" | Form appears with name, URL, description |
| 3 | Fill in tool details and save | Tool added to directory |
| 4 | Edit existing tool | Tool updated |
| 5 | Delete tool | Tool removed |
| 6 | Viewer sees tool list | Read-only, no add/edit/delete |

## TC-ADMIN-004: Public Sharing Control

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Admin clicks share icon on document | Share link generated |
| 2 | Copy and open share link | Document visible without login |
| 3 | Admin clicks share again | Sharing disabled |
| 4 | Open old share link | "Not found" or "Not shared" |
| 5 | Viewer tries to share | Share button not visible |

## TC-ADMIN-005: Comment Moderation

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Viewer posts a comment | Comment appears |
| 2 | Another viewer replies | Thread created |
| 3 | Admin deletes inappropriate comment | Comment removed |
| 4 | Viewer tries to delete another user's comment | 403 Forbidden |
| 5 | Viewer can delete own comment | Comment removed |
"""
    },
    {
        "id": _id(), "title": "Edge Cases & Error Handling", "category_id": SUB_TC_EDGE, "author_id": SYSTEM_AUTHOR,
        "created_at": NOW, "updated_at": NOW, "order": 0,
        "content": """# Edge Cases & Error Handling Test Cases

## TC-EDGE-001: Empty States

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | New user, no bookmarks | "No bookmarks yet" message |
| 2 | Search with no results | "No results found" message |
| 3 | Empty category | Category shown but no documents listed |
| 4 | Document with no content | Empty document viewer, no crash |
| 5 | Trash is empty | "Trash is empty" message |

## TC-EDGE-002: Long Content

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Create doc with 10000+ characters | Saves and renders correctly |
| 2 | Document with 50+ headings | TOC scrollable |
| 3 | Very long document title | Truncated in sidebar, full in viewer |
| 4 | Very long comment | Wraps correctly |

## TC-EDGE-003: Special Characters

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Title with quotes and brackets | Renders correctly |
| 2 | Content with HTML tags | Escaped, not executed |
| 3 | Search with special regex chars | No regex error |
| 4 | Tags with spaces | Trimmed properly |
| 5 | Comment with markdown | Renders as plain text |

## TC-EDGE-004: Network Errors

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Slow network on document load | Loading spinner shown |
| 2 | API returns 500 | Error message displayed |
| 3 | Session expires mid-use | Redirect to login |
| 4 | Offline mode | Graceful error handling |

## TC-EDGE-005: Concurrent Operations

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Two admins edit same document | Last save wins, version history preserves both |
| 2 | Delete document while another user views it | Viewer sees "not found" on next action |
| 3 | Bookmark a document that gets deleted | Bookmark quietly removed |

## TC-EDGE-006: URL Manipulation

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Navigate to /doc/nonexistent-id | "Document not found" message |
| 2 | Navigate to /share/invalid-id | "Not found" page |
| 3 | Manipulate API URLs | Proper 404/401/403 responses |
"""
    },
    {
        "id": _id(), "title": "Performance & Stress Test Cases", "category_id": SUB_TC_PERF, "author_id": SYSTEM_AUTHOR,
        "created_at": NOW, "updated_at": NOW, "order": 0,
        "content": """# Performance & Stress Test Cases

## TC-PERF-001: Page Load Times

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Login page load | < 2s | Lighthouse / DevTools |
| Dashboard initial load | < 3s | First Contentful Paint |
| Document viewer load | < 1s | Time from click to render |
| Search results | < 500ms | Time from keystroke to results |
| Mermaid diagram render | < 2s | Time from load to SVG visible |

## TC-PERF-002: Data Volume Tests

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Load with 100+ documents | Sidebar loads without lag |
| 2 | Load with 50+ categories | Navigation remains smooth |
| 3 | Document with 20+ mermaid charts | All render correctly |
| 4 | 500+ comments on one document | Comments paginate or scroll smoothly |

## TC-PERF-003: Memory & Resource Usage

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Navigate between 20+ documents | No memory leak in browser |
| 2 | Toggle dark/light mode 50 times | No degradation |
| 3 | Open/close search 50 times | Responsive throughout |
| 4 | Mermaid re-renders on theme toggle | No orphaned SVG elements |

## TC-PERF-004: API Response Times

| Endpoint | Target | Payload |
|----------|--------|---------|
| GET /api/categories | < 100ms | 40+ categories |
| GET /api/documents | < 200ms | 100+ documents |
| GET /api/search?q=test | < 300ms | Full-text search |
| POST /api/documents | < 200ms | Document creation |
| GET /api/documents/{id}/comments | < 150ms | 100+ comments |

## TC-PERF-005: Browser Compatibility

| Browser | Version | Status |
|---------|---------|--------|
| Chrome | Latest | Must pass all tests |
| Firefox | Latest | Must pass all tests |
| Safari | Latest | Must pass all tests |
| Edge | Latest | Must pass all tests |
| Mobile Chrome | Latest | Responsive layout verified |
| Mobile Safari | Latest | Responsive layout verified |

## TC-PERF-006: Accessibility Tests

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Tab through all interactive elements | Focus visible and logical order |
| 2 | Screen reader on document viewer | Content readable |
| 3 | High contrast mode | Text remains legible |
| 4 | Zoom to 200% | Layout doesn't break |
"""
    },

    # ===== AI AGENT & ORCHESTRATION TEST CASES =====
    {
        "id": _id(), "title": "AI Agent & Orchestration Test Cases", "category_id": SUB_TC_AGENT, "author_id": SYSTEM_AUTHOR,
        "created_at": NOW, "updated_at": NOW, "order": 0,
        "content": """# AI Agent & Orchestration Test Cases

Comprehensive test suite covering E1 orchestration, tool execution, subagent management, LLM proxy, and the complete agent lifecycle.

## E1 Orchestrator Tests

### TC-AGT-001: E1 Initialization

| Field | Detail |
|-------|--------|
| TC ID | TC-AGT-001 |
| Priority | Critical |
| Component | E1 Orchestrator |
| Preconditions | Platform deployed, agent service running |

**Steps:**
1. Send a new user message to the agent endpoint
2. Verify E1 receives the message via Agent Service
3. Check that E1 loads the system prompt from configuration
4. Verify tool registry is initialized with all available tools
5. Confirm subagent registry is loaded

**Expected Result:**
- E1 initializes within 2 seconds
- System prompt loaded correctly (no truncation)
- All tools registered (file ops, bash, search, screenshot, etc.)
- Subagent list matches configuration
- Session context created in database

### TC-AGT-002: Tool Selection Decision

| Field | Detail |
|-------|--------|
| TC ID | TC-AGT-002 |
| Priority | Critical |
| Component | E1 Decision Layer |
| Preconditions | E1 initialized, user message received |

**Steps:**
1. Send message: "Create a new file called test.py with hello world"
2. Monitor E1's decision layer
3. Verify E1 selects `create_file` tool (not bash, not edit)
4. Check tool parameters match the request
5. Verify tool execution in container

**Expected Result:**
- E1 correctly identifies `create_file` as the right tool
- Parameters: path="/app/test.py", content="print('hello world')"
- File created successfully in Kubernetes pod
- E1 reports success to user

### TC-AGT-003: Multi-Tool Orchestration

| Field | Detail |
|-------|--------|
| TC ID | TC-AGT-003 |
| Priority | High |
| Component | E1 Orchestrator |
| Preconditions | E1 initialized |

**Steps:**
1. Send message: "Read server.py, find the main route, and add a health check endpoint"
2. Monitor E1's tool call sequence
3. Verify E1 calls `view_file` first to read the file
4. Verify E1 calls `search_replace` to add the endpoint
5. Verify E1 calls `execute_bash` to test the endpoint

**Expected Result:**
- Tool calls in correct order: read -> edit -> verify
- No unnecessary tool calls
- Each tool call has correct parameters
- Final response summarizes all changes made

### TC-AGT-004: Parallel Tool Execution

| Field | Detail |
|-------|--------|
| TC ID | TC-AGT-004 |
| Priority | High |
| Component | Tool Execution Engine |
| Preconditions | Multiple independent operations needed |

**Steps:**
1. Send message requiring independent file operations (e.g., "Create files a.py, b.py, c.py")
2. Monitor tool execution
3. Verify E1 batches independent calls in parallel
4. Check all files created correctly

**Expected Result:**
- Independent tool calls executed in parallel (not sequential)
- All 3 files created correctly
- Execution time less than 3x sequential time
- No race conditions or file conflicts

## Subagent Tests

### TC-AGT-005: Subagent Delegation

| Field | Detail |
|-------|--------|
| TC ID | TC-AGT-005 |
| Priority | Critical |
| Component | Subagent System |
| Preconditions | E1 initialized, testing_agent available |

**Steps:**
1. Complete a feature implementation
2. Trigger testing via "test this feature"
3. Verify E1 delegates to testing_agent_v3_fork
4. Verify subagent receives full context (problem statement, files, credentials)
5. Verify subagent returns structured test report

**Expected Result:**
- E1 correctly identifies testing as a subagent task
- testing_agent receives complete context
- Subagent executes tests independently
- Test report returned in JSON format at /app/test_reports/
- E1 reads report and acts on findings

### TC-AGT-006: Subagent Context Isolation

| Field | Detail |
|-------|--------|
| TC ID | TC-AGT-006 |
| Priority | High |
| Component | Subagent System |
| Preconditions | Multiple subagents available |

**Steps:**
1. Call design_agent for UI guidelines
2. Immediately call testing_agent for API tests
3. Verify each subagent has independent context
4. Verify one subagent's actions don't affect another

**Expected Result:**
- Each subagent runs in isolated context
- No cross-contamination of instructions
- Both return correct results for their specific task
- Main agent correctly merges both results

### TC-AGT-007: Subagent Error Recovery

| Field | Detail |
|-------|--------|
| TC ID | TC-AGT-007 |
| Priority | Medium |
| Component | Subagent System |
| Preconditions | Subagent available |

**Steps:**
1. Trigger subagent with intentionally problematic input
2. Verify subagent handles error gracefully
3. Verify E1 receives error report
4. Verify E1 attempts alternative approach or reports to user

**Expected Result:**
- Subagent doesn't crash on bad input
- Error message returned to E1
- E1 doesn't retry infinitely
- User informed of issue with actionable next steps

## LLM Proxy Tests

### TC-AGT-008: Universal Key Routing

| Field | Detail |
|-------|--------|
| TC ID | TC-AGT-008 |
| Priority | Critical |
| Component | LLM Proxy |
| Preconditions | Emergent LLM key configured |

**Steps:**
1. Make API call with Universal Key specifying GPT-5.2
2. Verify proxy routes to OpenAI
3. Make call specifying Claude Sonnet
4. Verify proxy routes to Anthropic
5. Make call specifying Gemini Flash
6. Verify proxy routes to Google

**Expected Result:**
- Each call routed to correct provider
- Response format normalized across providers
- Token usage tracked per-call
- Cost attributed to user's balance

### TC-AGT-009: LLM Proxy Failover

| Field | Detail |
|-------|--------|
| TC ID | TC-AGT-009 |
| Priority | High |
| Component | LLM Proxy |
| Preconditions | Multiple providers configured |

**Steps:**
1. Simulate primary provider timeout (>30s)
2. Verify proxy attempts failover to secondary provider
3. Check response is still valid
4. Verify failover logged for monitoring

**Expected Result:**
- Automatic failover within 5 seconds of timeout
- Secondary provider returns valid response
- Failover event logged with reason
- User not aware of the switch (seamless)

### TC-AGT-010: Token Budget Enforcement

| Field | Detail |
|-------|--------|
| TC ID | TC-AGT-010 |
| Priority | Critical |
| Component | LLM Proxy |
| Preconditions | User has limited balance |

**Steps:**
1. Set user balance to a small amount (e.g., $0.01)
2. Make a large LLM call that would exceed balance
3. Verify proxy rejects the call
4. Verify clear error message returned

**Expected Result:**
- Call rejected before sending to provider
- Error: "Insufficient balance"
- No negative balance created
- User directed to top-up page

## Tool Execution Engine Tests

### TC-AGT-011: File Operations in Container

| Field | Detail |
|-------|--------|
| TC ID | TC-AGT-011 |
| Priority | Critical |
| Component | Tool Execution Engine |
| Preconditions | Kubernetes pod running |

**Steps:**
1. Create a file using create_file tool
2. Read the file using view_file tool
3. Edit the file using search_replace tool
4. Delete content and verify changes
5. Execute the file using execute_bash tool

**Expected Result:**
- File created at correct path
- Read returns exact content written
- Edit preserves unmodified content
- Bash execution returns correct output
- All operations within the same pod

### TC-AGT-012: Bash Execution Timeout

| Field | Detail |
|-------|--------|
| TC ID | TC-AGT-012 |
| Priority | High |
| Component | Tool Execution Engine |
| Preconditions | Bash tool available |

**Steps:**
1. Execute a command that takes > 120 seconds
2. Verify timeout is enforced
3. Verify partial output returned
4. Verify process killed after timeout

**Expected Result:**
- Command times out at 120 seconds
- Partial stdout/stderr captured
- Process terminated cleanly
- E1 informed of timeout (not hung)

## End-to-End Agent Workflow Tests

### TC-AGT-013: Full Feature Build Cycle

| Field | Detail |
|-------|--------|
| TC ID | TC-AGT-013 |
| Priority | Critical |
| Component | Full System |
| Preconditions | Fresh environment |

**Steps:**
1. Send: "Build a REST API with FastAPI that has CRUD for tasks"
2. Monitor E1 planning phase
3. Verify file creation (server.py, requirements.txt)
4. Verify dependency installation
5. Verify server starts successfully
6. Verify E1 tests endpoints with curl
7. Verify E1 provides summary

**Expected Result:**
- E1 creates well-structured code
- Dependencies installed correctly
- Server starts without errors
- All CRUD endpoints functional
- Summary includes what was built and how to use it

### TC-AGT-014: Bug Fix Workflow

| Field | Detail |
|-------|--------|
| TC ID | TC-AGT-014 |
| Priority | High |
| Component | Full System |
| Preconditions | Existing app with known bug |

**Steps:**
1. Report: "The login endpoint returns 500 error"
2. Verify E1 reads relevant log files
3. Verify E1 identifies root cause
4. Verify E1 applies fix
5. Verify E1 tests the fix
6. Verify E1 provides RCA summary

**Expected Result:**
- E1 investigates before fixing (reads logs first)
- Root cause correctly identified
- Fix applied surgically (minimal changes)
- Fix verified with curl test
- Clear summary of what was wrong and what was fixed

### TC-AGT-015: Context Window Management

| Field | Detail |
|-------|--------|
| TC ID | TC-AGT-015 |
| Priority | High |
| Component | E1 Orchestrator |
| Preconditions | Long session with many interactions |

**Steps:**
1. Conduct 50+ interactions in a single session
2. Monitor context window usage
3. Verify E1 handles context compaction
4. Verify E1 doesn't lose critical information
5. Test that E1 can still reference early decisions

**Expected Result:**
- Context compaction triggers automatically
- Critical information preserved (file paths, decisions)
- E1 can reference earlier work accurately
- No sudden quality degradation
- Memory file used for persistence if needed
"""
    },

    # ===== LIMITATIONS & CONSTRAINTS =====
    {
        "id": _id(), "title": "Platform Limitations", "category_id": CAT_LIMITATIONS, "author_id": SYSTEM_AUTHOR,
        "created_at": NOW, "updated_at": NOW, "order": 0,
        "content": """# Emergent Platform Limitations

An honest overview of current platform constraints, known limitations, and workarounds.

## Context Window Limits

| Constraint | Detail |
|-----------|--------|
| **LLM context window** | Each LLM has a maximum token limit (e.g., 200K for Claude). Very long conversations may lose early context |
| **Context compaction** | When approaching limits, E1 compacts context automatically. Some details may be lost |
| **Workaround** | Use memory files (PRD.md) to persist critical decisions across context refreshes |

## Execution Constraints

| Constraint | Detail |
|-----------|--------|
| **Bash timeout** | Commands time out after 120 seconds. Long-running processes must run in background |
| **File size** | Very large files (10K+ lines) may be truncated when viewed |
| **Package installation** | Some system packages may not be available in the container |
| **Port restrictions** | Only ports 3000 (frontend) and 8001 (backend) are exposed externally |

## LLM Limitations

| Constraint | Detail |
|-----------|--------|
| **Knowledge cutoff** | LLMs have training data cutoffs. May not know about very recent libraries or APIs |
| **Hallucination risk** | LLMs can generate plausible but incorrect code. Always verify critical logic |
| **Non-deterministic** | Same prompt may produce different results each time |
| **No internet browsing** | LLMs cannot browse the web directly. E1 uses web_search tool instead |
| **Token costs** | Every LLM call costs tokens. Complex tasks consume more budget |

## Agent Limitations

| Constraint | Detail |
|-----------|--------|
| **No persistent memory** | E1 does not remember across separate sessions. Each job starts fresh |
| **Single user per pod** | Each pod serves one user at a time. No real-time collaboration |
| **Subagent isolation** | Subagents have no context from previous calls. Full context must be provided each time |
| **No GUI interaction** | E1 cannot click buttons or interact with GUI apps directly (only via Playwright screenshots) |
| **Sequential tool calls** | Some tools cannot run in parallel when they have dependencies |

## Infrastructure Limitations

| Constraint | Detail |
|-----------|--------|
| **Pod lifecycle** | Pods may be recycled after inactivity. Unsaved work in temp directories may be lost |
| **Database size** | MongoDB storage has limits per user |
| **Git history** | Auto-commits create many small commits. Git log can be verbose |
| **Preview URL** | Preview URLs are temporary and change between sessions |
| **No custom domains** | Cannot attach custom domains to preview deployments |

## Integration Limitations

| Constraint | Detail |
|-----------|--------|
| **Emergent LLM Key** | Only works for text generation (OpenAI, Anthropic, Gemini), image gen (DALL-E, Nano Banana), video (Sora), and Whisper. Does NOT work for Stripe, fal.ai, email services etc. |
| **OAuth** | Only Emergent-managed Google Auth is supported out of the box |
| **Third-party APIs** | User must provide their own API keys for non-LLM services |
| **Webhook limits** | Inbound webhooks require the preview URL which changes |

## What E1 Cannot Do

- Cannot access private repositories or external databases directly
- Cannot send emails or SMS without configured services
- Cannot run GPU-intensive workloads (ML training, video rendering)
- Cannot modify its own system prompt or tool definitions
- Cannot access other users pods or data
- Cannot bypass rate limits or budget constraints
- Cannot persist data outside of MongoDB and the pod filesystem
"""
    },

    # ===== UI GUIDE =====
    {
        "id": _id(), "title": "Complete UI Guide", "category_id": CAT_UI_GUIDE, "author_id": SYSTEM_AUTHOR,
        "created_at": NOW, "updated_at": NOW, "order": 0,
        "content": """# Emergent Platform UI Guide

A complete and accurate walkthrough of every UI element in the Emergent development platform. This guide reflects the actual current layout.

## The Chat / Message Panel

The message panel is the primary interaction area. It is the central pane where you communicate with E1 and where key actions are located.

| Element | Location | Description |
|---------|----------|------------|
| **Message input** | Bottom of message panel | Text area where you type instructions to E1. Press Enter to send, Shift+Enter for new line |
| **Send button** | Right side of message input | Sends your message to the agent |
| **Save to GitHub** | Inside the message panel (NOT top nav) | Button to push your current codebase to a linked GitHub repository. Located near the message input area, not in the top navigation bar |
| **Message history** | Scrollable area above input | Shows the full conversation between you and E1 |
| **Agent responses** | In message history | E1 replies with text, code blocks, file diffs, and tool call results |
| **Tool call indicators** | Inline in agent responses | Shows when E1 is executing tools (file ops, bash, search). Displays tool name, status, and expandable output |
| **Thinking indicator** | Below last message | Animated indicator showing E1 is processing your request |
| **Attachments** | Near message input | Upload images or files for E1 to analyze |

## File Browser Panel

Located on the left side of the screen. Shows your project's file system.

| Element | Location | Description |
|---------|----------|------------|
| **Directory tree** | Left panel | Expandable folder structure of your entire project |
| **File icons** | Next to each file | Different icons for .py, .js, .css, .json, .md, .html etc. |
| **Click to open** | Any file in tree | Click any file to view its contents in the code editor panel |
| **Search files** | Top of file browser | Filter files by name across the entire project |

## Code Editor / Preview Panel

The right panel shows file contents and live app previews.

| Element | Location | Description |
|---------|----------|------------|
| **File tabs** | Top of right panel | Multiple files can be open simultaneously as tabs |
| **Syntax highlighting** | In code editor | Code is colored by language (Python, JavaScript, CSS, etc.) |
| **Line numbers** | Left margin of editor | Every line is numbered. E1 references these when explaining code |
| **Preview mode** | Tab in right panel | For web apps, shows a live browser preview of your running application |
| **Preview URL** | In preview panel header | The external URL where your app is accessible for testing. This URL changes between sessions |
| **Refresh button** | Preview panel toolbar | Manually refresh the preview if it doesn't auto-update |
| **Open in new tab** | Preview panel toolbar | Opens the preview in a full browser tab for better testing |

## Key Actions and Where to Find Them

This is the most important section. Users frequently look for these actions in the wrong place.

| Action | Where It Actually Is | How to Access |
|--------|---------------------|---------------|
| **Save to GitHub** | Message panel area | Look for the GitHub icon/button near the chat input. NOT in the top navigation bar |
| **Rollback** | Available as a feature | Revert to any previous auto-checkpoint. Each significant code change creates a checkpoint. Free and instant |
| **Deploy** | Deployment options available | Deploy your app to production with a permanent URL |
| **Share preview** | Preview panel | Share the preview URL with others for testing |

## Rollback System

Every significant code change E1 makes creates an automatic checkpoint (git commit). You can revert to any of these.

| Element | Description |
|---------|------------|
| **Checkpoint list** | Every significant change creates an auto-checkpoint |
| **Rollback** | Click to revert to any previous checkpoint |
| **Free and instant** | No cost, takes seconds to revert |
| **Git-based** | Each checkpoint is a git commit under the hood |
| **Non-destructive** | You can rollback and then rollback the rollback |

## Profile and Universal Key Settings

| Setting | Description |
|---------|------------|
| **Universal Key** | Your Emergent LLM API key that works across all AI providers (OpenAI, Anthropic, Google) |
| **Add Balance** | Top up your Universal Key balance. Navigate to Profile > Universal Key > Add Balance |
| **Auto Top-up** | Enable automatic balance replenishment so you never run out mid-task |
| **Usage Dashboard** | View token usage broken down by model and session |

## Universal Key Details

The Universal Key is a single API key (format: sk-emergent-xxx) that works across multiple providers through the Emergent proxy.

| Feature | Description |
|---------|------------|
| **Supported for text** | OpenAI (GPT-5.2, GPT-4o), Anthropic (Claude Sonnet 4.5), Google (Gemini 3 Flash/Pro) |
| **Supported for images** | OpenAI GPT Image 1, Google Nano Banana |
| **Supported for video** | Sora 2 video generation |
| **Supported for audio** | OpenAI Whisper (speech-to-text) |
| **NOT supported for** | Third-party services like Stripe, SendGrid, Twilio, fal.ai. These need their own API keys |
| **Key budget low?** | Go to Profile > Universal Key > Add Balance, or enable Auto Top-up |

## Agent Interaction Patterns

| Pattern | How to Use | Example |
|---------|-----------|---------|
| **Build something new** | Describe what you want clearly | "Build a REST API with user authentication and a React dashboard" |
| **Fix a bug** | Describe the symptoms | "Login returns 500 error when I click submit" |
| **Explain code** | Ask directly | "Explain what server.py does line by line" |
| **Modify existing code** | Be specific about what to change | "Add a dark mode toggle to the header component" |
| **Ask for help** | Ask about platform features | "How do I deploy this?" or "What does this error mean?" |
| **Integration** | Name the service | "Integrate Stripe payment processing" - E1 will use the integration playbook |

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| **Enter** | Send message to agent |
| **Shift+Enter** | New line in message input |
| **Ctrl/Cmd+K** | Quick file search in file browser |
"""

    },
]
