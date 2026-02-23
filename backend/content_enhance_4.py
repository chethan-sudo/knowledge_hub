"""Content Enhancement Script - Batch 4
Enhance remaining key documents with code examples and troubleshooting
Enhancement #1 + #2 + #6 for core documents"""

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

# ============================================================
# 1. Retrieval Augmented Generation (2454 -> ~6000 chars)
# ============================================================
update_doc("Retrieval Augmented Generation", """# Retrieval Augmented Generation (RAG)

RAG is the technique of giving an LLM access to external knowledge at query time, rather than relying solely on its training data. It's how you build AI features that know about *your* data.

## Why RAG Exists

LLMs have two fundamental limitations:

| Limitation | Example | RAG Solution |
|-----------|---------|-------------|
| **Knowledge cutoff** | "What's the latest React version?" → trained on old data | Retrieve current docs at query time |
| **No private data** | "What's our company's refund policy?" → not in training data | Retrieve from your knowledge base |
| **Hallucination** | Confident but wrong answers | Ground responses in retrieved facts |

## The RAG Pipeline

```mermaid
flowchart LR
    Q[User Question] --> E1[Embed Question]
    E1 --> S[Search Vector DB]
    S --> R[Retrieve Top-K Docs]
    R --> P[Build Prompt:<br/>Context + Question]
    P --> LLM[LLM Generates Answer]
    LLM --> A[Grounded Answer]
```

**Step-by-step:**

1. **Embed the question** — Convert the user's question into a vector (array of numbers) using an embedding model
2. **Search** — Find the most similar document vectors in your database
3. **Retrieve** — Pull the top K most relevant document chunks
4. **Augment** — Insert the retrieved text into the LLM prompt as context
5. **Generate** — The LLM answers using the retrieved context as its source of truth

## Implementation: Simple RAG with Emergent

### Step 1: Prepare Your Documents

```python
# Split documents into chunks (500-1000 tokens each)
def chunk_text(text, chunk_size=500, overlap=50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

# Example: Chunk your documentation
documents = [
    {"title": "Refund Policy", "content": "We offer full refunds within 30 days..."},
    {"title": "Pricing", "content": "Our plans start at $10/month..."},
]

all_chunks = []
for doc in documents:
    for i, chunk in enumerate(chunk_text(doc["content"])):
        all_chunks.append({
            "text": chunk,
            "source": doc["title"],
            "chunk_index": i
        })
```

### Step 2: Create Embeddings and Store

```python
# Using OpenAI embeddings (via Universal Key)
import openai

async def create_embedding(text):
    response = await openai.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

# Store in MongoDB with vector
for chunk in all_chunks:
    embedding = await create_embedding(chunk["text"])
    chunk["embedding"] = embedding
    await db.knowledge_base.insert_one(chunk)
```

### Step 3: Search at Query Time

```python
async def search_knowledge(query, top_k=5):
    query_embedding = await create_embedding(query)
    
    # MongoDB Atlas Vector Search (or manual cosine similarity)
    results = await db.knowledge_base.aggregate([
        {
            "$vectorSearch": {
                "queryVector": query_embedding,
                "path": "embedding",
                "numCandidates": 100,
                "limit": top_k,
                "index": "vector_index"
            }
        },
        {"$project": {"_id": 0, "text": 1, "source": 1, "score": {"$meta": "vectorSearchScore"}}}
    ]).to_list(top_k)
    
    return results
```

### Step 4: Generate an Answer

```python
async def answer_with_rag(question):
    # Retrieve relevant context
    context_docs = await search_knowledge(question)
    context = "\\n\\n".join([
        f"[Source: {doc['source']}]\\n{doc['text']}" 
        for doc in context_docs
    ])
    
    # Build augmented prompt
    messages = [
        {"role": "system", "content": f\"\"\"Answer the user's question using ONLY the provided context.
If the context doesn't contain the answer, say "I don't have information about that."

Context:
{context}\"\"\"},
        {"role": "user", "content": question}
    ]
    
    # Generate response
    response = await llm.chat(
        model="claude-sonnet-4-5",
        messages=messages
    )
    
    return {
        "answer": response.content,
        "sources": [doc["source"] for doc in context_docs]
    }
```

## Chunking Strategies

The way you split documents dramatically affects RAG quality:

| Strategy | How It Works | Best For |
|----------|-------------|----------|
| **Fixed size** | Split every N words | Simple, general purpose |
| **Paragraph** | Split on double newlines | Well-structured documents |
| **Semantic** | Split at topic boundaries | Long-form content |
| **Recursive** | Try headers → paragraphs → sentences | Mixed format documents |
| **Sliding window** | Overlapping chunks | Preserving context across boundaries |

**Critical parameter:** Chunk overlap. Without overlap, a fact split across two chunks may never be retrieved. 50-100 token overlap is typically sufficient.

## How E1's AI Chat Uses RAG

The AI chatbot in this Knowledge Hub uses a simplified form of RAG:

```
1. User asks a question
2. The current document's content is included as context
3. The LLM answers using that document context
4. Sources are cited in the response
```

This is "poor man's RAG" — instead of vector search, it uses the currently-viewed document as context. Simple but effective for a documentation chatbot.

## Common RAG Mistakes

| Mistake | Impact | Fix |
|---------|--------|-----|
| Chunks too large (>1000 tokens) | Retrieved text dilutes the answer | Use 300-500 token chunks |
| Chunks too small (<100 tokens) | Loses context and meaning | Use 300-500 token chunks |
| No overlap between chunks | Information at boundaries is lost | Add 50-100 token overlap |
| Embedding wrong content | Metadata embedded instead of text | Only embed the actual content |
| Not citing sources | User can't verify the answer | Return source documents with response |
| Using RAG for everything | Over-engineering simple lookups | Direct DB query is faster for structured data |

## When NOT to Use RAG

| Situation | Better Alternative |
|-----------|-------------------|
| Data fits in context window | Just include it in the prompt |
| Structured data queries | Direct database query (SQL/MongoDB) |
| Real-time data | API calls, not pre-indexed documents |
| Very small knowledge base (<10 docs) | Include all docs in the prompt |
| Exact match lookups | Traditional search/filter |
""")

