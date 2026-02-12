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
CAT_TOOLS = _id()
SUB_LLM_PROXY = _id()

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

    {"id": CAT_TOOLS, "name": "Tools & Resources", "icon": "Sparkles", "order": 11, "parent_id": None},

    {"id": SUB_LLM_PROXY, "name": "LLM Proxy", "icon": "Cpu", "order": 3, "parent_id": CAT_LLM},
]

DOCUMENTS = [
    # ===== SYSTEM ARCHITECTURE OVERVIEW (new!) =====
    {
        "id": _id(), "title": "System Architecture Overview", "category_id": CAT_PLATFORM, "author_id": SYSTEM_AUTHOR,
        "created_at": NOW, "updated_at": NOW, "order": -1,
        "content": """# System Architecture Overview

A complete map of how the Emergent platform works — from the moment a user types a message to the final response.

## End-to-End Flow

```mermaid
flowchart TD
    U[User] -->|types message| FE[Emergent Frontend]
    FE -->|sends via WebSocket/API| AS[Agent Service]
    AS -->|loads history, system prompt| AS
    AS -->|constructs full payload| E1[E1 Orchestrator]
    E1 -->|uses as reasoning engine| LLM[LLM Provider<br/>Claude / GPT / Gemini]
    LLM -->|returns reasoning + tool calls| E1
    E1 -->|decides: tool or text?| Decision{Decision}
    Decision -->|text response| AS
    Decision -->|tool call| TE[Tool Execution Engine]
    Decision -->|subagent call| SA[Subagent]
    TE -->|executes in container| POD[Kubernetes Pod]
    SA -->|spawns separate session| SA_LLM[Subagent LLM]
    SA_LLM -->|returns results| E1
    TE -->|returns results| E1
    E1 -->|loop continues until done| Decision
    AS -->|stores in DB, streams to user| FE
    FE -->|displays response| U
```

## Component Roles

| Component | What It Is | What It Does |
|-----------|-----------|-------------|
| **User** | The human | Sends messages, uploads files, triggers actions |
| **Emergent Frontend** | Chat UI (React) | Renders conversation, handles input, displays results |
| **Agent Service** | Backend infrastructure | Auth, sessions, history, tool routing, git versioning |
| **E1 Orchestrator** | The main AI agent | Decision-maker. Picks tools, delegates to subagents, drives workflow |
| **LLM Provider** | Claude/GPT/Gemini | Reasoning engine that E1 uses. Stateless — just computes |
| **Tool Execution Engine** | Runs tools | Validates and executes tool calls inside the container |
| **Subagents** | Specialized agents | Testing, design, integration experts — each with own LLM |
| **Kubernetes Pod** | Your workspace | Container with your code, MongoDB, frontend, backend |

## Data Flow Diagram

```mermaid
flowchart LR
    subgraph Cloud["Emergent Cloud"]
        DB[(Session DB)]
        STORE[(Asset Storage)]
        PROXY[Universal Key Proxy]
    end
    subgraph Cluster["Kubernetes Cluster"]
        ING[Ingress Controller]
        subgraph Pod["User Container"]
            BE[Backend :8001]
            FE_SRV[Frontend :3000]
            MONGO[(MongoDB)]
            GIT[.git]
        end
    end
    subgraph LLMs["LLM Providers"]
        OAI[OpenAI]
        ANT[Anthropic]
        GOO[Google]
    end
    DB <-->|conversation history| AS2[Agent Service]
    STORE <-->|uploaded files| AS2
    AS2 <-->|tool execution| Pod
    AS2 -->|LLM calls| PROXY
    PROXY --> OAI
    PROXY --> ANT
    PROXY --> GOO
    ING -->|/api/*| BE
    ING -->|/*| FE_SRV
    BE <--> MONGO
```

## Request Routing

```mermaid
flowchart TD
    REQ[Browser Request] --> DNS[DNS Resolution]
    DNS --> LB[Load Balancer]
    LB --> ING[K8s Ingress]
    ING -->|path starts with /api| BE[Backend :8001]
    ING -->|all other paths| FE[Frontend :3000]
    BE --> MONGO[(MongoDB)]
    BE --> RESP1[JSON Response]
    FE --> RESP2[HTML/JS/CSS]
```

## The Orchestration Loop

This is the core loop that powers every interaction:

```mermaid
flowchart TD
    START([User sends message]) --> RECV[E1 receives input]
    RECV --> REASON[E1 reasons using LLM]
    REASON --> DECIDE{What to do?}
    DECIDE -->|Need tool| TOOL[Execute Tool]
    DECIDE -->|Need subagent| AGENT[Call Subagent]
    DECIDE -->|Ready to respond| RESPOND[Send text response]
    TOOL -->|result| RECV
    AGENT -->|result| RECV
    RESPOND --> END([User sees response])
```

## Key Architectural Principles

- **E1 is the orchestrator, not an LLM.** It uses an LLM as its reasoning engine, but E1 itself is the decision-making agent layer.
- **LLMs are stateless.** The Agent Service maintains all conversation history and feeds it back with every call.
- **Subagents are independent.** They have no memory of previous calls. E1 provides full context each time.
- **Everything is containerized.** Each user gets an isolated Kubernetes pod with its own filesystem, database, and services.
- **Auto-commit everything.** Every action creates a git checkpoint for rollback capability.
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

E1 is the conductor of an orchestra. The LLM is its musical knowledge. The tools are the instruments. The Agent Service is the concert hall.
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

**Critical rule**: If E1 calls the same subagent twice, it must provide full context again — including what the previous call already did. The subagent has zero memory.
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

E1 maximizes parallel execution for speed, but respects dependencies between operations.
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

One key, one balance, all providers. Supports text generation, image generation (GPT Image 1, Nano Banana), video (Sora 2), and speech (Whisper, TTS).
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

**Every backend route MUST start with `/api`**. Without it, the ingress routes to the frontend, which returns HTML instead of JSON.

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

Each user gets an isolated pod with separate filesystem, database, environment variables, and network. Enforced by Kubernetes namespaces and network policies.
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

Changing your code rebuilds only Layer 4+. Lower layers are cached and reusable across all containers.
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

100 virtual changes might result in only 3 real DOM updates.

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

First request: ~50-200ms. Subsequent: ~5-20ms (cached DNS + kept-alive connection).
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

JWT structure: `header.payload.signature`. Payload is NOT encrypted — anyone can read it. But the signature proves it wasn't tampered with.

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

User never shares Google password with your app. You get verified identity with 2FA.
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

## Rolling Deployment (Zero Downtime)

```mermaid
flowchart TD
    S1["Step 1: Start new pod"] --> S2["Step 2: Health check passes"]
    S2 --> S3["Step 3: Route traffic to new pod"]
    S3 --> S4["Step 4: Drain old pod"]
    S4 --> S5["Step 5: Terminate old pod"]
```

Users never see downtime. Traffic gradually shifts from old to new.

## Deployment Options

| Option | Description |
|--------|-------------|
| **Emergent Native** | Managed production on Emergent infra |
| **GitHub Export** | Save to GitHub, deploy to Vercel/Railway/AWS |
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

**Rolled back**: Source code, configs, project structure.
**Not rolled back**: MongoDB data, conversation history, git history.

E1 never does `git reset` — users use the Rollback button instead. It's safer because it preserves platform files and handles dependency reinstallation.
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

All data encrypted in transit. Even if intercepted, it looks like random bytes.

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

Screenshots are taken at quality=20 to save tokens (80%+ savings). Full quality screenshots would consume excessive tokens in the LLM context window.
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
]
