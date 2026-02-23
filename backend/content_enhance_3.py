"""Content Enhancement Script - Batch 3
Enhancement #7: Getting Started / Onboarding Guide
Enhancement #3: Real-World Use Cases & Scenarios
Enhancement #4: Comparison & Decision-Making Content"""

from pymongo import MongoClient
from datetime import datetime, timezone
import uuid

client = MongoClient('mongodb://localhost:27017')
db = client['test_database']
NOW = datetime.now(timezone.utc).isoformat()

def _id():
    return str(uuid.uuid4())

def create_category(name, icon, order, parent_id=None, internal=False):
    cat_id = _id()
    doc = {"id": cat_id, "name": name, "icon": icon, "order": order, "parent_id": parent_id}
    if internal:
        doc["internal"] = True
    db.categories.insert_one(doc)
    print(f"Created category: {name} (id={cat_id})")
    return cat_id

def create_doc(title, category_id, content, order=0, tags=None):
    doc_id = _id()
    doc = {
        "id": doc_id, "title": title, "category_id": category_id,
        "author_id": "system", "created_at": NOW, "updated_at": NOW,
        "order": order, "deleted": False, "content": content
    }
    if tags:
        doc["tags"] = tags
    db.documents.insert_one(doc)
    print(f"Created doc: {title} ({len(content)} chars)")
    return doc_id

# ============================================================
# NEW CATEGORY: Getting Started (order: -1, appears first)
# ============================================================
CAT_GETTING_STARTED = create_category("Getting Started", "Rocket", -1)
SUB_FIRST_10 = create_category("Quick Start", "Sparkles", 0, CAT_GETTING_STARTED)
SUB_TALKING_TO_E1 = create_category("Working with E1", "MessageSquare", 1, CAT_GETTING_STARTED)
SUB_GLOSSARY = create_category("Glossary", "FileText", 2, CAT_GETTING_STARTED)

# --- Doc 1: Your First 10 Minutes ---
create_doc("Your First 10 Minutes on Emergent", SUB_FIRST_10, """# Your First 10 Minutes on Emergent

Welcome to Emergent! This guide walks you through everything you need to know to start building. By the end, you'll have a running app and understand how the platform works.

## What You're Working With

When you start a job on Emergent, you get:

| Resource | What It Is | How to Access |
|----------|-----------|---------------|
| **E1 Agent** | An AI that writes, runs, and tests code for you | Chat interface |
| **Kubernetes Pod** | Your own development server with full Linux access | Via E1's tools |
| **MongoDB** | A database, ready to use | `mongodb://localhost:27017` |
| **Preview URL** | A live URL where your app is accessible | Shown in the UI |
| **Frontend** | React app on port 3000 | Preview URL (no /api prefix) |
| **Backend** | FastAPI server on port 8001 | Preview URL + `/api/...` |

## Step 1: Describe What You Want to Build

Start with a clear description. The more specific, the better:

**Vague (E1 will ask follow-up questions):**
> "Build me a task manager"

**Specific (E1 can start immediately):**
> "Build a task manager with: user authentication, CRUD for tasks with title/description/due date/priority, a dashboard showing tasks grouped by priority, and a dark theme"

**Pro tip:** You don't need to have everything figured out. Start with the core feature, get it working, then iterate.

## Step 2: Watch E1 Work

After you send your request, E1 will:

1. **Plan** — Think about the architecture and approach
2. **Ask clarifying questions** — If anything is ambiguous
3. **Create files** — Backend routes, frontend components, database schemas
4. **Install dependencies** — Packages your app needs
5. **Test** — Run the app and verify it works
6. **Show you the result** — Screenshot or summary

You can watch this process in real-time. Every tool call (file creation, bash command, screenshot) is visible in the chat.

## Step 3: Try Your App

Once E1 says the MVP is ready:

1. **Click the preview URL** shown in the interface
2. Your app opens in a new tab
3. Test the features E1 built
4. Come back and tell E1 what to change

## Step 4: Iterate

This is where the magic happens. Tell E1:

- "The login button should be bigger"
- "Add a search bar to the dashboard"
- "The API is returning a 500 error when I submit the form"
- "Can you add dark mode?"

E1 reads your feedback, looks at the code, makes changes, and tests them. Each iteration is committed to Git automatically.

## What to Do When Something Goes Wrong

| Situation | What to Do |
|-----------|-----------|
| App shows a blank page | Tell E1 — it will check console errors and fix them |
| API returns an error | Share the error message with E1 |
| E1 seems stuck in a loop | Say "stop and try a different approach" |
| You want to undo E1's changes | Use the **Rollback** feature to go back to any checkpoint |
| App works in preview but not after restart | Data might be in filesystem instead of database — tell E1 |

## Understanding the Interface

| UI Element | Purpose |
|------------|---------|
| **Chat input** | Talk to E1 — describe features, report bugs, ask questions |
| **Preview URL** | Link to your running app |
| **Debug Panel** (bug icon) | See E1's internal decision-making |
| **Rollback** | Go back to any previous checkpoint |
| **Save to GitHub** | Push your code to a GitHub repository |
| **File tree** | Browse the files E1 has created |

## Tips for Getting the Best Results

1. **Be specific about what you want** — "Add a red delete button in the top-right corner" beats "add a delete button"
2. **Report bugs with context** — "When I click Submit on the form, nothing happens" is better than "it's broken"
3. **Iterate in small steps** — Get the core working first, then add features one by one
4. **Use screenshots** — If something looks wrong, describe what you see vs. what you expected
5. **Don't be afraid to ask E1 questions** — "How does the authentication work?" is a valid message

## Your First Project Ideas

| Difficulty | Project | What You'll Learn |
|-----------|---------|-------------------|
| Beginner | Todo list with categories | CRUD, state management |
| Beginner | Personal blog | Markdown rendering, routing |
| Intermediate | Chat application | Real-time updates, WebSockets |
| Intermediate | Dashboard with charts | Data visualization, API design |
| Advanced | E-commerce store | Payment integration, auth, file uploads |
| Advanced | AI-powered app | LLM integration, streaming responses |
""", order=0, tags=["getting-started", "beginner"])

