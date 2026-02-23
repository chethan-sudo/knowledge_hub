"""Content Authenticity Fix - Batch 1
Fix new documents: generalize E1/Emergent claims to general AI agent concepts"""

from pymongo import MongoClient
from datetime import datetime, timezone

client = MongoClient('mongodb://localhost:27017')
db = client['test_database']
NOW = datetime.now(timezone.utc).isoformat()

def update_doc(title, new_content):
    result = db.documents.update_one(
        {'title': title},
        {'$set': {'content': new_content, 'updated_at': NOW}}
    )
    print(f"{'UPDATED' if result.modified_count else 'NOT FOUND'}: {title} ({len(new_content)} chars)")

def rename_doc(old_title, new_title, new_content):
    result = db.documents.update_one(
        {'title': old_title},
        {'$set': {'title': new_title, 'content': new_content, 'updated_at': NOW}}
    )
    print(f"{'RENAMED' if result.modified_count else 'NOT FOUND'}: {old_title} -> {new_title} ({len(new_content)} chars)")

# ============================================================
# 1. Your First 10 Minutes → Generalized
# ============================================================
rename_doc("Your First 10 Minutes on Emergent", "Your First AI Coding Session", """# Your First AI Coding Session

This guide walks you through how to work with an AI coding agent for the first time. Whether you're using any AI-powered development platform, the workflow is similar: describe what you want, let the agent build it, then iterate.

## What an AI Coding Environment Provides

A typical AI coding environment gives you:

| Resource | What It Is | Purpose |
|----------|-----------|---------|
| **AI Agent** | An LLM-powered system that can plan, write code, and use tools | Your development partner |
| **Server Environment** | A cloud-based development server | Runs your code |
| **Database** | A database instance (e.g., MongoDB, PostgreSQL) | Stores your data |
| **Live Preview** | A URL where your running app is accessible | Test your app in the browser |
| **Version Control** | Git-based history of every change | Undo mistakes, track progress |

## Step 1: Describe What You Want to Build

Start with a clear description. The more specific, the better:

**Vague (the agent will need to ask follow-up questions):**
> "Build me a task manager"

**Specific (the agent can start immediately):**
> "Build a task manager with: user authentication, CRUD for tasks with title/description/due date/priority, a dashboard showing tasks grouped by priority, and a dark theme"

**Tip:** You don't need to have everything figured out upfront. Start with the core feature, get it working, then iterate.

## Step 2: Watch the Agent Work

After you send your request, a typical AI coding agent will:

1. **Plan** — Decide on the architecture and approach
2. **Ask clarifying questions** — If anything is ambiguous
3. **Create files** — Backend routes, frontend components, database schemas
4. **Install dependencies** — Packages your app needs
5. **Test** — Run the app and verify it works
6. **Show you the result** — Summary of what was built

You can usually watch this process in real-time. Every tool call (file creation, terminal command, screenshot) is visible.

## Step 3: Test Your App

Once the agent says the initial version is ready:

1. Open the live preview URL
2. Your app loads in a new tab
3. Test the features that were built
4. Come back and describe what to change

## Step 4: Iterate

This is where the real value is. Describe changes in natural language:

- "The login button should be bigger"
- "Add a search bar to the dashboard"
- "The API is returning a 500 error when I submit the form"
- "Can you add dark mode?"

The agent reads your feedback, examines the code, makes changes, and tests them.

## What to Do When Something Goes Wrong

| Situation | What to Do |
|-----------|-----------|
| App shows a blank page | Tell the agent — it can check console errors and server logs |
| API returns an error | Share the exact error message |
| Agent seems stuck in a loop | Ask it to stop and try a different approach |
| You want to undo changes | Use version control to roll back to a previous state |
| App works but data disappears on restart | Data might be stored in memory instead of the database |

## Tips for Getting the Best Results

1. **Be specific about what you want** — "Add a red delete button in the top-right corner" beats "add a delete button"
2. **Report bugs with context** — "When I click Submit on the form, nothing happens" is better than "it's broken"
3. **Iterate in small steps** — Get the core working first, then add features one by one
4. **Share error messages** — Copy the exact error text from the browser console or server logs
5. **Ask questions** — "How does the authentication work in our app?" is a perfectly valid message

## Starter Project Ideas

| Difficulty | Project | What You'll Learn |
|-----------|---------|-------------------|
| Beginner | Todo list with categories | CRUD operations, state management |
| Beginner | Personal blog | Markdown rendering, routing |
| Intermediate | Chat application | Real-time updates, WebSockets |
| Intermediate | Dashboard with charts | Data visualization, API design |
| Advanced | E-commerce store | Payment integration, auth, file uploads |
| Advanced | AI-powered app | LLM integration, streaming responses |
""")

