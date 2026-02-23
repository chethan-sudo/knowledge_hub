"""Content Authenticity Fix - Batch 2
Fix remaining documents with fabricated platform-specific claims"""

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
# 1. Token Economics → Remove fabricated prices
# ============================================================
update_doc("Token Economics & Billing", """# Token Economics & Billing

Understanding tokens is understanding the economics of AI. Every LLM interaction has a cost, and optimizing token usage directly impacts your budget and application performance.

## What Is a Token?

A token is the atomic unit of text for an LLM. It's not a word — it's a sub-word unit determined by the model's tokenizer.

### Examples

| Text | Token Count | Why |
|------|------------|-----|
| "Hello" | 1 | Common word = single token |
| "Hello world" | 2 | Two common words |
| "indescribable" | 3 | Split: `in` + `describ` + `able` |
| "GPT-4" | 3 | Split: `G` + `PT` + `-4` |
| "{ }" | 2 | Punctuation = individual tokens |

**Rule of thumb:** 1 token ≈ 3-4 English characters, or ≈ 0.75 words.

### Quick Estimation

```
A typical page of English text: ~500 words ≈ ~670 tokens
A typical API request: ~100-500 tokens
A large system prompt: ~10,000-20,000 tokens
Full conversation after 10 messages: ~30,000-80,000 tokens
```

## How Costs Are Calculated

LLM providers charge separately for input and output tokens:

```
Cost = (input_tokens × input_price) + (output_tokens × output_price)
```

**Output tokens typically cost 3-5x more** than input tokens because generation is more compute-intensive than processing input.

**Important:** Pricing changes frequently. Always check the provider's current pricing page:
- [OpenAI Pricing](https://openai.com/pricing)
- [Anthropic Pricing](https://www.anthropic.com/pricing)
- [Google AI Pricing](https://ai.google.dev/pricing)

## Where Your Tokens Go

In a typical AI agent interaction:

```
Token breakdown per message:
├── System prompt:        ~15,000 tokens (fixed, same every time)
├── Tool definitions:     ~8,000 tokens  (fixed, same every time)
├── Conversation history: ~5,000-80,000 tokens (grows each turn)
├── Your message:         ~100-500 tokens
└── Agent's response:     ~500-5,000 tokens
```

**Key insight:** ~23,000 tokens are "fixed cost" per message (system prompt + tools). This is why even a simple message consumes a significant number of tokens.

## Optimizing Token Usage

### 1. Reduce Input Tokens

```python
# Inefficient: Sending an entire document as context
messages = [{"role": "user", "content": f"Summarize: {entire_10000_word_doc}"}]

# Efficient: Send only the relevant section
relevant_section = extract_relevant_section(doc, query)
messages = [{"role": "user", "content": f"Summarize: {relevant_section}"}]
```

### 2. Use Cheaper Models for Simple Tasks

```python
# Route based on task complexity
if task_type == "categorize":
    model = "gpt-4o-mini"       # Fast, cheap
elif task_type == "complex_analysis":
    model = "claude-sonnet-4-5"  # Powerful, more expensive
```

### 3. Cache Responses

```python
import hashlib

async def cached_llm_call(prompt, model="gpt-4o-mini"):
    cache_key = hashlib.md5(f"{model}:{prompt}".encode()).hexdigest()
    
    # Check cache first
    cached = await db.llm_cache.find_one({"key": cache_key}, {"_id": 0})
    if cached:
        return cached["response"]  # Free!
    
    # Call LLM and cache the result
    response = await llm.chat(model=model, messages=[{"role": "user", "content": prompt}])
    await db.llm_cache.insert_one({
        "key": cache_key, 
        "response": response.content,
        "created_at": datetime.now(timezone.utc).isoformat()
    })
    return response.content
```

### 4. Limit Output Length

```python
response = await llm.chat(
    model="claude-sonnet-4-5",
    messages=messages,
    max_tokens=500  # Limit response length for concise answers
)
```

### 5. Use Streaming for Better UX

Streaming doesn't save tokens, but it makes the experience feel faster:

```python
# User sees text appearing word-by-word instead of waiting
async for chunk in llm.stream(model="claude-sonnet", messages=messages):
    yield chunk.content
```

## Monitoring Usage

Track your token usage to avoid cost surprises:

```python
async def tracked_llm_call(messages, model):
    response = await llm.chat(model=model, messages=messages)
    
    # Log the usage
    await db.usage_logs.insert_one({
        "model": model,
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
        "timestamp": datetime.now(timezone.utc).isoformat()
    })
    
    return response
```

## Common Cost Surprises

| Surprise | Cause | Prevention |
|----------|-------|-----------|
| "I only sent one message but used 50K tokens" | System prompt + tools = ~23K tokens baseline | This is normal for agent systems |
| "Costs spiked suddenly" | Long conversations = growing context per message | Start new sessions for unrelated tasks |
| "Simple task cost a lot" | Used an expensive model unnecessarily | Route simple tasks to cheaper models |
| "Batch processing was expensive" | Didn't cache repeated similar queries | Implement response caching |
""")