# --- Doc 2: How to Talk to E1 ---
create_doc("How to Talk to E1 Effectively", SUB_TALKING_TO_E1, """# How to Talk to E1 Effectively

E1 is a powerful AI agent, but like any tool, the quality of the output depends on the quality of the input. This guide teaches you how to communicate with E1 for the best results.

## The Communication Model

```mermaid
flowchart LR
    YOU[Your Message] --> E1[E1 Processes]
    E1 --> PLAN[Plans Approach]
    PLAN --> TOOLS[Executes Tools]
    TOOLS --> RESULT[Shows Result]
    RESULT --> YOU
```

E1 is not a chatbot — it's an **agent**. Every message you send triggers a planning cycle where E1 decides what tools to use and in what order. Your message quality directly affects this planning.

## Message Types and How E1 Handles Them

### 1. Feature Requests

**What E1 does:** Plans architecture → creates files → installs dependencies → tests → shows result

**Weak:**
> "Add authentication"

**Strong:**
> "Add Google OAuth authentication. Users should see a 'Sign in with Google' button on the login page. After signing in, redirect to the dashboard. Store the user's email and name in MongoDB."

**Why it matters:** The weak version forces E1 to make assumptions about auth type, UI placement, and data storage. The strong version eliminates ambiguity.

### 2. Bug Reports

**What E1 does:** Reads logs → examines code → identifies root cause → applies fix → tests

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

**What E1 does:** Identifies the component → modifies styles/layout → screenshots to verify

**Weak:**
> "Make it look better"

**Strong:**
> "The sidebar is too wide on mobile. Can you make it collapsible with a hamburger menu? Also, the card titles should be larger (maybe text-lg) and the spacing between cards feels too tight."

### 4. Questions

**What E1 does:** Answers based on the codebase and platform knowledge. No tool calls needed for pure questions.

> "How does the authentication flow work in our app?"
> "What database collections are we using?"
> "Can you explain the deployment pipeline?"

### 5. Course Corrections

**What E1 does:** Stops current approach, reassesses, tries alternative

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

### Technique 3: Share Screenshots

If the UI looks wrong, take a screenshot and describe it:
```
"The dashboard looks like [screenshot]. The chart 
should be full-width but it's squished to the left. 
The legend is overlapping the data labels."
```

### Technique 4: Prioritize Explicitly

```
"I have three things to fix:
1. (Critical) Login is completely broken
2. (Medium) Dashboard chart colors are wrong  
3. (Low) Footer text needs updating

Please fix in this order."
```

### Technique 5: Ask E1 to Explain Before Acting

```
"Before making changes, can you explain how the 
current authentication system works? I want to 
understand the flow before we modify it."
```

## What E1 Cannot Do (and What to Do Instead)

| Limitation | Workaround |
|-----------|-----------|
| Can't browse the web freely | Use `web_search` tool — ask E1 to search for specific things |
| Can't see your screen | Describe what you see, share screenshots |
| Can't access external databases | Provide connection strings or API keys |
| Can't remember previous sessions | Reference PRD.md or describe previous decisions |
| Can't run GPU workloads | Use cloud APIs for ML inference |

## The Feedback Loop

The most productive pattern is rapid iteration:

```
You: "Build feature X"
E1: [builds and shows result]
You: "Almost! Change Y and fix Z"
E1: [adjusts]
You: "Perfect. Now add feature W"
```

Each cycle takes 2-5 minutes. In an hour, you can iterate through 12-15 cycles — equivalent to days of solo development.
""", order=0, tags=["getting-started", "tips"])

