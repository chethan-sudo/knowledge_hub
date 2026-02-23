"""Content Enhancement Script - Enhancement #5: Expand Shallow Documents
Also includes #1 (Code Examples), #2 (Troubleshooting), #6 (Visual Content)"""

from pymongo import MongoClient
from datetime import datetime, timezone
import uuid

client = MongoClient('mongodb://localhost:27017')
db = client['test_database']
NOW = datetime.now(timezone.utc).isoformat()

def update_doc(title, new_content):
    result = db.documents.update_one(
        {'title': title},
        {'$set': {'content': new_content, 'updated_at': NOW}}
    )
    print(f"{'UPDATED' if result.modified_count else 'NOT FOUND'}: {title} ({len(new_content)} chars)")

# ============================================================
# 1. Understanding the Debug Panel (766 -> ~6000 chars)
# ============================================================
update_doc("Understanding the Debug Panel", """# Understanding the Debug Panel

The Debug Panel is your window into E1's brain. Every decision, every tool call, every LLM interaction is captured here. Understanding it is the difference between guessing what went wrong and *knowing*.

## Opening the Debug Panel

In the Emergent UI, click the **bug icon** in the top-right corner of the chat interface. The panel slides open, showing a timeline of every interaction in your current session.

## What Gets Captured

For every single message you send, the Debug Panel records:

| Component | What It Shows | Why It Matters |
|-----------|--------------|----------------|
| **LLM Request** | Full payload sent to Claude/GPT | See exactly what the AI was asked |
| **LLM Response** | Raw response with thinking tokens | See the AI's reasoning process |
| **Tool Calls** | Tool name, parameters, results, duration | Trace every action E1 took |
| **Token Usage** | Input/output tokens per call | Understand cost and context usage |
| **Timing** | Milliseconds per operation | Identify slow operations |

## Anatomy of a Debug Entry

```
┌─────────────────────────────────────────┐
│  Message #3: "Add a login endpoint"      │
├─────────────────────────────────────────┤
│  LLM Call #1                             │
│  ├─ Model: claude-sonnet-4-6             │
│  ├─ Input tokens: 45,230                 │
│  ├─ Output tokens: 2,100                 │
│  ├─ Duration: 8,450ms                    │
│  └─ Decision: call view_file             │
│                                          │
│  Tool: view_file                         │
│  ├─ Params: {path: "/app/backend/..."}   │
│  ├─ Result: [file contents]              │
│  └─ Duration: 120ms                      │
│                                          │
│  LLM Call #2                             │
│  ├─ Input tokens: 48,500                 │
│  ├─ Output tokens: 1,800                 │
│  ├─ Duration: 6,200ms                    │
│  └─ Decision: call search_replace        │
│                                          │
│  Tool: search_replace                    │
│  ├─ Params: {path, old_str, new_str}     │
│  ├─ Result: "Edit successful"            │
│  └─ Duration: 45ms                       │
└─────────────────────────────────────────┘
```

## Why Debug Looks "The Same"

First-time users often think every debug entry is identical. Here's why:

| Part | Changes Between Messages? | Size |
|------|--------------------------|------|
| System prompt | **No** — same every time | ~15,000 tokens |
| Tool definitions | **No** — same every time | ~8,000 tokens |
| Conversation history | **Yes** — grows each turn | 500-50,000+ tokens |
| Current message | **Yes** — your latest input | 10-500 tokens |
| Tool results | **Yes** — unique per action | Variable |

The system prompt dominates the view (~60% of the payload), making entries *look* identical at first glance. The dynamic content is there — you need to scroll past the system prompt to find it.

## Reading the Body Payload

The `body` field contains the actual request sent to the LLM provider:

```json
{
  "model": "claude-sonnet-4-6",
  "system": "You are E1, a full-stack coding agent...",
  "messages": [
    {"role": "user", "content": "Add a login endpoint"},
    {"role": "assistant", "content": "I'll add a login..."},
    {"role": "tool_result", "content": "{file contents}"}
  ],
  "tools": [
    {"name": "view_file", "description": "...", "input_schema": {...}},
    {"name": "search_replace", "description": "...", "input_schema": {...}}
  ],
  "max_tokens": 64000,
  "temperature": 1,
  "stream": true
}
```

### Key Fields Explained

| Field | What It Contains | Typical Size |
|-------|-----------------|-------------|
| `model` | Which LLM is being used | Fixed |
| `system` | The entire system prompt | ~15,000 tokens |
| `messages` | Full conversation history — grows every turn | 500-200,000 tokens |
| `tools` | All tool definitions with JSON schemas | ~8,000 tokens |
| `max_tokens` | Maximum response length | 64,000 |
| `temperature` | Creativity level (0=deterministic, 1=creative) | 1 |
| `stream` | Whether to stream tokens one-by-one | true |

## Practical Debugging Walkthroughs

### Scenario 1: "E1 Made the Wrong Tool Choice"

1. Open Debug Panel
2. Find the LLM call just before the wrong tool was used
3. Check `messages` — did E1 have enough context? Was a previous tool result misleading?
4. Check `system` — is the system prompt giving clear guidance for this scenario?
5. Common cause: E1 didn't read the file first, so it guessed the code structure

### Scenario 2: "E1 Is Slow"

1. Check `duration` on each LLM call — anything over 30,000ms is slow
2. Check `input_tokens` — if it's over 150,000, context is getting large
3. Check tool call durations — a slow `execute_bash` means the command itself is slow
4. Solution: Start a new session to reset context, or ask E1 to be more targeted

### Scenario 3: "E1 Keeps Repeating Itself"

1. Check the conversation history in `messages`
2. Look for loops: same tool calls with same parameters
3. Common cause: A tool is returning an error, and E1 keeps retrying with the same approach
4. Solution: Interrupt and give E1 more specific instructions

## Common Mistakes When Reading Debug

| Mistake | Reality |
|---------|---------|
| "The system prompt is wrong" | It's the same every time — that's by design |
| "Token count seems too high" | System prompt + tools = ~23,000 tokens baseline, before your conversation |
| "Duration is 0ms" | Some cached or no-op operations complete instantly |
| "I see `thinking` tokens" | Extended thinking is normal — it's the AI reasoning before responding |

## Verifying the Correct Agent Is Loaded

Use the Debug Panel for definitive verification:

1. **Copy a unique sentence** from the agent's prompt file on GitHub
2. **Start a job**, send any message, open Debug
3. **Search** for that unique sentence in `body.system`
4. **Found?** The correct prompt is loaded at runtime

This is the only reliable way to confirm which agent version is running.
""")