# ============================================================
# 2. How to Talk to E1 → Generalized
# ============================================================
rename_doc("How to Talk to E1 Effectively", "Communicating with AI Coding Agents", """# Communicating with AI Coding Agents

AI coding agents are powerful, but the quality of the output depends on the quality of the input. This guide teaches you how to communicate effectively for the best results.

## The Communication Model

```mermaid
flowchart LR
    YOU[Your Message] --> AGENT[Agent Processes]
    AGENT --> PLAN[Plans Approach]
    PLAN --> TOOLS[Executes Tools]
    TOOLS --> RESULT[Shows Result]
    RESULT --> YOU
```

An AI coding agent is not a chatbot — it's an **agent**. Every message you send triggers a planning cycle where the agent decides what tools to use and in what order. Your message quality directly affects this planning.

## Message Types

### 1. Feature Requests

**How the agent handles it:** Plans architecture → creates files → installs dependencies → tests → shows result

**Weak:**
> "Add authentication"

**Strong:**
> "Add Google OAuth authentication. Users should see a 'Sign in with Google' button on the login page. After signing in, redirect to the dashboard. Store the user's email and name in MongoDB."

**Why it matters:** The weak version forces the agent to make assumptions about auth type, UI placement, and data storage. The strong version eliminates ambiguity.

### 2. Bug Reports

**How the agent handles it:** Reads logs → examines code → identifies root cause → applies fix → tests

**Weak:**
> "It's broken"

**Strong:**
> "When I click the 'Submit' button on the /settings page, nothing happens. The browser console shows 'TypeError: Cannot read property map of undefined'. This started after the last change to the settings component."

**The ideal bug report includes:**

| Element | Example |
|---------|---------|
| **What you did** | "Clicked the Submit button on /settings" |
| **What happened** | "Nothing happened, no feedback" |
| **What you expected** | "Settings should save and show a success toast" |
| **Error messages** | "TypeError: Cannot read property 'map' of undefined" |
| **When it started** | "After the last change to settings" |

### 3. Design Feedback

**How the agent handles it:** Identifies the component → modifies styles/layout → verifies visually

**Weak:**
> "Make it look better"

**Strong:**
> "The sidebar is too wide on mobile. Can you make it collapsible with a hamburger menu? Also, the card titles should be larger (maybe text-lg) and the spacing between cards feels too tight."

### 4. Questions

The agent can answer questions about the codebase and architecture without making changes.

> "How does the authentication flow work in our app?"
> "What database collections are we using?"
> "Can you explain the API structure?"

### 5. Course Corrections

Tell the agent to change approach when something isn't working.

> "That approach isn't working. Let's try using a modal instead of a separate page."
> "Stop trying to fix the CSS. The issue is in the API response — the data structure changed."

## Power User Techniques

### Technique 1: Provide Context Before Asking

```
"I'm building a medical appointment booking system. 
The patient should be able to:
1. See available time slots
2. Book an appointment
3. Cancel within 24 hours
4. Receive a confirmation

Start with the booking API and database schema."
```

### Technique 2: Reference Specific Files

```
"In backend/server.py, the /api/appointments endpoint 
is returning a 500 error. Can you check the database 
query on line ~150?"
```

### Technique 3: Describe Visual Issues Clearly

If the UI looks wrong, describe what you see vs. what you expect:
```
"The dashboard chart should be full-width but it's 
squished to the left. The legend is overlapping 
the data labels."
```

### Technique 4: Prioritize Explicitly

```
"I have three things to fix:
1. (Critical) Login is completely broken
2. (Medium) Dashboard chart colors are wrong  
3. (Low) Footer text needs updating

Please fix in this order."
```

### Technique 5: Ask for Explanation Before Changes

```
"Before making changes, can you explain how the 
current authentication system works? I want to 
understand the flow before we modify it."
```

## Common Limitations of AI Coding Agents

| Limitation | Workaround |
|-----------|-----------|
| Can't see your screen directly | Describe what you see, share screenshots |
| Can't access external databases without credentials | Provide connection strings or API keys |
| May not remember decisions across separate sessions | Document decisions in a README or PRD file |
| Can make confident but wrong suggestions | Always review generated code critically |
| May struggle with very large codebases | Point to specific files and line ranges |

## The Feedback Loop

The most productive pattern is rapid iteration:

```
You: "Build feature X"
Agent: [builds and shows result]
You: "Almost! Change Y and fix Z"
Agent: [adjusts]
You: "Perfect. Now add feature W"
```

Each cycle takes 2-5 minutes. In an hour, you can iterate through 12-15 cycles — significantly faster than writing everything manually.
""")

