"""Content Enhancement Script - Batch 5
Enhance remaining documents: JWT Auth, Kubernetes, Deployment, 
Hot Reload, Browser Rendering, LLM Training, Token Economics"""

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
# 1. JWT & OAuth Authentication (3605 -> ~6500 chars)
# ============================================================
update_doc("JWT & OAuth Authentication", """# JWT & OAuth Authentication

Authentication is how your app verifies "who is this user?" This document covers the two most common approaches, with implementation examples.

## JWT (JSON Web Tokens)

### How JWT Works

```mermaid
sequenceDiagram
    participant U as User
    participant F as Frontend
    participant B as Backend
    participant DB as Database

    U->>F: Enter email + password
    F->>B: POST /api/auth/login
    B->>DB: Verify credentials
    DB->>B: User found, password matches
    B->>B: Create JWT token
    B->>F: Return {token: "eyJ..."}
    F->>F: Store token in localStorage
    
    Note over F,B: Subsequent requests
    F->>B: GET /api/profile (Authorization: Bearer eyJ...)
    B->>B: Verify & decode JWT
    B->>F: Return user data
```

### JWT Structure

A JWT has three parts, separated by dots:

```
eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiMTIzIn0.signature
│         Header        │        Payload         │  Signature │
```

| Part | Contains | Encoded? | Encrypted? |
|------|----------|----------|-----------|
| **Header** | Algorithm, token type | Base64 | No |
| **Payload** | User ID, expiry, claims | Base64 | No |
| **Signature** | HMAC of header + payload | Yes | N/A |

**Critical point:** JWTs are **encoded, not encrypted**. Anyone can decode the payload. Never put passwords or sensitive data in a JWT.

### Implementation

```python
import jwt
from datetime import datetime, timezone, timedelta

JWT_SECRET = os.environ["JWT_SECRET"]

def create_token(user_id: str) -> str:
    payload = {
        "user_id": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(days=7),
        "iat": datetime.now(timezone.utc)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")

def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(401, "Invalid token")

# Login endpoint
@router.post("/auth/login")
async def login(data: LoginRequest):
    user = await db.users.find_one({"email": data.email}, {"_id": 0})
    if not user or not verify_password(data.password, user["password_hash"]):
        raise HTTPException(401, "Invalid credentials")
    
    token = create_token(user["id"])
    return {"token": token, "user": {k: v for k, v in user.items() if k != "password_hash"}}

# Protected route using dependency injection
async def get_current_user(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(401, "Missing authentication token")
    token = authorization.split(" ")[1]
    payload = verify_token(token)
    user = await db.users.find_one({"id": payload["user_id"]}, {"_id": 0, "password_hash": 0})
    if not user:
        raise HTTPException(401, "User not found")
    return user
```

### Frontend Token Management

```javascript
// After login: store the token
const login = async (email, password) => {
  const response = await fetch(`${API}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password })
  });
  const data = await response.json();
  localStorage.setItem("auth-token", data.token);
  return data.user;
};

// For all authenticated requests: include the token
const authFetch = async (url, options = {}) => {
  const token = localStorage.getItem("auth-token");
  return fetch(url, {
    ...options,
    headers: {
      ...options.headers,
      "Authorization": `Bearer ${token}`
    }
  });
};

// Logout: remove the token
const logout = () => {
  localStorage.removeItem("auth-token");
  window.location.href = "/login";
};
```

## OAuth 2.0 (Google Sign-In)

### How OAuth Works

```mermaid
sequenceDiagram
    participant U as User
    participant F as Frontend
    participant G as Google
    participant B as Backend

    U->>F: Click "Sign in with Google"
    F->>G: Redirect to Google consent screen
    U->>G: Grant permission
    G->>F: Redirect back with authorization code
    F->>B: POST /api/auth/google {code}
    B->>G: Exchange code for tokens
    G->>B: Return access_token + user info
    B->>B: Find or create user in DB
    B->>B: Create session/JWT
    B->>F: Return {token, user}
```

### Key OAuth Concepts

| Term | Meaning |
|------|---------|
| **Client ID** | Your app's public identifier with Google |
| **Client Secret** | Your app's private key (never expose in frontend) |
| **Authorization Code** | Temporary code exchanged for tokens (single use) |
| **Access Token** | Short-lived token to access Google APIs |
| **Refresh Token** | Long-lived token to get new access tokens |
| **Scope** | What permissions your app requests (email, profile, etc.) |

### On Emergent: Google Auth Integration

Emergent provides managed Google OAuth. The flow is simplified:

```
1. User clicks "Sign in with Google"
2. Redirected to Google consent screen
3. Google redirects back with session_id
4. Frontend stores session, user is authenticated
```

You don't need to manage OAuth tokens yourself — the platform handles the exchange.

## JWT vs Session-Based Auth

| Feature | JWT | Session (Cookie) |
|---------|-----|-------------------|
| Storage | Client-side (localStorage) | Server-side (database) |
| Stateless? | Yes (server doesn't store sessions) | No (server must look up session) |
| Scalability | Excellent (no shared state) | Requires shared session store |
| Revocation | Hard (must wait for expiry) | Easy (delete from database) |
| Size | Larger (contains payload) | Small (just a session ID) |
| XSS vulnerability | If stored in localStorage | Less vulnerable with httpOnly cookies |
| CSRF vulnerability | Not vulnerable | Must use CSRF tokens |

**When to use JWT:** APIs consumed by mobile apps, microservices, stateless architectures.
**When to use sessions:** Traditional web apps, when you need easy revocation.

## Security Best Practices

| Practice | Why | How |
|----------|-----|-----|
| Hash passwords | Never store plaintext | Use `bcrypt` with salt rounds ≥ 12 |
| Short JWT expiry | Limit damage if token is stolen | 15 min access token + refresh token |
| HTTPS only | Prevent token interception | Set `Secure` flag on cookies |
| httpOnly cookies | Prevent XSS from reading tokens | Cookie can't be accessed by JavaScript |
| Validate on every request | Token might be expired/revoked | Use dependency injection |
| Rate limit login attempts | Prevent brute force | Max 5 attempts per minute |

## Troubleshooting Auth Issues

| Problem | Cause | Solution |
|---------|-------|----------|
| "Token expired" immediately | Server time is wrong or expiry too short | Check `exp` claim in JWT payload |
| CORS error on login | Preflight request blocked | Add CORS middleware before routes |
| Token works in curl, not browser | Missing `Bearer` prefix or CORS | Check `Authorization` header format |
| User not found after login | Token has wrong user_id | Verify token creation logic |
| "Invalid signature" | JWT_SECRET different between create/verify | Use same secret from .env |
| Login works, subsequent requests fail | Token not being sent | Check frontend `Authorization` header |
""")