# ============================================================
# 2. Agent Framework Landscape (863 -> ~5500 chars)
# ============================================================
update_doc("Agent Framework Landscape", """# Agent Framework Landscape

The AI agent ecosystem is evolving rapidly. Understanding where E1 fits — and how other frameworks approach the same problems — helps you make better architectural decisions.

## Framework Comparison

| Framework | Creator | Focus | Architecture | Production-Ready? |
|-----------|---------|-------|-------------|-------------------|
| **E1 (Emergent)** | Emergent Labs | Full-stack coding | Single orchestrator + specialist subagents | Yes |
| **LangChain** | LangChain Inc | General LLM apps | Chain/graph-based composition | Yes |
| **CrewAI** | CrewAI | Multi-agent teams | Role-based agent crews | Yes |
| **AutoGen** | Microsoft | Multi-agent conversation | Conversational agents | Yes |
| **OpenAI Assistants** | OpenAI | Managed agent service | API-based, hosted by OpenAI | Yes |
| **Anthropic MCP** | Anthropic | Tool protocol standard | Protocol layer, not a framework | N/A (protocol) |
| **LlamaIndex** | LlamaIndex | Data-focused agents | Index + query engine | Yes |
| **Semantic Kernel** | Microsoft | Enterprise integration | Plugin-based, .NET/Python | Yes |

## Deep Dive: How Each Approaches Key Problems

### Tool Use

| Framework | Approach | E1's Approach |
|-----------|----------|---------------|
| **LangChain** | Tools as Python functions decorated with `@tool` | Tools defined in `aps.yaml`, executed in Kubernetes pods |
| **CrewAI** | Tools assigned per-agent role | Tools shared across E1, delegated to subagents when specialized |
| **AutoGen** | Tools registered on agent instances | Centralized tool registry, available to all agents |
| **OpenAI Assistants** | JSON schema tool definitions via API | Similar schema approach, but self-hosted |

### Memory & Context

| Framework | Approach | E1's Approach |
|-----------|----------|---------------|
| **LangChain** | Buffer, summary, or vector memory modules | Context compaction + memory files (PRD.md) |
| **CrewAI** | Shared crew memory | Subagents are stateless; context passed per-call |
| **AutoGen** | Conversation history between agents | Full conversation in LLM context window |
| **Semantic Kernel** | Plugin-based memory stores | MongoDB + filesystem persistence |

### Multi-Agent Coordination

| Framework | Approach | E1's Approach |
|-----------|----------|---------------|
| **CrewAI** | Agents with roles, goals, backstories in a "crew" | Main agent (E1) delegates to specialist subagents |
| **AutoGen** | Agents chat with each other in conversation threads | E1 calls subagents as tools, receives structured responses |
| **LangChain** | LangGraph for stateful multi-step workflows | Implicit workflow via system prompt instructions |

## When to Use What

### Choose E1 (Emergent) When:
- You need a **complete development environment** (code + deploy + test)
- You want **zero infrastructure setup** — pods, databases, preview URLs all managed
- You need an agent that can **execute code**, not just generate it
- You're building **full-stack web applications**

### Choose LangChain When:
- You're building a **custom LLM application** (not a coding agent)
- You need **fine-grained control** over every chain step
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

## Key Architectural Difference: E1's Approach

Most frameworks treat the LLM as the **center of the system**. E1 treats the LLM as a **component within a larger orchestration layer**:

```mermaid
flowchart TB
    subgraph Others["Traditional Framework"]
        LLM1[LLM] --> T1[Tools]
        LLM1 --> T2[Memory]
        LLM1 --> T3[Retrieval]
    end
    subgraph E1Arch["E1 Architecture"]
        ORCH[Orchestrator] --> LLM2[LLM<br/>Reasoning Only]
        ORCH --> TOOLS[Tool Registry]
        ORCH --> SUB[Subagents]
        ORCH --> CTX[Context Manager]
        ORCH --> EXEC[Execution Engine<br/>Kubernetes Pod]
    end
```

The orchestrator controls the loop: receive input → ask LLM for a plan → execute tools → feed results back → repeat. The LLM never directly executes anything — it only reasons and decides.

## The MCP Protocol: A New Standard

Anthropic's **Model Context Protocol (MCP)** is emerging as a standard for how AI agents interact with tools:

| Aspect | Before MCP | With MCP |
|--------|-----------|----------|
| Tool integration | Custom per-framework | Standardized protocol |
| Tool discovery | Hardcoded in config | Dynamic discovery |
| Cross-framework | Not portable | Portable across frameworks |

E1 uses its own tool protocol today but the concepts align: tools are defined with schemas, called with parameters, and return structured results. MCP standardizes the *wire format* for this interaction.

## Common Misconception

> "Framework X is better than Framework Y"

This misses the point. Each framework optimizes for a different workflow. The right question is: **"Which framework matches my use case?"** — not which one has the most GitHub stars.
""")