# ============================================================
# 3. Platform Glossary → Generalized
# ============================================================
rename_doc("Platform Glossary", "AI Development Glossary", """# AI Development Glossary

A comprehensive reference of terms used in AI-powered development. Bookmark this page for quick lookups.

## A

**Agent** — A software system that uses an LLM to reason and take actions. Unlike a chatbot (which only generates text), an agent can execute code, read files, and interact with services.

**Agent Configuration** — A file or set of parameters that defines how an agent behaves: which LLM model to use, available tools, system prompt, timeout settings, and context management strategy.

## C

**Cold Start** — When a cloud development environment needs to be provisioned after a period of inactivity. Typically takes 15-60 seconds depending on the platform.

**Context Compaction** — When the conversation history approaches the LLM's token limit, some systems automatically summarize older messages to free up space. Critical information is preserved, but some details may be lost.

**Context Window** — The maximum number of tokens an LLM can process in a single request. For example, Claude has ~200K tokens, GPT-4 has ~128K tokens, and Gemini has up to 1M tokens. The system prompt, conversation history, and tool definitions all count toward this limit.

## D

**Debug Panel / Observability** — Tools that show the raw LLM requests and responses, tool calls, token usage, and timing for every interaction. Essential for understanding an agent's decision-making process.

## F

**Fork** — Creating a new agent session that continues from the state of a previous session. The new session typically receives a handoff summary but no conversation history.

## H

**Handoff Summary** — A structured document passed between sessions. Contains the problem statement, completed work, pending issues, code architecture, and technical decisions. Acts as institutional memory.

**Hot Reload** — Automatic restart of the frontend or backend when code files change. Common in modern development setups — code changes take effect without manually restarting servers.

## I

**Ingress** — In Kubernetes, the component that routes external HTTP/HTTPS traffic to internal services. Typically maps URL paths to specific backend ports.

## L

**LLM (Large Language Model)** — A neural network trained on text data that predicts the next token. Examples: Claude, GPT, Gemini. An LLM by itself cannot take actions — it only generates text. An agent wraps an LLM to give it the ability to act.

**LLM Proxy** — An intermediary service that routes LLM requests to the appropriate provider, handles authentication, tracks token usage, and enforces budget limits.

## M

**MCP (Model Context Protocol)** — A standard protocol by Anthropic for how AI agents interact with tools. Defines how tools are discovered, called, and how results are returned.

**Memory File** — A persistent file (like a README or PRD) stored in the project that preserves critical decisions and state across agent sessions. The agent reads this file at the start of each session to maintain continuity.

## P

**Pod** — In Kubernetes, the smallest deployable unit. In AI coding platforms, each user typically gets their own pod containing their development environment.

**PRD (Product Requirements Document)** — A file that captures the problem statement, implemented features, and remaining backlog. Used for continuity across sessions.

## R

**RAG (Retrieval Augmented Generation)** — A technique where relevant documents are retrieved from a knowledge base and included in the LLM prompt, allowing the model to answer questions about data it wasn't trained on.

**Rollback** — Reverting the codebase to a previous Git checkpoint. In AI-assisted development, every agent action typically creates a commit, so you can roll back to any previous state.

## S

**Seed Data** — Initial data loaded into the database when an application is first set up. Defines the starting content for the application.

**Subagent** — A specialist AI agent that a primary agent delegates specific tasks to. Examples: a testing agent, a design agent, a troubleshooting agent. Subagents are typically stateless and receive full context from the primary agent each time.

**Supervisor** — A process management system (like `supervisord`) that manages multiple services. Starts, stops, and restarts processes, and auto-restarts them if they crash.

## T

**Token** — The fundamental unit of text for LLMs. Roughly 3-4 English characters per token. "Hello world" = 2 tokens. Costs are calculated per-token, with separate rates for input and output tokens.

**Tool** — A capability that an AI agent can invoke to take actions. Examples: creating files, running terminal commands, reading files, searching the web, taking screenshots. Tools are defined with input/output schemas and executed in the agent's environment.

## W

**WebSocket** — A persistent, bidirectional communication protocol. Used for real-time features like collaborative editing, live chat, and streaming AI responses.
""")