# ============================================================
# 2. Git Internals → Remove fake Emergent-specific claims
# ============================================================
update_doc("Git Internals & Rollback", """# Git Internals & Rollback

Understanding Git's internal model helps you recover from almost any mistake. In AI-assisted development, Git is particularly important because agents make many automated commits.

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

## Auto-Commits in AI-Assisted Development

AI coding agents typically auto-commit after every action. This means your Git history looks like:

```
commit 7: "Added login endpoint"
commit 6: "Installed dependencies"
commit 5: "Created server.py"
commit 4: "Updated .env"
commit 3: "Created project structure"
commit 2: "Initial seed data"
commit 1: "Initial commit"
```

**Every step is a checkpoint you can return to.** This is the power of automated commits — granular rollback at any point.

## Rollback Strategies

| Method | How | When to Use |
|--------|-----|------------|
| **Platform rollback** | Use the UI/tool to select a checkpoint | Safest for AI-assisted environments |
| **git reset --hard** | `git reset --hard <commit>` | When you know exactly which commit to revert to |
| **git revert** | `git revert <commit>` | Creates a new commit that undoes changes (non-destructive) |
| **git checkout** | `git checkout <commit> -- <file>` | Restore a single file from a previous commit |

## Common Git Scenarios

### Scenario 1: "The last change broke my app"
```bash
# See recent commits
git log --oneline -10

# Revert to the commit before the breaking change
git reset --hard <commit-hash>
```

Or use your platform's rollback feature if available.

### Scenario 2: "I want to see what changed"
```bash
# View recent commits
git log --oneline -10

# See what changed in a specific commit
git show <commit-hash> --stat

# See the full diff of a commit
git show <commit-hash>
```

### Scenario 3: "I want to undo one specific file change"
```bash
# Restore a file from a specific commit
git checkout <commit-hash> -- path/to/file.py
```

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

Git compares trees by hash. If a file's blob hash is identical in both trees, the file hasn't changed — Git doesn't even look at the content. This makes diffing very fast.

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

The reflog keeps entries for 30 days by default. As long as you act within that window, nothing is truly lost in Git.

## Troubleshooting Git Issues

| Problem | Cause | Solution |
|---------|-------|----------|
| "Detached HEAD" | Checked out a commit directly | `git checkout main` to reattach |
| "Merge conflict" | Two branches changed same lines | Edit conflict markers, then commit |
| "Cannot push" | Remote has commits you don't have | `git pull --rebase` first |
| "Lost my changes" | Hard reset or force push | `git reflog` — Git keeps everything for 30 days |
| Cluttered commit history | Normal in AI-assisted development | Group related changes when pushing to main |
""")