# --- Doc 3: Platform Glossary ---
create_doc("Platform Glossary", SUB_GLOSSARY, """# Platform Glossary

A comprehensive reference of terms used across the Emergent platform. Bookmark this page for quick lookups.

## A

**Agent** — A software system that uses an LLM to reason and take actions. E1 is Emergent's primary agent. Unlike a chatbot (which only generates text), an agent can execute code, read files, and interact with services.

**Agent Service** — The backend service that manages agent lifecycle, message routing, and tool execution. It sits between the user interface and the LLM provider.

**aps.yaml** — Agent Configuration File. Defines which LLM model to use, available tools, system prompt reference, timeout settings, and context management strategy for each agent.

## C

**Cold Start** — When a pod needs to be allocated and initialized after a period of inactivity. Takes 15-45 seconds. During this time, the app shows a loading screen.

**Context Compaction** — When the conversation history approaches the LLM's token limit, E1 automatically summarizes older messages to free up space. Critical information is preserved, but some details may be lost.

**Context Window** — The maximum number of tokens an LLM can process in a single request. For Claude Sonnet, this is approximately 200K tokens. The system prompt, conversation history, and tool definitions all count toward this limit.

## D

**Debug Panel** — A UI component that shows the raw LLM requests and responses, tool calls, token usage, and timing for every interaction. Essential for understanding E1's decision-making process.

## E

**E1** — Emergent's primary AI coding agent. An orchestration system that uses an LLM (Claude, GPT, etc.) for reasoning while executing actions through tools in a Kubernetes pod.

**Emergent LLM Key (Universal Key)** — A single API key that routes to multiple LLM providers (OpenAI, Anthropic, Google). Simplifies integration by eliminating the need for separate API keys per provider. Works for text generation, image generation (DALL-E, Nano Banana), video (Sora), and Whisper.

## F

**Fork** — Creating a new agent session that continues from the state of a previous session. The new session gets a handoff summary but no conversation history.

## H

**Handoff Summary** — A structured document passed between forked sessions. Contains the original problem statement, completed work, pending issues, code architecture, and technical decisions. Acts as institutional memory across sessions.

**Hot Reload** — Automatic restart of the frontend or backend when code files change. Enabled by default on Emergent — you don't need to manually restart services after code changes.

## I

**Ingress** — The Kubernetes component that routes external HTTP/HTTPS traffic to the correct internal service. On Emergent, it routes `/api/*` requests to port 8001 (backend) and everything else to port 3000 (frontend).

## K

**Kubernetes Pod** — An isolated compute environment allocated to each user session. Contains the full development stack: Node.js, Python, MongoDB, and all application code. Pods are ephemeral — they're created on demand and recycled after inactivity.

## L

**LLM (Large Language Model)** — A neural network trained on text data that predicts the next token. Examples: Claude, GPT, Gemini. An LLM by itself cannot take actions — it only generates text. E1 wraps an LLM to give it the ability to act.

**LLM Proxy** — An intermediary service that routes LLM requests to the appropriate provider, handles authentication, tracks token usage, and enforces budget limits. The Universal Key is authenticated through this proxy.

## M

**MCP (Model Context Protocol)** — A standard protocol by Anthropic for how AI agents interact with tools. Defines how tools are discovered, called, and how results are returned.

**Memory File** — A persistent Markdown file (typically `PRD.md`) stored in the project that preserves critical decisions and state across agent sessions. E1 reads this file at the start of each forked session.

## P

**Preview URL** — A temporary, publicly accessible URL assigned to your pod. Format: `https://<app-name>.preview.emergentagent.com`. Changes when a new pod is allocated.

**PRD.md** — Product Requirements Document. A file at `/app/memory/PRD.md` that captures the original problem statement, implemented features, and remaining backlog. Used for continuity across sessions.

## R

**Rollback** — Reverting the codebase to a previous Git checkpoint. On Emergent, every E1 action creates a commit, so you can roll back to any previous state using the UI feature.

## S

**Seed Data** — Initial data loaded into the database when the application is first set up. On this Knowledge Hub, all documentation content is defined in `seed_data.py`.

**Subagent** — A specialist AI agent that E1 delegates specific tasks to. Examples: `testing_agent` (runs tests), `design_agent` (creates UI guidelines), `troubleshoot_agent` (root cause analysis). Subagents are stateless and receive full context from E1 each time.

**Supervisor** — A process management system (`supervisord`) that runs on the pod. It manages the frontend, backend, and MongoDB processes, automatically restarting them if they crash.

## T

**Token** — The fundamental unit of text for LLMs. Roughly 3-4 characters per token. "Hello world" = 2 tokens. Costs are calculated per-token, with separate rates for input and output tokens.

**Tool** — A capability that E1 can invoke to take actions. Examples: `create_file`, `execute_bash`, `view_file`, `web_search`, `screenshot`. Tools are defined in the agent configuration and executed in the Kubernetes pod.

## U

**Universal Key** — See "Emergent LLM Key."

## W

**WebSocket** — A persistent, bidirectional communication protocol. Used in Emergent for features like real-time collaborative editing and live streaming of agent responses.
""", order=0, tags=["getting-started", "reference"])

