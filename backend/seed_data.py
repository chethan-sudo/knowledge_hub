"""Seed data for Emergent Document Hub - Categories and Documents.

NOTE: Content has been significantly enhanced beyond what's in this file.
The MongoDB database contains the latest, expanded versions of all documents.
New categories (Getting Started, Tutorials) and 7 new documents were added
directly to MongoDB via content enhancement scripts.
To re-seed, drop the database first: db.categories.drop() && db.documents.drop()
"""
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
CAT_FAQ = _id()

# How Emergent Actually Works module
CAT_HOW_EMERGENT = _id()
SUB_AGENTS_MODELS = _id()
SUB_AGENT_LOOP_EM = _id()
SUB_TOOLS_DELEG = _id()
SUB_TRAJ_DEBUG = _id()
SUB_FAILURE_RECOVERY = _id()

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

    {"id": CAT_TESTCASES, "name": "Test Cases", "icon": "Check", "order": 10, "parent_id": None, "internal": True},
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
    {"id": CAT_FAQ, "name": "FAQ", "icon": "MessageSquare", "order": 14, "parent_id": None},

    # How Emergent Actually Works
    {"id": CAT_HOW_EMERGENT, "name": "How Emergent Actually Works", "icon": "Compass", "order": 15, "parent_id": None},
    {"id": SUB_AGENTS_MODELS, "name": "Agents & Models", "icon": "Users", "order": 0, "parent_id": CAT_HOW_EMERGENT},
    {"id": SUB_AGENT_LOOP_EM, "name": "The Agent Loop", "icon": "Cpu", "order": 1, "parent_id": CAT_HOW_EMERGENT},
    {"id": SUB_TOOLS_DELEG, "name": "Tools & Delegation", "icon": "Sparkles", "order": 2, "parent_id": CAT_HOW_EMERGENT},
    {"id": SUB_TRAJ_DEBUG, "name": "Trajectory & Debug Data", "icon": "Database", "order": 3, "parent_id": CAT_HOW_EMERGENT},
    {"id": SUB_FAILURE_RECOVERY, "name": "Failure & Recovery", "icon": "Lock", "order": 4, "parent_id": CAT_HOW_EMERGENT},
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
    FE -->|streaming| AS[Agent Service]
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

**Flow Explanation — End-to-End Request Flow (step by step):**

1. **User types a message** in the Emergent chat interface (e.g., "Build me a todo app with authentication")
2. **Frontend sends the message** via a streaming HTTP connection to the Agent Service. The frontend is a React web app that provides the chat UI, file browser, and live preview panel
3. **Agent Service receives and stores** the message in MongoDB (chat_history collection), creates or updates the job record, then routes the message to the E1 Orchestrator instance assigned to this job
4. **E1 Orchestrator processes the message.** E1 is NOT an LLM — it is a software system. It takes the user's message, combines it with the full system prompt (~15,000 tokens of rules), all previous conversation history, and all pending tool results, then sends this entire context to the LLM
5. **LLM Proxy intercepts the LLM call.** The proxy validates the Universal Key, checks the user's token budget, selects the correct provider (OpenAI, Anthropic, or Google based on the model requested), and forwards the request
6. **LLM Provider generates a response.** The LLM (e.g., Claude Sonnet) reads the full context and generates a response. This response may contain plain text (explanation to the user), structured tool calls (e.g., create_file, execute_bash), or subagent delegation requests
7. **LLM Proxy logs the response,** counts input and output tokens, calculates cost, deducts from the user's balance, and passes the response back to E1
8. **E1's Decision Layer parses the response.** If the LLM output contains tool calls → E1 sends them to the Tool Engine for execution in the K8s Pod. If it contains a subagent request → E1 spawns a subagent with its own LLM instance. If it's a text response → E1 sends it to the user
9. **Tool Engine executes in the K8s Pod.** Bash commands run in the container, files are created/modified on the pod filesystem, screenshots are taken via Playwright. Results are stored in the conversation database
10. **Subagent (if spawned) works independently** with its own LLM, completes its task (e.g., running tests), and returns results + git diff back to E1
11. **E1 decides: continue or done?** After processing tool results or subagent output, E1 decides whether more work is needed (loop back to step 4) or the task is complete (send final response to user)
12. **Response displayed to user** in the frontend chat interface. The user sees E1's explanation, code changes in the file browser, and live app updates in the preview panel
13. **MongoDB stores everything** — every message, every tool call, every LLM response, every audit entry. This enables conversation history, debugging, and billing

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

**Flow Explanation — Data Flow Between Layers (step by step):**

This diagram shows the SIX distinct layers in the Emergent platform and exactly how data flows between them:

1. **User Layer → Frontend:** The developer opens their browser and navigates to the Emergent platform. The browser loads the React App running on port 3000 inside the Kubernetes pod. This app renders the chat interface, file browser, and code preview

2. **Frontend → Backend (the app being built):** When the user previews their app, the React frontend at port 3000 serves the app's HTML/JS/CSS. API calls from the app go to FastAPI at port 8001. FastAPI reads/writes to MongoDB for the app's data. This is the user's application — the thing E1 is building

3. **Browser → Agent Service (AI chat):** Separately from the app, the browser maintains a streaming connection to the Agent Service for the AI chat. When the user types a message to E1, it goes through this channel — NOT through FastAPI. The Agent Service stores every message in MongoDB for conversation history

4. **Agent Service → E1 Instance:** The Agent Service routes the user's message to the E1 Instance assigned to this job. One E1 instance per active job. E1 receives the message along with full conversation history from MongoDB

5. **E1 Instance → LLM Proxy → External Providers:** When E1 needs to reason (every turn of the loop), it calls the LLM Proxy. The proxy authenticates with the Universal Key, routes to the appropriate provider (OpenAI, Anthropic, or Google), and streams the response back. The proxy handles billing, rate limiting, and failover

6. **E1 Instance → Pod Filesystem + Git:** When E1 executes tools (create_file, execute_bash), it operates directly on the Pod Filesystem. Every significant file change is auto-committed to the Git Repository, creating rollback checkpoints

**Key insight — Two separate paths exist:**
- **Path A (App traffic):** Browser → React :3000 → FastAPI :8001 → MongoDB. This is the user's application working normally
- **Path B (AI chat):** Browser → Agent Service → E1 → LLM Proxy → AI Providers. This is the development conversation with E1

These paths are independent. The app can serve traffic while E1 is simultaneously modifying its code

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
| Streaming Connection | Agent Service | Real time chat between user and E1 |

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

| Capability | LLM (Claude/GPT) | E1 (The Agent) |
|---|---|---|
| **Nature** | A model that generates text | A software system that acts |
| **Can run code?** | No | Yes, via tools |
| **Can read files?** | No | Yes, via tools |
| **Can call APIs?** | No | Yes, via subagents |
| **Has memory?** | No (stateless) | Yes (via Agent Service) |
| **Makes decisions?** | Proposes actions via structured output | Executes: picks tools, runs them, evaluates results |
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
- **First message check:** On the FIRST message of a new session or new project, E1 calls ask_human to clarify requirements before building. This is a rule in the system prompt to prevent wasted work from ambiguous instructions. For returning users with clear, specific requests (e.g., "fix the login bug"), E1 may proceed directly without clarification
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
flowchart LR
    E1[E1 Orchestrator] -->|test app| TA[Testing Agent]
    E1 -->|design UI| DA[Design Agent]
    E1 -->|integrate| IA[Integration Expert]
    E1 -->|debug| TRA[Troubleshoot Agent]
    E1 -->|question| SA[Support Agent]
    E1 -->|deploy| DEP[Deployment Agent]
    TA -->|report| E1
    DA -->|guidelines| E1
    IA -->|playbook| E1
    TRA -->|fix| E1
    SA -->|answer| E1
    DEP -->|status| E1
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
    C --> D[Transformer Blocks<br/>32-128 layers]
    D --> E[Output Layer]
    E --> F[Next Token Probabilities]
    F --> G[Sampling]
    G --> H[Generated Token]
```

**Flow Explanation — The Transformer Pipeline:**

- **What:** This shows how text becomes a prediction, step by step, inside an LLM
- **Input Text:** The raw prompt — e.g., "Write a Python function that sorts a list." This includes the ENTIRE conversation history plus system prompt, not just the latest message
- **Tokenizer:** Splits text into subword tokens using a fixed vocabulary (~50K-100K tokens). "Hello world" becomes [464, 3797]. Each token is an integer ID. This is deterministic — the same text always produces the same tokens
- **Embedding Layer:** Converts each token ID into a dense vector (e.g., 4096 dimensions). Also adds positional encoding so the model knows token order (token 1 vs token 100). Without positional encoding, the model would treat the input as a bag of words
- **Transformer Blocks (32-128 layers):** The core of the model. Each block has multi-head self-attention (tokens attend to each other to understand relationships) and a feed-forward network (where factual knowledge is stored as weights). The number of layers varies by model — larger models have more layers, with production LLMs typically having 32 to 128+ layers. Each layer refines the representation
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
| Startup | Minutes | Seconds (cached images) |
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

Run these commands in the terminal (via execute_bash tool or direct terminal access):

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

```mermaid
flowchart TD
    DB[(MongoDB)] --> C1[Collection: users]
    DB --> C2[Collection: documents]
    DB --> C3[Collection: jobs]
    C2 --> D1["Document {id, title, content, tags}"]
    C2 --> D2["Document {id, title, content, tags}"]
```

**Flow Explanation — MongoDB Data Organization:**

- **What:** This shows how MongoDB organizes data in a hierarchy: Database → Collections → Documents
- **Database:** A single MongoDB instance (connected via MONGO_URL) contains all data for the application
- **Collections:** Like tables in SQL. Each collection holds documents of a similar type (users, documents, jobs). Unlike SQL, documents in the same collection can have different fields
- **Documents:** Individual JSON-like objects. Each document has its own fields and can be nested (objects within objects, arrays within objects). No fixed schema means you can add new fields without migration scripts
- **Why MongoDB for Emergent:** Flexible schema is ideal for a platform where users build diverse applications. E1 can add fields to documents without ALTER TABLE migrations. The BSON format natively supports rich types (dates, binary, arrays)

## The ObjectId Problem

`ObjectId` is BSON, not JSON. `json.dumps({_id: ObjectId(...)})` will **crash** with `TypeError`.

**Fix 1**: Exclude `_id` — `db.find({}, {"_id": 0})`
**Fix 2**: Convert — `str(doc["_id"])`
**Fix 3**: Pydantic models with custom serializers

This is the single most common bug when building FastAPI + MongoDB applications. Every time you return MongoDB data in an API response, you must handle `_id`.

## Common Operations

| Operation | Motor (async) Code |
|-----------|-------------------|
| **Find all** | `await db.collection.find({}, {"_id": 0}).to_list(100)` |
| **Find one** | `await db.collection.find_one({"id": "abc"}, {"_id": 0})` |
| **Insert** | `await db.collection.insert_one({"id": "abc", "name": "test"})` |
| **Update** | `await db.collection.update_one({"id": "abc"}, {"$set": {"name": "new"}})` |
| **Delete** | `await db.collection.delete_one({"id": "abc"})` |
| **Count** | `await db.collection.count_documents({"status": "active"})` |
| **Aggregate** | `await db.collection.aggregate([{"$group": {...}}]).to_list(100)` |

## Indexing

| Without Index | With Index |
|---------------|-----------|
| Scans every document | Jumps directly to matches |
| O(n) | O(log n) |
| Seconds on large collections | Milliseconds |

Always index fields you query frequently. Use compound indexes for multi-field queries. Use text indexes for search.

## DateTime Handling

Always use `datetime.now(timezone.utc)` — never `datetime.utcnow()` (deprecated). Convert to ISO string before storing if needed: `datetime.now(timezone.utc).isoformat()`.
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
- **3. Idle:** When the user stops interacting. For minutes: everything keeps running. For hours: the container may hibernate (suspended state, wakes in approximately 30-60 seconds). For days: the container may be stopped entirely (recreated in approximately 1-3 minutes when the user returns). These times are approximate and vary by system load. Code and data persist through git and MongoDB
- **4. Resumption:** User returns after idle period. The pod is recreated if stopped, services restart, the last git state is restored. It feels seamless — the user picks up where they left off
- **5. Expiry:** After extended inactivity, the container is fully terminated and resources are freed. Conversation history is preserved in MongoDB. Code is preserved if saved to GitHub. The pod can be recreated from git state if the user returns

### Creation
New session → K8s pod provisioned → project template cloned → services started → preview URL assigned.

### Active
Messages exchanged, tools executed, code built, tests run. Auto-committed to git at each step.

### Idle
- **Minutes**: Everything running
- **Hours**: Container may hibernate (wakes in ~30-60s)
- **Days**: Container stopped (recreated in ~1-3 min on return)

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
- **Why screenshots are low quality:** Screenshots taken by the screenshot_tool use quality=20 (a low quality setting) to minimize file size. This dramatically reduces token usage when the image is sent to the LLM for analysis. A full-quality screenshot could consume 10,000+ tokens in the context window; a low-quality one uses ~2,000 tokens — an 80%+ reduction
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

The system prompt (~15,000 tokens) is identical every time and dominates the view. Dynamic content (your messages, tool results) is there but buried.

| Part | Changes Between Messages? |
|------|--------------------------|
| System prompt | Same every time |
| Tool definitions | Same every time |
| Conversation history | **Grows** with each message |
| Your latest message | **Different** each time |
| Tool calls & results | **Different** each time |

The first ~15,000 tokens look identical. Scroll past the system prompt to find the dynamic per-message content.
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
| **AutoGen** | Multi-agent conversations | Production-ready multi-agent framework |
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

*Note: The following timeline represents projections based on current trends, not guarantees. The pace of AI development may accelerate or shift.*

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
- Cache hit rate is typically observed around 5-15% for development workloads, though this varies significantly by use case
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

    # ===== TOOLS & RESOURCES =====
    {
        "id": _id(), "title": "Essential Tools & Resources", "category_id": CAT_TOOLS, "author_id": SYSTEM_AUTHOR,
        "created_at": NOW, "updated_at": NOW, "order": 0,
        "content": """# Essential Tools & Resources

A curated list of tools, libraries, and resources used across the Emergent platform.

## Core Libraries (Pre-installed)

| Library | Language | Purpose |
|---------|----------|---------|
| **FastAPI** | Python | Backend API framework with async support and auto-generated docs |
| **Motor** | Python | Async MongoDB driver for Python |
| **Pydantic** | Python | Data validation and serialization for API models |
| **React** | JavaScript | Frontend UI library for building component-based interfaces |
| **Axios** | JavaScript | HTTP client for making API calls from the frontend |
| **Tailwind CSS** | CSS | Utility-first CSS framework for rapid styling |
| **Shadcn/UI** | JavaScript/TypeScript | Pre-built UI components at /app/frontend/src/components/ui/ |
| **Mermaid** | JavaScript | Diagram and flowchart rendering from text |
| **Playwright** | Python | Browser automation for testing and screenshots |
| **Ruff** | Python | Fast Python linter (replaces pylint, flake8) |
| **ESLint** | JavaScript | JavaScript/TypeScript linter for code quality |

## Package Management

| Task | Command | Notes |
|------|---------|-------|
| Install Python package | `pip install package_name` | Then run `pip freeze > /app/backend/requirements.txt` |
| Install JS package | `cd /app/frontend && yarn add package_name` | Never use npm (causes breaking changes) |
| Check installed Python | `pip list` | |
| Check installed JS | `cd /app/frontend && yarn list --depth=0` | |

## Emergent-Specific Libraries

| Library | Install | Purpose |
|---------|---------|---------|
| **emergentintegrations** | `pip install emergentintegrations --extra-index-url https://d33sy5i8bnduwe.cloudfront.net/simple/` | LLM integration library for Universal Key. Supports OpenAI, Anthropic, Google text/image/video/audio |

