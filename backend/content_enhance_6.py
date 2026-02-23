"""Content Enhancement Script - Batch 6
Final batch: enhance remaining shorter documents"""

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
# 1. From Dev to Production (3264 -> ~6000 chars)
# ============================================================
update_doc("From Dev to Production", """# From Dev to Production

The journey from writing code to having a live, accessible application. On Emergent, much of this is automated — but understanding each step helps you debug deployment issues and build more robust apps.

## The Deployment Pipeline

```mermaid
flowchart LR
    DEV[Development<br/>Write & Test Code] --> BUILD[Build<br/>Compile & Bundle]
    BUILD --> TEST[Test<br/>Automated Checks]
    TEST --> DEPLOY[Deploy<br/>Push to Production]
    DEPLOY --> MONITOR[Monitor<br/>Watch for Issues]
```

## Stage 1: Development

On Emergent, development happens inside a Kubernetes pod:

| Component | What Happens | Where |
|-----------|-------------|-------|
| **Write code** | E1 creates/edits files | `/app/backend/`, `/app/frontend/src/` |
| **Install deps** | pip install, yarn add | `requirements.txt`, `package.json` |
| **Test locally** | curl, screenshots, test agent | Preview URL |
| **Auto-commit** | Every E1 action creates a Git commit | `.git/` |

### Preview Environment

Your preview URL (`https://xxx.preview.emergentagent.com`) is a live, accessible version of your app. It's not "production" but it's publicly accessible — anyone with the URL can see it.

```
Preview URL characteristics:
- HTTPS with valid TLS certificate
- Changes reflected immediately (hot reload)
- Temporary — changes when pod is recycled
- Full-stack: frontend + backend + database
```

## Stage 2: Build

### Frontend Build

```bash
# Development mode (what preview uses)
yarn start  # Fast, with hot reload, no optimization

# Production build (what deployment uses)
yarn build  # Slow, fully optimized
```

| Development | Production |
|------------|-----------|
| No minification | JavaScript minified |
| Source maps included | Source maps optional |
| Hot reload enabled | Static files served |
| Larger bundle size | Tree-shaking removes unused code |
| Fast startup | Slow build, fast load |

### Backend Build

Python doesn't have a "build" step — but deployment involves:

```bash
# Ensure all dependencies are captured
pip freeze > requirements.txt

# Verify the app starts cleanly
python -c "from server import app; print('OK')"
```

## Stage 3: Testing

Before deployment, ensure:

```bash
# Backend API tests
curl $API_URL/api/health              # Health check
curl $API_URL/api/documents           # Core functionality
curl -X POST $API_URL/api/tasks \\
  -H "Content-Type: application/json" \\
  -d '{"title":"test"}'               # Write operations

# Frontend tests
# Use screenshot tool or testing_agent to verify UI
```

### Testing Checklist

| Check | How | Priority |
|-------|-----|----------|
| API health check | `curl /api/health` | Critical |
| Core CRUD operations | curl each endpoint | Critical |
| Authentication flow | Login + protected route | High |
| Frontend loads | Screenshot check | High |
| Database seeded | Check document count | Medium |
| Error handling | Send invalid data | Medium |
| Environment variables | Verify `.env` is set | Critical |

## Stage 4: Deploy

### On Emergent: Save to GitHub

The simplest deployment path:

```
1. Click "Save to GitHub" in the chat interface
2. All auto-commits are pushed to your repository
3. Connect your repo to a hosting platform (Vercel, Railway, etc.)
4. Hosting platform auto-deploys from the main branch
```

### Production Considerations

| Concern | Development | Production |
|---------|------------|-----------|
| **Database** | Local MongoDB in pod | MongoDB Atlas (cloud) |
| **Environment** | `.env` file in pod | Environment variables in hosting platform |
| **CORS** | `allow_origins=["*"]` | Specific domain only |
| **Debug mode** | Enabled | Disabled |
| **Logging** | Console output | Structured logging service |
| **HTTPS** | Automatic (Emergent) | Configure SSL certificate |
| **Domain** | Preview URL (temporary) | Custom domain |

### Environment Variables for Production

```bash
# Development (.env in pod)
MONGO_URL="mongodb://localhost:27017"
CORS_ORIGINS="*"

# Production (hosting platform settings)
MONGO_URL="mongodb+srv://user:pass@cluster.mongodb.net/myapp"
CORS_ORIGINS="https://myapp.com"
JWT_SECRET="production-secret-from-secrets-manager"
```

**Never commit production secrets to Git.** Use your hosting platform's environment variable management.

## Stage 5: Monitor

After deployment, watch for:

| Metric | Tool | Alert Threshold |
|--------|------|----------------|
| Response time | Health check endpoint | > 2 seconds |
| Error rate | Application logs | > 1% of requests |
| Uptime | External monitoring | < 99.5% |
| Database connections | MongoDB monitoring | > 80% pool |
| Memory usage | Hosting platform metrics | > 80% |

### Health Check Endpoint

Every production app should have one:

```python
@router.get("/health")
async def health_check():
    try:
        # Verify database connection
        await db.command("ping")
        return {"status": "healthy", "database": "connected"}
    except Exception:
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "database": "disconnected"}
        )
```

## Deployment Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| App works locally, fails in production | Different environment variables | Check all env vars are set |
| "Module not found" in production | Package not in requirements.txt | `pip freeze > requirements.txt` |
| Database connection timeout | Wrong connection string or firewall | Verify MONGO_URL and network access |
| CORS errors in production | Using `allow_origins=["*"]` with credentials | Set specific origins |
| Static files not loading | Build step not run | Run `yarn build` in CI/CD |
| Slow cold start | Large dependencies or no connection pooling | Optimize imports, use connection pool |
""")