# ============================================================
# NEW CATEGORY: Tutorials (order: 0.5, between Getting Started and Platform Arch)
# ============================================================
CAT_TUTORIALS = create_category("Tutorials", "Telescope", -0.5)
SUB_TUT_CRUD = create_category("Build a CRUD API", "Server", 0, CAT_TUTORIALS)
SUB_TUT_DEBUG = create_category("Debugging Guide", "Search", 1, CAT_TUTORIALS)
SUB_TUT_COMPARE = create_category("Comparisons", "Layers", 2, CAT_TUTORIALS)

# --- Tutorial 1: Building a CRUD API Step-by-Step ---
create_doc("Building a REST API from Scratch", SUB_TUT_CRUD, """# Building a REST API from Scratch

A complete, step-by-step tutorial for building a task management API on Emergent. This covers database design, API routes, error handling, and testing.

## What We're Building

A task management API with:
- Create, read, update, delete tasks
- Filter by status and priority
- Pagination for listing tasks
- Proper error handling

## Step 1: Database Schema Design

Before writing any code, define your data model:

```python
# A task document in MongoDB
{
    "id": "uuid-string",
    "title": "Complete project proposal",
    "description": "Write the Q1 proposal with budget estimates",
    "status": "in_progress",    # todo | in_progress | done
    "priority": "high",          # low | medium | high
    "due_date": "2026-03-15T00:00:00Z",
    "created_at": "2026-02-01T10:30:00Z",
    "updated_at": "2026-02-01T10:30:00Z"
}
```

**Design decisions:**
- `id` is a UUID string (not MongoDB's ObjectId) — easier to serialize to JSON
- Timestamps in ISO 8601 format — universally parseable
- Status and priority as strings — flexible, self-documenting

## Step 2: Pydantic Models

Define request/response schemas using Pydantic:

```python
from pydantic import BaseModel
from typing import Optional
from enum import Enum

class TaskStatus(str, Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"

class TaskPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = ""
    status: TaskStatus = TaskStatus.todo
    priority: TaskPriority = TaskPriority.medium
    due_date: Optional[str] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[str] = None
```

**Why Pydantic?** It validates input automatically. If someone sends `status: "invalid"`, FastAPI returns a 422 error with a clear message — no manual validation needed.

## Step 3: CRUD Endpoints

```python
from fastapi import APIRouter, HTTPException, Query
from datetime import datetime, timezone
import uuid

router = APIRouter(prefix="/api")

# CREATE
@router.post("/tasks")
async def create_task(data: TaskCreate):
    task = {
        "id": str(uuid.uuid4()),
        **data.model_dump(),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    await db.tasks.insert_one(task)
    # Return without _id (MongoDB adds it automatically)
    return await db.tasks.find_one({"id": task["id"]}, {"_id": 0})

# READ (single)
@router.get("/tasks/{task_id}")
async def get_task(task_id: str):
    task = await db.tasks.find_one({"id": task_id}, {"_id": 0})
    if not task:
        raise HTTPException(404, "Task not found")
    return task

# READ (list with filtering and pagination)
@router.get("/tasks")
async def list_tasks(
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100)
):
    query = {}
    if status:
        query["status"] = status.value
    if priority:
        query["priority"] = priority.value
    
    skip = (page - 1) * limit
    tasks = await db.tasks.find(query, {"_id": 0}) \\
        .sort("created_at", -1) \\
        .skip(skip) \\
        .limit(limit) \\
        .to_list(limit)
    
    total = await db.tasks.count_documents(query)
    return {
        "tasks": tasks,
        "total": total,
        "page": page,
        "pages": (total + limit - 1) // limit
    }

# UPDATE
@router.put("/tasks/{task_id}")
async def update_task(task_id: str, data: TaskUpdate):
    task = await db.tasks.find_one({"id": task_id})
    if not task:
        raise HTTPException(404, "Task not found")
    
    update = {k: v for k, v in data.model_dump().items() if v is not None}
    if not update:
        # Nothing to update
        return await db.tasks.find_one({"id": task_id}, {"_id": 0})
    
    update["updated_at"] = datetime.now(timezone.utc).isoformat()
    await db.tasks.update_one({"id": task_id}, {"$set": update})
    return await db.tasks.find_one({"id": task_id}, {"_id": 0})

# DELETE
@router.delete("/tasks/{task_id}")
async def delete_task(task_id: str):
    result = await db.tasks.delete_one({"id": task_id})
    if result.deleted_count == 0:
        raise HTTPException(404, "Task not found")
    return {"status": "deleted", "id": task_id}
```

## Step 4: Testing with curl

```bash
# Create a task
curl -X POST $API_URL/api/tasks \\
  -H "Content-Type: application/json" \\
  -d '{"title": "Learn Emergent", "priority": "high"}'

# List all tasks
curl $API_URL/api/tasks

# Filter by status
curl "$API_URL/api/tasks?status=todo&priority=high"

# Update a task
curl -X PUT $API_URL/api/tasks/{id} \\
  -H "Content-Type: application/json" \\
  -d '{"status": "done"}'

# Delete a task
curl -X DELETE $API_URL/api/tasks/{id}
```

## Step 5: Common Patterns

### Error Response Format

Standardize your error responses:

```python
# Always return the same error shape
{"detail": "Task not found"}          # 404
{"detail": "Validation error", ...}   # 422 (automatic from Pydantic)
{"detail": "Not authorized"}          # 403
```

### Soft Delete Pattern

Instead of permanently deleting records:

```python
@router.delete("/tasks/{task_id}")
async def soft_delete_task(task_id: str):
    await db.tasks.update_one(
        {"id": task_id},
        {"$set": {"deleted": True, "deleted_at": NOW}}
    )
    return {"status": "deleted"}

# Always exclude soft-deleted items from queries
@router.get("/tasks")
async def list_tasks():
    query = {"deleted": {"$ne": True}}
    # ...
```

### Index Strategy

```python
# Create indexes for common query patterns
await db.tasks.create_index("id", unique=True)
await db.tasks.create_index("status")
await db.tasks.create_index("priority")
await db.tasks.create_index("created_at")
```

## MongoDB Gotchas

| Gotcha | What Happens | Prevention |
|--------|-------------|------------|
| Returning `_id` | `ObjectId is not JSON serializable` error | Always use `{"_id": 0}` in projections |
| Mutating insert dict | `insert_one` adds `_id` to your dict | Don't reuse the dict after insert |
| No schema enforcement | Typos in field names silently succeed | Use Pydantic models for validation |
| String vs ObjectId queries | Query returns nothing | Use string IDs (`uuid.uuid4()`) |
| `datetime.utcnow()` | Returns naive datetime (deprecated) | Use `datetime.now(timezone.utc)` |
""", order=0, tags=["tutorial", "backend", "api"])

