"""Content Authenticity Fix - Batch 3
Fix remaining documents: Docker, Assets, Kubernetes, Deployment, Hot Reload, RAG, Debugging"""

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
# 1. Docker → Remove fake "Emergent uses" claims
# ============================================================
update_doc("Docker & Container Fundamentals", """# Docker & Container Fundamentals

Containers are the building blocks of modern cloud infrastructure. Understanding how they work helps you debug environment issues and make better deployment decisions.

## What Is a Container?

A container is an **isolated process** that thinks it has its own operating system, filesystem, and network — but actually shares the host's kernel.

```mermaid
flowchart TB
    subgraph Host["Host Machine"]
        K[Linux Kernel]
        subgraph C1["Container 1"]
            A1[Your App + Dependencies]
        end
        subgraph C2["Container 2"]
            B1[Different App]
        end
        K --> C1
        K --> C2
    end
```

**Key insight:** Containers are NOT virtual machines. They don't run a separate OS kernel. They use Linux namespaces and cgroups to create isolation.

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
# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy dependency file first (better layer caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the port
EXPOSE 8001

# Start command
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

**That's why we copy `requirements.txt` before the code** — dependencies change less often, so the install layer stays cached.

## Container Networking

Services inside a container (or pod) communicate over localhost:

```
Frontend (port 3000) ←──→ Backend (port 8001)
                              ↕
                          Database (port 27017)
```

External traffic typically flows through a reverse proxy or load balancer:

```
User Browser
  → HTTPS → Load Balancer / Ingress
    → /api/* → Backend service
    → /*     → Frontend service
```

## Common Docker Commands

| Command | What It Does |
|---------|-------------|
| `docker build -t myapp .` | Build an image from Dockerfile |
| `docker run -p 3000:3000 myapp` | Start a container from an image |
| `docker ps` | List running containers |
| `docker logs <container>` | Show container output |
| `docker exec -it <container> bash` | Open a shell inside a container |
| `docker stop <container>` | Stop a container |

## Troubleshooting Container Issues

| Problem | Symptom | Solution |
|---------|---------|----------|
| Service won't start | Process exits immediately | Check logs for error messages |
| Port already in use | `Address already in use` error | Stop conflicting process or use a different port |
| Package not found | `ModuleNotFoundError` | Add to requirements.txt and rebuild |
| Out of memory | Process killed without error | Optimize memory usage or increase limits |
| Filesystem full | `No space left on device` | Clean up temp files and unused images |

## Best Practices

| Practice | Why |
|----------|-----|
| List dependencies in requirements.txt / package.json | Reproducible builds |
| Don't store data in the container filesystem | Data is lost when container restarts; use a database |
| Use environment variables for configuration | Same image works in all environments |
| Keep images small | Faster builds and deployments |
| Use .dockerignore | Exclude node_modules, .git from build context |
""")

# ============================================================
# 2. Assets → Remove platform-specific claims
# ============================================================
update_doc("Assets & File Processing", """# Assets & File Processing

How to handle file uploads, storage, and serving in a web application.

## The File Lifecycle

```mermaid
flowchart LR
    U[User Upload] --> V[Validation]
    V --> S[Storage]
    S --> CDN[Serve via URL]
```

1. **Upload** — File selected via frontend input or generated programmatically
2. **Validation** — Check file type, size limits, and content
3. **Storage** — Save to filesystem, database, or cloud storage
4. **Serve** — Make available via URL for display or download

## Storage Options

| Option | Persistence | Best For | Example |
|--------|------------|----------|---------|
| **Local filesystem** | Lost on server restart (ephemeral) | Temporary processing | `/tmp/uploads/` |
| **Database (GridFS)** | Permanent | Small files, metadata-heavy | MongoDB GridFS |
| **Cloud storage** | Permanent | Production file hosting | AWS S3, Google Cloud Storage |
| **CDN** | Permanent + cached globally | Public assets, images | CloudFront, Cloudflare |

**For production:** Always use cloud storage or a database. Local filesystem is only suitable for temporary processing.

## Handling File Uploads

### Backend: Receiving Files (FastAPI)

```python
from fastapi import UploadFile, File, HTTPException

@api_router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Validate file type
    allowed_types = ["image/png", "image/jpeg", "application/pdf"]
    if file.content_type not in allowed_types:
        raise HTTPException(400, "File type not allowed")
    
    # Validate file size (10MB limit)
    contents = await file.read()
    if len(contents) > 10 * 1024 * 1024:
        raise HTTPException(400, "File too large (max 10MB)")
    
    # Save to filesystem
    file_path = f"/app/uploads/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(contents)
    
    return {"filename": file.filename, "size": len(contents)}
```

### Frontend: Uploading Files

```jsx
const handleUpload = async (event) => {
  const file = event.target.files[0];
  const formData = new FormData();
  formData.append("file", file);
  
  const response = await fetch(`${API}/upload`, {
    method: "POST",
    body: formData,
    // Do NOT set Content-Type header — browser sets it 
    // automatically with the correct multipart boundary
  });
  
  const data = await response.json();
  console.log("Uploaded:", data.filename);
};
```

### Chunked Upload for Large Files

For files larger than typical proxy limits (~5MB), use chunked uploads:

```javascript
async function uploadChunked(file, chunkSize = 1024 * 1024) {
  const totalChunks = Math.ceil(file.size / chunkSize);
  const uploadId = crypto.randomUUID();
  
  for (let i = 0; i < totalChunks; i++) {
    const start = i * chunkSize;
    const chunk = file.slice(start, start + chunkSize);
    const formData = new FormData();
    formData.append("chunk", chunk);
    formData.append("uploadId", uploadId);
    formData.append("chunkIndex", i);
    formData.append("totalChunks", totalChunks);
    
    await fetch(`${API}/upload/chunk`, {
      method: "POST",
      body: formData,
    });
  }
  
  // Tell server to assemble chunks
  return fetch(`${API}/upload/finalize`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ uploadId, filename: file.name }),
  });
}
```

## Image Optimization Best Practices

| Technique | How | Impact |
|-----------|-----|--------|
| Compress on upload | Use `Pillow` to reduce quality to 80% | 50-70% size reduction |
| Serve correct size | Generate thumbnails for lists | Faster page loads |
| Use WebP format | Convert PNG/JPEG to WebP | 25-35% smaller |
| Lazy loading | `<img loading="lazy" />` | Defer off-screen images |

## Troubleshooting File Issues

| Problem | Cause | Solution |
|---------|-------|----------|
| "File not found" after restart | Stored in ephemeral filesystem | Use database or cloud storage |
| Upload fails silently | Body size limit exceeded | Use chunked uploads |
| "Content-Type not set" | Manually set on FormData | Don't set Content-Type — let the browser handle it |
| Large upload timeout | File too large for single request | Implement chunked upload |
| Image URL returns 404 | Server restarted, file was in /tmp | Use persistent storage |
""")