# ============================================================
# 2. Hot Reload & Process Management (2378 -> ~5000 chars)
# ============================================================
update_doc("Hot Reload & Process Management", """# Hot Reload & Process Management

On Emergent, services are managed by Supervisor — a process manager that ensures your frontend, backend, and database stay running. Hot reload means you almost never need to restart services manually.

## Supervisor Architecture

```mermaid
flowchart TD
    S[Supervisord<br/>Process Manager] --> F[Frontend<br/>React on port 3000]
    S --> B[Backend<br/>FastAPI on port 8001]
    S --> M[MongoDB<br/>on port 27017]
    S --> N[Nginx<br/>Reverse Proxy]
```

Supervisor starts when the pod initializes and manages all services. If a process crashes, Supervisor automatically restarts it.

## Process Configuration

Each service has a Supervisor config:

| Service | Port | Auto-restart | Hot Reload |
|---------|------|-------------|------------|
| Frontend (React) | 3000 | Yes | Yes (webpack dev server) |
| Backend (FastAPI) | 8001 | Yes | Yes (uvicorn --reload) |
| MongoDB | 27017 | Yes | N/A (database) |
| Nginx | 80 | Yes | Requires restart |

## Hot Reload: How It Works

### Frontend (React)
When you change any `.js`, `.jsx`, `.css` file in `/app/frontend/src/`:

```
1. Webpack detects file change
2. Recompiles only the changed module
3. Pushes update to browser via WebSocket (HMR)
4. Browser applies changes WITHOUT full page reload
5. React state is preserved (in most cases)
```

**Result:** You see changes in ~1-2 seconds, without losing your place in the app.

### Backend (FastAPI)
When you change any `.py` file in `/app/backend/`:

```
1. Uvicorn's file watcher detects change
2. Server process is killed and restarted
3. New code is loaded
4. Server is ready again in ~2-3 seconds
```

**Result:** API changes take effect automatically. In-memory state is lost (which is fine — use MongoDB for persistence).

## When to Restart Manually

Hot reload handles **code changes** automatically. You only need manual restarts for:

| Change Type | Need Restart? | Command |
|------------|--------------|---------|
| Edit `.py` or `.js` files | No | Automatic |
| Edit `.css` files | No | Automatic |
| Edit `.env` file | **Yes** | `sudo supervisorctl restart backend` |
| Install Python package | **Yes** | `sudo supervisorctl restart backend` |
| Install npm/yarn package | **Yes** | `sudo supervisorctl restart frontend` |
| Edit `nginx.conf` | **Yes** | `sudo supervisorctl restart nginx` |
| MongoDB config change | **Yes** | `sudo supervisorctl restart mongodb` |

## Supervisor Commands

```bash
# Check status of all services
sudo supervisorctl status

# Output example:
# backend    RUNNING   pid 142, uptime 0:45:30
# frontend   RUNNING   pid 145, uptime 0:45:30
# mongodb    RUNNING   pid 139, uptime 0:45:31

# Restart a specific service
sudo supervisorctl restart backend
sudo supervisorctl restart frontend

# View service logs
tail -n 50 /var/log/supervisor/backend.out.log    # stdout
tail -n 50 /var/log/supervisor/backend.err.log    # stderr
tail -n 50 /var/log/supervisor/frontend.out.log
tail -n 50 /var/log/supervisor/frontend.err.log

# Stop/start a service
sudo supervisorctl stop backend
sudo supervisorctl start backend
```

## Common Process Issues and Fixes

| Symptom | Cause | Fix |
|---------|-------|-----|
| Service shows FATAL | Crash loop — bad code or missing dependency | Check `*.err.log` for the error |
| "Address already in use" | Previous process didn't shut down | Don't start services manually; use supervisor |
| Backend keeps restarting | Syntax error in Python file | Fix the error, hot reload will recover |
| Frontend shows blank page | Compilation error | Check `frontend.err.log` for the build error |
| Changes not appearing | File not in watched directory | Ensure files are in `/app/frontend/src/` or `/app/backend/` |
| MongoDB connection refused | MongoDB not running | `sudo supervisorctl restart mongodb` |

## Process Lifecycle Events

```
Pod Start:
1. Supervisord starts (PID 1)
2. MongoDB starts (waits for data directory)
3. Backend starts (waits for MongoDB)
4. Frontend starts (npm/yarn dev server)
5. Nginx starts (routes traffic)

Code Change (Hot Reload):
1. File change detected by watcher
2. Service recompiles/restarts automatically
3. Ready in 1-3 seconds

Service Crash:
1. Process exits with error
2. Supervisor detects exit
3. Automatic restart (with backoff if crashing repeatedly)
4. After 3 rapid failures: enters FATAL state
5. Manual intervention needed: check logs, fix code, restart

Pod Shutdown:
1. Supervisor sends SIGTERM to all processes
2. Processes have 10 seconds to clean up
3. SIGKILL sent if still running
4. Pod terminated
```

## Best Practices

| Practice | Why |
|----------|-----|
| Always check logs before restarting | The restart might just crash again |
| Use `supervisorctl restart`, not `kill` | Supervisor tracks the process properly |
| Don't start duplicate processes | You'll get port conflicts |
| Keep terminal sessions for log tailing | `tail -f /var/log/supervisor/backend.err.log` |
| Use `&& pip freeze > requirements.txt` after installs | Ensure dependencies are captured |
""")