# --- Tutorial 2: Debugging a 500 Error ---
create_doc("Debugging a 500 Error Step-by-Step", SUB_TUT_DEBUG, """# Debugging a 500 Error Step-by-Step

A practical walkthrough of how to diagnose and fix a server error, following the same process E1 uses.

## The Scenario

Your app was working, and now an endpoint returns:

```json
{
    "detail": "Internal Server Error"
}
```

No useful information. Just a 500 status code. Here's how to find and fix the problem.

## Step 1: Check the Logs

The **first and most important step**. Always check logs before touching code.

```bash
# Backend logs (most recent 100 lines)
tail -n 100 /var/log/supervisor/backend.err.log

# Look for the actual error
tail -n 100 /var/log/supervisor/backend.err.log | grep -A 5 "Error\\|Exception\\|Traceback"
```

**What you're looking for:**

```
Traceback (most recent call last):
  File "/app/backend/server.py", line 142, in get_tasks
    tasks = await db.tasks.find(query).to_list(100)
  File "motor/core.py", line 246, in to_list
    ...
TypeError: 'NoneType' object is not iterable
```

The traceback tells you:
- **Which file:** `server.py`
- **Which line:** 142
- **Which function:** `get_tasks`
- **The actual error:** `TypeError: 'NoneType' object is not iterable`

## Step 2: Reproduce the Error

Before fixing anything, **reproduce it consistently**:

```bash
# Try the exact request that's failing
curl -v $API_URL/api/tasks

# Check: does it fail every time?
# Check: does it fail with specific parameters?
curl "$API_URL/api/tasks?status=done"   # This one works
curl "$API_URL/api/tasks?status=invalid" # This one fails!
```

## Step 3: Identify the Root Cause

Common root causes for 500 errors:

| Root Cause | Clue in Logs | Example |
|-----------|-------------|---------|
| **Unhandled None** | `'NoneType' object has no attribute` | Forgot to check if query returned results |
| **Missing field** | `KeyError: 'status'` | Document in DB missing expected field |
| **Bad ObjectId** | `ObjectId is not JSON serializable` | Returning MongoDB `_id` in response |
| **Import error** | `ModuleNotFoundError` | Package not installed or wrong import |
| **Syntax error** | `SyntaxError: invalid syntax` | Typo in code, hot reload loaded bad code |
| **Database connection** | `ServerSelectionTimeoutError` | MongoDB not running |
| **Environment variable** | `KeyError: 'MONGO_URL'` | Missing or misconfigured .env |

## Step 4: Apply the Fix

For our example (`TypeError: 'NoneType' object is not iterable`):

```python
# BEFORE (broken):
@router.get("/tasks")
async def get_tasks(status: str = None):
    query = {"status": status}  # If status is None, query = {"status": None}
    tasks = await db.tasks.find(query, {"_id": 0}).to_list(100)
    return tasks

# AFTER (fixed):
@router.get("/tasks")
async def get_tasks(status: str = None):
    query = {}
    if status:
        query["status"] = status  # Only filter if status provided
    tasks = await db.tasks.find(query, {"_id": 0}).to_list(100)
    return tasks
```

## Step 5: Verify the Fix

```bash
# Test the exact same request that was failing
curl $API_URL/api/tasks
# Should return 200 with task list

# Test edge cases
curl "$API_URL/api/tasks?status=done"
curl "$API_URL/api/tasks?status=todo"
curl $API_URL/api/tasks  # No filter
```

## Step 6: Check for Similar Issues

If this bug existed in `/api/tasks`, the same pattern might exist in other endpoints:

```bash
# Search for similar patterns in the codebase
grep -n "query = {" /app/backend/server.py
```

Fix all instances, not just the one you found.

## Debugging Cheat Sheet

### Quick Diagnosis Commands

```bash
# Is the backend running?
sudo supervisorctl status backend

# Recent errors?
tail -20 /var/log/supervisor/backend.err.log

# Is MongoDB running?
sudo supervisorctl status mongodb

# Can you reach the API?
curl -s -o /dev/null -w "%{http_code}" $API_URL/api/health

# What's in the database?
python3 -c "
from pymongo import MongoClient
db = MongoClient('mongodb://localhost:27017')['test_database']
print(list(db.list_collection_names()))
"
```

### Common Fix Patterns

| Error Type | Quick Fix |
|-----------|----------|
| `ObjectId not serializable` | Add `{"_id": 0}` to all MongoDB queries |
| `ModuleNotFoundError` | `pip install <module> && pip freeze > requirements.txt` |
| `Connection refused` | `sudo supervisorctl restart backend` |
| `CORS error` (in browser) | Check CORS middleware is before routes |
| `422 Unprocessable Entity` | Check request body matches Pydantic model |

### Prevention Checklist

- Always exclude `_id` from MongoDB responses
- Always check `find_one` result for `None` before using
- Always validate input with Pydantic models
- Always test with curl after making changes
- Always check logs, not just the HTTP response
""", order=0, tags=["tutorial", "debugging"])