# ============================================================
# 2. Docker & Container Fundamentals (2270 -> ~5500 chars)
# ============================================================
update_doc("Docker & Container Fundamentals", """# Docker & Container Fundamentals

Containers are the building blocks of Emergent's infrastructure. Every development environment runs inside a container. Understanding how they work helps you debug environment issues and make better architectural decisions.

## What Is a Container?

A container is an **isolated process** that thinks it has its own operating system, filesystem, and network — but actually shares the host's kernel.

```mermaid
flowchart TB
    subgraph Host["Host Machine (Kubernetes Node)"]
        K[Linux Kernel]
        subgraph C1["Container 1 (Your Pod)"]
            A1[Node.js + React]
            A2[Python + FastAPI]
            A3[MongoDB]
        end
        subgraph C2["Container 2 (Another User)"]
            B1[Different App]
        end
        K --> C1
        K --> C2
    end
```

**Key insight:** Containers are NOT virtual machines. They don't run a separate OS kernel. They use Linux namespaces and cgroups to create isolation while sharing the host kernel.

## Container vs VM

| Feature | Container | Virtual Machine |
|---------|-----------|-----------------|
| Startup time | Seconds | Minutes |
| Size | MBs (just your app) | GBs (full OS) |
| Isolation | Process-level | Hardware-level |
| Performance | Near-native | ~5-15% overhead |
| OS Kernel | Shared with host | Own kernel |
| Density | 100s per host | 10s per host |

## Dockerfile: The Blueprint

A Dockerfile defines how to build a container image:

```dockerfile
# Base image — the starting point
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy dependency file first (better caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the port your app uses
EXPOSE 8001

# The command to run when container starts
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8001"]
```

### Layer Caching

Each Dockerfile instruction creates a **layer**. Docker caches layers that haven't changed:

```
Layer 1: FROM python:3.11-slim        ← Cached (rarely changes)
Layer 2: COPY requirements.txt .       ← Cached if file unchanged
Layer 3: RUN pip install ...           ← Cached if requirements unchanged
Layer 4: COPY . .                      ← Rebuilds when code changes
```

**That's why we copy `requirements.txt` before the code** — dependencies change less often than code, so the install layer stays cached.

## How Emergent Uses Containers

On Emergent, you don't write Dockerfiles directly. The platform manages containers for you:

```mermaid
flowchart LR
    U[You Start a Job] --> A[Platform Allocates Pod]
    A --> B[Pod Contains:]
    B --> B1[Python 3.11]
    B --> B2[Node.js 18]
    B --> B3[MongoDB 7]
    B --> B4[Nginx]
    B --> B5[Supervisord]
    B --> B6[Git]
```

All these services run inside a single Kubernetes pod (which contains one or more containers).

## Common Docker Commands (for reference)

While E1 handles containers automatically, knowing these helps you understand the logs:

| Command | What It Does | When You'd See It |
|---------|-------------|-------------------|
| `docker build` | Creates an image from Dockerfile | During deployment |
| `docker run` | Starts a container from an image | Pod initialization |
| `docker ps` | Lists running containers | Debugging |
| `docker logs` | Shows container output | Checking errors |
| `docker exec` | Runs a command inside a container | E1's bash tool does this |

## Container Networking

Inside your Emergent pod, services communicate over localhost:

```
Frontend (port 3000) ←──→ Backend (port 8001)
                              ↕
                          MongoDB (port 27017)
```

External traffic flows through the Kubernetes ingress:

```
User Browser
    → HTTPS → Kubernetes Ingress (TLS termination)
        → /api/* → Nginx → Backend (port 8001)
        → /* → Nginx → Frontend (port 3000)
```

## Troubleshooting Container Issues

| Problem | Symptom | Solution |
|---------|---------|----------|
| Service won't start | `supervisorctl status` shows FATAL | Check logs: `tail /var/log/supervisor/*.err.log` |
| Port already in use | `Address already in use` error | Don't start services manually; use supervisor |
| Package not found | `ModuleNotFoundError` | Install it: `pip install X && pip freeze > requirements.txt` |
| Out of memory | Process killed, no error message | Optimize your app's memory usage |
| Filesystem full | `No space left on device` | Clean up temp files: `rm -rf /tmp/*` |
| Node modules missing | `Module not found` error | `cd /app/frontend && yarn install` |

## Best Practices

| Practice | Why |
|----------|-----|
| Install dependencies in requirements.txt | Reproducible builds |
| Don't store data in the container filesystem | Data lost on restart; use MongoDB |
| Use environment variables for config | Same container works in all environments |
| Don't run as root in production | Security principle of least privilege |
| Keep images small | Faster startup, less storage |
""")