# ============================================================
# 3. Rate Limiting → Remove fabricated Kubernetes ingress values
# ============================================================
update_doc("Rate Limiting Layers", """# Rate Limiting Layers

Rate limiting operates at multiple layers in a modern web application. Understanding these layers helps you debug "why is my request failing?" scenarios.

## The Rate Limiting Stack

```mermaid
flowchart TD
    REQ[Incoming Request] --> L1[Layer 1: Reverse Proxy / Load Balancer<br/>Connection-level limits]
    L1 --> L2[Layer 2: Web Server<br/>Request rate limits]
    L2 --> L3[Layer 3: Application Middleware<br/>Business logic limits]
    L3 --> L4[Layer 4: External API<br/>Provider rate limits]
    L4 --> APP[Application Logic]
```

## Layer Details

### Layer 1: Reverse Proxy / Load Balancer

The outermost layer, typically handled by Nginx, a cloud load balancer, or Kubernetes ingress:

| Common Setting | Purpose |
|---------------|---------|
| Max connections per IP | Prevent connection flooding |
| Request body size limit | Prevent memory exhaustion (often ~1-10MB) |
| Connection timeout | Free up stale connections |
| WebSocket timeout | Allow long-lived connections |

**When you hit this:** You'll see a `413 Request Entity Too Large` or `503 Service Unavailable`. Your request never reaches your application.

### Layer 2: Web Server (Nginx, etc.)

| Common Setting | Purpose |
|---------------|---------|
| Requests per second per IP | Prevent request flooding |
| Burst allowance | Short spikes are tolerated |
| Proxy pass timeout | Prevent hung backends |

**When you hit this:** You'll see a `429 Too Many Requests` from the web server. The error won't have your app's JSON format.

### Layer 3: Application Middleware

This is where **you** control rate limiting:

```python
from fastapi import Request
from datetime import datetime
import time

# Simple in-memory rate limiter
rate_limit_store = {}

async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host
    now = time.time()
    
    # Clean old entries (1-minute window)
    rate_limit_store[client_ip] = [
        t for t in rate_limit_store.get(client_ip, [])
        if now - t < 60
    ]
    
    # Check limit
    if len(rate_limit_store.get(client_ip, [])) >= 100:
        return JSONResponse(
            status_code=429,
            content={"detail": "Too many requests. Try again in a minute."}
        )
    
    # Record this request
    rate_limit_store.setdefault(client_ip, []).append(now)
    return await call_next(request)
```

### Layer 4: External API Rate Limits

When your app calls external APIs (LLM providers, payment processors, etc.):

| Provider | Typical Limits |
|----------|---------------|
| OpenAI | Requests per minute, tokens per minute (varies by tier) |
| Anthropic | Requests per minute (varies by plan) |
| Stripe | 100 requests/second |
| Google APIs | Varies per API |

## How to Identify Which Layer Blocked You

| Error Response | Likely Layer | What to Do |
|---------------|-------------|-----------|
| `413 Request Entity Too Large` | Reverse proxy | Reduce payload or use chunked uploads |
| `429` with plain HTML error page | Web server (Nginx) | Wait and retry, reduce frequency |
| `429` with JSON `{"detail": "..."}` | Your application | Check your rate limit configuration |
| `429` from an external API | External provider | Implement backoff and retry |
| `503 Service Unavailable` | Any layer | Service may be starting up — wait and retry |

## Implementing Rate Limiting in Your App

### Per-User Rate Limiting

```python
from collections import defaultdict
import time

class RateLimiter:
    def __init__(self, max_requests=60, window_seconds=60):
        self.max_requests = max_requests
        self.window = window_seconds
        self.requests = defaultdict(list)
    
    def is_allowed(self, user_id: str) -> bool:
        now = time.time()
        self.requests[user_id] = [
            t for t in self.requests[user_id]
            if now - t < self.window
        ]
        if len(self.requests[user_id]) >= self.max_requests:
            return False
        self.requests[user_id].append(now)
        return True

limiter = RateLimiter(max_requests=30, window_seconds=60)
```

### Best Practices

| Practice | Why |
|----------|-----|
| Use sliding windows, not fixed windows | Prevents burst at window boundaries |
| Return `Retry-After` header | Tells clients when to retry |
| Different limits for different endpoints | AI endpoints need stricter limits than static data |
| Log rate limit hits | Monitor for abuse patterns |
| Exempt health check endpoints | Monitoring shouldn't be rate-limited |

## Troubleshooting Rate Limits

| Symptom | Diagnosis | Fix |
|---------|-----------|-----|
| Random 429 errors | Proxy-level rate limiting | Reduce rapid sequential calls |
| 413 on file upload | Body size limit | Use chunked upload |
| AI features stop working | Provider rate limit or budget exhausted | Check provider dashboard |
| All requests failing (503) | Service starting up | Wait 30 seconds, retry |
| Only POST requests failing | Rate limit on write endpoints | Check middleware configuration |
""")