# ============================================================
# 3. Enhance LLM Training Stages (3313 -> ~5500 chars)
# ============================================================
update_doc("LLM Training Stages", """# LLM Training Stages

How a Large Language Model goes from raw text to a capable AI. Understanding this helps you set realistic expectations and use models more effectively.

## The Training Pipeline

```mermaid
flowchart LR
    D[Data Collection<br/>Terabytes of text] --> P[Pre-training<br/>Next token prediction]
    P --> F[Fine-tuning<br/>Instruction following]
    F --> R[RLHF/DPO<br/>Human preference alignment]
    R --> M[Deployed Model<br/>Ready for use]
```

## Stage 1: Data Collection

| Source | Content | Size |
|--------|---------|------|
| Common Crawl | Web pages | ~60% |
| Books | Published literature | ~15% |
| Wikipedia | Encyclopedic knowledge | ~5% |
| Code | GitHub repositories | ~10% |
| Scientific papers | ArXiv, journals | ~5% |
| Other | Forums, docs, social media | ~5% |

**Key considerations:**
- Data quality > data quantity. Filtering out low-quality text is critical
- Deduplication: removing near-identical content prevents memorization
- Balance: too much code → poor natural language; too much chat → poor reasoning
- Legal: training data copyright is an active legal area

Total dataset size: typically 1-15 trillion tokens for frontier models.

## Stage 2: Pre-training

The model learns to predict the next token given all previous tokens:

```
Input:  "The capital of France is"
Target: "Paris"

Input:  "def fibonacci(n):\n    if n <= 1:\n        return"
Target: " n"
```

### What the model learns:

| Capability | How It's Learned |
|-----------|-----------------|
| Grammar | Predicting word order in billions of sentences |
| Facts | Completing factual statements seen in training |
| Reasoning | Predicting logical next steps in arguments |
| Code | Predicting next token in millions of programs |
| Math | Pattern matching on mathematical text |
| Language | Predicting text in 100+ languages |

### The Training Process

```
For each batch of text:
  1. Feed tokens into the model
  2. Model predicts next token
  3. Compare prediction to actual next token
  4. Calculate loss (how wrong was the prediction?)
  5. Backpropagate gradients
  6. Update model weights
  Repeat ~1 trillion times
```

**Cost:** Pre-training a frontier model costs $10M-$100M+ in compute (GPUs running for months).

**Result:** A model that can complete any text — but it has no concept of "being helpful" or "following instructions."

## Stage 3: Fine-tuning (SFT - Supervised Fine-Tuning)

The base model is a text completer, not an assistant. Fine-tuning teaches it to follow instructions:

```
Training example:
{
  "instruction": "Write a haiku about programming",
  "response": "Semicolons fall\\nLike autumn leaves in the code\\nBugs bloom in the spring"
}
```

### What changes:

| Before SFT | After SFT |
|-----------|----------|
| "Write a poem" → continues with random text | "Write a poem" → writes a poem |
| "Summarize this:" → continues the text | "Summarize this:" → writes a summary |
| No concept of conversation turns | Understands user/assistant turns |
| Can generate harmful content freely | Begins to learn boundaries |

**Dataset size:** 10,000-1,000,000 high-quality instruction-response pairs.

## Stage 4: Alignment (RLHF / DPO)

Reinforcement Learning from Human Feedback teaches the model which responses humans prefer:

```mermaid
flowchart TD
    P[Prompt] --> R1[Response A]
    P --> R2[Response B]
    R1 --> H[Human Evaluator]
    R2 --> H
    H --> PREF["'A is better'"]
    PREF --> RM[Reward Model<br/>Learns human preferences]
    RM --> RL[Reinforcement Learning<br/>Model optimizes for preference]
```

### Human Evaluation Criteria

| Criterion | Example |
|-----------|---------|
| **Helpfulness** | Does it actually answer the question? |
| **Harmlessness** | Does it refuse dangerous requests? |
| **Honesty** | Does it say "I don't know" when appropriate? |
| **Formatting** | Is the response well-structured? |
| **Conciseness** | Does it avoid unnecessary verbosity? |

### RLHF vs DPO

| Approach | How It Works | Pros | Cons |
|----------|-------------|------|------|
| **RLHF** | Train reward model → use RL to optimize | Well-understood | Complex, expensive |
| **DPO** | Directly optimize from preference pairs | Simpler, cheaper | Newer, less proven |

## What Happens at Inference Time

When you send a prompt to an LLM:

```
1. Tokenize: "Hello" → [15496]
2. Embed: [15496] → [0.023, -0.891, 0.445, ...]  (4096+ dimensions)
3. Process through transformer layers (32-128 layers)
4. Output layer: probability distribution over all tokens
5. Sampling: select next token based on temperature
6. Repeat from step 2 with the new token appended
```

### Sampling Parameters

| Parameter | Effect | Typical Value |
|-----------|--------|--------------|
| **Temperature** | Randomness. 0 = always pick most likely. 1 = more varied | 0-1 |
| **Top-p** | Only consider tokens with cumulative probability ≤ p | 0.9-0.95 |
| **Top-k** | Only consider the k most likely tokens | 40-100 |
| **Max tokens** | Maximum response length | Task-dependent |

## Why This Matters for Using LLMs

| Training Fact | Practical Implication |
|--------------|----------------------|
| Trained on internet text | May reflect internet biases |
| Knowledge has a cutoff date | Can't know about recent events |
| Optimized for "helpful" responses | May agree with you when it shouldn't |
| Learned patterns, not logic | Can make confident logical errors |
| Fine-tuned on instruction-following | Explicit instructions work better than hints |
| Aligned to be safe | May refuse valid requests that seem risky |
""")