## Useful Commands

| Command | Purpose |
|---------|---------|
| `sudo supervisorctl status` | Check if backend/frontend/MongoDB are running |
| `sudo supervisorctl restart backend` | Restart backend after .env or package changes |
| `sudo supervisorctl restart frontend` | Restart frontend after .env or package changes |
| `tail -n 100 /var/log/supervisor/backend.err.log` | View backend error logs |
| `tail -n 100 /var/log/supervisor/frontend.err.log` | View frontend error logs |
| `git log --oneline -10` | View last 10 code checkpoints |
| `mongosh` | Access MongoDB shell directly |

## External Documentation

| Resource | URL | When to Use |
|----------|-----|-------------|
| **FastAPI Docs** | https://fastapi.tiangolo.com | Backend development reference |
| **React Docs** | https://react.dev | Frontend development reference |
| **MongoDB Manual** | https://www.mongodb.com/docs/manual/ | Database queries and operations |
| **Tailwind CSS** | https://tailwindcss.com/docs | CSS utility class reference |
| **Mermaid Docs** | https://mermaid.js.org/intro/ | Diagram syntax reference |
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

## TC-AGT-001: E1 Initialization

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Send a new user message to the agent endpoint | E1 receives message via Agent Service |
| 2 | Check system prompt loading from configuration | System prompt loaded correctly (no truncation) |
| 3 | Verify tool registry initialization | All tools registered (file ops, bash, search, screenshot, etc.) |
| 4 | Confirm subagent registry is loaded | Subagent list matches configuration |
| 5 | Check session context creation | Session context created in database, init < 2 seconds |

## TC-AGT-002: Tool Selection Decision

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Send message: "Create a new file called test.py with hello world" | E1 receives and processes the request |
| 2 | Monitor E1's decision layer for tool selection | E1 selects `create_file` tool (not bash, not edit) |
| 3 | Verify tool parameters match the request | Parameters: path="/app/test.py", content="print('hello world')" |
| 4 | Verify tool execution in Kubernetes container | File created successfully in pod |
| 5 | Check E1 response to user | E1 reports success with file path |

## TC-AGT-003: Multi-Tool Orchestration

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Send: "Read server.py, find the main route, and add a health check endpoint" | E1 begins planning phase |
| 2 | Monitor first tool call | E1 calls `view_file` to read the file |
| 3 | Monitor second tool call | E1 calls `search_replace` to add the endpoint |
| 4 | Monitor third tool call | E1 calls `execute_bash` to test the endpoint |
| 5 | Verify final response | Summary of all changes, no unnecessary tool calls |

## TC-AGT-004: Parallel Tool Execution

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Send: "Create files a.py, b.py, c.py with hello world" | E1 identifies independent operations |
| 2 | Monitor tool execution batching | E1 batches all 3 `create_file` calls in parallel |
| 3 | Check all files created correctly | All 3 files exist with correct content |
| 4 | Verify execution timing | Time < 3x sequential time, no race conditions |

## TC-AGT-005: Subagent Delegation

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Complete a feature implementation | Feature code written |
| 2 | Trigger testing via "test this feature" | E1 identifies testing as a subagent task |
| 3 | Verify E1 delegates to testing_agent | testing_agent receives full context (problem, files, credentials) |
| 4 | Verify subagent executes tests independently | Tests run without main agent involvement |
| 5 | Check test report | JSON report at /app/test_reports/, E1 reads and acts on findings |

## TC-AGT-006: Subagent Context Isolation

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Call design_agent for UI guidelines | design_agent returns UI guidelines |
| 2 | Immediately call testing_agent for API tests | testing_agent returns test results |
| 3 | Verify each subagent has independent context | No cross-contamination of instructions |
| 4 | Verify main agent merges both results | Both results correctly incorporated |

## TC-AGT-007: Subagent Error Recovery

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Trigger subagent with intentionally problematic input | Subagent receives bad input |
| 2 | Verify subagent handles error gracefully | No crash, error message returned to E1 |
| 3 | Verify E1 receives error report | E1 does not retry infinitely |
| 4 | Check user notification | User informed with actionable next steps |

## TC-AGT-008: Universal Key Routing

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Make API call with Universal Key specifying GPT-5.2 | Proxy routes call to OpenAI |
| 2 | Make call specifying Claude Sonnet | Proxy routes call to Anthropic |
| 3 | Make call specifying Gemini Flash | Proxy routes call to Google |
| 4 | Check response format across providers | Responses normalized, token usage tracked |
| 5 | Verify billing | Cost attributed to user's balance |

## TC-AGT-009: LLM Proxy Failover

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Simulate primary provider timeout (>30s) | Timeout detected by proxy |
| 2 | Verify proxy attempts failover to secondary provider | Automatic failover within 5 seconds |
| 3 | Check response validity | Secondary provider returns valid response |
| 4 | Verify failover logging | Event logged with reason, seamless to user |

## TC-AGT-010: Token Budget Enforcement

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Set user balance to $0.01 | Balance updated |
| 2 | Make a large LLM call exceeding balance | Call rejected before sending to provider |
| 3 | Verify error message | "Insufficient balance" error returned |
| 4 | Check balance did not go negative | No negative balance, user directed to top-up |

## TC-AGT-011: File Operations in Container

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Create a file using create_file tool | File created at correct path |
| 2 | Read the file using view_file tool | Returns exact content written |
| 3 | Edit the file using search_replace tool | Edit preserves unmodified content |
| 4 | Execute the file using execute_bash tool | Correct output returned |
| 5 | Verify all operations in same pod | All operations within single Kubernetes pod |

## TC-AGT-012: Bash Execution Timeout

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Execute a command that takes > 120 seconds | Command starts executing |
| 2 | Wait for timeout enforcement | Timeout at 120 seconds |
| 3 | Verify partial output returned | Partial stdout/stderr captured |
| 4 | Verify process cleanup | Process terminated cleanly, E1 informed |

## TC-AGT-013: Full Feature Build Cycle

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Send: "Build a REST API with FastAPI that has CRUD for tasks" | E1 enters planning phase |
| 2 | Verify file creation | server.py and requirements.txt created |
| 3 | Verify dependency installation | All packages installed correctly |
| 4 | Verify server startup | Server starts without errors |
| 5 | Verify endpoint testing | E1 tests endpoints with curl, all CRUD functional |
| 6 | Check final summary | Summary includes what was built and usage instructions |

## TC-AGT-014: Bug Fix Workflow

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Report: "The login endpoint returns 500 error" | E1 begins investigation |
| 2 | Verify E1 reads relevant log files | Logs read before attempting any fix |
| 3 | Verify root cause identification | Correct root cause identified |
| 4 | Verify fix applied | Minimal, surgical code change |
| 5 | Verify fix tested and summarized | Fix verified with curl, clear RCA summary provided |