# ============================================================
# 3. Enhance "Where AI Agents Are Heading" (2641 -> ~6000 chars)
# ============================================================
update_doc("Where AI Agents Are Heading", """# Where AI Agents Are Heading

The current generation of AI agents — including E1 — represents the beginning of a fundamental shift in software development. This document explores the trajectory: what works today, what's emerging, and what the future likely holds.

## The Evolution Timeline

```mermaid
flowchart LR
    A[2022<br/>ChatGPT Launch<br/>Text Generation] --> B[2023<br/>Function Calling<br/>Tool Use]
    B --> C[2024<br/>AI Agents<br/>Multi-step Reasoning]
    C --> D[2025-26<br/>Autonomous Agents<br/>Self-correcting Systems]
    D --> E[Future<br/>Agent Ecosystems<br/>Agent-to-Agent]
```

## Where We Are Today (2025-2026)

### What Works Well

| Capability | Maturity | Example |
|-----------|----------|---------|
| Code generation | High | E1 generates full-stack apps |
| Tool use | High | File ops, bash, browser automation |
| Multi-step reasoning | Medium-High | Plan → execute → verify → iterate |
| Error recovery | Medium | Retries, alternative approaches |
| Testing | Medium | Automated test generation and execution |

### What's Still Hard

| Challenge | Current State | Why It's Hard |
|-----------|--------------|---------------|
| Ambiguous requirements | Agent asks for clarification | Natural language is inherently ambiguous |
| Large codebase understanding | Struggles with 100K+ line projects | Context window limits |
| Creative design | Tends toward "AI slop" patterns | Trained on average, not exceptional |
| Long-running tasks | Context degradation over time | Token limits, memory loss |
| Novel problem solving | Relies on training data patterns | Can't truly innovate |

## Emerging Capabilities (2025-2026)

### 1. Computer Use / Browser Agents

Agents that can see and interact with GUIs:

```
User: "Go to our staging site and test the checkout flow"
Agent: 
  1. Opens browser
  2. Navigates to staging URL
  3. Adds item to cart
  4. Fills checkout form
  5. Verifies confirmation page
  6. Reports results with screenshots
```

This is already partially possible with Playwright integration. The next generation will have native visual understanding — clicking buttons, reading UI state, and adapting to layout changes.

### 2. Self-Correcting Agents

Current agents attempt fixes and sometimes loop. Next-generation agents will:

- **Predict failures** before they happen (based on code patterns)
- **Run validation automatically** after every change
- **Learn from past mistakes** within a session
- **Escalate** when confidence is low instead of guessing

### 3. Collaborative Multi-Agent Systems

Instead of one agent doing everything:

```mermaid
flowchart TD
    PM[Product Manager Agent<br/>Writes specs] --> ARCH[Architect Agent<br/>Designs system]
    ARCH --> DEV[Developer Agent<br/>Writes code]
    DEV --> QA[QA Agent<br/>Tests thoroughly]
    QA --> DEV
    QA --> DEPLOY[DevOps Agent<br/>Deploys safely]
```

Each agent is specialized and operates on a different level of abstraction. E1's subagent system is an early version of this pattern.

### 4. Persistent Memory

Current limitation: Agents forget between sessions. Future agents will:

- Remember your coding style and preferences
- Recall architectural decisions from weeks ago
- Build a knowledge graph of your codebase
- Proactively warn about conflicting decisions

## What the Future Looks Like

### Near Future (2026-2027)

| Feature | Impact |
|---------|--------|
| **Codebase-aware agents** | Agent understands entire project, not just visible files |
| **Automatic testing** | Every code change is tested before committing |
| **Multi-modal understanding** | Analyze screenshots, Figma designs, whiteboard photos |
| **Natural language deployment** | "Deploy to production with blue-green strategy" |

### Medium Future (2027-2029)

| Feature | Impact |
|---------|--------|
| **Agent-to-agent protocols** | Standard way for agents to collaborate |
| **Continuous learning** | Agents improve from every interaction |
| **Domain-specific agents** | Healthcare, finance, legal specialists |
| **Zero-shot deployment** | Describe an app, get a deployed product |

### Long-Term Vision (2030+)

The end state is not "AI replacing developers" — it's a fundamental change in the abstraction level of software creation:

| Era | Abstraction Level | Tool |
|-----|-------------------|------|
| 1960s | Machine code | Punch cards |
| 1970s | Assembly | Text editors |
| 1990s | High-level languages | IDEs |
| 2010s | Frameworks & libraries | VS Code, GitHub |
| 2020s | Natural language | AI Agents |
| 2030s | Intent-level | Agent Ecosystems |

The progression is clear: each generation raises the abstraction level, making the previous generation's complexity invisible.

## Challenges That Remain Unsolved

### 1. The Alignment Problem
How do you ensure an autonomous agent does what you *mean*, not just what you *said*?

### 2. The Verification Problem
As agents build more complex systems, how do humans verify the output is correct? We can't read every line of generated code.

### 3. The Trust Problem
When should you trust an agent to deploy to production without human review?

### 4. The Liability Problem
When an AI agent introduces a security vulnerability, who is responsible?

## What This Means for Developers

The role of a developer is shifting from **writing code** to **directing agents**:

| Old Skill | New Equivalent |
|-----------|----------------|
| Writing code | Describing intent clearly |
| Debugging | Reviewing agent output |
| Architecture design | System-level thinking |
| Testing | Defining acceptance criteria |
| Code review | Agent output review |

**The developers who thrive** will be those who can operate at a higher abstraction level — thinking about systems, user needs, and business logic — while letting agents handle implementation details.
""")