# ============================================================
# 3. Prompt Engineering Techniques (1173 -> ~7000 chars)
# ============================================================
update_doc("Prompt Engineering Techniques", """# Prompt Engineering Techniques

The system prompt is what transforms a generic LLM into E1. Same LLM + different prompt = completely different agent. This document covers the techniques that make E1's prompt effective, with examples you can apply to your own AI applications.

## The Anatomy of E1's System Prompt

E1's system prompt is approximately **15,000 tokens** and follows a deliberate structure:

```
┌─────────────────────────────────┐
│  1. Identity & Role Definition  │  "You are E1..."
├─────────────────────────────────┤
│  2. Environment Setup           │  Ports, URLs, services
├─────────────────────────────────┤
│  3. Development Workflow        │  Step-by-step process
├─────────────────────────────────┤
│  4. Tool Usage Guidelines       │  When/how to use each tool
├─────────────────────────────────┤
│  5. Critical Rules              │  Hard constraints
├─────────────────────────────────┤
│  6. Integration Guidelines      │  3rd party service rules
├─────────────────────────────────┤
│  7. Testing Protocol            │  How to verify work
├─────────────────────────────────┤
│  8. UI/UX Guidelines            │  Design standards
└─────────────────────────────────┘
```

## Technique 1: Role Definition

**What it does:** Establishes identity, expertise level, and behavioral boundaries.

**Bad example:**
```
You are a helpful assistant that writes code.
```

**Good example (E1's approach):**
```
You are E1, a full-stack coding agent created by Emergent Labs.
Your responsibility is to build and modify full-stack applications.
```

**Why it works:** Specific identity ("E1") creates consistent behavior. "Full-stack coding agent" narrows the domain, preventing the LLM from trying to be a general chatbot.

## Technique 2: Structured Sections with XML Tags

**What it does:** Uses XML-like tags to create parseable, referenceable sections.

**Example from E1's prompt:**
```xml
<ENVIRONMENT SETUP>
  Backend runs on 0.0.0.0:8001
  Frontend runs on port 3000
  All backend routes prefixed with /api
</ENVIRONMENT SETUP>

<CRITICAL RULES>
  NEVER delete initial keys from .env files
  Use yarn for frontend dependencies
</CRITICAL RULES>
```

**Why it works:** LLMs can "search" within structured sections more reliably than in flat text. When E1 needs to check a port number, it "looks in" the `ENVIRONMENT SETUP` section, reducing hallucination.

## Technique 3: Few-Shot Examples

**What it does:** Provides concrete examples instead of abstract descriptions.

**Bad example:**
```
Use descriptive test IDs for all elements.
```

**Good example (E1's approach):**
```
Every interactive element MUST have a data-testid.
Naming: Use clear, kebab-case, describing the element's function.
Example: data-testid="login-form-submit-button"
Example: data-testid="patient-dashboard"
```

**Why it works:** The LLM pattern-matches from examples. Given `login-form-submit-button`, it will generate `signup-form-email-input` — following the same convention without being told the rule explicitly.

## Technique 4: Negative Instructions (Don'ts)

**What it does:** Explicitly prevents known failure modes.

**Examples from E1's prompt:**
```
- Do NOT use uvicorn to start your own server
- NEVER delete initial keys from .env files
- Do NOT add comments in .env files
- Avoid emoji characters for icons
```

**Why it works:** LLMs tend toward "helpful" behaviors that can be destructive in a development environment (like "helpfully" restarting a server or "cleaning up" an .env file). Negative instructions override these defaults.

## Technique 5: Decision Trees

**What it does:** Provides conditional logic for tool/action selection.

**Example from E1's prompt:**
```
### Quick Testing Rules:
- Single/Small Change: Self-test (Curl + Screenshot)
- Multiple Features: Batch coding -> One Screenshot -> Testing Agent
- 3+ related endpoints: testing_agent_v3_fork
- Recurring blocker: Troubleshoot subagent
```

**Why it works:** Instead of hoping the LLM makes the right meta-decision, you encode the decision tree directly. The LLM follows the tree rather than improvising.

## Technique 6: Self-Checking Prompts

**What it does:** Forces the LLM to verify its own output before proceeding.

**Example from E1's prompt:**
```
Every time you write code that returns data from MongoDB, 
pause and answer these questions:
- Did I exclude _id in the projection?
- Did I insert/update? MongoDB mutates input dicts
- Are there any ObjectId references in my response?
If "yes" or "maybe," trace the actual contents before returning.
```

**Why it works:** This creates an internal "review step" that catches common bugs before they reach the user. It's essentially pair-programming with yourself.

## Technique 7: Priority Hierarchies

**What it does:** Resolves conflicts when multiple instructions apply.

**Example from E1's prompt:**
```
Priority: Last working item > User Verification > 
(Issues, In progress task) > Upcoming Tasks
```

**Why it works:** Without explicit priorities, the LLM picks whatever seems most "helpful" in the moment — which might be the wrong thing. Priority hierarchies prevent thrashing between tasks.

## Technique 8: Output Format Control

**What it does:** Constrains the format of generated output.

**Example:**
```
Finish should include:
- What you completed (with testing status). Max 3 lines.
- Next Action Items
- Future/Backlog
- One ENHANCEMENT relevant to the app's purpose
```

**Why it works:** LLMs tend to be verbose. Format constraints produce consistent, scannable output that users can quickly parse.

## Common Prompt Engineering Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Too vague | "Be helpful" — means nothing specific | Define exact behaviors and examples |
| Too long without structure | LLM loses track of instructions | Use sections, headers, XML tags |
| Contradictory instructions | "Be concise" + "Explain thoroughly" | Specify when each applies |
| No examples | LLM invents its own patterns | Always provide concrete examples |
| No negative instructions | LLM does "helpful" but destructive things | Explicitly list what NOT to do |
| Assuming knowledge | "Use the standard approach" | State the exact approach you want |

## Try It Yourself: Building a Custom Agent Prompt

Here's a template for creating your own agent prompt:

```markdown
# Role
You are [NAME], a [DOMAIN] specialist. You [PRIMARY FUNCTION].

# Environment
- [Service 1] runs on [port/URL]
- [Service 2] configuration: [details]
- Database: [type and connection]

# Workflow
1. When user asks for [X], first [STEP 1]
2. Then [STEP 2]
3. Always verify by [VERIFICATION METHOD]

# Rules
- NEVER [dangerous action 1]
- ALWAYS [required action 1]
- When in doubt, [fallback behavior]

# Examples
User: "[example input]"
Agent: "[example output showing desired format]"
```

## Advanced: Chain-of-Thought Prompting

E1 uses **extended thinking** — the LLM has a dedicated space to reason before responding. This is different from chain-of-thought prompting in a regular prompt:

| Approach | How It Works | When to Use |
|----------|-------------|-------------|
| **Zero-shot** | Just ask the question | Simple, factual queries |
| **Few-shot** | Provide examples before asking | Pattern-matching tasks |
| **Chain-of-thought** | "Think step by step" in the prompt | Multi-step reasoning |
| **Extended thinking** | Dedicated thinking tokens (model feature) | Complex planning, debugging |

E1's system prompt doesn't say "think step by step" — instead, the model's thinking capability is enabled at the API level via model configuration. The system prompt focuses on *what* to think about, not *how* to think.
""")