# --- Comparison Doc: When to Use Which LLM ---
create_doc("Choosing the Right LLM", SUB_TUT_COMPARE, """# Choosing the Right LLM

A practical comparison of the major LLM providers available through Emergent's Universal Key. This guide helps you pick the right model for your use case.

## Quick Comparison Matrix

| Model | Provider | Best For | Speed | Cost | Context Window |
|-------|----------|----------|-------|------|---------------|
| **Claude Sonnet 4.5** | Anthropic | Complex coding, long docs | Medium | Medium | 200K tokens |
| **GPT-5.2** | OpenAI | General tasks, fast iteration | Fast | Medium-High | 128K tokens |
| **GPT-4o** | OpenAI | Balanced performance | Fast | Medium | 128K tokens |
| **GPT-4o-mini** | OpenAI | Quick tasks, low cost | Very Fast | Low | 128K tokens |
| **Gemini 3 Flash** | Google | Speed-critical, high volume | Very Fast | Low | 1M tokens |
| **Gemini 3 Pro** | Google | Complex reasoning | Medium | Medium | 1M tokens |
| **Claude Haiku 4.5** | Anthropic | Simple tasks, low cost | Very Fast | Very Low | 200K tokens |

## When to Use Each Model

### Claude Sonnet 4.5
**Best for:** Complex coding tasks, detailed analysis, long-form content

```
Strengths:
+ Excellent at following complex instructions
+ Best-in-class code generation
+ Strong reasoning with thinking tokens
+ Large context window (200K)

Weaknesses:
- Slower than GPT models
- Can be verbose
- Higher cost for simple tasks
```

**Use when:** Building full-stack applications, debugging complex issues, writing detailed documentation.

### GPT-5.2
**Best for:** General-purpose tasks with high quality needs

```
Strengths:
+ Fast response times
+ Strong at diverse tasks
+ Good multimodal capabilities
+ Reliable function calling

Weaknesses:
- Smaller context window than Claude/Gemini
- Can hallucinate confidently
- Less careful with edge cases than Claude
```

**Use when:** Rapid prototyping, conversational AI, general coding tasks.

### Gemini 3 Flash
**Best for:** High-speed processing, large context needs

```
Strengths:
+ Extremely fast
+ Lowest cost per token
+ 1M token context window
+ Good for batch processing

Weaknesses:
- Less precise for complex code
- May miss nuanced instructions
- Weaker at following long system prompts
```

**Use when:** Processing large documents, real-time applications, cost-sensitive batch operations.

## Cost Comparison

Approximate costs per 1M tokens (via Universal Key):

| Model | Input Cost | Output Cost | Typical API Call |
|-------|-----------|------------|-----------------|
| Claude Haiku 4.5 | $0.25 | $1.25 | ~$0.001 |
| GPT-4o-mini | $0.15 | $0.60 | ~$0.001 |
| Gemini 3 Flash | $0.10 | $0.40 | ~$0.0005 |
| GPT-4o | $2.50 | $10.00 | ~$0.01 |
| Claude Sonnet 4.5 | $3.00 | $15.00 | ~$0.015 |
| GPT-5.2 | $5.00 | $15.00 | ~$0.02 |
| Gemini 3 Pro | $3.50 | $10.50 | ~$0.015 |

*Prices are approximate and may vary. Check your Universal Key dashboard for current rates.*

## Decision Framework

```mermaid
flowchart TD
    START[What are you building?] --> Q1{Need speed or quality?}
    Q1 -->|Speed| Q2{Budget sensitive?}
    Q1 -->|Quality| Q3{Complex code?}
    Q2 -->|Yes| FLASH[Gemini 3 Flash]
    Q2 -->|No| MINI[GPT-4o-mini]
    Q3 -->|Yes| SONNET[Claude Sonnet 4.5]
    Q3 -->|No| GPT[GPT-5.2 or GPT-4o]
```

## Using Multiple Models in One App

You can use different models for different features:

```python
# Cheap model for simple categorization
response_category = await llm.chat(
    model="gemini-3-flash",
    messages=[{"role": "user", "content": f"Categorize: {text}"}]
)

# Powerful model for complex generation
response_content = await llm.chat(
    model="claude-sonnet-4-5",
    messages=[{"role": "user", "content": f"Write detailed analysis of: {text}"}]
)
```

**This is called "model routing"** — use the cheapest model that can handle each specific task. It can reduce costs by 50-80% compared to using a premium model for everything.

## Image Generation Comparison

| Model | Provider | Best For | Style |
|-------|----------|----------|-------|
| **GPT Image 1** | OpenAI | Photorealistic, product mockups | Photographic, clean |
| **Nano Banana** | Google/Gemini | Artistic, illustrations | Creative, stylized |

Both work with the Emergent Universal Key. Neither requires a separate API key.

## Common Mistakes

| Mistake | Problem | Better Approach |
|---------|---------|----------------|
| Using GPT-5.2 for everything | Expensive, slower than needed | Route simple tasks to Haiku/mini |
| Using Flash for code review | Misses nuanced bugs | Use Sonnet for code quality |
| Not setting temperature | Default may be wrong for your use case | 0 for facts, 0.7 for creative, 1 for variety |
| Ignoring token limits | Silent truncation | Count tokens, use larger context models for big inputs |
| Not testing different models | Assuming one model fits all | A/B test with your actual data |
""", order=0, tags=["tutorial", "comparison", "llm"])