# ============================================================
# 4. Enhance MongoDB Document Model (2888 -> ~6000 chars)
# ============================================================
update_doc("MongoDB Document Model", """# MongoDB Document Model

MongoDB stores data as flexible JSON-like documents. Understanding the document model — and its gotchas — is essential for building reliable applications on Emergent.

## Documents, Not Rows

In MongoDB, a single "record" is a document — a nested JSON object:

```json
{
    "_id": ObjectId("507f1f77bcf86cd799439011"),
    "name": "Alice",
    "email": "alice@example.com",
    "profile": {
        "bio": "Full-stack developer",
        "skills": ["Python", "React", "MongoDB"]
    },
    "posts": [
        {"title": "My First Post", "likes": 42},
        {"title": "Learning MongoDB", "likes": 128}
    ]
}
```

**vs. SQL equivalent (3 tables):**
```
users:    id=1, name="Alice", email="alice@example.com"
profiles: user_id=1, bio="Full-stack developer"
skills:   user_id=1, skill="Python"
          user_id=1, skill="React"
posts:    user_id=1, title="My First Post", likes=42
```

One MongoDB document replaces three SQL tables. This is called **denormalization** — embedding related data directly in the document.

## When to Embed vs. Reference

| Pattern | Use When | Example |
|---------|----------|---------|
| **Embed** | Data is always accessed together | User profile inside user doc |
| **Embed** | Data belongs to parent exclusively | Order items inside order |
| **Reference** | Data is shared across documents | Author referenced by many posts |
| **Reference** | Data is very large or frequently updated | Comments on a post |

### Embed Pattern
```python
# Comments embedded in post document
post = {
    "title": "My Post",
    "comments": [
        {"author": "Bob", "text": "Great!", "date": "2026-01-15"},
        {"author": "Carol", "text": "Thanks!", "date": "2026-01-16"}
    ]
}
# One query gets the post AND all comments
post = await db.posts.find_one({"title": "My Post"}, {"_id": 0})
```

### Reference Pattern
```python
# Author as a reference (separate collection)
post = {"title": "My Post", "author_id": "user-123"}
author = await db.users.find_one({"id": "user-123"}, {"_id": 0})
# Two queries needed, but author data isn't duplicated
```

## CRUD Operations

### Create
```python
# Insert one document
result = await db.tasks.insert_one({
    "id": str(uuid.uuid4()),
    "title": "Learn MongoDB",
    "status": "todo",
    "created_at": datetime.now(timezone.utc).isoformat()
})
# WARNING: insert_one MODIFIES the dict, adding _id to it!
```

### Read
```python
# Find one document (ALWAYS exclude _id)
task = await db.tasks.find_one({"id": task_id}, {"_id": 0})

# Find many with filter, sort, and limit
tasks = await db.tasks.find(
    {"status": "todo"},
    {"_id": 0}
).sort("created_at", -1).limit(20).to_list(20)

# Count documents
total = await db.tasks.count_documents({"status": "todo"})
```

### Update
```python
# Update specific fields (don't overwrite entire document)
await db.tasks.update_one(
    {"id": task_id},
    {"$set": {"status": "done", "updated_at": NOW}}
)

# Increment a counter
await db.posts.update_one(
    {"id": post_id},
    {"$inc": {"view_count": 1}}
)

# Add to an array
await db.tasks.update_one(
    {"id": task_id},
    {"$push": {"tags": "urgent"}}
)
```

### Delete
```python
# Delete one
await db.tasks.delete_one({"id": task_id})

# Soft delete (recommended)
await db.tasks.update_one(
    {"id": task_id},
    {"$set": {"deleted": True, "deleted_at": NOW}}
)
```

## Aggregation Pipeline

For complex queries, MongoDB uses a pipeline of stages:

```python
# Most viewed documents in the last 7 days
pipeline = [
    {"$match": {"viewed_at": {"$gte": week_ago}}},
    {"$group": {
        "_id": "$document_id",
        "title": {"$first": "$title"},
        "view_count": {"$sum": 1}
    }},
    {"$sort": {"view_count": -1}},
    {"$limit": 10},
    {"$project": {"_id": 0, "document_id": "$_id", "title": 1, "view_count": 1}}
]
results = await db.doc_views.aggregate(pipeline).to_list(10)
```

## Indexing Strategy

Indexes make queries fast. Without them, MongoDB scans every document:

```python
# Create indexes for common query patterns
await db.tasks.create_index("id", unique=True)       # Lookup by ID
await db.tasks.create_index("status")                 # Filter by status
await db.tasks.create_index("created_at")             # Sort by date
await db.tasks.create_index([                          # Compound index
    ("status", 1), ("priority", -1)
])

# Text index for full-text search
await db.documents.create_index([
    ("title", "text"), ("content", "text")
])
```

| Index Type | Use Case | Example |
|-----------|----------|---------|
| **Single field** | Filter or sort on one field | `{"status": 1}` |
| **Compound** | Filter on multiple fields together | `{"status": 1, "priority": -1}` |
| **Text** | Full-text search | `{"title": "text", "content": "text"}` |
| **Unique** | Prevent duplicates | `{"email": 1}, unique=True` |

## The _id Gotcha (Critical!)

MongoDB automatically adds an `_id` field (ObjectId type) to every document. **ObjectId is NOT JSON serializable:**

```python
# THIS WILL CRASH your API:
task = await db.tasks.find_one({"id": task_id})
return task  # 💥 ObjectId is not JSON serializable

# ALWAYS exclude _id:
task = await db.tasks.find_one({"id": task_id}, {"_id": 0})
return task  # ✅ Works

# Also watch out for insert_one mutation:
doc = {"id": "123", "title": "Test"}
await db.tasks.insert_one(doc)
return doc  # 💥 doc now has _id field added by insert_one!
```

## Troubleshooting MongoDB

| Problem | Cause | Solution |
|---------|-------|----------|
| `ObjectId not serializable` | Returning `_id` in response | Use `{"_id": 0}` in all projections |
| Query returns nothing | Using string where ObjectId expected | Use string IDs (`uuid.uuid4()`) |
| Duplicate key error | Unique index violated | Check for existing document before insert |
| Slow queries | Missing index | Add index for the query pattern |
| Data disappeared | Pod recycled, or `drop()` called | Check if data was persisted in the right database |
| `insert_one` corrupts dict | MongoDB mutates the input dict | Don't reuse dict after insert, or use `dict(doc)` |
""")