# ============================================================
# 4. React Virtual DOM & Hooks (1967 -> ~5500 chars)
# ============================================================
update_doc("React Virtual DOM & Hooks", """# React Virtual DOM & Hooks

React's power comes from its reconciliation algorithm and hooks system. This document explains both in depth, with practical examples relevant to building on Emergent.

## The Reconciliation Pipeline

```mermaid
flowchart LR
    SC[State Change] --> VDOM[New Virtual DOM]
    VDOM --> DIFF[Diff Algorithm]
    DIFF --> MIN[Minimal Update List]
    MIN --> REAL[Apply to Real DOM]
    REAL --> RENDER[Browser Paints]
```

**How it works:**

1. **State Change** — Something triggers a re-render: `setState`, `useReducer` dispatch, context change, or parent re-render
2. **Virtual DOM** — React creates a new lightweight JavaScript object tree representing the desired UI
3. **Diff Algorithm** — React compares new vs old Virtual DOM using an O(n) heuristic:
   - Different element type? Destroy old tree, build new one
   - Same element type? Update only changed props
   - List items? Use `key` prop to track identity
4. **Minimal Updates** — Only the changed DOM nodes are updated
5. **Browser Paint** — The browser re-renders only affected pixels

## Why Keys Matter

```jsx
// BAD: React can't track items across re-renders
{items.map((item, index) => (
  <ListItem key={index} data={item} />
))}

// GOOD: React can identify and reuse each item
{items.map(item => (
  <ListItem key={item.id} data={item} />
))}
```

Without stable keys, React destroys and recreates every list item on every re-render. With stable keys, it only updates items that actually changed. This matters enormously for performance in lists with 100+ items.

## Hooks Deep Dive

### useState: The Basics

```jsx
const [count, setCount] = useState(0);

// Direct update
setCount(5);

// Functional update (use when new state depends on old)
setCount(prev => prev + 1);
```

**Gotcha:** State updates are asynchronous and batched. This doesn't work:
```jsx
setCount(count + 1);
setCount(count + 1); // Still uses the OLD count value!
// Result: count increments by 1, not 2

// Fix: use functional updates
setCount(prev => prev + 1);
setCount(prev => prev + 1); // Correctly increments by 2
```

### useEffect: Side Effects

```jsx
useEffect(() => {
  // Runs after render
  const subscription = api.subscribe(data);

  // Cleanup function — runs before next effect or unmount
  return () => subscription.unsubscribe();
}, [data]); // Only re-run when `data` changes
```

**Common Mistakes:**

| Mistake | What Happens | Fix |
|---------|-------------|-----|
| Missing dependency | Stale closures — uses old values | Add all referenced variables to deps array |
| Object in deps | Infinite re-render loop | Use `useMemo` to stabilize the object |
| No cleanup | Memory leaks from subscriptions/timers | Always return a cleanup function |
| Empty deps `[]` | Effect runs only once (mount) | Intentional for "on mount" effects only |

### useCallback: Memoizing Functions

```jsx
// Without useCallback: new function created every render
// Child components re-render unnecessarily
const handleClick = () => doSomething(id);

// With useCallback: same function reference between renders
const handleClick = useCallback(() => {
  doSomething(id);
}, [id]); // Only recreate when id changes
```

**When to use:** When passing callbacks to child components wrapped in `React.memo`, or when the callback is a dependency of `useEffect`.

### useMemo: Memoizing Computations

```jsx
// Expensive computation runs every render
const sorted = items.sort((a, b) => a.name.localeCompare(b.name));

// With useMemo: only re-computes when items change
const sorted = useMemo(() => {
  return items.sort((a, b) => a.name.localeCompare(b.name));
}, [items]);
```

### useRef: Escaping the Render Cycle

```jsx
const wsRef = useRef(null);

// Persists across renders without triggering re-render
wsRef.current = new WebSocket(url);

// Common use: accessing DOM elements
const inputRef = useRef(null);
<input ref={inputRef} />
inputRef.current.focus(); // Direct DOM access
```

## Performance Optimization Checklist

| Technique | When to Use | Impact |
|-----------|------------|--------|
| `React.memo()` | Component re-renders with same props | Prevents unnecessary child renders |
| `useCallback` | Callbacks passed to memoized children | Stabilizes function references |
| `useMemo` | Expensive computations in render | Caches computed values |
| `key` prop | Dynamic lists | Enables efficient list diffing |
| Code splitting | Large apps with many routes | Reduces initial bundle size |
| `lazy()` + `Suspense` | Route-level components | Loads components on demand |

## Common React Anti-Patterns

### 1. State That Should Be Derived
```jsx
// BAD: Synchronized state
const [items, setItems] = useState([]);
const [count, setCount] = useState(0);
// Must manually keep count in sync with items

// GOOD: Derive from source of truth
const [items, setItems] = useState([]);
const count = items.length; // Always correct
```

### 2. Props Drilling
```jsx
// BAD: Passing props through 5 component levels
<App user={user}>
  <Layout user={user}>
    <Sidebar user={user}>
      <UserBadge user={user} />

// GOOD: Use Context for truly global state
const UserContext = createContext(null);
// Any descendant can access: useContext(UserContext)
```

### 3. useEffect for Everything
```jsx
// BAD: Effect to transform data
useEffect(() => {
  setFilteredItems(items.filter(i => i.active));
}, [items]);

// GOOD: Compute during render
const filteredItems = items.filter(i => i.active);
// Or with useMemo if expensive:
const filteredItems = useMemo(() => items.filter(i => i.active), [items]);
```

## Troubleshooting React Issues

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Infinite re-render loop | Object/array in useEffect deps | Memoize with useMemo |
| Stale state in callback | Missing dependency in useCallback | Add to deps array |
| Component not updating | Mutating state directly | Always create new objects/arrays |
| Memory leak warning | Missing cleanup in useEffect | Return cleanup function |
| Slow list rendering | Missing or index-based keys | Use stable unique keys |
""")