# ============================================================
# 4. Choosing the Right LLM → Remove fabricated prices
# ============================================================
update_doc("Choosing the Right LLM", """# Choosing the Right LLM

A practical comparison of the major LLM models. This guide helps you pick the right model for your use case based on their actual strengths and trade-offs.

## Quick Comparison

| Model | Provider | Best For | Relative Speed | Context Window |
|-------|----------|----------|---------------|---------------|
| **Claude Sonnet** | Anthropic | Complex coding, long documents | Medium | 200K tokens |
| **GPT-4o** | OpenAI | Balanced performance | Fast | 128K tokens |
| **GPT-4o-mini** | OpenAI | Quick tasks, low cost | Very Fast | 128K tokens |
| **Gemini Flash** | Google | Speed-critical, high volume | Very Fast | 1M tokens |
| **Gemini Pro** | Google | Complex reasoning | Medium | 1M tokens |
| **Claude Haiku** | Anthropic | Simple tasks, low cost | Very Fast | 200K tokens |

*Note: Model versions and capabilities evolve rapidly. Check provider documentation for the latest specifications.*

## When to Use Each Model

### Claude Sonnet (Anthropic)
**Best for:** Complex coding tasks, detailed analysis, long-form content

- Excellent at following complex, multi-step instructions
- Strong code generation across many languages
- Extended thinking capability for step-by-step reasoning
- Large context window (200K tokens)
- Tends to be more careful and thorough than competitors
- Slower than GPT models for simple tasks

### GPT-4o / GPT-4o-mini (OpenAI)
**Best for:** General-purpose tasks, rapid prototyping

- Fast response times
- Good at diverse tasks (text, code, analysis)
- Strong function/tool calling
- GPT-4o-mini is very cost-effective for simple tasks
- Smaller context window than Claude or Gemini

### Gemini Flash / Pro (Google)
**Best for:** Processing large documents, speed-critical applications

- Extremely fast (especially Flash)
- 1M token context window — can process entire codebases
- Cost-effective for batch processing
- Flash is ideal for high-volume, simpler tasks
- Pro handles complex reasoning well

## Decision Framework

```mermaid
flowchart TD
    START[What are you building?] --> Q1{Need speed or quality?}
    Q1 -->|Speed| Q2{Budget sensitive?}
    Q1 -->|Quality| Q3{Complex code?}
    Q2 -->|Yes| FLASH[Gemini Flash]
    Q2 -->|No| MINI[GPT-4o-mini]
    Q3 -->|Yes| SONNET[Claude Sonnet]
    Q3 -->|No| GPT[GPT-4o]
```

## Cost Optimization: Model Routing

You don't have to use one model for everything. Use different models for different tasks:

```python
# Cheap, fast model for simple categorization
response = await llm.chat(
    model="gpt-4o-mini",  # or gemini-flash
    messages=[{"role": "user", "content": f"Categorize this text: {text}"}]
)

# Powerful model for complex generation
response = await llm.chat(
    model="claude-sonnet",
    messages=[{"role": "user", "content": f"Write a detailed analysis of: {text}"}]
)
```

**This is called "model routing"** — use the cheapest model that can handle each specific task. It can reduce costs significantly compared to using a premium model for everything.

## Key Parameters That Affect Output

| Parameter | What It Does | Typical Values |
|-----------|-------------|---------------|
| **temperature** | Controls randomness. 0 = deterministic, 1 = creative | 0 for facts, 0.7 for creative |
| **max_tokens** | Maximum response length | Depends on task |
| **top_p** | Nucleus sampling — limits token selection pool | 0.9-0.95 |
| **system prompt** | Instructions that shape the model's behavior | Task-specific |

## Image Generation Models

| Model | Provider | Strengths |
|-------|----------|-----------|
| **DALL-E / GPT Image** | OpenAI | Photorealistic, good with text in images |
| **Imagen / Gemini Image** | Google | Artistic, stylized outputs |

## Common Mistakes

| Mistake | Problem | Better Approach |
|---------|---------|----------------|
| Using the most expensive model for everything | Wasteful, slower than needed | Route simple tasks to cheaper models |
| Using a fast model for code review | Misses nuanced bugs | Use a more capable model for quality-critical tasks |
| Not setting temperature appropriately | Wrong output style | 0 for factual, 0.7 for creative, 1 for variety |
| Ignoring context window limits | Silent truncation of input | Check token count, use models with larger windows for big inputs |
| Not testing different models | Assuming one model fits all | Compare outputs on your actual use case |
""")