# ============================================================
# 2. Kubernetes & Container Orchestration (3314 -> ~5500 chars)
# ============================================================
update_doc("Kubernetes & Container Orchestration", """# Kubernetes & Container Orchestration

Kubernetes (K8s) is the system that manages all the containers on Emergent. It handles pod allocation, scaling, networking, and self-healing. You don't need to manage K8s directly, but understanding it helps you debug issues and understand platform behavior.

## What Kubernetes Does

```mermaid
flowchart TD
    U[Users] --> I[Ingress Controller<br/>Routes HTTPS traffic]
    I --> S1[Pod: User A<br/>React + FastAPI + MongoDB]
    I --> S2[Pod: User B<br/>Different App]
    I --> S3[Pod: User C<br/>Different App]
    K[Kubernetes Control Plane] --> S1
    K --> S2
    K --> S3
```

Kubernetes is the **operating system for the cluster**. It decides:
- Which physical machine runs each pod
- When to create or destroy pods
- How to route network traffic
- What to do when a pod crashes

## Key Concepts

| Concept | What It Is | Emergent Example |
|---------|-----------|-----------------|
| **Pod** | Smallest deployable unit (1+ containers) | Your development environment |
| **Node** | A physical/virtual machine in the cluster | The server running your pod |
| **Namespace** | Logical isolation boundary | Separates users from each other |
| **Service** | Stable network endpoint for pods | How ingress finds your pod |
| **Ingress** | External traffic routing rules | Maps your preview URL to your pod |
| **PersistentVolume** | Storage that survives pod restarts | MongoDB data directory |
| **ConfigMap/Secret** | Configuration and credentials | Your `.env` variables |

## Pod Lifecycle on Emergent

```mermaid
stateDiagram-v2
    [*] --> Pending: User starts job
    Pending --> Running: Resources allocated
    Running --> Running: Active development
    Running --> Idle: No activity
    Idle --> Terminated: Timeout reached
    Terminated --> Pending: User returns
    Running --> CrashLoop: Fatal error
    CrashLoop --> Running: Auto-restart
```

### What Happens at Each Stage

| Stage | Duration | What's Happening |
|-------|----------|-----------------|
| **Pending** | 5-15s | K8s finding a node with resources, pulling container images |
| **Running** | Minutes to hours | Your full dev environment is active |
| **Idle** | Configurable | Pod still running but no user activity |
| **Terminated** | Instant | Pod destroyed, resources freed |
| **CrashLoop** | Varies | Container keeps crashing, K8s retries with backoff |

## Resource Management

Each pod gets allocated resources:

| Resource | Allocated | Purpose |
|----------|-----------|---------|
| **CPU** | Shared (burstable) | Processing power |
| **Memory** | Limited per pod | RAM for your processes |
| **Storage** | Ephemeral + persistent | Files and database |
| **Network** | Shared bandwidth | API calls, web traffic |

If your process tries to use more memory than allocated, Kubernetes **kills it** (OOMKilled). The process restarts automatically but loses in-memory state.

## Networking: How Traffic Reaches Your App

```
User's browser
  → DNS: hub-preview-2.preview.emergentagent.com → IP address
    → Kubernetes Ingress Controller (port 443)
      → TLS termination (HTTPS → HTTP)
        → Ingress rules: /api/* → backend service → pod:8001
        → Ingress rules: /* → frontend service → pod:3000
```

### Port Mapping

| External | Internal | Service |
|----------|----------|---------|
| 443 (HTTPS) | 3000 | Frontend (React) |
| 443 (HTTPS) + `/api/` | 8001 | Backend (FastAPI) |
| Not exposed | 27017 | MongoDB (internal only) |

**MongoDB is never exposed to the internet.** It's only accessible from within the pod via `localhost:27017`.

## Self-Healing

Kubernetes automatically handles failures:

| Failure | K8s Response | User Impact |
|---------|-------------|-------------|
| Process crashes | Restart container | 2-5 second interruption |
| Node failure | Move pod to healthy node | 30-60 second interruption |
| Network partition | Route traffic to available pods | May experience brief errors |
| Resource exhaustion | Kill and restart over-limit processes | Process restart, data in memory lost |

## Scaling

On Emergent, each user gets their own pod (no multi-tenancy within a pod):

```
10 concurrent users = 10 pods
100 concurrent users = 100 pods
Idle users = pods scaled down to 0
```

This is **horizontal scaling** — adding more pods rather than making existing ones bigger.

## Troubleshooting Kubernetes Issues

| Symptom | Likely K8s Cause | What to Do |
|---------|-----------------|-----------|
| Pod takes long to start | Resource contention on cluster | Wait 30-60s, it'll resolve |
| App intermittently unreachable | Pod being rescheduled | Implement retry logic |
| "502 Bad Gateway" | Pod starting up, not ready yet | Wait, or implement health checks |
| Process killed with no error | OOMKilled (out of memory) | Optimize memory usage |
| Preview URL changed | New pod allocated | Use `REACT_APP_BACKEND_URL` from .env |
| Files disappeared | Pod was recycled | Store data in MongoDB, not filesystem |

## What You Don't Need to Worry About

Emergent handles all K8s operations for you:

| Concern | Handled By |
|---------|-----------|
| Pod creation and destruction | Platform |
| TLS certificates | cert-manager (auto-renewal) |
| Ingress configuration | Platform |
| Resource allocation | Platform defaults |
| Node management | Cloud provider |
| Monitoring infrastructure | Platform |

Your job is to write application code. Kubernetes ensures it runs reliably.
""")