# ============================================================
# 4. Enhance Token Economics & Billing (2465 -> ~5500 chars)
# ============================================================
update_doc("Token Economics & Billing", """# Token Economics & Billing

Understanding tokens is understanding the economics of AI. Every LLM interaction has a cost, and optimizing token usage directly impacts your budget and application performance.

## What Is a Token?

A token is the atomic unit of text for an LLM. It's not a word — it's a sub-word unit determined by the model's tokenizer.

### Examples

| Text | Token Count | Tokens |
|------|------------|--------|
| "Hello" | 1 | `Hello` |
| "Hello world" | 2 | `Hello` + ` world` |
| "indescribable" | 3 | `in` + `describ` + `able` |
| "GPT-4" | 3 | `G` + `PT` + `-4` |
| "{ }" | 2 | `{` + ` }` |
| "你好世界" | 4 | One token per character (CJK) |

**Rule of thumb:** 1 token ≈ 3-4 English characters, or ≈ 0.75 words.

### Quick Estimation

```
A typical page of English text: ~500 words ≈ ~670 tokens
A typical API request: ~100-500 tokens
E1's system prompt: ~15,000 tokens
Full conversation after 10 messages: ~30,000-80,000 tokens
```

## How Costs Are Calculated

LLM providers charge separately for input and output tokens:

```
Cost = (input_tokens × input_price) + (output_tokens × output_price)
```

### Price Comparison (per 1M tokens, approximate)

| Model | Input | Output | Typical API Call Cost |
|-------|-------|--------|---------------------|
| GPT-4o-mini | $0.15 | $0.60 | $0.001 |
| Gemini 3 Flash | $0.10 | $0.40 | $0.0005 |
| Claude Haiku 4.5 | $0.25 | $1.25 | $0.001 |
| GPT-4o | $2.50 | $10.00 | $0.01 |
| Claude Sonnet 4.5 | $3.00 | $15.00 | $0.015 |
| GPT-5.2 | $5.00 | $15.00 | $0.02 |

**Output tokens cost more** because generation is more compute-intensive than reading input.

## Where Your Tokens Go

In a typical E1 interaction:

```mermaid
flowchart TD
    TOTAL[Total Tokens per Message<br/>~50,000 tokens] --> SYS[System Prompt<br/>~15,000 tokens<br/>Same every time]
    TOTAL --> TOOLS[Tool Definitions<br/>~8,000 tokens<br/>Same every time]
    TOTAL --> HIST[Conversation History<br/>~20,000 tokens<br/>Grows each turn]
    TOTAL --> MSG[Your Message<br/>~500 tokens]
    TOTAL --> OUT[E1's Response<br/>~5,000 tokens]
```

**Key insight:** ~23,000 tokens are "fixed cost" every message (system prompt + tools). This is why even a simple "hello" costs tokens.

## The Universal Key (Emergent LLM Key)

The Universal Key simplifies billing across providers:

| Feature | Detail |
|---------|--------|
| **One key, all providers** | Works with OpenAI, Anthropic, Google |
| **Unified billing** | Single balance for all LLM usage |
| **Automatic routing** | Specify model name, key handles the rest |
| **Usage tracking** | See per-call costs in your dashboard |

### Managing Your Balance

```
Profile → Universal Key → Add Balance
```

Set up auto top-up to avoid running out mid-session.

### What the Universal Key Supports

| Capability | Supported? | Models |
|-----------|-----------|--------|
| Text generation | Yes | Claude, GPT, Gemini |
| Image generation | Yes | GPT Image 1, Nano Banana |
| Video generation | Yes | Sora 2 |
| Speech-to-text | Yes | Whisper |
| Embeddings | Check | Provider-dependent |
| Stripe, fal.ai, etc. | **No** | Requires separate keys |

## Optimizing Token Usage

### 1. Reduce Input Tokens

```python
# BAD: Sending entire document as context
messages = [{"role": "user", "content": f"Summarize: {entire_10000_word_doc}"}]

# GOOD: Send only relevant sections
relevant_section = extract_relevant_section(doc, query)
messages = [{"role": "user", "content": f"Summarize: {relevant_section}"}]
```

### 2. Use Cheaper Models for Simple Tasks

```python
# Expensive: Using GPT-5.2 to categorize text
# Cost: ~$0.02 per call

# Cheap: Using GPT-4o-mini for the same task
# Cost: ~$0.001 per call (20x cheaper!)

# Route based on task complexity
if task_type == "categorize":
    model = "gpt-4o-mini"
elif task_type == "complex_analysis":
    model = "claude-sonnet-4-5"
```

### 3. Cache Responses

```python
import hashlib

async def cached_llm_call(prompt, model="gpt-4o-mini"):
    cache_key = hashlib.md5(f"{model}:{prompt}".encode()).hexdigest()
    cached = await db.llm_cache.find_one({"key": cache_key}, {"_id": 0})
    if cached:
        return cached["response"]  # Free!
    
    response = await llm.chat(model=model, messages=[{"role": "user", "content": prompt}])
    await db.llm_cache.insert_one({"key": cache_key, "response": response.content, "created_at": NOW})
    return response.content
```

### 4. Limit Output Length

```python
# Control max output tokens
response = await llm.chat(
    model="claude-sonnet-4-5",
    messages=messages,
    max_tokens=500  # Limit response length
)
```

### 5. Use Streaming for Better UX

Streaming doesn't save tokens, but it makes the experience faster:

```python
# User sees text appearing word-by-word instead of waiting
# for the entire response to generate
async for chunk in llm.stream(model="claude-sonnet-4-5", messages=messages):
    yield chunk.content
```

## Monitoring Usage

Track your token usage to avoid surprises:

```python
# Log every LLM call
async def tracked_llm_call(messages, model):
    response = await llm.chat(model=model, messages=messages)
    
    await db.usage_logs.insert_one({
        "model": model,
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
        "estimated_cost": calculate_cost(model, response.usage),
        "timestamp": NOW
    })
    
    return response
```

## Common Billing Surprises

| Surprise | Cause | Prevention |
|----------|-------|-----------|
| "I only sent one message but used 50K tokens" | System prompt + conversation history | Normal — 23K is baseline |
| "Costs spiked suddenly" | Long conversation = growing context | Start new sessions for unrelated tasks |
| "Balance ran out mid-conversation" | No auto top-up configured | Enable auto top-up in settings |
| "Simple task cost $0.05" | Used expensive model unnecessarily | Route simple tasks to cheaper models |
""")

print("\n=== Enhancement Batch 5 Complete ===")
print("Updated: JWT Auth, Hot Reload, LLM Training, Token Economics")