# ============================================================
# 5. Understanding the Debug Panel → Generalized
# ============================================================
rename_doc("Understanding the Debug Panel", "Understanding AI Agent Observability", """# Understanding AI Agent Observability

When working with AI coding agents, observability tools let you see exactly what the agent is doing: which LLM calls it makes, which tools it uses, how many tokens are consumed, and how long each step takes. This is essential for debugging unexpected agent behavior.

## What Gets Captured

For every interaction with an AI agent, observability tools typically record:

| Component | What It Shows | Why It Matters |
|-----------|--------------|----------------|
| **LLM Request** | Full payload sent to the LLM | See exactly what the AI was asked |
| **LLM Response** | Raw response including reasoning | See the AI's thought process |
| **Tool Calls** | Tool name, parameters, results, duration | Trace every action taken |
| **Token Usage** | Input/output tokens per call | Understand cost and context usage |
| **Timing** | Milliseconds per operation | Identify slow operations |

## Anatomy of an Agent Interaction

A single user message can trigger multiple LLM calls and tool executions:

```
┌─────────────────────────────────────────┐
│  User: "Add a login endpoint"            │
├─────────────────────────────────────────┤
│  LLM Call #1                             │
│  ├─ Input tokens: ~45,000                │
│  ├─ Output tokens: ~2,000                │
│  ├─ Duration: ~8 seconds                 │
│  └─ Decision: read the server file       │
│                                          │
│  Tool: view_file                         │
│  ├─ Params: {path: "/app/server.py"}     │
│  ├─ Result: [file contents]              │
│  └─ Duration: ~100ms                     │
│                                          │
│  LLM Call #2                             │
│  ├─ Input tokens: ~48,000                │
│  ├─ Output tokens: ~1,800                │
│  ├─ Duration: ~6 seconds                 │
│  └─ Decision: edit the server file       │
│                                          │
│  Tool: edit_file                         │
│  ├─ Params: {path, changes}              │
│  ├─ Result: "Edit successful"            │
│  └─ Duration: ~50ms                      │
└─────────────────────────────────────────┘
```

## Why Requests Look Similar

A common confusion: every debug entry looks nearly identical at first glance. Here's why:

| Part of the Request | Changes Between Messages? | Typical Size |
|---------------------|--------------------------|-------------|
| System prompt | **No** — same every time | ~10,000-20,000 tokens |
| Tool definitions | **No** — same every time | ~5,000-10,000 tokens |
| Conversation history | **Yes** — grows each turn | 500-100,000+ tokens |
| Current message | **Yes** — your latest input | 10-500 tokens |

The system prompt and tool definitions dominate the payload (~60-70%), making entries *look* identical. The dynamic content (your messages, tool results) is there — you need to scroll past the static content to find it.

## The LLM Request Payload

A typical LLM API request contains:

```json
{
  "model": "claude-sonnet-4-5",
  "system": "You are an AI coding assistant...",
  "messages": [
    {"role": "user", "content": "Add a login endpoint"},
    {"role": "assistant", "content": "I'll read the server file..."},
    {"role": "tool_result", "content": "{file contents}"}
  ],
  "tools": [
    {"name": "view_file", "description": "...", "input_schema": {...}},
    {"name": "edit_file", "description": "...", "input_schema": {...}}
  ],
  "max_tokens": 4096,
  "temperature": 0.7,
  "stream": true
}
```

### Key Fields

| Field | What It Contains |
|-------|-----------------|
| `model` | Which LLM is being used |
| `system` | The system prompt — instructions defining agent behavior |
| `messages` | Full conversation history — grows every turn |
| `tools` | Tool definitions with JSON schemas |
| `max_tokens` | Maximum response length |
| `temperature` | Creativity level (0=deterministic, 1=creative) |
| `stream` | Whether to stream tokens one-by-one |

## Practical Debugging Scenarios

### Scenario 1: "The agent made the wrong tool choice"

1. Find the LLM call just before the wrong tool was used
2. Check `messages` — did the agent have enough context?
3. Was a previous tool result misleading or incomplete?
4. Common cause: The agent didn't read the relevant file first, so it guessed the code structure

### Scenario 2: "The agent is slow"

1. Check `duration` on each LLM call — anything over 30 seconds is unusually slow
2. Check `input_tokens` — if over 150,000, the context window is getting very large
3. Check tool call durations — a slow terminal command means the command itself is slow
4. Solution: Start a new session to reset context, or be more targeted in your requests

### Scenario 3: "The agent keeps repeating itself"

1. Check the conversation history in `messages`
2. Look for loops: same tool calls with same parameters
3. Common cause: A tool is returning an error, and the agent keeps retrying the same approach
4. Solution: Interrupt and provide more specific instructions or a different approach

## Token Usage Patterns

Understanding where tokens go helps optimize costs:

```
Typical token distribution per message:
- System prompt:        ~15,000 tokens (fixed cost, same every time)
- Tool definitions:     ~8,000 tokens  (fixed cost)
- Conversation history: ~5,000-80,000 tokens (grows each turn)
- Your message:         ~100-500 tokens
- Agent response:       ~500-5,000 tokens
```

**Key insight:** ~23,000 tokens are "fixed overhead" every message. This is why even a simple "hello" consumes tokens.

## Common Misinterpretations

| What You See | What It Actually Means |
|-------------|----------------------|
| "The same data every time" | System prompt + tools are constant. Look at the messages array for what changes. |
| "Huge token count on a simple request" | The system prompt (~15K) and tools (~8K) are included every time. |
| "Duration is 0ms" | Some cached or no-op operations complete instantly. |
| "Thinking tokens" in output | Extended thinking / chain-of-thought is normal — the AI reasons before responding. |
""")