# ============================================================
# 3. How Transformers Work (3558 -> ~6000 chars)
# ============================================================
update_doc("How Transformers Work", """# How Transformers Work

The Transformer architecture is the foundation of every modern LLM. Understanding it helps you reason about why LLMs behave the way they do — their strengths, limitations, and failure modes.

## The Big Picture

An LLM is a neural network that predicts the next token given all previous tokens.

```mermaid
flowchart LR
    A[Input Text] --> B[Tokenizer]
    B --> C[Embedding Layer]
    C --> D[Transformer Blocks<br/>32-128 layers]
    D --> E[Output Layer]
    E --> F[Next Token<br/>Probabilities]
    F --> G[Sampling]
    G --> H[Generated Token]
```

**The core loop:** Predict one token → append it to the input → predict the next token → repeat. This is why LLM output appears word by word — each token is generated sequentially.

## Step-by-Step: Inside the Transformer

### 1. Tokenization

Text is split into sub-word tokens using a fixed vocabulary:

| Text | Tokens | Token IDs |
|------|--------|-----------|
| "Hello world" | `Hello`, ` world` | [15496, 995] |
| "unhappiness" | `un`, `happiness` | [348, 41098] |
| "```python" | ` ``` `, `python` | [7559, 31373] |
| "E1 agent" | `E`, `1`, ` agent` | [36, 16, 5765] |

Common words = 1 token. Rare words = split into sub-words. Numbers and special characters = individual tokens.

### 2. Embedding

Each token ID is converted to a high-dimensional vector (typically 4096-12288 dimensions):

```
Token "Hello" (ID: 15496) → [0.023, -0.891, 0.445, ..., 0.112]
                             ← 4096+ floating point numbers →
```

**Positional encoding** is added so the model knows the order of tokens. Without it, "dog bites man" and "man bites dog" would look identical.

### 3. Self-Attention (The Key Innovation)

Self-attention lets each token "look at" every other token in the sequence to understand context:

```mermaid
flowchart LR
    T1[The] --> A{Attention}
    T2[cat] --> A
    T3[sat] --> A
    T4[on] --> A
    T5[the] --> A
    T6[mat] --> A
    A --> O[Each token gets a<br/>context-aware representation]
```

**How attention works:**

For each token, the model asks: "Which other tokens are relevant to understanding *this* token?"

```
"The bank by the river"
  - "bank" attends strongly to "river" → meaning: riverbank
  
"The bank approved the loan"
  - "bank" attends strongly to "loan" → meaning: financial institution
```

Same word, different meaning — determined by attention to surrounding context.

### The Q, K, V Mechanism

Each token produces three vectors:

| Vector | Purpose | Analogy |
|--------|---------|---------|
| **Query (Q)** | "What am I looking for?" | A search query |
| **Key (K)** | "What do I contain?" | A search index entry |
| **Value (V)** | "What information do I provide?" | The actual content |

```
Attention score = softmax(Q · K^T / √d)
Output = score × V
```

High Q·K similarity = high attention score = that token's Value is important for the current position.

### Multi-Head Attention

Instead of one attention mechanism, transformers use multiple "heads" in parallel:

| Head | What It Might Learn |
|------|-------------------|
| Head 1 | Syntax — subject/verb agreement |
| Head 2 | Semantics — word meaning in context |
| Head 3 | Position — relative distance between tokens |
| Head 4 | Coreference — "it" refers to "the cat" |

Multiple heads allow the model to attend to different aspects of the input simultaneously.

### 4. Feed-Forward Network

After attention, each token's representation passes through a neural network:

```
Input → Linear(4096 → 16384) → ReLU → Linear(16384 → 4096) → Output
```

This is where the model stores "knowledge" — factual associations learned during training. The attention mechanism provides context; the feed-forward network provides knowledge.

### 5. Layer Stacking

Modern LLMs stack 32-128 transformer blocks:

```
Layer 1:  Attention → Feed-Forward  (basic syntax)
Layer 2:  Attention → Feed-Forward  (word relationships)
...
Layer 32: Attention → Feed-Forward  (complex reasoning)
Layer 64: Attention → Feed-Forward  (abstract concepts)
...
Layer 128: Attention → Feed-Forward (highest-level understanding)
```

Earlier layers handle syntax and basic patterns. Later layers handle semantics, reasoning, and abstract concepts.

### 6. Output: Next Token Prediction

The final layer produces a probability distribution over the entire vocabulary (~100K tokens):

```
"The capital of France is" →
  Paris: 0.92
  Lyon: 0.03
  a: 0.01
  the: 0.008
  ...
  zzzzz: 0.0000001
```

### 7. Sampling

The sampling strategy determines which token is selected:

| Strategy | Behavior | Use Case |
|----------|----------|----------|
| **Greedy** (temp=0) | Always pick highest probability | Factual, deterministic |
| **Low temp** (0.3) | Mostly pick top choices | Balanced, slightly varied |
| **Medium temp** (0.7) | Good mix of likely and creative | General purpose |
| **High temp** (1.0) | Wide distribution, more random | Creative writing |
| **Top-p** (nucleus) | Only consider tokens with cumulative prob ≤ p | Prevents bizarre outputs |

## Why This Architecture Works

| Property | Why It Matters |
|----------|---------------|
| **Parallelizable** | All tokens processed simultaneously (unlike RNNs) |
| **Scalable** | More layers + more data = better performance |
| **Context-aware** | Self-attention captures long-range dependencies |
| **General-purpose** | Same architecture works for text, code, images, audio |

## Implications for Users

| Transformer Property | Practical Impact |
|---------------------|-----------------|
| Fixed context window | Long conversations lose early context |
| Token-by-token generation | Output appears word by word |
| Attention is O(n²) | Very long inputs are expensive |
| Pattern matching, not reasoning | Can fail on novel logic problems |
| Probabilistic output | Same input can produce different outputs |
| No persistent memory | Each request starts fresh |
""")

print("\n=== Enhancement Batch 6 Complete ===")
print("Updated: Deployment, Kubernetes, Transformers")