## TC-AGT-015: Context Window Management

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Conduct 50+ interactions in a single session | Session progresses normally |
| 2 | Monitor context window usage | Usage tracked |
| 3 | Verify context compaction triggers | Automatic compaction when approaching limits |
| 4 | Verify critical information preserved | File paths, decisions still accessible |
| 5 | Test reference to early decisions | E1 accurately references earlier work, memory file used if needed |
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
| **Rollback** | Message panel / chat area | Look for the Rollback option near the chat input area, alongside Save to GitHub. Reverts to any previous auto-checkpoint. Free and instant |
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

    # ===== FAQ =====
    {
        "id": _id(), "title": "Frequently Asked Questions", "category_id": CAT_FAQ, "author_id": SYSTEM_AUTHOR,
        "created_at": NOW, "updated_at": NOW, "order": 0,
        "content": """# Frequently Asked Questions

Common questions from the Emergent team, answered with accurate technical detail.

## How does E1 communicate with the LLM?

E1 does NOT chat with the LLM the way you chat with ChatGPT. It uses **function calling / tool use** — a special API mode.

E1 sends the LLM three things in every API call:
- **System prompt** (~15,000 tokens of rules and instructions)
- **Messages** (full conversation history including all previous tool calls and their results)
- **Tool definitions** (JSON schemas for every available tool — create_file, execute_bash, etc.)

The LLM responds with either:
- **Text** (explanation to the user) — `stop_reason: end_turn`
- **Structured tool calls** (JSON specifying which tool to call with what parameters) — `stop_reason: tool_use`

Example LLM response with tool call:
```json
{
  "type": "tool_use",
  "name": "mcp_create_file",
  "input": {
    "path": "/app/server.py",
    "file_text": "from fastapi import FastAPI..."
  }
}
```

E1 then executes the tool and feeds the result back to the LLM for the next decision.

## Who writes the code — E1 or the LLM?

**The LLM writes the code.** E1 does NOT generate code. E1 decides what needs to be done (orchestration), then asks the LLM to generate the code. The LLM outputs a tool call with the code as a parameter. E1 executes that tool call — it places the file at the right path.

So E1 is the **decision maker** and the LLM is the **code generator**.

## Who decides the project structure?

**The LLM proposes it**, guided by **E1's system prompt**. The system prompt contains rules like:
- Backend code goes in /app/backend/
- Frontend code goes in /app/frontend/src/
- API routes must be prefixed with /api
- Use FastAPI for backend, React for frontend

The LLM follows these constraints when generating tool calls.

## If there's an edit, does E1 send the whole code to the LLM?

**No.** E1 sends:
- The relevant file contents (reads the file first using view_file)
- The user's request (e.g., "add dark mode")
- The full conversation history

The LLM responds with a `search_replace` tool call — it specifies the exact text to find and what to replace it with. It does NOT rewrite the entire file.

## What is the Universal Key?

A single API key (format: `sk-emergent-xxx`) that works across multiple LLM providers through Emergent's proxy:

- **Supported for text:** OpenAI (GPT-5.2, GPT-4o), Anthropic (Claude Sonnet, Opus), Google (Gemini Flash, Pro)
- **Supported for images:** OpenAI GPT Image 1, Google Nano Banana
- **Supported for video:** Sora 2
- **Supported for audio:** OpenAI Whisper (speech-to-text)
- **NOT supported for:** Stripe, SendGrid, Twilio, fal.ai, or any non-LLM service

The proxy authenticates with your Universal Key, routes to the correct provider, tracks token usage, and deducts from your balance.

If your key budget is low: Profile > Universal Key > Add Balance, or enable Auto Top-up.

## How do integrations work? (e.g., Stripe)

When you ask E1 to integrate a third-party service like Stripe:

1. E1 calls the **Integration Playbook Expert** subagent
2. The subagent returns a verified playbook with exact code, SDK version, and setup steps
3. E1 asks you for the required API keys (Stripe keys are NOT handled through the Universal Key)
4. E1 implements the code exactly as the playbook specifies

**Important:** The Universal Key only works for LLM providers. Third-party services (Stripe, SendGrid, Twilio) require their own API keys.

## What is stored in the database?

Everything:
- **chat_history:** Every message between user and E1
- **job_audits:** Every tool call — tool name, input, output, duration, timestamp
- **jobs:** Job ID, user ID, status, model used, timestamps
- **job_metadata:** Which LLM model, system prompt version, available tools
- **users:** User accounts, sessions
- **env_variables:** Per-user environment variables

## What does the Debug panel show?

The Debug panel shows the **raw LLM API call log**. Key fields:

| Field | What It Shows |
|-------|--------------|
| `log.url` | Which provider was called (api.anthropic.com, api.openai.com) |
| `log.status_code` | 200 = success, 429 = rate limited, 500 = provider error |
| `log.latency_ms` | How long the LLM took to respond (in milliseconds) |
| `response_body.model` | Exact model version used (e.g., claude-sonnet-4-6) |
| `response_body.stop_reason` | Why the LLM stopped: end_turn (text), tool_use (calling a tool), max_tokens (hit limit) |
| `response_body.usage` | Token breakdown: cache_creation, cache_read, input, output tokens |
| `body.system` | The full system prompt sent to the LLM |
| `body.messages` | Full conversation history including all tool calls and results |
| `body.tools` | All tool definitions available to the LLM |

The first ~15,000 tokens in the Debug body look identical every time — that is the system prompt. Scroll past it to find the actual conversation content.

## What does latency mean in Debug?

**Latency** = the time between when the request was sent to the LLM provider and when the full response came back. Measured in milliseconds.

| Latency | What It Means |
|---------|---------------|
| < 5,000 ms | Fast — simple response |
| 5,000 - 15,000 ms | Normal — typical code generation |
| 15,000 - 30,000 ms | Moderate — complex reasoning or long output |
| 30,000 - 60,000 ms | Slow — very large context |
| > 60,000 ms | Warning — possible provider issues |

It does NOT include tool execution time, network time to the user, or E1's decision-making time. It only measures the LLM provider's thinking time.

## What is inside body in the Debug panel?

The body contains 10 fields — the actual request payload sent to the LLM:

| Field | What It Contains |
|-------|-----------------|
| `model` | Which LLM to use (e.g., claude-sonnet-4-6) |
| `system` | The ~15,000 token system prompt — same every call |
| `messages` | Full conversation history — grows every turn |
| `tools` | Tool definitions with JSON schemas — same every call |
| `max_tokens` | Maximum output length (e.g., 64000) |
| `temperature` | Randomness (1 = creative, 0 = deterministic) |
| `top_p` | Nucleus sampling parameter |
| `top_k` | Top-k sampling parameter |
| `stream` | Whether to stream response token-by-token |
| `metadata` | User ID, session ID for billing |

## What is aps.yaml?

The Agent Configuration file that defines everything about how an agent behaves:

- **metadata:** Agent ID, name, version, tags
- **spec.model:** Which LLM provider, model, temperature, max_tokens, thinking params
- **spec.prompt:** The prompt_id that loads the system prompt
- **spec.toolsets:** All available tools grouped by type (MCP tools, builtins, subagents)
- **overrides:** Tool renaming (internal names to display names) and custom descriptions
- **policy:** Max iterations, timeout
- **context:** Squashing strategy, threshold, preserve_last_n messages
- **hooks:** Communication layer (secondary LLM for formatting finish/ask_human responses)

The resolution chain: Use Case + Model → aps.yaml → agent_id → agent file → prompt_id → runtime system prompt.

## What is the communication layer hook?

A **second, cheaper LLM** (GPT-4.1-mini) that post-processes certain responses. It only activates for `finish` and `ask_human` tool calls — formatting the output for cleaner user-facing messages. Regular tool calls and code generation go directly through the primary model.

## How can I verify the correct agent is deployed?

**L1 Verification (Configuration):**
1. Check Use Case + Model selection in UI
2. Open aps.yaml → find the agent_id for that model
3. Open the agent file → find the prompt_id
4. Verify the UI shows the correct prompt_id as the agent name

**L2 Verification (Runtime):**
1. Copy unique sentences from the prompt file in GitHub
2. Start a job, send a message, open Debug
3. Search for those unique sentences in the runtime system prompt (body.system)
4. If found → correct prompt is loaded at runtime
"""
    },

    # ===================================================================
    # HOW EMERGENT ACTUALLY WORKS — 12 documents from real trajectory data
    # ===================================================================

    # --- Doc 1: The Emergent Agent Ecosystem ---
    {
        "id": _id(), "title": "The Emergent Agent Ecosystem", "category_id": SUB_AGENTS_MODELS, "author_id": SYSTEM_AUTHOR,
        "created_at": NOW, "updated_at": NOW, "order": 0,
        "content": """# The Emergent Agent Ecosystem

A data-driven overview of every actor in the Emergent platform — derived from real production trajectory analysis across multiple jobs.

## Platform Overview

Emergent is a **Go-based orchestration platform** running on Linux. It coordinates multiple AI agents across different LLM providers to build full-stack applications autonomously. The platform is NOT a single agent — it is an ecosystem of **2 agent types, 8 expertise configurations, 8+ LLM models, and 33 tools**.

## The Two Agent Types

Every agent in Emergent is one of two types:

| Agent Type | Role | When Active |
|-----------|------|-------------|
| **EmergentAssistant** | Main agent — plans, writes code, manages files, orchestrates sub-agents | Always running during a job |
| **SkilledAssistant** | Sub-agent — specialized worker delegated to by the main agent | Only during delegation (TRANSITION_MAIN_TO_SUB) |

## Full Ecosystem Diagram

```mermaid
flowchart TB
    subgraph Platform["Emergent Platform (Go + Linux)"]
        JM["job_metadata<br/>model_name, prompt_name"]
        APS["aps.yaml<br/>Agent Configuration"]
    end

    subgraph Main["EmergentAssistant (Main Agent)"]
        M1["Codex 5.3 Expertise<br/>Models: galapagos-alpha, gpt-5.3-codex,<br/>macaroni-alpha, spark-preview"]
        M2["Opus 4.5 Expertise<br/>Model: claude-opus-4-5"]
        M3["General Agent<br/>Model: gpt-5.3-codex-spark-preview"]
    end

    subgraph Sub["SkilledAssistant (Sub-Agents)"]
        S1["Design Agent<br/>gemini-3-pro-preview"]
        S2["Testing Agent (Codex)<br/>gpt-5.3-codex"]
        S3["Testing Agent v3 Fork (Opus)<br/>claude-opus-4-5"]
        S4["Testing Agent v3 (Sonnet 4)<br/>claude-sonnet-4"]
        S5["Auto Frontend Testing<br/>claude-sonnet-4-5"]
        S6["Support Agent"]
        S7["Deep Testing Backend v2"]
    end

    Platform --> Main
    Main -->|"TRANSITION_MAIN_TO_SUB"| Sub
    Sub -->|"TRANSITION_SUB_TO_MAIN"| Main
```

## Key Numbers from Real Data

These numbers come from analyzing real production trajectories across multiple jobs:

| Metric | Value |
|--------|-------|
| Distinct agent+expertise+model+tool combinations | **132** |
| Agent types | **2** (EmergentAssistant, SkilledAssistant) |
| Expertise configurations | **8** |
| Distinct LLM models | **8+** |
| Distinct tools/functions | **33** |
| Execution modes | **3** (SKIP, TRANSITION_MAIN_TO_SUB, TRANSITION_SUB_TO_MAIN) |

## The Three Execution Modes

Every trajectory step has an `execution_mode`:

| Mode | Count | Meaning |
|------|-------|---------|
| `SKIP` | 1,950 | Normal agent step — the main agent executes a tool |
| `TRANSITION_MAIN_TO_SUB` | 34 | Main agent delegates to a sub-agent |
| `TRANSITION_SUB_TO_MAIN` | 29 | Sub-agent completes and returns control |

The imbalance (34 → sub, 29 ← back) means some sub-agent sessions were still active when data was captured.

## How a Typical Job Flows

1. **Job starts** → Platform reads `job_metadata` for model and prompt configuration
2. **Main agent initializes** → EmergentAssistant begins with assigned model and expertise
3. **Core loop runs** → Agent calls LLM → gets tool_use response → executes tool → feeds result back
4. **Delegation happens** → Main agent calls a delegation tool (e.g., `testing_agent`) → TRANSITION_MAIN_TO_SUB
5. **Sub-agent works** → SkilledAssistant runs its own loop with its own model
6. **Sub-agent returns** → TRANSITION_SUB_TO_MAIN → main agent continues
7. **Job completes** → Main agent calls `finish` tool

## LLM Providers Used

Emergent is **multi-provider** — it uses models from three different companies:

| Provider | Models | Used For |
|----------|--------|----------|
| **OpenAI** | gpt-5.3-codex, gpt-5.3-codex-spark-preview, galapagos-alpha, macaroni-alpha | Main agent (codex expertise), testing agent (codex) |
| **Anthropic** | claude-opus-4-5, claude-sonnet-4, claude-sonnet-4-5 | Main agent (opus expertise), testing agents (v3, auto frontend) |
| **Google** | gemini-3-pro-preview | Design agent exclusively |

> **Note:** `galapagos-alpha` and `macaroni-alpha` are experimental/internal model names that may represent pre-release or A/B test variants.
"""
    },

    # --- Doc 2: All 8 Expertise Types & Their Models ---
    {
        "id": _id(), "title": "All 8 Expertise Types & Their Models", "category_id": SUB_AGENTS_MODELS, "author_id": SYSTEM_AUTHOR,
        "created_at": NOW, "updated_at": NOW, "order": 1,
        "content": """# All 8 Expertise Types & Their Models

Every agent in Emergent has an `expertise_type` — a configuration string that determines its system prompt, available tools, and which LLM model it uses. There are **8 distinct expertise types** observed in production.

## Main Agent Expertise Types (EmergentAssistant)

### 1. full_stack_app_builder_cloud_v8_codex_5_3

The **primary workhorse** — used for most full-stack app building jobs.

| Field | Value |
|-------|-------|
| Agent Type | EmergentAssistant |
| Purpose | Full-stack application building (React + FastAPI + MongoDB) |
| Models | `galapagos-alpha`, `gpt-5.3-codex`, `gpt-5.3-codex-spark-preview`, `macaroni-alpha` |
| Prompt | `infinite_fullstack_codex_5_3` |
| Frequency | Most common expertise in production |

**Why 4 different models for the same expertise?** The platform runs A/B experiments and canary deployments. The same expertise type can be routed to different models:
- `gpt-5.3-codex` — the stable production model
- `gpt-5.3-codex-spark-preview` — the Spark environment preview
- `galapagos-alpha` — experimental variant (codename)
- `macaroni-alpha` — experimental variant (codename)

### 2. full_stack_app_builder_cloud_v8_opus_4_5

Same full-stack building capability but using **Anthropic's Claude Opus**.

| Field | Value |
|-------|-------|
| Agent Type | EmergentAssistant |
| Purpose | Full-stack app building (alternative to Codex) |
| Model | `claude-opus-4-5-20251101` |
| Prompt | `infinite_fullstack_opus_4_5` |

### 3. general_agent_codex_5_3

A **general-purpose agent** — not specialized for full-stack building.

| Field | Value |
|-------|-------|
| Agent Type | EmergentAssistant |
| Purpose | General tasks, non-app-building workflows |
| Model | `gpt-5.3-codex-spark-preview` |

## Sub-Agent Expertise Types (SkilledAssistant)

### 4. design_agent_full_stack_gemini_3_pro

The **design specialist** — uses Google's Gemini for UI/UX decisions.

| Field | Value |
|-------|-------|
| Agent Type | SkilledAssistant |
| Purpose | UI design, layout, color schemes, component structure |
| Model | `gemini-3-pro-preview` |
| Delegation Tool | `design_agent_full_stack` |
| Reference | Uses `design_guidelines.json` for design constraints |

### 5. testing_agent_codex_5_3

Testing sub-agent using **OpenAI Codex** — the original testing agent.

| Field | Value |
|-------|-------|
| Agent Type | SkilledAssistant |
| Purpose | Writing and running tests (Playwright, pytest) |
| Model | `gpt-5.3-codex` |
| Delegation Tool | `testing_agent` |

### 6. testing_agent_v3_fork_opus_4_5

Testing sub-agent using **Claude Opus** — a forked variant of v3.

| Field | Value |
|-------|-------|
| Agent Type | SkilledAssistant |
| Purpose | Advanced testing with Claude Opus capabilities |
| Model | `claude-opus-4-5-20251101` |
| Delegation Tool | `testing_agent_v3_fork` |

### 7. testing_agent_v3_sonnet_4

Testing sub-agent using **Claude Sonnet 4**.

| Field | Value |
|-------|-------|
| Agent Type | SkilledAssistant |
| Purpose | Testing with balanced speed/quality (Sonnet 4) |
| Model | `claude-sonnet-4-20250514` |
| Delegation Tool | `testing_agent_v3` |

### 8. auto_frontend_testing_agent_sonnet_3_7

**Automated frontend testing** agent using Claude Sonnet 4.5.

| Field | Value |
|-------|-------|
| Agent Type | SkilledAssistant |
| Purpose | Automated Playwright frontend tests, screenshot comparison |
| Model | `claude-sonnet-4-5-20250929` |
| Delegation Tool | `auto_frontend_testing_agent` |

> **Note:** Despite the name containing "sonnet_3_7", this expertise actually maps to `claude-sonnet-4-5-20250929` — the naming reflects when the config was originally created, not the current model.

## Multi-Model Routing Diagram

```mermaid
flowchart LR
    subgraph Expertise["expertise_type"]
        E1["codex_5_3"]
        E2["opus_4_5"]
        E3["general_agent"]
        E4["design_gemini"]
        E5["testing_codex"]
        E6["testing_v3_fork_opus"]
        E7["testing_v3_sonnet"]
        E8["auto_frontend_sonnet"]
    end

    subgraph Models["LLM Models"]
        GA["galapagos-alpha"]
        GC["gpt-5.3-codex"]
        SP["spark-preview"]
        MA["macaroni-alpha"]
        CO["claude-opus-4-5"]
        CS4["claude-sonnet-4"]
        CS45["claude-sonnet-4-5"]
        GM["gemini-3-pro"]
    end

    E1 --> GA
    E1 --> GC
    E1 --> SP
    E1 --> MA
    E2 --> CO
    E3 --> SP
    E4 --> GM
    E5 --> GC
    E6 --> CO
    E7 --> CS4
    E8 --> CS45
```

## How the Platform Selects a Model

The selection chain:

1. **User creates a job** → selects a "Use Case" + "Model" in the UI
2. **Platform looks up `aps.yaml`** → finds the matching `agent_id` for that combination
3. **Agent file loaded** → contains the `expertise_type` and `prompt_id`
4. **`job_metadata` written** → stores `model_name` and `prompt_name` for the job
5. **Agent spawned** → uses the configured model

The `job_metadata` record is critical because it's what `auto_compact` reads when spawning fork agents (see "Model Selection, Routing & auto_compact" doc).
"""
    },

    # --- Doc 3: Model Selection, Routing & auto_compact ---
    {
        "id": _id(), "title": "Model Selection, Routing & auto_compact", "category_id": SUB_AGENTS_MODELS, "author_id": SYSTEM_AUTHOR,
        "created_at": NOW, "updated_at": NOW, "order": 2,
        "content": """# Model Selection, Routing & auto_compact

How models are assigned, how they can change mid-job, and the auto_compact mechanism that caused a real production model switch.

## The Configuration Chain

```mermaid
flowchart TD
    UI["User selects Use Case + Model"] --> APS["aps.yaml lookup"]
    APS --> AgentFile["Agent file loaded<br/>expertise_type + prompt_id"]
    AgentFile --> JM["job_metadata written<br/>model_name, prompt_name"]
    JM --> Spawn["Agent spawned with model"]
    Spawn --> Loop["Agent loop runs"]
    Loop -->|"context too large"| AC["auto_compact triggered"]
    AC --> Fork["Fork agent spawned"]
    Fork -->|"reads job_metadata"| JM
```

## What is auto_compact?

When the conversation history grows too large for the model's context window, the platform triggers **auto_compact** — an automatic context compaction:

1. The current conversation is **summarized** into a shorter version
2. The current agent **stops**
3. A new **fork agent** is spawned to continue the job
4. The fork agent reads its configuration from **job_metadata** (not from the previous agent)

This is where model changes can happen.

## Real Example: Job 2abc6159 (budget-insights-io)

This is a real production incident where the model changed mid-job:

### Timeline

| Step | Time (UTC) | Event | Model |
|------|-----------|-------|-------|
| 0–186 | 11:46–14:35 | Normal execution — building the app | **galapagos-alpha** |
| 187 | 14:35:31 | `auto_compact` triggered — context summarized | (system event) |
| 188 | 14:36:43 | Transition step (default_tool, empty) | galapagos-alpha |
| 189 | 14:37:03 | Fork agent starts — calls `ask_human` with plan | **gpt-5.3-codex** |
| 190–335 | 14:37–16:00 | Continues building with new model | **gpt-5.3-codex** |

### Root Cause

The original agent was assigned `galapagos-alpha` (likely via experiment routing). But `job_metadata` had:

```
model_name = "gpt-5.3-codex?reasoning_effort=high"
prompt_name = "infinite_fullstack_codex_5_3"
```

When `auto_compact` spawned the fork agent, it read from `job_metadata` → got `gpt-5.3-codex` instead of the runtime model `galapagos-alpha`.

**Key insight:** The fork agent always uses the **configured** model from `job_metadata`, not the **runtime** model of the previous agent.

## Testing Agent Model Routing

The main agent can invoke different testing sub-agents, each with its own model. In the same job (2abc6159), three different testing rounds used three different models:

| Round | Steps | Expertise Type | Model |
|-------|-------|---------------|-------|
| 1st | 35–61 | testing_agent_codex_5_3 | gpt-5.3-codex |
| 2nd | 275–290 | testing_agent_v3_fork_opus_4_5 | claude-opus-4-5 |
| 3rd | 293–321 | auto_frontend_testing_agent_sonnet_3_7 | claude-sonnet-4-5 |

This is **by design** — the platform intentionally routes different testing expertise types to different models.

## Other Events That Affect Models

| Event | Effect on Model |
|-------|----------------|
| `exit_cost_credit_limit_reached` | Model set to `None` — agent paused until credits added |
| `pause` | Model set to `None` — agent paused by user |
| Resume after pause | Model restored from `job_metadata` (may differ from pre-pause model) |
| `auto_compact` | Fork agent reads `job_metadata` — may get different model |
| A/B experiment | Same expertise_type routed to experimental model (galapagos-alpha, macaroni-alpha) |

## How to Trace a Model Change

To investigate whether a model changed during a job, query the trajectories table:

```sql
SELECT step_id, created_at, model_name, function_name, execution_mode
FROM trajectories
WHERE job_id = 'your-job-id'
ORDER BY step_id;
```

Look for:
- A step where `function_name = 'auto_compact'`
- The step immediately after where `model_name` changes
- Any steps where `model_name IS NULL` (credit limit or pause)
"""
    },

    # --- Doc 4: The Agent Loop Step by Step ---
    {
        "id": _id(), "title": "The Agent Loop Step by Step", "category_id": SUB_AGENT_LOOP_EM, "author_id": SYSTEM_AUTHOR,
        "created_at": NOW, "updated_at": NOW, "order": 0,
        "content": """# The Agent Loop Step by Step

The core execution loop that powers every Emergent agent — how the platform turns a user message into working code, one LLM call at a time.

## The Loop in 6 Steps

```mermaid
flowchart TD
    A["1. Build Context<br/>system prompt + message history + tool definitions"] --> B["2. POST to LLM<br/>Send context to model API"]
    B --> C["3. Parse Response<br/>Extract thinking + tool_use blocks"]
    C --> D{"4. Check stop_reason"}
    D -->|"tool_use"| E["5. Execute Tool(s)<br/>Run the tool, capture output"]
    D -->|"end_turn"| G["Agent done for this turn"]
    D -->|"max_tokens"| H["Context too long — may trigger auto_compact"]
    E --> F["6. Append Result<br/>Add tool result to message history"]
    F --> A
```

## Step-by-Step Breakdown

### Step 1: Build Context

Every LLM call sends three things:
- **`system`** — The system prompt (~15,000 tokens). Same every call.
- **`messages`** — The full conversation history. **Grows every iteration.**
- **`tools`** — JSON schemas for all available tools. Same every call.

```json
{
  "model": "gpt-5.3-codex",
  "system": [{"type": "text", "text": "You are an AI assistant..."}],
  "messages": [
    {"role": "user", "content": "Build a todo app"},
    {"role": "assistant", "content": [{"type": "tool_use", "name": "execute_bash", ...}]},
    {"role": "user", "content": [{"type": "tool_result", "content": "..."}]}
  ],
  "tools": [{"name": "execute_bash", "description": "...", "input_schema": {...}}, ...],
  "max_tokens": 64000,
  "temperature": 1,
  "stream": true
}
```

### Step 2: POST to LLM

The platform sends an HTTP POST to the model provider's API. The response streams back token-by-token.

### Step 3: Parse Response

The LLM response contains one or more **content blocks**:

- **`thinking`** — Internal reasoning (visible in debug logs)
- **`text`** — Plain text output
- **`tool_use`** — A tool call with name + input JSON

Example response:
```json
{
  "content": [
    {"type": "thinking", "text": "I need to create the React component..."},
    {"type": "tool_use", "id": "tool_abc", "name": "create_file", "input": {"file_path": "/app/src/App.js", "content": "..."}}
  ],
  "stop_reason": "tool_use"
}
```

### Step 4: Check stop_reason

| stop_reason | Meaning | What Happens Next |
|------------|---------|-------------------|
| `tool_use` | The model wants to execute a tool | Execute the tool, feed result back, loop again |
| `end_turn` | The model is done (no more tool calls) | Agent turn ends, await next user message |
| `max_tokens` | Response was truncated — hit output limit | May trigger `auto_compact` to free context space |

### Step 5: Execute Tool(s)

The platform executes the requested tool and captures its output. If the response contains **multiple** `tool_use` blocks, they may be wrapped in `PARALLEL_TOOLS` for concurrent execution.

### Step 6: Append Result

The tool result is appended to the message history as a `tool_result` message:

```json
{"role": "user", "content": [{"type": "tool_result", "tool_use_id": "tool_abc", "content": "File created successfully"}]}
```

Then the loop returns to Step 1 with the expanded context.

## Message Accumulation

Each iteration adds **2 messages** to the history:
1. The assistant's response (with thinking + tool_use)
2. The tool result

After 100 iterations, the context can reach **200+ messages**. This is why `auto_compact` exists — to summarize and compress the history when it grows too large.

## PARALLEL_TOOLS

When the LLM returns multiple tool calls in a single response, the platform wraps them in a `PARALLEL_TOOLS` pseudo-function:

```json
{
  "function_name": "PARALLEL_TOOLS",
  "traj_payload": {
    "tool_calls": [
      {"name": "view_file", "input": {"file_path": "/app/src/App.js"}},
      {"name": "view_file", "input": {"file_path": "/app/src/index.js"}}
    ]
  }
}
```

In the trajectory database, `PARALLEL_TOOLS` shows up as a single step, but it contains multiple underlying tool executions.

## How Many Iterations Per Job?

From real data:
- **Small apps:** 50–100 steps
- **Medium apps:** 150–250 steps
- **Large apps (like budget-insights-io):** 300–400+ steps

The number of steps depends on app complexity, testing thoroughness, and how many sub-agent delegations occur.
"""
    },

    # --- Doc 5: Inside One LLM Call ---
    {
        "id": _id(), "title": "Inside One LLM Call", "category_id": SUB_AGENT_LOOP_EM, "author_id": SYSTEM_AUTHOR,
        "created_at": NOW, "updated_at": NOW, "order": 1,
        "content": """# Inside One LLM Call

What happens during a single LLM API call — the debug log fields, request/response structure, token economics, and caching.

## The Debug Log Structure

Each LLM call produces a debug log with **14 key fields**:

| # | Field | Type | Description |
|---|-------|------|-------------|
| 1 | `llm_call_id` | string | Unique ID for this specific LLM call |
| 2 | `model` | string | Model used (e.g., "gpt-5.3-codex") |
| 3 | `created_at` | timestamp | When the call was made |
| 4 | `duration_ms` | number | How long the call took in milliseconds |
| 5 | `status` | string | "success" or "error" |
| 6 | `body` | object | The full request body sent to the LLM |
| 7 | `response` | object | The full response from the LLM |
| 8 | `usage` | object | Token counts (input, output, cache) |
| 9 | `stop_reason` | string | Why the model stopped generating |
| 10 | `thinking` | string | The model's internal reasoning (if available) |
| 11 | `tool_calls` | array | Tool calls extracted from the response |
| 12 | `error` | object | Error details (if status is "error") |
| 13 | `context_management` | object | Context window stats and compaction info |
| 14 | `cache_performance` | object | Cache hit/miss rates |

## The Request Body (`body`)

```json
{
  "model": "gpt-5.3-codex",
  "system": [
    {
      "type": "text",
      "text": "You are an AI assistant that builds full-stack applications...",
      "cache_control": {"type": "ephemeral"}
    }
  ],
  "messages": [
    {"role": "user", "content": "Build a budget tracking app"},
    {"role": "assistant", "content": [{"type": "thinking", "text": "..."}, {"type": "tool_use", ...}]},
    {"role": "user", "content": [{"type": "tool_result", ...}]}
  ],
  "tools": [
    {
      "name": "execute_bash",
      "description": "Execute a shell command in the container",
      "input_schema": {
        "type": "object",
        "properties": {
          "command": {"type": "string", "description": "The bash command to execute"}
        },
        "required": ["command"]
      }
    }
  ],
  "max_tokens": 64000,
  "temperature": 1,
  "top_p": 1,
  "top_k": 0,
  "stream": true,
  "metadata": {"user_id": "usr_abc123"}
}
```

## Token Economics

A typical LLM call's token breakdown:

| Component | Tokens | Notes |
|-----------|--------|-------|
| System prompt | ~15,000 | Cached after first call |
| Tool definitions | ~8,000 | Cached after first call |
| Message history | 5,000–200,000+ | Grows each iteration |
| Output | 1,000–16,000 | Varies per response |

## Caching — The 88% Hit Rate

The system prompt and tool definitions are the same every call. The platform uses **prompt caching** to avoid re-processing them:

```json
{
  "usage": {
    "input_tokens": 45000,
    "output_tokens": 3500,
    "cache_creation_input_tokens": 0,
    "cache_read_input_tokens": 39600
  }
}
```

In this example:
- Total input: 45,000 tokens
- Cached (reused): 39,600 tokens → **88% cache hit rate**
- Fresh (new content): 5,400 tokens (only the new messages)

Cache hits are significantly cheaper — typically **90% discount** on input token costs.

## The Response

```json
{
  "id": "msg_abc123",
  "type": "message",
  "role": "assistant",
  "content": [
    {
      "type": "thinking",
      "text": "The user wants a budget tracker. I'll start by creating the React frontend..."
    },
    {
      "type": "tool_use",
      "id": "toolu_xyz789",
      "name": "create_file",
      "input": {
        "file_path": "/app/frontend/src/App.js",
        "content": "import React from 'react';\\n..."
      }
    }
  ],
  "model": "gpt-5.3-codex",
  "stop_reason": "tool_use",
  "usage": {
    "input_tokens": 45000,
    "output_tokens": 3500
  }
}
```

## Context Management

As the conversation grows, the platform tracks context utilization:

```json
{
  "context_management": {
    "total_context_window": 200000,
    "used_tokens": 156000,
    "utilization_percent": 78,
    "compaction_threshold": 85,
    "will_compact_next": false
  }
}
```

When `utilization_percent` exceeds the `compaction_threshold` (typically 85%), `auto_compact` triggers on the next iteration.

## Streaming

Responses stream token-by-token. In Chrome DevTools, you can see this as Server-Sent Events (SSE):

```
data: {"type": "content_block_delta", "delta": {"type": "thinking_delta", "thinking": "I need to"}}
data: {"type": "content_block_delta", "delta": {"type": "thinking_delta", "thinking": " create the"}}
data: {"type": "content_block_delta", "delta": {"type": "thinking_delta", "thinking": " React app"}}
...
data: {"type": "message_stop"}
```

Each `content_block_delta` contains a small chunk of the response. The frontend reconstructs the full response by concatenating these deltas.
"""
    },

    # --- Doc 6: The Complete 33-Tool Catalog ---
    {
        "id": _id(), "title": "The Complete 33-Tool Catalog", "category_id": SUB_TOOLS_DELEG, "author_id": SYSTEM_AUTHOR,
        "created_at": NOW, "updated_at": NOW, "order": 0,
        "content": """# The Complete 33-Tool Catalog

Every tool and function observed in real Emergent production trajectories — categorized, with frequency data and payload examples.

## Tool Categories Overview

```mermaid
pie title Tool Usage Distribution (Top 10)
    "execute_bash" : 480
    "apply_patch" : 445
    "view_file" : 313
    "PARALLEL_TOOLS" : 204
    "create_file" : 77
    "screenshot_tool" : 74
    "browser_automation" : 70
    "view_bulk" : 67
    "search_replace" : 63
    "finish" : 46
```

## Core Tools (High Frequency)

| Tool | Count | Description |
|------|-------|-------------|
| `execute_bash` | 480 | Execute shell commands in the Linux container |
| `apply_patch` | 445 | Apply unified diff patches to existing files |
| `view_file` | 313 | Read file contents (supports line ranges) |
| `PARALLEL_TOOLS` | 204 | Wrapper for concurrent tool execution |
| `create_file` | 77 | Create a new file with specified content |
| `screenshot_tool` | 74 | Capture browser screenshots for visual inspection |
| `browser_automation` | 70 | Control Playwright browser (click, type, navigate) |
| `view_bulk` | 67 | Read multiple files in one call |
| `search_replace` | 63 | Find and replace text in files |
| `finish` | 46 | Signal job completion with summary message |
| `ask_human` | 26 | Ask the user a question and wait for response |
| `glob_files` | 23 | Search for files matching a glob pattern |

### execute_bash Example
```json
{
  "name": "execute_bash",
  "input": {
    "command": "cd /app && npm install react-router-dom"
  }
}
```

### apply_patch Example
```json
{
  "name": "apply_patch",
  "input": {
    "patch": "--- a/src/App.js\\n+++ b/src/App.js\\n@@ -10,3 +10,5 @@\\n import React from 'react';\\n+import { BrowserRouter } from 'react-router-dom';\\n"
  }
}
```

### create_file Example
```json
{
  "name": "create_file",
  "input": {
    "file_path": "/app/frontend/src/components/Header.jsx",
    "content": "import React from 'react';\\n\\nexport default function Header() {\\n  return <header>My App</header>;\\n}"
  }
}
```

## Linting Tools

| Tool | Count | Description |
|------|-------|-------------|
| `lint_javascript` | 19 | Run ESLint on JavaScript/React files |
| `lint_python` | 17 | Run flake8/pylint on Python files |

These are triggered automatically after code changes to catch syntax errors early.

## Reasoning Tool

| Tool | Count | Description |
|------|-------|-------------|
| `think` | 16 | Internal reasoning step — no external action |

The `think` tool allows the agent to reason through complex decisions without executing any action. It's recorded in the trajectory but produces no side effects.

## Sub-Agent Delegation Tools (7 tools)

These tools trigger `TRANSITION_MAIN_TO_SUB` — spawning a specialized sub-agent:

| Tool | Count | Purpose | Sub-Agent Model |
|------|-------|---------|-----------------|
| `design_agent_full_stack` | 12 | UI/UX design decisions | gemini-3-pro-preview |
| `testing_agent` | 12 | Run tests (original, Codex-based) | gpt-5.3-codex |
| `testing_agent_v3` | 3 | Run tests (v3, Sonnet 4) | claude-sonnet-4 |
| `testing_agent_v3_fork` | 2 | Run tests (v3 fork, Opus) | claude-opus-4-5 |
| `auto_frontend_testing_agent` | 2 | Automated Playwright frontend tests | claude-sonnet-4-5 |
| `deep_testing_backend_v2` | 1 | Deep backend testing (rare) | varies |
| `support_agent` | 2 | User support/communication (rare) | varies |

### Delegation Flow
```json
{
  "name": "testing_agent",
  "input": {
    "instructions": "Run all unit tests for the budget tracking module and fix any failures"
  }
}
```

When this tool is called:
1. The trajectory records `execution_mode = TRANSITION_MAIN_TO_SUB`
2. A SkilledAssistant is spawned with the appropriate expertise type
3. The sub-agent runs its own agent loop (multiple steps)
4. When done, `TRANSITION_SUB_TO_MAIN` returns control

## Specialized Tools

| Tool | Count | Description |
|------|-------|-------------|
| `integration_playbook_expert_v2` | 7 | Integration testing playbook execution |
| `image_selector_tool` | 8 | Select and process images for the app |
| `web_search_tool_v2` | 2 | Search the web for information |
| `image_generation_tool` | 1 | Generate images using AI |
| `insert_text` | 1 | Insert text at a specific position in a file |

## System Events (Not User-Callable)

These appear in trajectories but are platform events, not agent-initiated tools:

| Function | Count | Description |
|----------|-------|-------------|
| `initial-llm` | 16 | First LLM call of an agent session |
| `default_tool` | 8 | Transition/placeholder step |
| `exit_cost_credit_limit_reached` | 7 | Job paused — user ran out of credits |
| `auto_compact` | 5 | Context compaction triggered |
| `ENV_CREATION_FAILED` | 2 | Container environment failed to start |
| `pause` | 1 | Job manually paused by user |

### exit_cost_credit_limit_reached
When credits run out, the agent records this event and sets `model_name = None`. The job resumes when the user adds more credits.

### ENV_CREATION_FAILED
The Linux container failed to start. This is an infrastructure error — the agent cannot proceed until the environment is recreated.

## PARALLEL_TOOLS Deep Dive

When the LLM returns multiple tool calls, they are batched:

```json
{
  "function_name": "PARALLEL_TOOLS",
  "traj_payload": {
    "parallel_tool_calls": [
      {"id": "tool_1", "name": "view_file", "input": {"file_path": "/app/src/App.js"}},
      {"id": "tool_2", "name": "view_file", "input": {"file_path": "/app/src/index.js"}},
      {"id": "tool_3", "name": "view_file", "input": {"file_path": "/app/src/styles.css"}}
    ]
  }
}
```

The platform executes all three `view_file` calls concurrently, then returns all results to the LLM in the next iteration.
"""
    },

    # --- Doc 7: Sub-Agent Delegation — 7 Delegation Paths ---
    {
        "id": _id(), "title": "Sub-Agent Delegation — 7 Delegation Paths", "category_id": SUB_TOOLS_DELEG, "author_id": SYSTEM_AUTHOR,
        "created_at": NOW, "updated_at": NOW, "order": 1,
        "content": """# Sub-Agent Delegation — 7 Delegation Paths

How the main agent delegates to specialized sub-agents, the transition mechanism, and details of all 7 delegation paths observed in production.

## The Delegation Mechanism

```mermaid
sequenceDiagram
    participant Main as EmergentAssistant<br/>(Main Agent)
    participant Platform as Emergent Platform
    participant Sub as SkilledAssistant<br/>(Sub-Agent)

    Main->>Platform: Call delegation tool<br/>(e.g., testing_agent)
    Note over Platform: TRANSITION_MAIN_TO_SUB
    Platform->>Sub: Spawn sub-agent<br/>with expertise_type & model
    loop Sub-Agent Loop
        Sub->>Sub: LLM call → tool execution → result
    end
    Sub->>Platform: Sub-agent calls finish
    Note over Platform: TRANSITION_SUB_TO_MAIN
    Platform->>Main: Return sub-agent results
    Main->>Main: Continue with results
```

## The 7 Delegation Paths

### 1. design_agent_full_stack (12 invocations)

**Purpose:** UI/UX design decisions — layout, color schemes, component structure, responsive design.

| Field | Value |
|-------|-------|
| Sub-Agent Expertise | `design_agent_full_stack_gemini_3_pro` |
| Model | `gemini-3-pro-preview` |
| Trigger | Main agent needs design guidance |
| Reference File | `design_guidelines.json` |

**Why Gemini?** The design agent uses Google's Gemini for its strong multimodal capabilities — it can reason about visual layouts and design patterns effectively.

**Typical invocation:**
```json
{
  "name": "design_agent_full_stack",
  "input": {
    "instructions": "Design the dashboard layout for the budget tracking app. Include a sidebar navigation, header with user info, and main content area with charts."
  }
}
```

### 2. testing_agent (12 invocations)

**Purpose:** Write and execute tests using the original Codex-based testing agent.

| Field | Value |
|-------|-------|
| Sub-Agent Expertise | `testing_agent_codex_5_3` |
| Model | `gpt-5.3-codex` |
| Tools Available | execute_bash, view_file, apply_patch, screenshot_tool, browser_automation |

### 3. testing_agent_v3 (3 invocations)

**Purpose:** Next-generation testing with Claude Sonnet 4.

| Field | Value |
|-------|-------|
| Sub-Agent Expertise | `testing_agent_v3_sonnet_4` |
| Model | `claude-sonnet-4-20250514` |
| Improvements | Better test planning, more thorough coverage |

### 4. testing_agent_v3_fork (2 invocations)

**Purpose:** Advanced testing with Claude Opus — the most capable testing agent.

| Field | Value |
|-------|-------|
| Sub-Agent Expertise | `testing_agent_v3_fork_opus_4_5` |
| Model | `claude-opus-4-5-20251101` |
| Use Case | Complex test scenarios requiring deep reasoning |

### 5. auto_frontend_testing_agent (2 invocations)

**Purpose:** Automated Playwright frontend testing with screenshot comparison.

| Field | Value |
|-------|-------|
| Sub-Agent Expertise | `auto_frontend_testing_agent_sonnet_3_7` |
| Model | `claude-sonnet-4-5-20250929` |
| Tools | browser_automation, screenshot_tool, execute_bash |
| Specialty | Visual regression testing, automated UI interaction |

### 6. deep_testing_backend_v2 (1 invocation)

**Purpose:** Deep backend testing — rare but intensive.

| Field | Value |
|-------|-------|
| Frequency | Very rare (1 observed) |
| Focus | Backend API testing, database integrity, edge cases |

### 7. support_agent (2 invocations)

**Purpose:** User support and communication.

| Field | Value |
|-------|-------|
| Frequency | Rare (2 observed) |
| Focus | Formatting user-facing messages, clarifying requirements |

## How Many Testing Agents Can Run in One Job?

In the budget-insights-io job (2abc6159), **three different testing agents** ran in sequence:

```mermaid
gantt
    title Testing Agent Sequence in Job 2abc6159
    dateFormat HH:mm
    axisFormat %H:%M
    section Testing
    testing_agent (Codex)        :t1, 12:00, 30min
    testing_agent_v3_fork (Opus) :t2, 15:00, 15min
    auto_frontend (Sonnet 4.5)   :t3, 15:20, 30min
```

The platform selects different testing agents based on what type of testing is needed at that point in the job.

## Transition Tracking in the Database

Every delegation creates trajectory entries with specific execution modes:

```sql
-- Find all delegation events for a job
SELECT step_id, function_name, execution_mode, model_name, created_at
FROM trajectories
WHERE job_id = 'your-job-id'
  AND execution_mode IN ('TRANSITION_MAIN_TO_SUB', 'TRANSITION_SUB_TO_MAIN')
ORDER BY step_id;
```

Expected output pattern:
```
step  | function_name            | execution_mode           | model
------+--------------------------+--------------------------+------------------
35    | testing_agent            | TRANSITION_MAIN_TO_SUB   | gpt-5.3-codex
61    | finish                   | TRANSITION_SUB_TO_MAIN   | gpt-5.3-codex
275   | testing_agent_v3_fork    | TRANSITION_MAIN_TO_SUB   | claude-opus-4-5
290   | finish                   | TRANSITION_SUB_TO_MAIN   | claude-opus-4-5
```
"""
    },

    # --- Doc 8: Predefined vs Agent-Created Files ---
    {
        "id": _id(), "title": "Predefined vs Agent-Created Files", "category_id": SUB_TOOLS_DELEG, "author_id": SYSTEM_AUTHOR,
        "created_at": NOW, "updated_at": NOW, "order": 2,
        "content": """# Predefined vs Agent-Created Files

The Emergent container comes with a base image containing predefined files. The agent then creates, modifies, and extends these files during a job.

## The Base Image

Every job starts in a **Linux container** with a predefined file structure:

```
/app/
├── frontend/
│   ├── src/
│   │   ├── App.js          (React 19 entry point)
│   │   ├── index.js         (ReactDOM render)
│   │   └── index.css        (Global styles)
│   ├── package.json         (React 19 + dependencies)
│   ├── tailwind.config.js   (Tailwind CSS configuration)
│   └── postcss.config.js    (PostCSS configuration)
├── backend/
│   ├── server.py            (FastAPI server)
│   └── requirements.txt     (Python dependencies)
├── package.json             (Root package.json for monorepo)
├── .env                     (Environment variables)
└── start.sh                 (Startup script)
```

## Predefined Files — What's Already There

### Frontend Stack
- **React 19** with functional components and hooks
- **Tailwind CSS** for styling
- **ShadCN UI** components (pre-installed)
- **Lucide React** icons
- **Vite** as the build tool

### Backend Stack
- **FastAPI** (Python) with CORS, static file serving
- **MongoDB** (motor async driver)
- **Uvicorn** as the ASGI server

### Key Configuration
- The frontend proxies API calls to the backend via Vite's proxy config
- The backend serves the frontend build as static files in production
- MongoDB runs locally in the container

## What the Agent Creates

During a typical job, the agent creates **50–200+ new files**:

| Category | Examples |
|----------|---------|
| React components | `Header.jsx`, `Dashboard.jsx`, `Sidebar.jsx` |
| API routes | New endpoints in `server.py` or separate route files |
| Database models | MongoDB collection schemas, seed data |
| Styles | Additional CSS files, component-specific styles |
| Tests | `test_api.py`, `test_frontend.spec.js` |
| Config | `.prettierrc`, `jest.config.js` |
| Assets | Downloaded images via `image_selector_tool` |

## The System Prompt Template

The agent's system prompt includes instructions about the predefined environment:

```
You are building a full-stack web application.
The project structure is already set up at /app/ with:
- Frontend: React 19 + Tailwind + ShadCN at /app/frontend/
- Backend: FastAPI + MongoDB at /app/backend/
- The app is running and accessible in the browser.

IMPORTANT:
- Do NOT delete or recreate the base files — extend them.
- Use the existing package.json dependencies before installing new ones.
- The ShadCN components are already available — import them directly.
```

## How the Agent Extends vs Replaces

The agent follows a pattern of **extending** predefined files rather than replacing them:

1. **App.js** — The agent adds new routes, components, and state management to the existing React app structure
2. **server.py** — New API endpoints are added alongside the existing FastAPI routes
3. **package.json** — New dependencies are `npm install`ed, adding to the existing list

However, the agent **may rewrite** files entirely when:
- The predefined content doesn't match the requirements
- A complete restructuring is needed
- The file is simple enough to regenerate (e.g., `index.css`)

## Tool Usage for File Operations

| Operation | Primary Tool | Fallback |
|-----------|-------------|----------|
| Create new file | `create_file` | `execute_bash` (echo/cat) |
| Modify existing file | `apply_patch` | `search_replace` |
| Read file | `view_file` | `view_bulk` (multiple files) |
| Delete file | `execute_bash` (rm) | — |
| Rename/move | `execute_bash` (mv) | — |
| Find files | `glob_files` | `execute_bash` (find) |
"""
    },

    # --- Doc 9: Trajectory Database Schema ---
    {
        "id": _id(), "title": "Trajectory Database Schema", "category_id": SUB_TRAJ_DEBUG, "author_id": SYSTEM_AUTHOR,
        "created_at": NOW, "updated_at": NOW, "order": 0,
        "content": """# Trajectory Database Schema

The complete database schema for Emergent's trajectory system — the tables, columns, and JSONB payloads that store every agent action.

## Core Tables

### trajectories (15 columns)

The main table — one row per agent step.

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID | Primary key |
| `job_id` | UUID | Which job this belongs to |
| `step_id` | INTEGER | Sequential step number (0, 1, 2, ...) |
| `agent_name` | VARCHAR | "EmergentAssistant" or "SkilledAssistant" |
| `expertise_type` | VARCHAR | e.g., "full_stack_app_builder_cloud_v8_codex_5_3" |
| `model_name` | VARCHAR | e.g., "gpt-5.3-codex" (NULL during pause/credit limit) |
| `function_name` | VARCHAR | Tool called (e.g., "execute_bash", "apply_patch") |
| `execution_mode` | VARCHAR | "SKIP", "TRANSITION_MAIN_TO_SUB", "TRANSITION_SUB_TO_MAIN" |
| `traj_payload` | JSONB | Full payload — tool input, output, metadata |
| `created_at` | TIMESTAMP | When this step was recorded |
| `updated_at` | TIMESTAMP | Last update time |
| `duration_ms` | INTEGER | How long this step took |
| `token_usage` | JSONB | Token counts for the LLM call |
| `error` | JSONB | Error details (NULL if successful) |
| `metadata` | JSONB | Additional metadata |

### actions_observations (23 columns)

Detailed action-observation pairs with more granular data.

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID | Primary key |
| `trajectory_id` | UUID | FK to trajectories |
| `job_id` | UUID | Which job |
| `step_id` | INTEGER | Step number |
| `action_type` | VARCHAR | "tool_call" or "tool_result" |
| `tool_name` | VARCHAR | Tool name |
| `tool_input` | JSONB | Input parameters sent to the tool |
| `tool_output` | JSONB | Output returned by the tool |
| `tool_is_error` | BOOLEAN | Whether the tool execution errored |
| `thinking` | TEXT | LLM's internal reasoning |
| `text_output` | TEXT | Any text response from the LLM |
| `model_name` | VARCHAR | Model used |
| `input_tokens` | INTEGER | Input token count |
| `output_tokens` | INTEGER | Output token count |
| `cache_creation_tokens` | INTEGER | Tokens used for cache creation |
| `cache_read_tokens` | INTEGER | Tokens read from cache |
| `total_cost` | DECIMAL | Cost of this LLM call |
| `duration_ms` | INTEGER | Duration in milliseconds |
| `stop_reason` | VARCHAR | "tool_use", "end_turn", "max_tokens" |
| `created_at` | TIMESTAMP | When recorded |
| `updated_at` | TIMESTAMP | Last update |
| `error` | JSONB | Error details |
| `metadata` | JSONB | Additional metadata |

### job_metadata

Job-level configuration — critical for understanding model routing.

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID | Job ID (primary key) |
| `model_name` | VARCHAR | Configured model (e.g., "gpt-5.3-codex?reasoning_effort=high") |
| `prompt_name` | VARCHAR | Prompt configuration (e.g., "infinite_fullstack_codex_5_3") |
| `parent_job_id` | UUID | Parent job (for forked jobs) |
| `root_job_id` | UUID | Root of the job chain |
| `status` | VARCHAR | "IN_PROGRESS", "COMPLETED", "FAILED" |
| `created_at` | TIMESTAMP | When the job started |
| `updated_at` | TIMESTAMP | Last update |
| `title` | VARCHAR | User-given job title |
| `metadata` | JSONB | Additional job metadata |

## The traj_payload JSONB

The `traj_payload` column contains the full context of each step. Structure varies by `function_name`:

### For tool calls (e.g., execute_bash)
```json
{
  "tool_call_id": "toolu_abc123",
  "name": "execute_bash",
  "input": {
    "command": "cd /app && npm test"
  },
  "output": {
    "stdout": "PASS src/App.test.js\\n  4 tests passed",
    "stderr": "",
    "exit_code": 0
  },
  "thinking": "I need to run the tests to verify my changes work correctly..."
}
```

### For PARALLEL_TOOLS
```json
{
  "parallel_tool_calls": [
    {"id": "tool_1", "name": "view_file", "input": {"file_path": "/app/src/App.js"}},
    {"id": "tool_2", "name": "view_file", "input": {"file_path": "/app/src/index.js"}}
  ],
  "parallel_results": [
    {"id": "tool_1", "output": "...file contents..."},
    {"id": "tool_2", "output": "...file contents..."}
  ]
}
```

### For auto_compact
```json
{
  "summary": "Compacted conversation from 186 steps. The agent was building a budget tracking app with React frontend and FastAPI backend...",
  "original_step_count": 186,
  "compressed_token_count": 4500
}
```

## Useful SQL Queries for QA

### Job overview — all steps with models
```sql
SELECT step_id, function_name, model_name, execution_mode,
       duration_ms, created_at
FROM trajectories
WHERE job_id = 'your-job-id'
ORDER BY step_id;
```

### Find all sub-agent delegations
```sql
SELECT step_id, function_name, execution_mode, model_name
FROM trajectories
WHERE job_id = 'your-job-id'
  AND execution_mode != 'SKIP'
ORDER BY step_id;
```

### Token usage per step
```sql
SELECT step_id, function_name, model_name,
       token_usage->>'input_tokens' AS input,
       token_usage->>'output_tokens' AS output,
       token_usage->>'cache_read_input_tokens' AS cached
FROM trajectories
WHERE job_id = 'your-job-id'
ORDER BY step_id;
```

### Find errors
```sql
SELECT step_id, function_name, error, model_name
FROM trajectories
WHERE job_id = 'your-job-id'
  AND error IS NOT NULL
ORDER BY step_id;
```

### Count tool usage per job
```sql
SELECT function_name, COUNT(*) as usage_count
FROM trajectories
WHERE job_id = 'your-job-id'
GROUP BY function_name
ORDER BY usage_count DESC;
```
"""
    },

    # --- Doc 10: Reading Debug Logs ---
    {
        "id": _id(), "title": "Reading Debug Logs", "category_id": SUB_TRAJ_DEBUG, "author_id": SYSTEM_AUTHOR,
        "created_at": NOW, "updated_at": NOW, "order": 1,
        "content": """# Reading Debug Logs

How to use Chrome DevTools to inspect Emergent's real-time trajectory streaming, debug JSON logs, and token analysis.

## Where Debug Data Lives

Debug data is accessible in two places:

1. **Browser Debug Panel** — Real-time view in the Emergent UI (click "Debug" button)
2. **Chrome DevTools** — Network tab shows raw SSE streams and API calls

## Chrome DevTools — Network Tab

### Trajectory Streaming (SSE)

Open DevTools → Network → Filter by "EventStream".

You'll see a long-lived connection that streams trajectory events:

```
Request URL: https://app.emergent.sh/api/v1/jobs/{job_id}/trajectories/stream
Request Method: GET
Status: 200
Type: eventsource
```

Each event in the stream:
```
data: {"type": "trajectory", "step_id": 42, "function_name": "execute_bash", "model_name": "gpt-5.3-codex", ...}

data: {"type": "trajectory", "step_id": 43, "function_name": "apply_patch", "model_name": "gpt-5.3-codex", ...}
```

### Debug JSON Log

The debug panel shows the full LLM call details. Each entry contains:

```json
{
  "llm_call_id": "call_abc123",
  "model": "gpt-5.3-codex",
  "step_id": 42,
  "duration_ms": 8500,
  "status": "success",
  "body": {
    "model": "gpt-5.3-codex",
    "system": [{"type": "text", "text": "You are an AI assistant...", "cache_control": {"type": "ephemeral"}}],
    "messages": ["... full conversation history ..."],
    "tools": ["... tool definitions ..."],
    "max_tokens": 64000,
    "temperature": 1,
    "stream": true
  },
  "response": {
    "content": [
      {"type": "thinking", "text": "I need to fix the CSS layout..."},
      {"type": "tool_use", "name": "apply_patch", "input": {"patch": "..."}}
    ],
    "stop_reason": "tool_use",
    "usage": {
      "input_tokens": 45000,
      "output_tokens": 3500,
      "cache_creation_input_tokens": 0,
      "cache_read_input_tokens": 39600
    }
  }
}
```

## How to Trace a Request End-to-End

### Step 1: Find the trajectory step
In the Emergent UI, note the step number you want to investigate.

### Step 2: Open DevTools Network tab
Filter for XHR or Fetch requests. Look for calls to:
- `/api/v1/jobs/{job_id}/trajectories` — full trajectory list
- `/api/v1/jobs/{job_id}/debug` — debug log for a specific step

### Step 3: Check the request body
In the debug log, expand `body.messages` to see the full conversation context sent to the LLM. The **last message** is what triggered this response.

### Step 4: Check the response
Expand `response.content` to see:
- `thinking` blocks — the model's reasoning
- `tool_use` blocks — what tool was called and with what input

### Step 5: Check token usage
```
input_tokens: 45,000  (total input)
cache_read:   39,600  (from cache — 88%)
fresh input:   5,400  (new content — 12%)
output_tokens: 3,500  (model's response)
```

## Chrome DevTools — Application Tab

### localStorage
Emergent stores some client-side data:
- Session preferences
- UI state (sidebar collapsed, dark mode)
- Debug panel settings

### Cookies
- Authentication tokens
- Session IDs

## Chrome DevTools — Console Tab

Watch for:
- SSE connection errors (lost trajectory stream)
- WebSocket reconnection messages
- API error responses (4xx, 5xx)

## Token Analysis Techniques

### Calculate cache hit rate
```
cache_hit_rate = cache_read_input_tokens / input_tokens * 100
```

### Estimate cost per step
```
cost = (fresh_input_tokens * input_price) + (cached_tokens * cached_price) + (output_tokens * output_price)
```

Where cached_price is typically ~10% of input_price.

### Track context growth
Plot `input_tokens` over step_id — you'll see a growing curve as the conversation accumulates. When `auto_compact` fires, the token count drops sharply.

```
Step 0:   input_tokens = 23,000  (system + tools + first message)
Step 50:  input_tokens = 85,000  (growing conversation)
Step 100: input_tokens = 156,000 (approaching limit)
Step 101: auto_compact! input_tokens drops to 28,000
Step 102: input_tokens = 29,000  (fresh start with summary)
```
"""
    },

    # --- Doc 13: SQL Query Cookbook for Trajectory Analysis ---
    {
        "id": _id(), "title": "SQL Query Cookbook for Trajectory Analysis", "category_id": SUB_TRAJ_DEBUG, "author_id": SYSTEM_AUTHOR,
        "created_at": NOW, "updated_at": NOW, "order": 2,
        "content": """# SQL Query Cookbook for Trajectory Analysis

Battle-tested SQL queries used during real production investigations against the Emergent postgres-spark database. Each query includes what it reveals and when to use it.

---

## 1. Full Agent & Model Taxonomy

**When to use:** You need to understand the complete universe of agents, models, and tools available on the platform — not just for one job, but across all jobs.

```sql
SELECT
    agent_name,
    expertise_type,
    model_name,
    function_name,
    COUNT(*) AS invocation_count
FROM trajectories
GROUP BY agent_name, expertise_type, model_name, function_name
ORDER BY agent_name, expertise_type, model_name, invocation_count DESC;
```

**What it reveals:**
- Every distinct agent + expertise + model + tool combination ever used
- How frequently each tool is invoked per agent configuration
- Experimental model names (galapagos-alpha, macaroni-alpha) tied to their expertise types
- Real data returned 132 distinct combinations across the platform

---

## 2. Trace Model Changes Across a Job

**When to use:** You suspect the model changed mid-job (e.g., after auto_compact) and need to find exactly where.

```sql
SELECT
    step_id,
    created_at,
    model_name,
    function_name,
    execution_mode
FROM trajectories
WHERE job_id = 'your-job-id'
ORDER BY step_id;
```

**What to look for:**
- A row where `model_name` changes from one value to another
- The step right before the change often has `function_name = 'auto_compact'`
- Steps where `model_name IS NULL` indicate a credit limit hit or pause

**Pro tip:** Wrap this in a window function to auto-detect changes:

```sql
SELECT step_id, model_name, function_name, created_at,
       LAG(model_name) OVER (ORDER BY step_id) AS prev_model
FROM trajectories
WHERE job_id = 'your-job-id'
ORDER BY step_id;
```

Then filter for rows where `model_name != prev_model`.

---

## 3. Distinct Models Used in a Specific Job

**When to use:** Quick check — how many and which models were involved in a single job.

```sql
SELECT DISTINCT model_name,
       MIN(step_id) AS first_step,
       MAX(step_id) AS last_step,
       COUNT(*) AS step_count
FROM trajectories
WHERE job_id = 'your-job-id'
GROUP BY model_name
ORDER BY first_step;
```

**What it reveals:**
- Every model that touched the job
- The step range where each model was active
- How many steps each model handled
- NULL model_name rows indicate paused/credit-limited periods

---

## 4. All Sub-Agent Delegations in a Job

**When to use:** You want to see every time the main agent handed off to a sub-agent, which sub-agent ran, and when control returned.

```sql
SELECT
    step_id,
    function_name,
    execution_mode,
    agent_name,
    expertise_type,
    model_name,
    created_at
FROM trajectories
WHERE job_id = 'your-job-id'
  AND execution_mode IN ('TRANSITION_MAIN_TO_SUB', 'TRANSITION_SUB_TO_MAIN')
ORDER BY step_id;
```

**Expected output pattern:**
```
step | function_name            | execution_mode           | agent_name       | model
-----+--------------------------+--------------------------+------------------+------------------
35   | testing_agent            | TRANSITION_MAIN_TO_SUB   | SkilledAssistant | gpt-5.3-codex
61   | finish                   | TRANSITION_SUB_TO_MAIN   | SkilledAssistant | gpt-5.3-codex
275  | testing_agent_v3_fork    | TRANSITION_MAIN_TO_SUB   | SkilledAssistant | claude-opus-4-5
290  | finish                   | TRANSITION_SUB_TO_MAIN   | SkilledAssistant | claude-opus-4-5
```

**What it reveals:**
- Which delegation tool was used (testing_agent, design_agent_full_stack, etc.)
- Which model the sub-agent ran with
- How many steps the sub-agent took (gap between MAIN_TO_SUB and SUB_TO_MAIN)
- Imbalances (more MAIN_TO_SUB than SUB_TO_MAIN means a sub-agent was still active)

---

## 5. Tool Usage Frequency Per Job

**When to use:** You want a breakdown of which tools the agent used most heavily in a specific job.

```sql
SELECT
    function_name,
    COUNT(*) AS usage_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 1) AS pct
FROM trajectories
WHERE job_id = 'your-job-id'
GROUP BY function_name
ORDER BY usage_count DESC;
```

**What it reveals:**
- The agent's tool usage pattern for this specific app
- Whether the job was code-heavy (lots of apply_patch, create_file) vs debug-heavy (lots of execute_bash, view_file)
- How many PARALLEL_TOOLS batches occurred
- Whether sub-agent delegation tools were invoked

---

## 6. Job Metadata & Configuration Lookup

**When to use:** You need to find the configured model and prompt for a job — especially to understand auto_compact behavior.

```sql
SELECT
    id AS job_id,
    title,
    model_name,
    prompt_name,
    status,
    parent_job_id,
    root_job_id,
    created_at
FROM job_metadata
WHERE id = 'your-job-id';
```

**Critical insight:** The `model_name` here is what auto_compact fork agents use. If this differs from the runtime model (e.g., job_metadata says `gpt-5.3-codex` but the agent was running `galapagos-alpha`), a model change WILL occur after auto_compact.

---

## 7. Find All Errors in a Job

**When to use:** Something went wrong and you need to find every error event.

```sql
SELECT
    step_id,
    function_name,
    model_name,
    error::text AS error_detail,
    created_at
FROM trajectories
WHERE job_id = 'your-job-id'
  AND (error IS NOT NULL OR function_name IN (
    'exit_cost_credit_limit_reached',
    'ENV_CREATION_FAILED',
    'auto_compact'
  ))
ORDER BY step_id;
```

**What it reveals:**
- All explicit errors (LLM timeouts, tool failures)
- Credit limit events (even though they may not have error field set)
- Environment creation failures
- auto_compact events (not errors per se, but often significant)

---

## 8. Timeline of All Events for a Job

**When to use:** You want a complete chronological view of a job — ideal for building a timeline or Gantt chart.

```sql
SELECT
    step_id,
    created_at,
    function_name,
    agent_name,
    model_name,
    execution_mode,
    duration_ms,
    CASE
        WHEN function_name = 'auto_compact' THEN 'COMPACTION'
        WHEN function_name = 'exit_cost_credit_limit_reached' THEN 'CREDIT_LIMIT'
        WHEN function_name = 'ENV_CREATION_FAILED' THEN 'ENV_FAILURE'
        WHEN function_name = 'pause' THEN 'PAUSED'
        WHEN execution_mode = 'TRANSITION_MAIN_TO_SUB' THEN 'DELEGATION_START'
        WHEN execution_mode = 'TRANSITION_SUB_TO_MAIN' THEN 'DELEGATION_END'
        WHEN function_name = 'finish' THEN 'FINISHED'
        WHEN function_name = 'ask_human' THEN 'WAITING_FOR_USER'
        ELSE 'NORMAL'
    END AS event_type
FROM trajectories
WHERE job_id = 'your-job-id'
ORDER BY step_id;
```

**What it reveals:**
- Full chronological timeline with human-readable event types
- Duration of each step (useful for finding slow LLM calls)
- Clear markers for delegation boundaries, pauses, and failures

---

## 9. All Distinct Expertise Types & Their Models (Platform-Wide)

**When to use:** You need to document which expertise types exist and what models they map to.

```sql
SELECT
    agent_name,
    expertise_type,
    ARRAY_AGG(DISTINCT model_name) AS models,
    COUNT(*) AS total_steps
FROM trajectories
WHERE model_name IS NOT NULL
GROUP BY agent_name, expertise_type
ORDER BY agent_name, total_steps DESC;
```

**What it reveals:**
- Every expertise type in the platform
- Which models each expertise type has been routed to (including experimental ones)
- Relative frequency (how often each expertise is used)
- Multi-model routing: same expertise → multiple models (A/B testing)

---

## 10. Count Trajectories Per Job (Find Large/Problematic Jobs)

**When to use:** You want to identify the longest or most complex jobs.

```sql
SELECT
    t.job_id,
    jm.title,
    jm.model_name AS configured_model,
    COUNT(*) AS step_count,
    COUNT(DISTINCT t.model_name) AS models_used,
    MIN(t.created_at) AS started_at,
    MAX(t.created_at) AS last_activity,
    EXTRACT(EPOCH FROM (MAX(t.created_at) - MIN(t.created_at))) / 3600 AS duration_hours
FROM trajectories t
LEFT JOIN job_metadata jm ON t.job_id::text = jm.id::text
GROUP BY t.job_id, jm.title, jm.model_name
ORDER BY step_count DESC
LIMIT 20;
```

**What it reveals:**
- The largest jobs by step count
- Which jobs used multiple models
- Job duration in hours
- Configured model vs actual models used

---

## 11. All Delegation Tool Usage (Platform-Wide)

**When to use:** You want to see how often each sub-agent delegation tool is invoked across the platform.

```sql
SELECT
    function_name AS delegation_tool,
    COUNT(*) AS invocations,
    COUNT(DISTINCT job_id) AS distinct_jobs,
    ARRAY_AGG(DISTINCT model_name) AS models_used
FROM trajectories
WHERE function_name IN (
    'testing_agent', 'testing_agent_v3', 'testing_agent_v3_fork',
    'auto_frontend_testing_agent', 'deep_testing_backend_v2',
    'support_agent', 'design_agent_full_stack'
)
GROUP BY function_name
ORDER BY invocations DESC;
```

**What it reveals:**
- Which sub-agent delegation tools are used most
- How many distinct jobs use each delegation tool
- Which models the sub-agents run on

---

## 12. Detect auto_compact Model Switches

**When to use:** You want to find ALL jobs where auto_compact caused a model change — not just one job, but platform-wide.

```sql
WITH model_changes AS (
    SELECT
        job_id,
        step_id,
        model_name,
        LAG(model_name) OVER (PARTITION BY job_id ORDER BY step_id) AS prev_model,
        function_name
    FROM trajectories
    WHERE model_name IS NOT NULL
)
SELECT
    mc.job_id,
    jm.title,
    mc.step_id,
    mc.prev_model,
    mc.model_name AS new_model,
    mc.function_name
FROM model_changes mc
LEFT JOIN job_metadata jm ON mc.job_id::text = jm.id::text
WHERE mc.prev_model IS NOT NULL
  AND mc.model_name != mc.prev_model
ORDER BY mc.job_id, mc.step_id;
```

**What it reveals:**
- Every model switch across all jobs
- The exact step where the switch happened
- What the previous and new models were
- Which function triggered the switch (usually auto_compact or a delegation)

---

## 13. Token Usage Analysis Per Job

**When to use:** You want to analyze token consumption, cache efficiency, and cost indicators for a job.

```sql
SELECT
    step_id,
    function_name,
    model_name,
    (token_usage->>'input_tokens')::int AS input_tokens,
    (token_usage->>'output_tokens')::int AS output_tokens,
    (token_usage->>'cache_read_input_tokens')::int AS cached_tokens,
    CASE
        WHEN (token_usage->>'input_tokens')::int > 0 THEN
            ROUND((token_usage->>'cache_read_input_tokens')::numeric /
                  (token_usage->>'input_tokens')::numeric * 100, 1)
        ELSE 0
    END AS cache_hit_pct
FROM trajectories
WHERE job_id = 'your-job-id'
  AND token_usage IS NOT NULL
ORDER BY step_id;
```

**What it reveals:**
- Per-step token consumption
- Cache hit rate trend (should be 80-90% after the first few steps)
- Context growth over time (input_tokens increases each step)
- When auto_compact fires (input_tokens drops dramatically)

---

## Quick Reference: Connection Details

```
Host: 10.0.2.3
Port: 6544
Database: postgres-spark
User: postgres

# Python (psycopg2)
import psycopg2
conn = psycopg2.connect(
    host='10.0.2.3', port=6544,
    dbname='postgres-spark', user='postgres',
    password='<your-password>'
)
```

> **Note:** Replace `'your-job-id'` in all queries with the actual UUID of the job you're investigating.
"""
    },

    # --- Doc 11: When Things Go Wrong ---
    {
        "id": _id(), "title": "When Things Go Wrong", "category_id": SUB_FAILURE_RECOVERY, "author_id": SYSTEM_AUTHOR,
        "created_at": NOW, "updated_at": NOW, "order": 0,
        "content": """# When Things Go Wrong

Six failure patterns observed in real Emergent production jobs — what causes them, how the platform recovers, and how to identify them in trajectory data.

## Failure Pattern Overview

```mermaid
flowchart TD
    subgraph Failures["6 Failure Patterns"]
        F1["HTTP 500/429<br/>LLM API errors"]
        F2["tool_is_error<br/>Tool execution failures"]
        F3["max_tokens<br/>Response truncation"]
        F4["auto_compact<br/>Model change"]
        F5["Credit limit<br/>exit_cost_credit_limit_reached"]
        F6["ENV_CREATION_FAILED<br/>Container start failure"]
    end

    subgraph Recovery["Recovery Mechanisms"]
        R1["Automatic retry<br/>(with backoff)"]
        R2["Agent self-corrects<br/>(reads error, tries again)"]
        R3["auto_compact<br/>(compress context)"]
        R4["Fork agent<br/>(new agent instance)"]
        R5["User adds credits<br/>(manual resume)"]
        R6["Environment recreated<br/>(platform retry)"]
    end

    F1 --> R1
    F2 --> R2
    F3 --> R3
    F4 --> R4
    F5 --> R5
    F6 --> R6
```

## 1. HTTP 500/429 — LLM API Errors

**What:** The LLM provider returns an error — usually rate limiting (429) or server error (500).

**Example from real data:**
```
Step -1 (13:37 UTC): CallLLM StartToClose timeout
Error: "The LLM call timed out after 120 seconds"
```

**Recovery:** The platform automatically retries with exponential backoff. Most 429 errors resolve within 30–60 seconds.

**How to spot in trajectories:**
```sql
SELECT step_id, error, created_at
FROM trajectories
WHERE job_id = 'your-job-id'
  AND error IS NOT NULL
  AND error::text LIKE '%timeout%' OR error::text LIKE '%429%' OR error::text LIKE '%500%';
```

## 2. tool_is_error — Tool Execution Failures

**What:** A tool was called but failed to execute properly.

**Common causes:**
- `execute_bash` command failed (non-zero exit code)
- `apply_patch` couldn't apply the diff (context mismatch)
- `create_file` path doesn't exist
- `browser_automation` element not found

**Recovery:** The agent reads the error output and self-corrects. This is a key capability — the agent treats tool errors as feedback and adjusts its approach.

**Example:**
```json
{
  "function_name": "execute_bash",
  "tool_is_error": true,
  "output": {
    "stderr": "ERROR: Module not found: 'react-charts'. Did you mean 'recharts'?",
    "exit_code": 1
  }
}
```
The agent's next step: `execute_bash` with `npm install recharts`.

## 3. max_tokens — Response Truncation

**What:** The LLM's response was cut off because it hit the `max_tokens` limit (typically 64,000).

**Impact:** The response may contain an incomplete tool call — JSON cut off mid-string. This means the tool cannot execute.

**Recovery:**
- For minor truncation: the agent retries with a more concise prompt
- For severe cases: `auto_compact` triggers to free context space

**How to spot:**
```sql
SELECT step_id, function_name
FROM trajectories
WHERE job_id = 'your-job-id'
  AND traj_payload->>'stop_reason' = 'max_tokens';
```

## 4. auto_compact — Model Change

**What:** Context compaction triggered, spawning a fork agent that may use a different model.

**Impact:** The model changes mid-job. Code style and approach may subtly shift.

**Real example (job 2abc6159):**
- Steps 0–186: `galapagos-alpha`
- Step 187: `auto_compact`
- Steps 189–335: `gpt-5.3-codex`

**Recovery:** The fork agent continues the job with a summarized context. It reads the summary and picks up where the previous agent left off.

**How to spot:**
```sql
SELECT step_id, function_name, model_name
FROM trajectories
WHERE job_id = 'your-job-id'
  AND function_name = 'auto_compact';
```

## 5. Credit Limit — exit_cost_credit_limit_reached

**What:** The user ran out of credits. The agent is paused.

**Impact:** `model_name` is set to `None`. The agent cannot make LLM calls.

**Real example (job 2abc6159):**
```
Step 15 (11:46 UTC): exit_cost_credit_limit_reached
Model: None
--- User adds credits ---
Step 16: Agent resumes with gpt-5.3-codex
```

**Recovery:** User adds more credits → agent resumes. The model used after resume comes from `job_metadata`.

**How to spot:**
```sql
SELECT step_id, function_name, model_name, created_at
FROM trajectories
WHERE job_id = 'your-job-id'
  AND function_name = 'exit_cost_credit_limit_reached';
```

## 6. ENV_CREATION_FAILED — Container Start Failure

**What:** The Linux container environment failed to start.

**Impact:** The agent cannot execute any tools — no bash, no file creation, nothing.

**Causes:**
- Docker/Kubernetes resource limits
- Base image pull failure
- Network connectivity issues

**Recovery:** The platform retries container creation. If it fails repeatedly, the job may need manual intervention.

**How to spot:**
```sql
SELECT step_id, function_name, error, created_at
FROM trajectories
WHERE job_id = 'your-job-id'
  AND function_name = 'ENV_CREATION_FAILED';
```

## 7. Image MIME Type Mismatch (Bonus)

**What:** The agent tried to process an image but the MIME type didn't match the actual file format.

**Real example (job 2abc6159, 14:58 UTC):**
```
400 Bad Request: PNG MIME type declared but JPEG data received
```

**Impact:** SkilledAssistant error during image processing. The agent retries with the correct format or skips the image.

## QA Checklist for Failure Analysis

When investigating a failed or problematic job:

1. **Count errors:** `SELECT COUNT(*) FROM trajectories WHERE job_id = ? AND error IS NOT NULL`
2. **Check for auto_compact:** Did the model change? How many compactions occurred?
3. **Check for credit limits:** Was the job paused? How long?
4. **Check for ENV failures:** Did the container start successfully?
5. **Check tool_is_error rate:** What percentage of tool calls failed?
6. **Check final step:** Did the job finish with `finish` tool, or did it stall?
"""
    },

    # --- Doc 12: Real Job Walkthrough — Budget Insights ---
    {
        "id": _id(), "title": "Real Job Walkthrough — Budget Insights", "category_id": SUB_FAILURE_RECOVERY, "author_id": SYSTEM_AUTHOR,
        "created_at": NOW, "updated_at": NOW, "order": 1,
        "content": """# Real Job Walkthrough — Budget Insights

An end-to-end walkthrough of a real Emergent job (2abc6159, "budget-insights-io") — 335 steps, multiple models, sub-agent delegations, and failure recovery. This maps everything from the other documents to actual trajectory data.

## Job Overview

| Field | Value |
|-------|-------|
| Job ID | `2abc6159-8d76-44f4-924e-12e5d9ec981f` |
| Title | budget-insights-io |
| Total Steps | 335 |
| Duration | ~4.5 hours (11:46 – 16:00 UTC) |
| Status | IN_PROGRESS (at time of analysis) |
| Models Used | galapagos-alpha → gpt-5.3-codex (+ testing sub-agent models) |

## Phase 1: Initialization (Steps 0–15)

```mermaid
flowchart LR
    S0["Step 0<br/>initial-llm<br/>galapagos-alpha"] --> S1["Steps 1–14<br/>Building starts<br/>create_file, execute_bash"]
    S1 --> S15["Step 15<br/>CREDIT LIMIT HIT<br/>model = None"]
    S15 -->|"User adds credits"| S16["Step 16<br/>Resume<br/>galapagos-alpha"]
```

- **Step 0:** Agent initializes with `galapagos-alpha` model
- **Steps 1–14:** Initial project setup — creating files, installing dependencies
- **Step 15 (11:46 UTC):** `exit_cost_credit_limit_reached` — credits ran out
- **Step 16:** User adds credits, agent resumes

## Phase 2: Main Development (Steps 16–186)

The longest phase — the main agent builds the budget tracking application:

| Activity | Steps | Tools Used |
|----------|-------|-----------|
| Frontend setup | 16–40 | create_file, execute_bash |
| Testing round 1 | 35–61 | testing_agent (Codex) → TRANSITION_MAIN_TO_SUB |
| Backend API | 62–100 | create_file, apply_patch, execute_bash |
| UI components | 100–150 | create_file, apply_patch, screenshot_tool |
| Integration | 150–186 | apply_patch, execute_bash, browser_automation |

**Model throughout:** `galapagos-alpha`

### First Testing Delegation (Steps 35–61)

The main agent delegates to the testing sub-agent:
1. Step 35: `testing_agent` called → `TRANSITION_MAIN_TO_SUB`
2. Steps 36–60: SkilledAssistant (testing_agent_codex_5_3) runs tests
3. Step 61: Sub-agent calls `finish` → `TRANSITION_SUB_TO_MAIN`
4. Main agent receives test results and continues

## Phase 3: auto_compact & Model Change (Steps 187–189)

The critical event:

| Step | Time | Event | Model |
|------|------|-------|-------|
| 186 | 14:35:30 | Last normal step — applying patches | galapagos-alpha |
| 187 | 14:35:31 | `auto_compact` triggered | (system) |
| 188 | 14:36:43 | Transition step (default_tool) | galapagos-alpha |
| 189 | 14:37:03 | Fork agent starts — calls `ask_human` | **gpt-5.3-codex** |

**Root cause:** `job_metadata.model_name = "gpt-5.3-codex"`. The fork agent read this instead of inheriting `galapagos-alpha`.

## Phase 4: Continued Development (Steps 189–274)

The fork agent continues building with `gpt-5.3-codex`:

| Activity | Steps | Notes |
|----------|-------|-------|
| Plan presentation | 189 | ask_human — shows user what was done and next steps |
| Continued development | 190–274 | More features, bug fixes, styling |

**LLM Timeout (13:37 UTC):** A `CallLLM StartToClose timeout` error occurred but the job auto-recovered.

**Image MIME Error (14:58 UTC):** A 400 Bad Request for PNG/JPEG mismatch during image processing. SkilledAssistant error — non-fatal.

## Phase 5: Advanced Testing (Steps 275–321)

Two more testing delegations with different models:

### Testing Round 2: Opus (Steps 275–290)
```
Step 275: testing_agent_v3_fork → TRANSITION_MAIN_TO_SUB
Model: claude-opus-4-5-20251101
Steps 276–289: Sub-agent runs tests
Step 290: finish → TRANSITION_SUB_TO_MAIN
```

### Testing Round 3: Sonnet 4.5 (Steps 293–321)
```
Step 293: auto_frontend_testing_agent → TRANSITION_MAIN_TO_SUB
Model: claude-sonnet-4-5-20250929
Steps 294–320: Automated frontend tests with screenshots
Step 321: finish → TRANSITION_SUB_TO_MAIN
```

## Phase 6: Final Steps (Steps 322–335)

| Step | Time | Event |
|------|------|-------|
| 322–325 | 15:30 | Final bug fixes and polish |
| 326 | 15:36 | `pause` — model set to None |
| 327 | — | Resume — continues as gpt-5.3-codex |
| 328–335 | — | Finishing up |

## Complete Model Timeline

```mermaid
gantt
    title Model Usage Across Job 2abc6159
    dateFormat HH:mm
    axisFormat %H:%M
    section Main Agent
    galapagos-alpha (steps 0-186)     :m1, 11:46, 170min
    gpt-5.3-codex (steps 189-335)     :m2, 14:37, 85min
    section Sub-Agents
    testing_agent Codex (35-61)       :s1, 12:15, 25min
    testing_v3_fork Opus (275-290)    :s2, 15:00, 15min
    auto_frontend Sonnet (293-321)    :s3, 15:20, 25min
    section Events
    Credit limit (step 15)            :milestone, e1, 11:46, 0min
    auto_compact (step 187)           :milestone, e2, 14:35, 0min
    Pause (step 326)                  :milestone, e3, 15:36, 0min
```

## Summary Statistics

| Metric | Value |
|--------|-------|
| Total steps | 335 |
| Main agent steps | ~280 |
| Sub-agent steps | ~55 |
| Models used | 5 (galapagos-alpha, gpt-5.3-codex, claude-opus-4-5, claude-sonnet-4-5, gpt-5.3-codex) |
| auto_compact events | 1 |
| Credit limit events | 1 |
| Errors | 3 (timeout, MIME mismatch, one tool error) |
| Testing delegations | 3 rounds with 3 different models |

## Key Takeaways

1. **Multi-model is real** — a single job can use 5+ different LLM models
2. **auto_compact changes models** — the fork agent reads from `job_metadata`, not the runtime model
3. **Sub-agents are specialized** — each testing round may use a different model/expertise
4. **Self-recovery works** — the agent recovered from timeout, credit limit, and image errors without human intervention
5. **Jobs are long** — 335 steps over 4.5 hours is typical for complex applications
"""
    },
]