# ============================================================
# 6. Agent Framework Landscape → Fix E1-specific claims
# ============================================================
update_doc("Agent Framework Landscape", """# Agent Framework Landscape

The AI agent ecosystem is evolving rapidly. Understanding the major frameworks helps you choose the right tool and understand different architectural approaches.

## Framework Comparison

| Framework | Creator | Focus | Architecture | Production-Ready? |
|-----------|---------|-------|-------------|-------------------|
| **LangChain** | LangChain Inc | General LLM apps | Chain/graph-based composition | Yes |
| **CrewAI** | CrewAI | Multi-agent teams | Role-based agent crews | Yes |
| **AutoGen** | Microsoft | Multi-agent conversation | Conversational agents | Yes |
| **OpenAI Assistants** | OpenAI | Managed agent service | API-based, hosted by OpenAI | Yes |
| **Anthropic MCP** | Anthropic | Tool protocol standard | Protocol layer, not a framework | N/A (protocol) |
| **LlamaIndex** | LlamaIndex | Data-focused agents | Index + query engine | Yes |
| **Semantic Kernel** | Microsoft | Enterprise integration | Plugin-based, .NET/Python | Yes |

## How Each Approaches Key Problems

### Tool Use

| Framework | Approach |
|-----------|----------|
| **LangChain** | Tools as Python functions decorated with `@tool` |
| **CrewAI** | Tools assigned per-agent role |
| **AutoGen** | Tools registered on agent instances |
| **OpenAI Assistants** | JSON schema tool definitions via API |

### Memory & Context

| Framework | Approach |
|-----------|----------|
| **LangChain** | Buffer, summary, or vector memory modules |
| **CrewAI** | Shared crew memory |
| **AutoGen** | Conversation history between agents |
| **Semantic Kernel** | Plugin-based memory stores |

### Multi-Agent Coordination

| Framework | Approach |
|-----------|----------|
| **CrewAI** | Agents with roles, goals, backstories work as a "crew" |
| **AutoGen** | Agents chat with each other in conversation threads |
| **LangChain (LangGraph)** | Stateful multi-step workflows with graph structure |

## When to Use What

### Choose LangChain When:
- You're building a **custom LLM application** (chatbot, RAG pipeline, data processing)
- You need **fine-grained control** over every step
- You're integrating multiple data sources with **complex retrieval pipelines**
- Your team has Python expertise and wants to own the infrastructure

### Choose CrewAI When:
- Your problem naturally breaks into **distinct roles** (researcher, writer, reviewer)
- You want agents to **collaborate autonomously** with minimal human intervention
- You're building **content generation pipelines** or **research workflows**

### Choose OpenAI Assistants When:
- You want the **simplest possible setup** — no self-hosting
- You're okay with **vendor lock-in** to OpenAI
- You need **built-in file search and code interpreter**
- Your use case is **conversational AI** (customer support, tutoring)

### Choose AutoGen When:
- You need **multi-agent conversations** where agents debate and refine outputs
- You're building a **research or analysis pipeline** with multiple perspectives
- You want agents to **code and execute** in a sandboxed environment

## Key Architectural Patterns

### Pattern 1: Orchestrator + Specialists

A central agent decides which specialist to call:

```mermaid
flowchart TD
    ORCH[Orchestrator Agent] --> S1[Coding Agent]
    ORCH --> S2[Testing Agent]
    ORCH --> S3[Design Agent]
    ORCH --> S4[Research Agent]
```

The orchestrator handles routing, while specialists handle domain-specific work. This is the pattern used by most production AI coding platforms.

### Pattern 2: Peer Collaboration

Agents communicate as equals:

```mermaid
flowchart LR
    A1[Agent A] <--> A2[Agent B]
    A2 <--> A3[Agent C]
    A1 <--> A3
```

Used by CrewAI and AutoGen. Good for tasks that benefit from multiple perspectives.

### Pattern 3: Pipeline

Each agent processes sequentially:

```mermaid
flowchart LR
    A1[Research] --> A2[Draft] --> A3[Review] --> A4[Publish]
```

Simple and predictable. Good for content generation workflows.

## The MCP Protocol: A New Standard

Anthropic's **Model Context Protocol (MCP)** is emerging as a standard for how AI agents interact with tools:

| Aspect | Before MCP | With MCP |
|--------|-----------|----------|
| Tool integration | Custom per-framework | Standardized protocol |
| Tool discovery | Hardcoded in config | Dynamic discovery |
| Cross-framework | Not portable | Portable across frameworks |

MCP standardizes the *wire format* for tool interaction: tools are defined with schemas, called with parameters, and return structured results.

## Common Misconception

> "Framework X is better than Framework Y"

This misses the point. Each framework optimizes for a different workflow. The right question is: **"Which framework matches my use case?"** — not which one has the most GitHub stars.
""")