# ============================================================
# 4. SSL/TLS & CORS → Generalize platform claims
# ============================================================
update_doc("SSL/TLS & CORS", """# SSL/TLS & CORS

Security at the transport and browser level. Understanding these is essential for debugging "why can't my frontend talk to my backend?" problems.

## TLS in a Typical Web Architecture

```mermaid
flowchart LR
    B[Browser] -->|HTTPS| LB[Load Balancer / Ingress<br/>TLS Termination]
    LB -->|HTTP| N[Web Server]
    N -->|HTTP| A[Your App]
```

**TLS typically terminates at the load balancer or ingress.** Your application code only sees plain HTTP traffic internally:

| Layer | Protocol | TLS Handled By |
|-------|----------|---------------|
| Browser ↔ Load Balancer | HTTPS (TLS 1.3) | Load balancer / cert-manager |
| Load Balancer ↔ App | HTTP | No TLS needed (internal network) |

In most cloud platforms, you don't configure SSL certificates in your app. The platform handles certificate provisioning and renewal automatically (often via Let's Encrypt).

## CORS: Cross-Origin Resource Sharing

CORS is the browser's security mechanism that blocks frontend JavaScript from making requests to a different origin.

### What Is an "Origin"?

```
https://my-app.example.com:443
  │          │               │
  scheme     host            port
```

Two URLs have the **same origin** only if scheme + host + port all match.

### How CORS Works

```mermaid
sequenceDiagram
    participant B as Browser
    participant S as Server
    B->>S: OPTIONS /api/data (preflight)
    Note right of B: "Can I make a POST from this origin?"
    S->>B: 200 OK + CORS headers
    Note left of S: "Yes, these origins/methods are allowed"
    B->>S: POST /api/data (actual request)
    S->>B: 200 OK + data + CORS headers
```

**Preflight requests** happen automatically for "non-simple" requests (POST with JSON, custom headers, etc.).

### CORS Configuration in FastAPI

```python
from starlette.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # In production: list specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**For development**, `allow_origins=["*"]` is fine. **For production**, restrict this to your specific domain(s).

### CORS Headers Explained

| Header | Purpose | Example |
|--------|---------|---------|
| `Access-Control-Allow-Origin` | Which origins can access | `*` or `https://example.com` |
| `Access-Control-Allow-Methods` | Which HTTP methods are allowed | `GET, POST, PUT, DELETE` |
| `Access-Control-Allow-Headers` | Which request headers are allowed | `Content-Type, Authorization` |
| `Access-Control-Allow-Credentials` | Allow cookies/auth headers | `true` or `false` |
| `Access-Control-Max-Age` | How long to cache preflight response | `3600` (1 hour) |

## Common Security Headers

| Header | Purpose | Value |
|--------|---------|-------|
| `X-Content-Type-Options` | Prevent MIME sniffing | `nosniff` |
| `X-Frame-Options` | Prevent clickjacking | `DENY` or `SAMEORIGIN` |
| `Strict-Transport-Security` | Force HTTPS | `max-age=31536000` |
| `Content-Security-Policy` | Control resource loading | Domain-specific |

## Troubleshooting CORS Issues

### The Error Message

```
Access to fetch at 'https://api.example.com/data' from origin 
'https://my-app.com' has been blocked by CORS policy
```

### Decision Tree

| Check | If Yes | If No |
|-------|--------|-------|
| Is the backend running? | Continue debugging | Start the backend first |
| Can you curl the endpoint? | CORS is the issue (browser-only) | Backend bug, not CORS |
| Does the response have CORS headers? | Headers might be wrong | CORS middleware not applied |
| Is it a preflight (OPTIONS) request? | OPTIONS handler missing | Check allowed origins |

### Common CORS Fixes

```python
# Fix 1: Ensure CORS middleware is added BEFORE routes
app = FastAPI()
app.add_middleware(CORSMiddleware, ...)  # BEFORE router
app.include_router(api_router)

# Fix 2: Don't set CORS headers manually AND use middleware
# Pick one approach — they conflict

# Fix 3: For cookies/auth, credentials must be true
# AND allow_origins cannot be "*" — use specific origins
```

### Why CORS Only Affects Browsers

| Client | Subject to CORS? | Why |
|--------|-----------------|-----|
| Browser (fetch/XHR) | **Yes** | Browser enforces same-origin policy |
| curl | No | Command-line tools don't have origins |
| Postman | No | Not a browser |
| Server-to-server | No | CORS is a browser-only mechanism |
| Mobile app (native) | No | Native apps don't have origins |

This is why "it works in Postman but not in my app" is almost always a CORS issue.

## HTTPS Best Practices

| Practice | Why |
|----------|-----|
| Never mix HTTP and HTTPS content | Mixed content is blocked by browsers |
| Use relative URLs for API calls | Automatically uses the page's protocol |
| Set `Secure` flag on cookies | Prevents cookies from being sent over HTTP |
| Use environment variables for API URLs | Ensures correct protocol in all environments |
""")