# ============================================================
# 5. Git Internals & Rollback (1656 -> ~5000 chars)
# ============================================================
update_doc("Git Internals & Rollback", """# Git Internals & Rollback

Understanding Git's internal model helps you recover from almost any mistake. On Emergent, Git is also the backbone of the rollback system.

## Git's Object Model

```mermaid
flowchart TD
    C1[Commit abc123] --> T1[Tree: root/]
    T1 --> B1[Blob: server.py]
    T1 --> B2[Blob: .env]
    T1 --> T2[Tree: src/]
    T2 --> B3[Blob: App.js]
    C1 --> C0[Parent Commit def456]
```

**Everything in Git is an object:**

| Object Type | What It Stores | Identified By |
|------------|----------------|---------------|
| **Blob** | File contents (no filename!) | SHA-1 hash of content |
| **Tree** | Directory listing (names → blob/tree refs) | SHA-1 hash |
| **Commit** | Tree ref + parent ref + author + message | SHA-1 hash |
| **Tag** | Named pointer to a commit | Name string |

Key insight: Git doesn't store *diffs*. Every commit contains a *complete snapshot* of every file. Disk space is managed through compression and deduplication (same content = same blob hash).

## How Branches Work

A branch is just a **text file containing a commit hash**:

```
.git/refs/heads/main → abc123def456...
.git/HEAD → ref: refs/heads/main
```

When you commit, Git:
1. Creates new blob objects for changed files
2. Creates a new tree object pointing to all blobs
3. Creates a new commit object pointing to the tree + parent commit
4. Updates the branch file to point to the new commit

That's it. "Branching" is literally writing 40 characters to a file.

## The Emergent Auto-Commit System

On Emergent, E1 auto-commits after every step. This means:

```
commit 7: "Added login endpoint"
commit 6: "Installed dependencies"
commit 5: "Created server.py"
commit 4: "Updated .env"
commit 3: "Created project structure"
commit 2: "Initial seed data"
commit 1: "Initial commit"
```

**Every step is a checkpoint you can return to.**

### Using Rollback on Emergent

| Method | How | When to Use |
|--------|-----|------------|
| **UI Rollback** | Click "Rollback" in the Emergent chat, select a checkpoint | Safest — recommended for most cases |
| **Git Reset** (manual) | `git reset --hard <commit>` | Only if you understand the consequences |

**Important:** Always use the UI rollback feature. Manual `git reset` can conflict with Emergent's internal tracking.

## Common Git Scenarios

### Scenario 1: "E1 broke my app, I want to go back"
1. Click **Rollback** in the chat interface
2. Select the checkpoint before the breaking change
3. The codebase reverts to that exact state
4. Continue working from the restored state

### Scenario 2: "I want to see what changed"
```bash
# View recent commits
git log --oneline -10

# See what changed in a specific commit
git show <commit-hash> --stat

# See the full diff of a commit
git show <commit-hash>
```

### Scenario 3: "I want to save my work to GitHub"
Use the **"Save to GitHub"** button in the chat input. This pushes all auto-commits to your connected GitHub repository.

## How Git Diff Actually Works

```mermaid
flowchart LR
    A[Old Tree] --> D{Compare}
    B[New Tree] --> D
    D --> S1[Same hash = unchanged]
    D --> S2[Different hash = changed]
    D --> S3[Missing = deleted]
    D --> S4[New = added]
```

Git compares trees by hash. If a file's blob hash is identical in both trees, the file is unchanged — Git doesn't even look at the content. This makes diffing very fast, even for large repositories.

## Under the Hood: What `git commit` Does

```
1. Stage: git add file.py
   → Creates blob object for file.py
   → Updates .git/index (staging area)

2. Commit: git commit -m "message"
   → Creates tree object from staging area
   → Creates commit object (tree + parent + message)
   → Updates branch ref to new commit hash

3. Storage:
   → Objects stored in .git/objects/
   → Compressed with zlib
   → Packed periodically for efficiency
```

## Troubleshooting Git Issues

| Problem | Cause | Solution |
|---------|-------|----------|
| "Detached HEAD" | Checked out a commit directly | `git checkout main` to reattach |
| "Merge conflict" | Two branches changed same lines | Edit conflict markers, then commit |
| "Cannot push" | Remote has commits you don't | `git pull --rebase` first |
| "Lost my changes" | Hard reset or force push | `git reflog` — Git keeps everything for 30 days |
| Auto-commit clutters history | Expected on Emergent | Use "Save to GitHub" which preserves the full history |

## Git Reflog: Your Safety Net

Even after `git reset --hard`, your old commits aren't gone:

```bash
git reflog
# Shows EVERY position HEAD has been at:
# abc1234 HEAD@{0}: reset: moving to abc1234
# def5678 HEAD@{1}: commit: Added login endpoint  ← still here!
# ghi9012 HEAD@{2}: commit: Created server.py

git checkout def5678  # Recover the "lost" commit
```

The reflog keeps entries for 30 days by default. As long as you act within that window, nothing is truly lost.
""")

print("\n=== Enhancement #5 Batch 1 Complete ===")
print("Updated: Debug Panel, Agent Framework Landscape, Prompt Engineering, React Virtual DOM, Git Internals")