# ============================================================
# 3. RAG → Remove "E1's AI Chat" references
# ============================================================
update_doc("Retrieval Augmented Generation", """# Retrieval Augmented Generation (RAG)

RAG is the technique of giving an LLM access to external knowledge at query time, rather than relying solely on its training data. It's how you build AI features that know about *your* data.

## Why RAG Exists

LLMs have two fundamental limitations:

| Limitation | Example | RAG Solution |
|-----------|---------|-------------|
| **Knowledge cutoff** | Doesn't know about recent events | Retrieve current docs at query time |
| **No private data** | Doesn't know your company's policies | Retrieve from your knowledge base |
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

1. **Embed** — Convert the question into a vector using an embedding model
2. **Search** — Find the most similar document vectors
3. **Retrieve** — Pull the top K relevant document chunks
4. **Augment** — Insert retrieved text into the LLM prompt as context
5. **Generate** — The LLM answers using the retrieved context

## Implementation Example

### Step 1: Chunk Your Documents

```python
def chunk_text(text, chunk_size=500, overlap=50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks
```

### Step 2: Create Embeddings

```python
# Using an embedding model
async def create_embedding(text):
    response = await embedding_model.create(input=text)
    return response.data[0].embedding

# Store chunks with their embeddings
for chunk in chunks:
    embedding = await create_embedding(chunk["text"])
    chunk["embedding"] = embedding
    await db.knowledge_base.insert_one(chunk)
```

### Step 3: Search at Query Time

```python
async def search_knowledge(query, top_k=5):
    query_embedding = await create_embedding(query)
    
    # Use vector similarity search
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
        {"$project": {"_id": 0, "text": 1, "source": 1}}
    ]).to_list(top_k)
    
    return results
```

### Step 4: Generate an Answer

```python
async def answer_with_rag(question):
    context_docs = await search_knowledge(question)
    context = "\\n\\n".join([
        f"[Source: {doc['source']}]\\n{doc['text']}" 
        for doc in context_docs
    ])
    
    messages = [
        {"role": "system", "content": f\"\"\"Answer using ONLY the provided context.
If the context doesn't contain the answer, say "I don't have that information."

Context:
{context}\"\"\"},
        {"role": "user", "content": question}
    ]
    
    response = await llm.chat(messages=messages)
    return {
        "answer": response.content,
        "sources": [doc["source"] for doc in context_docs]
    }
```

## Chunking Strategies

| Strategy | How It Works | Best For |
|----------|-------------|----------|
| **Fixed size** | Split every N words | Simple, general purpose |
| **Paragraph** | Split on double newlines | Well-structured documents |
| **Semantic** | Split at topic boundaries | Long-form content |
| **Sliding window** | Overlapping chunks | Preserving context across boundaries |

**Critical parameter: overlap.** Without overlap, a fact split across two chunks may never be retrieved. 50-100 token overlap is typically sufficient.

## Simpler Alternatives to Full RAG

Not every use case needs vector search:

| Approach | How It Works | When to Use |
|----------|-------------|-------------|
| **Full RAG** | Vector embeddings + similarity search | Large knowledge bases (1000+ docs) |
| **Context stuffing** | Include relevant docs directly in prompt | Small knowledge bases (<10 docs) |
| **Keyword search + LLM** | Traditional search, then LLM summarizes | Existing search infrastructure |
| **Direct database query** | SQL/MongoDB query | Structured data (not free-form text) |

## Common RAG Mistakes

| Mistake | Impact | Fix |
|---------|--------|-----|
| Chunks too large (>1000 tokens) | Dilutes the answer with irrelevant text | Use 300-500 token chunks |
| Chunks too small (<100 tokens) | Loses context and meaning | Use 300-500 token chunks |
| No overlap between chunks | Information at boundaries lost | Add 50-100 token overlap |
| Not citing sources | User can't verify answers | Return source metadata with response |
| Using RAG for everything | Over-engineering simple lookups | Use direct DB queries for structured data |
""")