# ============================================================
# 5. Session Lifecycle → Generalize
# ============================================================
update_doc("Session Lifecycle", """# Session Lifecycle

Understanding how sessions work in cloud development environments — from resource allocation to data persistence.

## A Typical Cloud Dev Session

```mermaid
sequenceDiagram
    participant U as User
    participant P as Platform
    participant ENV as Environment
    participant DB as Database

    U->>P: Start a session
    P->>ENV: Allocate compute resources
    ENV->>ENV: Start services (backend, frontend, database)
    ENV->>P: Ready signal
    P->>U: Session active, preview URL assigned
    
    Note over U,ENV: Active Development
    
    U->>ENV: Write code, test app
    ENV->>DB: Store data
    
    Note over U,ENV: Inactivity Period
    
    P->>ENV: Recycle resources (scale down)
    Note over ENV: Ephemeral storage lost
    Note over DB: Database data preserved
```

## What Survives Resource Recycling?

| Data Type | Survives? | Why |
|-----------|-----------|-----|
| Database records (MongoDB, PostgreSQL) | **Yes** | Persisted to disk |
| Git commits (pushed) | **Yes** | Stored on remote |
| Cloud-stored files | **Yes** | External storage |
| Environment variables (configured) | **Yes** | Restored from config |
| Files in project directory | **Partial** | Only if committed to Git |
| Files in /tmp/ | **No** | Temporary filesystem |
| Running processes | **No** | New environment, new processes |
| In-memory state (variables) | **No** | New process = new memory |
| WebSocket connections | **No** | Must reconnect |

## Session State Management

### Server-Side Sessions (Database)

```python
# Store session data in MongoDB — survives environment recycling
@api_router.post("/session/create")
async def create_session():
    session_id = str(uuid.uuid4())
    session = {
        "id": session_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "data": {}
    }
    await db.sessions.insert_one(session)
    return {"session_id": session_id}

@api_router.get("/session/{session_id}")
async def get_session(session_id: str):
    session = await db.sessions.find_one(
        {"id": session_id}, {"_id": 0}
    )
    if not session:
        raise HTTPException(404, "Session not found")
    return session
```

### Client-Side State (localStorage)

```javascript
// Persists across page refreshes
// Stored in the user's browser, not on the server

// Save state
localStorage.setItem("user-prefs", JSON.stringify({
  theme: "dark",
  sidebarWidth: 280,
  lastViewedDoc: "abc-123"
}));

// Restore state
const prefs = JSON.parse(
  localStorage.getItem("user-prefs") || "{}"
);
```

### Choosing the Right Storage

| Need | Use | Why |
|------|-----|-----|
| User preferences (theme, layout) | `localStorage` | Browser-local, instant, no API call |
| Application data (documents, records) | Database | Persistent, queryable, shared across clients |
| Temporary computation results | In-memory variables | Fast, but lost on refresh |
| Large files | Cloud storage / database | Survives server restarts |
| Authentication tokens | HTTP-only cookies | Secure, automatic on requests |

## Handling Cold Starts

When a cloud development environment needs to start up, the app should handle it gracefully:

```jsx
function App() {
  const [loading, setLoading] = useState(true);
  const [connectionError, setConnectionError] = useState(false);

  const loadData = async () => {
    try {
      const response = await fetch(`${API_URL}/data`);
      if (response.ok) {
        setData(await response.json());
        setLoading(false);
      }
    } catch (error) {
      setConnectionError(true);
      setTimeout(loadData, 3000); // Retry in 3 seconds
    }
  };

  useEffect(() => { loadData(); }, []);

  if (connectionError) {
    return <LoadingScreen message="Connecting to server..." />;
  }
  // ... render app
}
```

## Troubleshooting Session Issues

| Symptom | Cause | Solution |
|---------|-------|----------|
| Data disappeared after a break | Stored in filesystem, not database | Use MongoDB for important data |
| "Connection refused" on return | Environment is cold-starting | Implement retry logic with loading UI |
| WebSocket won't connect | Old connection is stale | Implement auto-reconnect |
| Environment variables missing | `.env` not committed or not configured | Check environment configuration |
| Login state lost | Token expired or session cleared | Store auth state in database or use refresh tokens |
""")