# --- Comparison Doc: MongoDB vs PostgreSQL ---
create_doc("MongoDB vs PostgreSQL on Emergent", SUB_TUT_COMPARE, """# MongoDB vs PostgreSQL on Emergent

When should you use MongoDB (the default) vs PostgreSQL? This comparison helps you make the right choice for your project.

## Quick Comparison

| Feature | MongoDB | PostgreSQL |
|---------|---------|------------|
| **Default on Emergent** | Yes | No (requires setup) |
| **Data model** | Documents (flexible JSON) | Tables (strict schema) |
| **Schema** | Schema-less (flexible) | Schema-enforced (strict) |
| **Query language** | MongoDB Query Language | SQL |
| **Joins** | Manual ($lookup) | Native JOIN |
| **Transactions** | Supported (since 4.0) | Full ACID, battle-tested |
| **Best for** | Prototyping, varied data shapes | Relational data, reporting |

## Choose MongoDB When:

### 1. You're Prototyping
MongoDB's flexible schema means you can change your data structure without migrations:

```python
# Week 1: Simple task
{"title": "Buy groceries", "done": false}

# Week 2: Add priority (no migration needed!)
{"title": "Buy groceries", "done": false, "priority": "high"}

# Week 3: Add nested data
{"title": "Buy groceries", "done": false, "priority": "high",
 "subtasks": [{"title": "Milk", "done": true}]}
```

With PostgreSQL, each of these changes requires an `ALTER TABLE` migration.

### 2. Your Data Is Naturally Document-Shaped
If your data has nested structures, arrays, or varying fields:

```python
# Blog post with comments — natural as a document
{
    "title": "My Post",
    "content": "...",
    "tags": ["python", "fastapi"],
    "comments": [
        {"author": "Alice", "text": "Great post!"},
        {"author": "Bob", "text": "Thanks for sharing"}
    ]
}
```

### 3. You Need to Move Fast
- No migrations to manage
- No schema to define upfront
- Direct JSON storage = less ORM overhead
- Built into every Emergent pod

## Choose PostgreSQL When:

### 1. You Have Complex Relationships
When data naturally connects through foreign keys:

```sql
-- Orders referencing customers and products
SELECT o.id, c.name, p.title, o.quantity
FROM orders o
JOIN customers c ON o.customer_id = c.id
JOIN products p ON o.product_id = p.id
WHERE c.name = 'Alice';
```

In MongoDB, this requires multiple queries or `$lookup` aggregation.

### 2. You Need Strict Data Integrity

```sql
-- PostgreSQL enforces constraints at the database level
CREATE TABLE accounts (
    id SERIAL PRIMARY KEY,
    balance DECIMAL NOT NULL CHECK (balance >= 0),
    email VARCHAR UNIQUE NOT NULL
);
-- Impossible to have negative balance or duplicate emails
```

### 3. You Need Complex Queries
SQL is powerful for analytics:

```sql
-- Top 5 customers by total spending, last 30 days
SELECT c.name, SUM(o.total) as total_spent
FROM orders o
JOIN customers c ON o.customer_id = c.id
WHERE o.created_at > NOW() - INTERVAL '30 days'
GROUP BY c.name
ORDER BY total_spent DESC
LIMIT 5;
```

## Side-by-Side Code Comparison

### Create a Record

**MongoDB:**
```python
task = {"id": str(uuid.uuid4()), "title": "Learn MongoDB", "done": False}
await db.tasks.insert_one(task)
```

**PostgreSQL:**
```python
await db.execute(
    "INSERT INTO tasks (title, done) VALUES ($1, $2) RETURNING id",
    "Learn PostgreSQL", False
)
```

### Query with Filter

**MongoDB:**
```python
tasks = await db.tasks.find(
    {"done": False, "priority": "high"},
    {"_id": 0}
).to_list(100)
```

**PostgreSQL:**
```python
tasks = await db.fetch(
    "SELECT * FROM tasks WHERE done = false AND priority = 'high'"
)
```

### Update a Record

**MongoDB:**
```python
await db.tasks.update_one(
    {"id": task_id},
    {"$set": {"done": True, "completed_at": NOW}}
)
```

**PostgreSQL:**
```python
await db.execute(
    "UPDATE tasks SET done = true, completed_at = NOW() WHERE id = $1",
    task_id
)
```

## The Practical Answer

For most projects on Emergent, **start with MongoDB** because:

1. It's already installed and running on every pod
2. No schema migrations = faster iteration
3. JSON in, JSON out = perfect for REST APIs
4. You can always migrate to PostgreSQL later if needed

Switch to PostgreSQL when you find yourself:
- Writing complex `$lookup` aggregations regularly
- Needing strict foreign key constraints
- Building reporting/analytics features that need SQL
- Working with highly relational data (e-commerce, ERP)
""", order=1, tags=["tutorial", "comparison", "database"])

print("\n=== Enhancement Batch 3 Complete ===")
print("Created: Getting Started category + 3 docs, Tutorials category + 4 docs")