# ============================================================
# 5. Enhance FastAPI Request Lifecycle (3122 -> ~6000 chars)
# ============================================================
update_doc("FastAPI Request Lifecycle", """# FastAPI Request Lifecycle

Understanding how a request flows through FastAPI — from URL to response — helps you debug issues and write better APIs.

## The Request Journey

```mermaid
flowchart TD
    REQ[HTTP Request] --> MW1[CORS Middleware]
    MW1 --> MW2[Custom Middleware]
    MW2 --> ROUTE[Route Matching]
    ROUTE --> DEP[Dependency Injection]
    DEP --> VAL[Pydantic Validation]
    VAL --> HANDLER[Route Handler Function]
    HANDLER --> SERIAL[Response Serialization]
    SERIAL --> RESP[HTTP Response]
```

**Each step can fail, producing different error types:**

| Step | Failure | HTTP Code | Error Example |
|------|---------|-----------|---------------|
| CORS Middleware | Origin not allowed | Blocked by browser | CORS error in console |
| Route Matching | URL doesn't match any route | 404 | `{"detail": "Not Found"}` |
| Dependency Injection | Dependency raises exception | Varies | Auth failure → 401 |
| Pydantic Validation | Request body doesn't match model | 422 | `{"detail": [{"loc": ["body", "email"], "msg": "field required"}]}` |
| Route Handler | Unhandled exception in your code | 500 | `{"detail": "Internal Server Error"}` |
| Serialization | Response can't be converted to JSON | 500 | ObjectId serialization error |

## Dependency Injection Deep Dive

FastAPI's DI system is powerful and often misunderstood:

```python
from fastapi import Depends, Header, HTTPException

# Simple dependency: extract and validate auth
async def get_current_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(401, "Not authenticated")
    # Validate token, look up user
    user = await db.users.find_one({"token": authorization}, {"_id": 0})
    if not user:
        raise HTTPException(401, "Invalid token")
    return user

# Dependency that depends on another dependency
async def require_admin(user=Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(403, "Admin access required")
    return user

# Using dependencies in routes
@router.get("/admin/users")
async def list_users(user=Depends(require_admin)):
    # `user` is guaranteed to be an admin here
    return await db.users.find({}, {"_id": 0}).to_list(100)

@router.get("/profile")
async def get_profile(user=Depends(get_current_user)):
    # `user` is any authenticated user
    return user
```

**How the dependency chain works:**

```
Request to /admin/users
  → FastAPI calls require_admin()
    → require_admin calls get_current_user() via Depends
      → get_current_user extracts auth header
      → Validates token, returns user
    → require_admin checks role == "admin"
    → Returns admin user
  → Route handler receives verified admin user
```

## Request Validation with Pydantic

```python
from pydantic import BaseModel, Field
from typing import Optional

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field("", max_length=2000)
    priority: str = Field("medium", pattern="^(low|medium|high)$")

@router.post("/tasks")
async def create_task(data: TaskCreate):
    # If we reach here, data is GUARANTEED to be valid
    # FastAPI automatically returns 422 for invalid input
    task = {"id": str(uuid.uuid4()), **data.model_dump()}
    await db.tasks.insert_one(task)
    return await db.tasks.find_one({"id": task["id"]}, {"_id": 0})
```

**What happens with invalid input:**
```bash
curl -X POST /api/tasks -d '{"title": "", "priority": "critical"}'

# Response (422):
{
    "detail": [
        {
            "type": "string_too_short",
            "loc": ["body", "title"],
            "msg": "String should have at least 1 character"
        },
        {
            "type": "string_pattern_mismatch",
            "loc": ["body", "priority"],
            "msg": "String should match pattern '^(low|medium|high)$'"
        }
    ]
}
```

## Middleware: Before and After Every Request

```python
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import time

class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.time()
        response = await call_next(request)
        duration = time.time() - start
        response.headers["X-Process-Time"] = f"{duration:.3f}s"
        logger.info(f"{request.method} {request.url.path} - {duration:.3f}s")
        return response

app.add_middleware(TimingMiddleware)
```

**Middleware execution order matters:**
```
Request  → CORS → Timing → Auth → Route Handler
Response ← CORS ← Timing ← Auth ← Route Handler
```

Middleware added **last** runs **first** (it's a stack, not a queue).

## Background Tasks

For operations that don't need to block the response:

```python
from fastapi import BackgroundTasks

async def send_notification(user_email: str, message: str):
    # This runs AFTER the response is sent
    await email_service.send(user_email, message)

@router.post("/tasks")
async def create_task(data: TaskCreate, background_tasks: BackgroundTasks):
    task = {"id": str(uuid.uuid4()), **data.model_dump()}
    await db.tasks.insert_one(task)
    
    # Schedule notification (doesn't delay the response)
    background_tasks.add_task(send_notification, "user@example.com", "New task created")
    
    return await db.tasks.find_one({"id": task["id"]}, {"_id": 0})
```

## Async vs Sync Routes

```python
# Async route (preferred for I/O operations)
@router.get("/tasks")
async def get_tasks():  # Uses 'async def'
    return await db.tasks.find({}, {"_id": 0}).to_list(100)

# Sync route (for CPU-bound operations)
@router.get("/compute")
def heavy_computation():  # Uses 'def' (no async)
    return {"result": expensive_calculation()}
```

**Rule of thumb:** Use `async def` for everything that involves database calls, HTTP requests, or file I/O. Use `def` only for CPU-bound operations.

## Troubleshooting FastAPI

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| 404 on valid route | Route prefix missing (`/api`) | Check router prefix |
| 422 on POST request | Request body doesn't match model | Check Pydantic model vs sent data |
| 500 with no useful error | Unhandled exception in handler | Check `backend.err.log` for traceback |
| CORS error in browser | Middleware not configured or wrong order | Add CORS middleware before routes |
| Slow response | Blocking sync code in async route | Use `async def` with `await` |
| "Method not allowed" (405) | Wrong HTTP method | Check route decorator (GET vs POST) |
| Auth working in curl, not browser | CORS blocking preflight | Enable `allow_credentials=True` |
""")

print("\n=== Enhancement Batch 4 Complete ===")
print("Updated: RAG, Docker, Future of AI, MongoDB, FastAPI")