# ============================================================
# 4. Debugging a 500 Error → Already mostly general, minor fix
# ============================================================
update_doc("Debugging a 500 Error Step-by-Step", """# Debugging a 500 Error Step-by-Step

A practical walkthrough of how to diagnose and fix a server error, following a systematic debugging process.

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
# Check recent backend error logs
tail -n 100 /var/log/supervisor/backend.err.log

# Search for the actual error
grep -A 5 "Error\\|Exception\\|Traceback" /var/log/supervisor/backend.err.log | tail -30
```

**What you're looking for:**

```
Traceback (most recent call last):
  File "/app/backend/server.py", line 142, in get_tasks
    tasks = await db.tasks.find(query).to_list(100)
TypeError: 'NoneType' object is not iterable
```

This tells you:
- **Which file:** `server.py`
- **Which line:** 142
- **Which function:** `get_tasks`
- **The actual error:** `TypeError: 'NoneType' object is not iterable`

## Step 2: Reproduce the Error

Before fixing anything, **reproduce it consistently**:

```bash
# Try the exact request that's failing
curl -v $API_URL/api/tasks

# Does it fail with specific parameters?
curl "$API_URL/api/tasks?status=done"     # Works?
curl "$API_URL/api/tasks?status=invalid"  # Fails?
```

## Step 3: Identify the Root Cause

Common root causes for 500 errors:

| Root Cause | Clue in Logs | Example |
|-----------|-------------|---------|
| **Unhandled None** | `'NoneType' has no attribute` | Query returned no results |
| **Missing field** | `KeyError: 'status'` | Document missing expected field |
| **Bad ObjectId** | `ObjectId is not JSON serializable` | Returning MongoDB `_id` |
| **Import error** | `ModuleNotFoundError` | Package not installed |
| **Syntax error** | `SyntaxError` | Typo in code |
| **Database connection** | `ServerSelectionTimeoutError` | Database not running |
| **Missing env var** | `KeyError: 'MONGO_URL'` | .env not configured |

## Step 4: Apply the Fix

For our example (`TypeError` from a query):

```python
# BEFORE (broken):
@router.get("/tasks")
async def get_tasks(status: str = None):
    query = {"status": status}  # If None, query = {"status": None}
    tasks = await db.tasks.find(query, {"_id": 0}).to_list(100)
    return tasks

# AFTER (fixed):
@router.get("/tasks")
async def get_tasks(status: str = None):
    query = {}
    if status:
        query["status"] = status
    tasks = await db.tasks.find(query, {"_id": 0}).to_list(100)
    return tasks
```

## Step 5: Verify the Fix

```bash
# Test the exact same request that was failing
curl $API_URL/api/tasks

# Test edge cases
curl "$API_URL/api/tasks?status=done"
curl "$API_URL/api/tasks?status=todo"
curl $API_URL/api/tasks  # No filter
```

## Step 6: Check for Similar Issues

If this bug existed in one endpoint, the same pattern might exist elsewhere:

```bash
grep -n "query = {" /app/backend/server.py
```

Fix all instances, not just the one you found.

## Quick Diagnosis Commands

```bash
# Is the backend running?
sudo supervisorctl status backend

# Recent errors?
tail -20 /var/log/supervisor/backend.err.log

# Is the database running?
sudo supervisorctl status mongodb

# Can you reach the API?
curl -s -o /dev/null -w "%{http_code}" $API_URL/api/health
```

## Common Fix Patterns

| Error Type | Quick Fix |
|-----------|----------|
| `ObjectId not serializable` | Add `{"_id": 0}` to all MongoDB queries |
| `ModuleNotFoundError` | `pip install <module> && pip freeze > requirements.txt` |
| `Connection refused` | `sudo supervisorctl restart backend` |
| `CORS error` (in browser) | Check CORS middleware is before routes |
| `422 Unprocessable Entity` | Check request body matches Pydantic model |

## Prevention Checklist

- Always exclude `_id` from MongoDB responses
- Always check `find_one` result for `None` before using
- Always validate input with Pydantic models
- Always test with curl after making changes
- Always check logs, not just the HTTP response
""")

print("\n=== Authenticity Fix Batch 3 Complete ===")