# ============================================================
# 6. MongoDB vs PostgreSQL → Remove "on Emergent" branding
# ============================================================
rename_doc("MongoDB vs PostgreSQL on Emergent", "MongoDB vs PostgreSQL", """# MongoDB vs PostgreSQL

When should you use MongoDB vs PostgreSQL? This comparison helps you make the right choice for your project.

## Quick Comparison

| Feature | MongoDB | PostgreSQL |
|---------|---------|------------|
| **Data model** | Documents (flexible JSON) | Tables (strict schema) |
| **Schema** | Schema-less (flexible) | Schema-enforced (strict) |
| **Query language** | MongoDB Query Language | SQL |
| **Joins** | Manual (`$lookup`) | Native `JOIN` |
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

## Choose PostgreSQL When:

### 1. You Have Complex Relationships

```sql
SELECT o.id, c.name, p.title, o.quantity
FROM orders o
JOIN customers c ON o.customer_id = c.id
JOIN products p ON o.product_id = p.id
WHERE c.name = 'Alice';
```

In MongoDB, this requires multiple queries or `$lookup` aggregation.

### 2. You Need Strict Data Integrity

```sql
CREATE TABLE accounts (
    id SERIAL PRIMARY KEY,
    balance DECIMAL NOT NULL CHECK (balance >= 0),
    email VARCHAR UNIQUE NOT NULL
);
-- Impossible to have negative balance or duplicate emails
```

### 3. You Need Complex Queries

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

For most projects, **start with MongoDB** if:
- You're prototyping and need flexibility
- Your data is naturally document-shaped
- You want minimal setup overhead

**Switch to PostgreSQL** when:
- You find yourself writing complex `$lookup` aggregations regularly
- You need strict foreign key constraints
- You're building reporting/analytics features that need SQL
- You're working with highly relational data (e-commerce, ERP)
""")

# ============================================================
# 7. Building a REST API → Remove "on Emergent" references
# ============================================================
update_doc("Building a REST API from Scratch", """# Building a REST API from Scratch

A complete, step-by-step tutorial for building a task management API with FastAPI and MongoDB. Covers database design, API routes, error handling, and testing.

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

Define request/response schemas:

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

**Why Pydantic?** It validates input automatically. If someone sends `status: "invalid"`, FastAPI returns a 422 error with a clear message.

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
  -d '{"title": "Learn FastAPI", "priority": "high"}'

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

### Soft Delete

Instead of permanently deleting records:

```python
@router.delete("/tasks/{task_id}")
async def soft_delete_task(task_id: str):
    await db.tasks.update_one(
        {"id": task_id},
        {"$set": {"deleted": True, "deleted_at": NOW}}
    )
    return {"status": "deleted"}

# Exclude soft-deleted items from all queries
@router.get("/tasks")
async def list_tasks():
    query = {"deleted": {"$ne": True}}
    # ...
```

### Index Strategy

```python
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
| `datetime.utcnow()` | Returns naive datetime (deprecated) | Use `datetime.now(timezone.utc)` |
""")

print("\n=== Authenticity Fix Batch 2 Complete ===")