# ============================================================
# 7. Prompt Engineering → Remove fake E1 prompt examples
# ============================================================
update_doc("Prompt Engineering Techniques", """# Prompt Engineering Techniques

A system prompt is what transforms a generic LLM into a specialized agent. Same LLM + different prompt = completely different behavior. This document covers techniques that make AI agent prompts effective, with examples you can apply to your own applications.

## The Anatomy of an Agent System Prompt

A well-structured agent system prompt typically follows this pattern:

```
┌─────────────────────────────────┐
│  1. Identity & Role Definition  │  "You are a [role]..."
├─────────────────────────────────┤
│  2. Environment Setup           │  Available tools, APIs, constraints
├─────────────────────────────────┤
│  3. Workflow Instructions       │  Step-by-step process
├─────────────────────────────────┤
│  4. Tool Usage Guidelines       │  When/how to use each tool
├─────────────────────────────────┤
│  5. Rules & Constraints         │  Hard boundaries
├─────────────────────────────────┤
│  6. Output Format               │  How to structure responses
├─────────────────────────────────┤
│  7. Examples                    │  Concrete demonstrations
└─────────────────────────────────┘
```

## Technique 1: Role Definition

**What it does:** Establishes identity, expertise level, and behavioral boundaries.

**Weak:**
```
You are a helpful assistant that writes code.
```

**Strong:**
```
You are a senior full-stack developer specializing in React 
and FastAPI. You write production-quality code with error 
handling, tests, and documentation.
```

**Why it works:** A specific role narrows the output distribution. The LLM generates code differently when it "is" a senior developer vs. a generic assistant.

## Technique 2: Structured Sections

**What it does:** Uses headers, XML tags, or Markdown to create parseable, referenceable sections.

**Example:**
```xml
<ENVIRONMENT>
  Database: MongoDB on localhost:27017
  Backend: FastAPI on port 8001
  Frontend: React on port 3000
</ENVIRONMENT>

<RULES>
  - Always validate user input before processing
  - Never expose database IDs in API responses
  - Use environment variables for all credentials
</RULES>
```

**Why it works:** LLMs can "navigate" within structured sections more reliably than flat text. When the model needs to check a configuration, it references the specific section, reducing hallucination.

## Technique 3: Few-Shot Examples

**What it does:** Provides concrete examples instead of abstract descriptions.

**Weak:**
```
Use descriptive IDs for test elements.
```

**Strong:**
```
Every interactive element must have a data-testid attribute.
Use clear, kebab-case naming that describes the element's function.

Examples:
  data-testid="login-form-submit-button"
  data-testid="user-profile-email-input"
  data-testid="dashboard-stats-card"
```

**Why it works:** The LLM pattern-matches from examples. Given these examples, it will generate `signup-form-password-input` — following the same convention without explicit rules.

## Technique 4: Negative Instructions (Don'ts)

**What it does:** Explicitly prevents known failure modes.

**Examples:**
```
- Do NOT start additional server processes manually
- NEVER delete environment configuration files
- Do NOT add comments in .env files
- Avoid using emoji characters for UI icons
```

**Why it works:** LLMs tend toward "helpful" behaviors that can be destructive. They might "helpfully" restart a server or "clean up" a config file. Negative instructions override these defaults.

## Technique 5: Decision Trees

**What it does:** Provides conditional logic for choosing between approaches.

**Example:**
```
Testing strategy:
- Small change (1 file): Test with curl or a quick check
- Medium feature (2-3 files): Run automated tests
- Large feature (many files): Use the full test suite
- Bug that keeps recurring: Run comprehensive regression tests
```

**Why it works:** Instead of hoping the LLM makes the right meta-decision, you encode the decision tree directly. The LLM follows the tree rather than improvising.

## Technique 6: Self-Checking Prompts

**What it does:** Forces the LLM to verify its own output before proceeding.

**Example:**
```
Before returning any data from the database, check:
- Did I exclude internal IDs from the response?
- Could any field contain a non-serializable type?
- Did I handle the case where the query returns no results?
If the answer to any question is "yes" or "maybe," 
fix the issue before proceeding.
```

**Why it works:** This creates an internal "review step" that catches common bugs before they reach the user.

## Technique 7: Priority Hierarchies

**What it does:** Resolves conflicts when multiple instructions apply.

**Example:**
```
Priority order:
1. Fix any broken functionality first
2. Address user-reported bugs
3. Complete in-progress features
4. Start new features
```

**Why it works:** Without explicit priorities, the LLM picks whatever seems most "helpful" in the moment. Priority hierarchies prevent task-switching and ensure the most important work happens first.

## Technique 8: Output Format Control

**What it does:** Constrains the format of generated output.

**Example:**
```
Response format:
- Summary of what was done (max 3 lines)
- List of files changed
- Any remaining issues
- Suggested next steps
```

**Why it works:** LLMs tend to be verbose. Format constraints produce consistent, scannable output.

## Common Prompt Engineering Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Too vague | "Be helpful" means nothing specific | Define exact behaviors with examples |
| Too long without structure | LLM loses track of instructions | Use sections, headers, delimiters |
| Contradictory instructions | "Be concise" + "Explain thoroughly" | Specify when each applies |
| No examples | LLM invents its own patterns | Always provide 2-3 concrete examples |
| No negative instructions | LLM does "helpful" but destructive things | Explicitly list what NOT to do |
| Assuming the LLM knows your stack | "Use the standard approach" | State the exact approach you want |

## Advanced: Chain-of-Thought vs Extended Thinking

| Approach | How It Works | When to Use |
|----------|-------------|-------------|
| **Zero-shot** | Just ask the question | Simple, factual queries |
| **Few-shot** | Provide examples before asking | Pattern-matching tasks |
| **Chain-of-thought** | "Think step by step" in the prompt | Multi-step reasoning |
| **Extended thinking** | Dedicated thinking tokens (model feature) | Complex planning, debugging |

Chain-of-thought is a prompting technique you can use with any model. Extended thinking is a model-level feature (available in some Claude and GPT models) where the model has a dedicated space to reason before producing output.

## Template: Building Your Own Agent Prompt

```markdown
# Role
You are [NAME], a [DOMAIN] specialist. You [PRIMARY FUNCTION].

# Environment
- [Service 1] runs on [port/URL]
- Database: [type and connection]

# Workflow
1. When asked for [X], first [STEP 1]
2. Then [STEP 2]
3. Always verify by [VERIFICATION METHOD]

# Rules
- NEVER [dangerous action]
- ALWAYS [required action]
- When in doubt, [fallback behavior]

# Examples
User: "[example input]"
Assistant: "[example output showing desired format]"
```
""")

print("\n=== Authenticity Fix Batch 1 Complete ===")
