"""Batch 2 — Technical Gap Documents (7 new docs)"""
from pymongo import MongoClient
from datetime import datetime, timezone
import uuid

client = MongoClient('mongodb://localhost:27017')
db = client['test_database']
NOW = datetime.now(timezone.utc).isoformat()

def _id(): return str(uuid.uuid4())

def create_cat(name, icon, order, parent_id=None):
    cat_id = _id()
    db.categories.insert_one({"id": cat_id, "name": name, "icon": icon, "order": order, "parent_id": parent_id})
    print(f"Category: {name}")
    return cat_id

def create_doc(title, cat_id, content, order=0, tags=None):
    doc_id = _id()
    doc = {"id": doc_id, "title": title, "category_id": cat_id, "author_id": "system",
           "created_at": NOW, "updated_at": NOW, "order": order, "deleted": False, "content": content}
    if tags: doc["tags"] = tags
    db.documents.insert_one(doc)
    print(f"  Doc: {title} ({len(content)} chars)")

# Existing IDs
CAT_LLM = "52c88f91-c6d7-401b-8b56-c29a8a639a56"
SUB_TOKENS = "e785794a-1318-4f7c-be20-36db8cb03be0"
CAT_ADVANCED = "a7aa2f11-d978-48e1-b5cd-2af037632309"
CAT_ANATOMY = "a2a89675-2987-4313-b6a8-4690d7f330e3"
SUB_FRAMEWORKS = "9aee9d5d-18b5-4e54-bebf-b0ec0c2c153b"
CAT_TUTORIALS = "f73c6407-fa1a-4887-89bf-b57a3f38269f"
SUB_COMPARISONS = "ecbe74be-348e-4df0-a149-84531eba899c"

# New subcategories
SUB_FUNCTION_CALLING = create_cat("Function Calling", "Zap", 3, CAT_LLM)
SUB_MULTI_AGENT = create_cat("Multi-Agent Systems", "Users", 5, CAT_ANATOMY)
SUB_EVAL = create_cat("Evaluation", "Search", 6, CAT_ANATOMY)

# ============================================================
# 1. Function Calling Deep Dive
# ============================================================
create_doc("Function Calling & Tool Use", SUB_FUNCTION_CALLING, r"""# Function Calling & Tool Use

Function calling is the mechanism that turns an LLM from a text generator into an agent's reasoning engine. It's how the model says "I want to use a tool" in a structured, parseable way.

## What Is Function Calling?

Without function calling, an LLM can only generate text:
```
User: "What's the weather in Tokyo?"
LLM: "I don't have access to real-time weather data."
```

With function calling, the LLM can request tool use:
```
User: "What's the weather in Tokyo?"
LLM: {"tool": "get_weather", "arguments": {"city": "Tokyo"}}
→ Tool executes → {"temp": 22, "condition": "sunny"}
LLM: "It's 22°C and sunny in Tokyo right now."
```

The LLM doesn't execute the tool — it **requests** the tool call via structured JSON. The agent's execution layer runs it.

## How It Works at the API Level

### Step 1: Define Tools

You tell the LLM what tools are available using JSON schemas:

```json
{
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "get_weather",
        "description": "Get current weather for a city",
        "parameters": {
          "type": "object",
          "properties": {
            "city": {
              "type": "string",
              "description": "City name, e.g., Tokyo"
            }
          },
          "required": ["city"]
        }
      }
    }
  ]
}
```

### Step 2: LLM Decides to Call a Tool

When the LLM determines it needs external data, it returns a **tool call** instead of text:

```json
{
  "role": "assistant",
  "content": null,
  "tool_calls": [
    {
      "id": "call_abc123",
      "type": "function",
      "function": {
        "name": "get_weather",
        "arguments": "{\"city\": \"Tokyo\"}"
      }
    }
  ]
}
```

### Step 3: Execute and Return Result

Your code executes the function and sends the result back:

```json
{
  "role": "tool",
  "tool_call_id": "call_abc123",
  "content": "{\"temp\": 22, \"condition\": \"sunny\"}"
}
```

### Step 4: LLM Generates Final Response

The LLM sees the tool result and formulates a natural language answer:
```
"It's currently 22°C and sunny in Tokyo."
```

## Tool Choice Modes

| Mode | Behavior | When to Use |
|------|----------|------------|
| `auto` | LLM decides whether to call a tool or respond with text | Default — most flexible |
| `required` | LLM must call at least one tool | When you always need an action |
| `none` | LLM cannot call any tools | When you want text-only responses |
| Specific tool | LLM must call a particular tool | When you know exactly which tool is needed |

## Parallel Tool Calls

Modern LLMs can request multiple tool calls in a single response:

```json
{
  "tool_calls": [
    {"function": {"name": "get_weather", "arguments": "{\"city\": \"Tokyo\"}"}},
    {"function": {"name": "get_weather", "arguments": "{\"city\": \"London\"}"}},
    {"function": {"name": "get_weather", "arguments": "{\"city\": \"New York\"}"}}
  ]
}
```

The agent can execute all three in parallel, saving round-trips.

## Structured Outputs

A related concept: constraining the LLM to output valid JSON matching a schema. This is different from function calling:

| Feature | Function Calling | Structured Output |
|---------|-----------------|-------------------|
| **Purpose** | Request tool execution | Generate formatted data |
| **Output** | Tool call with arguments | JSON matching a schema |
| **Who executes?** | The agent's tool layer | No execution needed |
| **Example** | "Search the web for X" | "Extract name, email from this text" |

### Structured Output Example

```json
{
  "response_format": {
    "type": "json_schema",
    "json_schema": {
      "name": "extracted_contact",
      "schema": {
        "type": "object",
        "properties": {
          "name": {"type": "string"},
          "email": {"type": "string"},
          "phone": {"type": "string"}
        },
        "required": ["name", "email"]
      }
    }
  }
}
```

The LLM is guaranteed to return valid JSON matching this schema — no parsing errors, no missing fields.

## Implementation Example (Python)

```python
import openai

# Define the tool
tools = [{
    "type": "function",
    "function": {
        "name": "search_database",
        "description": "Search for records in the database",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"},
                "limit": {"type": "integer", "description": "Max results", "default": 10}
            },
            "required": ["query"]
        }
    }
}]

# Send request with tools
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Find all users named Alice"}],
    tools=tools,
    tool_choice="auto"
)

# Check if LLM wants to call a tool
message = response.choices[0].message
if message.tool_calls:
    for tool_call in message.tool_calls:
        args = json.loads(tool_call.function.arguments)
        # Execute the actual function
        result = search_database(**args)
        # Send result back to LLM
        messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": json.dumps(result)})
```

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Vague tool descriptions | LLM uses wrong tool | Write clear, specific descriptions with examples |
| Too many tools (50+) | LLM confused about which to pick | Group related tools, limit to 10-20 active tools |
| Missing parameter descriptions | LLM hallucinates parameter values | Describe every parameter with examples |
| Not handling parallel calls | Execute sequentially, wasting time | Check for multiple tool_calls and parallelize |
| Ignoring tool_choice | LLM calls tools when it shouldn't | Use `none` when you want text-only responses |
""", tags=["core-concepts", "llm", "function-calling"])

# ============================================================
# 2. Multi-Agent Communication
# ============================================================
create_doc("Multi-Agent Communication", SUB_MULTI_AGENT, """# Multi-Agent Communication

How AI agents communicate with each other — protocols, patterns, and the emerging standards that make multi-agent systems work.

## Why Multi-Agent?

A single agent can do many things, but some tasks benefit from specialization:

| Approach | Strengths | Weaknesses |
|----------|----------|-----------|
| **Single agent** | Simple, no coordination overhead | Limited expertise, large context |
| **Multi-agent** | Specialized skills, parallel work | Coordination complexity, context sharing |

## Communication Patterns

### 1. Orchestrator-Worker (Hub and Spoke)

```mermaid
flowchart TD
    O[Orchestrator] -->|task| W1[Worker 1]
    O -->|task| W2[Worker 2]
    O -->|task| W3[Worker 3]
    W1 -->|result| O
    W2 -->|result| O
    W3 -->|result| O
```

The orchestrator controls all communication. Workers never talk to each other.

**How context is shared:** The orchestrator packages relevant context into each worker's task. Workers return structured results. The orchestrator synthesizes everything.

**Used by:** Most production AI coding platforms.

### 2. Peer-to-Peer (Mesh)

```mermaid
flowchart LR
    A1[Agent 1] <-->|message| A2[Agent 2]
    A2 <-->|message| A3[Agent 3]
    A1 <-->|message| A3
```

Agents communicate directly with each other.

**How context is shared:** Agents send messages to each other in a shared conversation thread. Each agent sees the full thread.

**Used by:** CrewAI, AutoGen.

### 3. Blackboard (Shared State)

```mermaid
flowchart TD
    BB[(Shared Blackboard)] --> A1[Agent 1: reads & writes]
    BB --> A2[Agent 2: reads & writes]
    BB --> A3[Agent 3: reads & writes]
```

Agents share a common knowledge base. Each agent reads the current state, does its work, and writes results back.

**Used by:** Research agents, collaborative writing systems.

### 4. Pipeline (Sequential Handoff)

```mermaid
flowchart LR
    A1[Research Agent] -->|findings| A2[Analysis Agent]
    A2 -->|insights| A3[Writing Agent]
    A3 -->|draft| A4[Review Agent]
```

Each agent processes sequentially, handing results to the next.

**Used by:** Content generation pipelines, data processing workflows.

## Emerging Protocols

### Model Context Protocol (MCP) — Anthropic

MCP standardizes how agents discover and use tools:

| Aspect | Before MCP | With MCP |
|--------|-----------|----------|
| Tool discovery | Hardcoded in configuration | Dynamic — agent queries available tools at runtime |
| Tool interface | Custom per framework | Standardized JSON-RPC protocol |
| Cross-platform | Tools not portable | Same tool works across MCP-compatible agents |

**MCP Architecture:**
```
Agent (MCP Client) ←→ MCP Server (exposes tools)
                          ├── Database tools
                          ├── File system tools
                          └── API tools
```

The key insight: tools are **servers**, not libraries. An agent connects to a tool server, discovers available capabilities, and calls them using a standard protocol.

### Agent-to-Agent (A2A) — Google

A2A focuses on how agents communicate with other agents (not just tools):

| Feature | Purpose |
|---------|---------|
| **Agent Cards** | JSON description of an agent's capabilities |
| **Task protocol** | Standard way to assign tasks between agents |
| **Streaming** | Real-time communication during task execution |
| **Push notifications** | Notify when a long-running task completes |

### How MCP and A2A Complement Each Other

| Protocol | Focus | Scope |
|----------|-------|-------|
| **MCP** | Agent ↔ Tool communication | How agents use tools |
| **A2A** | Agent ↔ Agent communication | How agents collaborate |

They solve different problems and can coexist in the same system.

## Context Sharing Challenges

The hardest problem in multi-agent systems: how much context does each agent need?

| Strategy | Approach | Tradeoff |
|----------|---------|----------|
| **Full context** | Every agent sees everything | Expensive (tokens), may overwhelm |
| **Minimal context** | Agent only gets what it needs for its specific task | Efficient, but agent may miss relevant info |
| **Summarized context** | Full history summarized into key points | Balanced, but summaries lose details |
| **Shared memory** | All agents read/write to common store | Flexible, but needs coordination |

## Practical Implementation

### Simple Orchestrator-Worker in Python

```python
async def orchestrate(user_request):
    # Plan
    plan = await main_agent.plan(user_request)
    
    # Delegate to specialists
    if plan.needs_testing:
        test_results = await testing_agent.run(
            context=plan.implementation_summary,
            files=plan.changed_files
        )
    
    if plan.needs_design:
        design = await design_agent.run(
            app_type=plan.app_type,
            requirements=plan.ui_requirements
        )
    
    # Synthesize results
    return await main_agent.synthesize(
        test_results=test_results,
        design=design,
        original_request=user_request
    )
```

## Common Multi-Agent Failures

| Failure | Cause | Fix |
|---------|-------|-----|
| **Contradictory outputs** | Agents give conflicting advice | Orchestrator must resolve conflicts |
| **Context loss** | Worker doesn't get enough context | Package comprehensive task descriptions |
| **Infinite delegation** | Agent A delegates to B, B delegates back to A | Set delegation depth limits |
| **Redundant work** | Two agents do the same thing | Clear role boundaries |
| **Coordination overhead** | More time coordinating than working | Only use multi-agent when specialization genuinely helps |
""", tags=["core-concepts", "architecture", "multi-agent"])

# ============================================================
# 3. Evaluation & Observability
# ============================================================
create_doc("Evaluation & Observability", SUB_EVAL, """# Evaluation & Observability

How to measure if your agent is actually working well — and how to debug it when it's not.

## Why Evaluate Agents?

Traditional software is deterministic: same input → same output. Agents are non-deterministic: same input → potentially different actions, different results. This makes evaluation fundamentally harder.

## What to Measure

### Task-Level Metrics

| Metric | What It Measures | How to Compute |
|--------|-----------------|---------------|
| **Task completion rate** | % of tasks completed successfully | Successful tasks / total tasks |
| **Accuracy** | Was the output correct? | Human review or automated checks |
| **Iterations to complete** | How many loops before done? | Count LLM calls per task |
| **Time to complete** | Wall-clock time for the full task | End timestamp - start timestamp |
| **Cost per task** | Total token cost | Sum of all LLM call costs |
| **Escalation rate** | How often the agent asks for human help | Escalations / total tasks |

### Turn-Level Metrics

| Metric | What It Measures | Signal |
|--------|-----------------|--------|
| **Tool choice accuracy** | Did the agent pick the right tool? | Wrong tool = wasted iteration |
| **Parameter accuracy** | Were tool parameters correct? | Wrong params = errors |
| **Retry rate** | How often does a tool call fail and retry? | High retry = poor planning |
| **Token efficiency** | Tokens used vs. task complexity | Excessive tokens = verbose prompting |

### System-Level Metrics

| Metric | Purpose | Alert Threshold |
|--------|---------|----------------|
| **LLM latency** | Response time from provider | > 30 seconds |
| **Tool execution time** | Time to execute each tool | > 60 seconds |
| **Error rate** | % of tool calls that fail | > 10% |
| **Context window usage** | How full is the context? | > 80% capacity |

## Observability: Seeing Inside the Agent

### What to Log

Every agent interaction should produce an audit trail:

```json
{
  "turn_id": "turn-42",
  "timestamp": "2026-02-23T10:00:00Z",
  "input": "User asked to add a login endpoint",
  "llm_call": {
    "model": "claude-sonnet-4-5",
    "input_tokens": 45000,
    "output_tokens": 2100,
    "latency_ms": 8500,
    "cost_usd": 0.017
  },
  "decision": "call tool: view_file",
  "tool_call": {
    "name": "view_file",
    "params": {"path": "server.py"},
    "result_size": 3200,
    "duration_ms": 120,
    "success": true
  }
}
```

### Trace Visualization

A good observability system shows the full trace of an agent task:

```
Task: "Add login endpoint"
├── Turn 1: LLM call (8.5s, 47K tokens)
│   └── Tool: view_file("server.py") → 120ms, success
├── Turn 2: LLM call (6.2s, 49K tokens)
│   └── Tool: search_replace("server.py", ...) → 45ms, success
├── Turn 3: LLM call (4.1s, 50K tokens)
│   └── Tool: execute_bash("curl /api/login") → 350ms, success
└── Turn 4: LLM call (3.0s, 51K tokens)
    └── Response: "Login endpoint added successfully"

Total: 4 turns, 21.8s LLM time, 515ms tool time, $0.06
```

## Evaluation Approaches

### 1. Human Evaluation (Gold Standard)

Have humans judge agent outputs:

| Criterion | Scale | Question |
|-----------|-------|----------|
| **Correctness** | 1-5 | Did the agent produce the right result? |
| **Completeness** | 1-5 | Did it handle all requirements? |
| **Efficiency** | 1-5 | Did it take a reasonable number of steps? |
| **Code quality** | 1-5 | Is the generated code clean and maintainable? |

**Pros:** Most accurate. **Cons:** Expensive, slow, doesn't scale.

### 2. Automated Test Suites

Write tests that verify agent behavior:

```python
def test_agent_creates_api():
    result = agent.run("Create a /health endpoint")
    # Check that the file was created
    assert file_exists("server.py")
    # Check that the endpoint works
    response = requests.get("http://localhost:8000/health")
    assert response.status_code == 200
```

**Pros:** Fast, repeatable, scalable. **Cons:** Only catches specific known issues.

### 3. LLM-as-Judge

Use another LLM to evaluate the agent's output:

```python
evaluation = await judge_llm.evaluate(
    task="Add a login endpoint",
    agent_output=result,
    criteria=["correctness", "security", "code_quality"]
)
# Returns: {"correctness": 4, "security": 3, "code_quality": 4, "feedback": "Missing rate limiting"}
```

**Pros:** Scalable, nuanced. **Cons:** Judge LLM can be wrong too.

## Common Evaluation Pitfalls

| Pitfall | Problem | Fix |
|---------|---------|-----|
| **Only measuring completion** | Agent "completes" tasks but output is wrong | Add accuracy and quality metrics |
| **No baseline** | Don't know if agent is getting better or worse | Track metrics over time |
| **Testing on easy cases** | Agent looks great on simple tasks but fails on real ones | Include hard, edge-case scenarios |
| **Ignoring cost** | Agent works but uses 100x more tokens than needed | Track cost per task |
| **Not testing failure recovery** | Agent works on first try but can't handle errors | Deliberately introduce failures |

## Building an Evaluation Pipeline

```mermaid
flowchart LR
    TASKS[Test Tasks] --> AGENT[Run Agent]
    AGENT --> RESULTS[Collect Results]
    RESULTS --> AUTO[Automated Checks]
    RESULTS --> HUMAN[Human Review<br/>Sample]
    RESULTS --> LLM_J[LLM Judge]
    AUTO --> METRICS[Metrics Dashboard]
    HUMAN --> METRICS
    LLM_J --> METRICS
```

A production evaluation pipeline combines all three approaches: automated tests for known behaviors, LLM judge for quality scoring, and periodic human review for calibration.
""", tags=["core-concepts", "evaluation", "observability"])

# ============================================================
# 4. Fine-Tuning vs Prompting vs RAG
# ============================================================
create_doc("Fine-Tuning vs Prompting vs RAG", SUB_COMPARISONS, """# Fine-Tuning vs Prompting vs RAG

Three ways to customize LLM behavior — each with different strengths, costs, and use cases. Choosing the right one (or combination) is a critical architectural decision.

## Quick Comparison

| Approach | What Changes | Cost | Latency Impact | Best For |
|----------|-------------|------|---------------|----------|
| **Prompting** | The input text sent to the model | Free (just tokens) | None | Behavior control, formatting, examples |
| **RAG** | External knowledge added to the prompt | Medium (embedding + search infra) | +100-500ms (retrieval) | Private data, current information |
| **Fine-Tuning** | The model's weights | High ($100-$10,000+) | None (faster inference) | Consistent style, specialized domains |

## Prompting (System Prompt Engineering)

**What it is:** Crafting instructions that steer the model's behavior without changing the model itself.

```
System prompt: "You are a Python expert. Always use type hints.
Follow PEP 8. Prefer f-strings over .format()."

→ The same model now generates Python-specific, styled code
```

**When to use:**
- You want to control output format, tone, or style
- You need the model to follow specific rules
- You have a small number of examples to demonstrate desired behavior

**Limitations:**
- Eats into the context window (system prompt = fewer tokens for conversation)
- Model may not follow instructions consistently on complex rules
- Can't teach the model genuinely new knowledge

## RAG (Retrieval Augmented Generation)

**What it is:** Retrieving relevant documents from a knowledge base and including them in the prompt before the LLM generates a response.

```
User: "What's our refund policy?"
→ Retrieve: [refund_policy.md chunk]
→ Prompt: "Using this context: [policy text]. Answer: What's our refund policy?"
→ LLM generates answer grounded in the actual policy
```

**When to use:**
- The model needs access to private or current data
- Knowledge changes frequently (product catalogs, docs, policies)
- You need citations and source attribution
- You have a large knowledge base (too big to fit in a prompt)

**Limitations:**
- Adds latency (embedding + vector search + retrieval)
- Retrieved chunks may not contain the answer
- Quality depends heavily on chunking strategy and embedding model

## Fine-Tuning

**What it is:** Training the model's weights on your specific data, creating a specialized version of the model.

```
Training data:
{"input": "Convert to SQL: show all users", "output": "SELECT * FROM users;"}
{"input": "Convert to SQL: count orders by month", "output": "SELECT DATE_TRUNC('month', created_at)..."}
× 1000 examples

→ The model learns your specific SQL dialect, table names, and conventions
```

**When to use:**
- You need consistent style/format across thousands of outputs
- The task is specialized (medical coding, legal analysis, custom SQL)
- You want to reduce prompt length (fine-tuned model needs fewer instructions)
- Latency is critical (fine-tuned model is faster than long prompts)

**Limitations:**
- Expensive to train and maintain
- Needs high-quality training data (hundreds to thousands of examples)
- Model can "forget" general knowledge (catastrophic forgetting)
- Must retrain when requirements change

## Decision Framework

```mermaid
flowchart TD
    START[What do you need?] --> Q1{Need private/current data?}
    Q1 -->|Yes| RAG[Use RAG]
    Q1 -->|No| Q2{Need consistent specialized style?}
    Q2 -->|Yes| Q3{Have 500+ training examples?}
    Q3 -->|Yes| FT[Fine-Tune]
    Q3 -->|No| PROMPT[Use Prompting]
    Q2 -->|No| PROMPT
```

## Combining Approaches

The best systems often use all three together:

| Layer | Approach | Purpose |
|-------|----------|---------|
| **Base** | Fine-tuned model | Specialized domain knowledge, consistent style |
| **Context** | RAG | Current data, user-specific information |
| **Instructions** | System prompt | Task-specific rules, output format |

Example: A medical coding agent might use:
1. **Fine-tuned model** trained on ICD-10 codes
2. **RAG** to retrieve the latest coding guidelines
3. **System prompt** with specific output format requirements

## Cost Comparison

| Approach | Upfront Cost | Per-Query Cost | Maintenance |
|----------|-------------|---------------|-------------|
| **Prompting** | $0 | Token cost for prompt | Update prompt text |
| **RAG** | Embedding infrastructure | Token cost + retrieval overhead | Re-index when data changes |
| **Fine-Tuning** | $100-$10,000+ training | Lower token cost (shorter prompts) | Retrain when requirements change |

## Common Mistakes

| Mistake | Problem | Better Approach |
|---------|---------|----------------|
| Fine-tuning when prompting would work | Expensive, slow iteration | Try prompting first — it's free |
| RAG with bad chunking | Retrieves irrelevant content | Test chunking strategies, use overlap |
| Not combining approaches | Relies on one technique for everything | Layer them: fine-tune + RAG + prompt |
| Fine-tuning on small data | Model overfits or barely changes | Need 500+ high-quality examples minimum |
| RAG without evaluation | Don't know if retrieved context helps | Measure answer quality with and without RAG |
""", order=2, tags=["comparison", "architecture", "rag"])

# ============================================================
# 5. Cost Optimization Strategies
# ============================================================
SUB_COST = create_cat("Cost Optimization", "Sparkles", 3, CAT_TUTORIALS)

create_doc("Cost Optimization for AI Agents", SUB_COST, """# Cost Optimization for AI Agents

AI agents can be expensive — every LLM call, every tool execution, every token costs money. This guide covers practical strategies to reduce costs without sacrificing quality.

## Where the Money Goes

| Cost Center | % of Total | What Drives It |
|------------|-----------|---------------|
| **LLM API calls** | 70-90% | Token count × price per token |
| **Embedding calls** | 5-15% | RAG indexing and search |
| **Compute** | 5-10% | Container runtime, tool execution |
| **Storage** | 1-5% | Database, file storage |

LLM calls dominate. Optimizing token usage is the highest-leverage action.

## Strategy 1: Model Routing

Use cheap models for easy tasks, expensive models for hard ones:

```python
def choose_model(task_type):
    routing = {
        "classify": "gpt-4o-mini",      # Simple → cheap
        "summarize": "gpt-4o-mini",      # Simple → cheap
        "code_review": "claude-sonnet",   # Complex → powerful
        "architecture": "claude-sonnet",  # Complex → powerful
        "translate": "gemini-flash",      # Fast → cheap
    }
    return routing.get(task_type, "gpt-4o")  # Default → balanced
```

**Impact:** 50-80% cost reduction compared to using a premium model for everything.

## Strategy 2: Prompt Caching

Cache responses for identical or similar prompts:

```python
import hashlib

async def cached_call(prompt, model):
    cache_key = hashlib.sha256(f"{model}:{prompt}".encode()).hexdigest()
    
    cached = await db.cache.find_one({"key": cache_key}, {"_id": 0})
    if cached:
        return cached["response"]  # Free!
    
    response = await llm.chat(model=model, messages=[{"role": "user", "content": prompt}])
    await db.cache.insert_one({"key": cache_key, "response": response.content})
    return response.content
```

**Impact:** Eliminates redundant API calls entirely. Especially effective for repeated queries (e.g., classifying similar inputs).

## Strategy 3: Context Window Management

The biggest hidden cost: context grows with every turn.

```
Turn 1:  System prompt (15K) + User message (100) = 15,100 tokens
Turn 5:  System prompt (15K) + History (10K) + Message (100) = 25,100 tokens
Turn 15: System prompt (15K) + History (40K) + Message (100) = 55,100 tokens
Turn 30: System prompt (15K) + History (100K) + Message (100) = 115,100 tokens
```

**Strategies:**
- **Summarize old messages** — compress early conversation into a summary
- **Drop irrelevant tool results** — don't carry large file contents forever
- **Start new sessions** for unrelated tasks — reset the context
- **Use retrieval** instead of full history — only include relevant past turns

## Strategy 4: Efficient Tool Use

Each tool call triggers another LLM call. Fewer tool calls = fewer LLM calls.

| Inefficient | Efficient |
|-------------|-----------|
| Read file A → LLM → Read file B → LLM → Read file C | Read files A, B, C in parallel → single LLM call |
| Create files one at a time (5 LLM calls) | Create all files in parallel (1 LLM call) |
| Check logs → LLM → check more logs → LLM | Read all relevant logs at once |

**Impact:** Parallelizing 5 sequential reads into 1 parallel read saves 4 LLM round-trips.

## Strategy 5: Shorter System Prompts

Every token in the system prompt is sent with EVERY API call:

```
15,000 token prompt × 30 turns = 450,000 input tokens just for the system prompt
10,000 token prompt × 30 turns = 300,000 input tokens

Savings: 150,000 tokens = significant cost reduction
```

**How:** Remove redundant instructions, use concise language, move rarely-needed rules to a retrieval system.

## Strategy 6: Output Length Control

Set `max_tokens` to limit response length:

```python
# For simple classification:
response = await llm.chat(messages=messages, max_tokens=50)

# For code generation:
response = await llm.chat(messages=messages, max_tokens=2000)

# Don't use max_tokens=64000 for a yes/no question
```

## Cost Monitoring

Track costs in real-time to catch runaway spending:

```python
async def tracked_call(messages, model):
    response = await llm.chat(model=model, messages=messages)
    
    cost = calculate_cost(model, response.usage)
    await db.usage.insert_one({
        "model": model,
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
        "cost": cost,
        "timestamp": datetime.now(timezone.utc).isoformat()
    })
    
    # Alert if session cost exceeds threshold
    session_total = await get_session_cost(session_id)
    if session_total > BUDGET_LIMIT:
        raise BudgetExceededError("Session budget exceeded")
    
    return response
```

## Quick Reference: Optimization Checklist

| Strategy | Effort | Impact | Priority |
|----------|--------|--------|----------|
| Model routing | Low | 50-80% savings | Do first |
| Prompt caching | Low | Varies (high for repeated queries) | Do first |
| Parallel tool calls | Low | 30-50% fewer LLM calls | Do first |
| Context management | Medium | 20-40% savings on long sessions | Do second |
| Shorter system prompt | Medium | 10-20% savings | Do second |
| Output length control | Low | 5-15% savings | Easy win |
| Budget monitoring | Medium | Prevents runaway costs | Essential |
""", tags=["tutorial", "cost-optimization"])

# ============================================================
# 6. Real-World Agent Examples
# ============================================================
SUB_EXAMPLES = create_cat("Real-World Examples", "Telescope", 4, CAT_TUTORIALS)

create_doc("Real-World AI Agents: Case Studies", SUB_EXAMPLES, """# Real-World AI Agents: Case Studies

A survey of production AI agents — how they work, what patterns they use, and what we can learn from each.

## Coding Agents

### Devin (Cognition)

**What it is:** An autonomous software engineering agent that can handle entire development tasks end-to-end.

| Aspect | Detail |
|--------|--------|
| **Architecture** | Orchestrator with full dev environment (terminal, browser, editor) |
| **Key pattern** | Plan-and-Execute with long-horizon planning |
| **Unique feature** | Can work on tasks for hours autonomously |
| **Tools** | Terminal, browser, code editor, git |
| **LLM** | Proprietary fine-tuned model |

**Key insight:** Devin's strength is persistence — it can work through complex multi-step tasks without human intervention, retrying and adapting its approach.

### Cursor Agent Mode

**What it is:** An AI coding assistant integrated into a code editor (VS Code fork) that can make multi-file changes.

| Aspect | Detail |
|--------|--------|
| **Architecture** | Editor-integrated agent with file system access |
| **Key pattern** | ReAct with codebase-aware context |
| **Unique feature** | Indexes entire codebase for context-aware suggestions |
| **Tools** | File read/write, terminal, codebase search |
| **LLM** | Multiple models (Claude, GPT) — user selects |

**Key insight:** Cursor's codebase indexing lets it understand your project structure, making tool choices more accurate than agents that start blind.

### Claude Code (Anthropic)

**What it is:** A terminal-based AI coding agent that operates directly in your development environment.

| Aspect | Detail |
|--------|--------|
| **Architecture** | Terminal agent with direct filesystem access |
| **Key pattern** | ReAct with permission-gated tool use |
| **Unique feature** | Runs locally in your terminal, sees your actual project |
| **Tools** | File ops, bash, browser (via MCP), git |
| **LLM** | Claude models |

**Key insight:** Claude Code's permission system (ask before destructive actions) is a practical implementation of the human-in-the-loop safety pattern.

### GitHub Copilot Workspace

**What it is:** An agent that can plan and implement changes across a GitHub repository.

| Aspect | Detail |
|--------|--------|
| **Architecture** | Cloud-based agent operating on GitHub repos |
| **Key pattern** | Plan-and-Execute with human approval gates |
| **Unique feature** | Starts from a GitHub issue, generates a plan, implements across files |
| **Tools** | GitHub API, file operations, CI/CD integration |
| **LLM** | GPT models |

**Key insight:** Starting from a structured issue (not free-form chat) gives the agent a clearer task definition, improving plan quality.

## Research Agents

### Perplexity

**What it is:** A search engine powered by AI agents that research and synthesize information from multiple sources.

| Aspect | Detail |
|--------|--------|
| **Architecture** | Search + RAG + synthesis agent |
| **Key pattern** | Retrieve → Read → Synthesize → Cite |
| **Unique feature** | Real-time web search with source citations |
| **Tools** | Web search, page reading, knowledge retrieval |

**Key insight:** Perplexity's citation system solves the hallucination trust problem — every claim is linked to a source the user can verify.

### GPT Researcher

**What it is:** An open-source agent that conducts multi-step research on any topic.

| Aspect | Detail |
|--------|--------|
| **Architecture** | Multi-agent: Planner → Searcher → Reviewer → Writer |
| **Key pattern** | Plan-and-Execute with multiple specialized sub-agents |
| **Unique feature** | Generates comprehensive research reports with sources |

**Key insight:** Separating research planning from execution lets each agent focus on what it does best.

## Patterns Across All Agents

| Pattern | Who Uses It | Why |
|---------|------------|-----|
| **ReAct loop** | All of them | Fundamental think-act-observe cycle |
| **Tool sandboxing** | Devin, Claude Code | Safety — limit what agents can do |
| **Human approval gates** | Copilot Workspace, Claude Code | Trust — human confirms before destructive actions |
| **Codebase indexing** | Cursor | Context — understand the project before acting |
| **Specialized sub-agents** | GPT Researcher | Efficiency — divide and conquer |
| **Plan before execute** | Devin, Copilot Workspace | Quality — think first, act second |

## Lessons for Building Your Own Agent

| Lesson | Source | Takeaway |
|--------|--------|----------|
| Let agents retry and adapt | Devin | Don't give up after one failure — implement retry with different approaches |
| Index the codebase | Cursor | Context-aware agents make better tool choices |
| Gate destructive actions | Claude Code | Ask before deleting, deploying, or overwriting |
| Start from structured input | Copilot Workspace | Structured task descriptions beat free-form chat |
| Cite sources | Perplexity | Transparency builds trust — show where information comes from |
| Separate planning from execution | GPT Researcher | Plan quality improves when it's a dedicated step |
""", tags=["case-studies", "architecture"])

# ============================================================
# 7. Ethical Considerations (bonus doc under Safety)
# ============================================================
SUB_SAFETY = db.categories.find_one({"name": "Safety & Guardrails"})['id']

create_doc("Ethical Considerations for AI Agents", SUB_SAFETY, """# Ethical Considerations for AI Agents

AI agents that can take real-world actions raise ethical questions that go beyond traditional LLM safety. This document covers the key considerations for anyone building or deploying agents.

## The Autonomy Spectrum

| Level | Description | Human Involvement | Example |
|-------|------------|-------------------|---------|
| **1. Advisory** | Agent suggests, human decides and acts | Every action | Code completion suggestions |
| **2. Supervised** | Agent acts, human approves first | Critical actions | PR review before merge |
| **3. Semi-autonomous** | Agent acts freely within bounds, escalates edge cases | Exceptions only | Coding agent with sandboxed environment |
| **4. Autonomous** | Agent acts independently for extended periods | Minimal | Long-running research agents |

Most production agents today operate at level 2-3. The higher the autonomy, the more critical the safety guardrails.

## Key Ethical Concerns

### 1. Accountability

When an agent introduces a security vulnerability, who is responsible?

| Stakeholder | Argument |
|------------|----------|
| **The user** | They approved the agent's output |
| **The platform** | They built and deployed the agent |
| **The LLM provider** | The model generated the vulnerable code |
| **Nobody** | It's a novel situation without clear precedent |

**Current practice:** Most platforms include terms stating the user is responsible for reviewing and deploying agent output. But this creates tension — if the agent is sold as "autonomous," users may not review carefully.

### 2. Transparency

Users should understand:
- When they're interacting with an AI (not a human)
- What actions the agent can take
- What data the agent can access
- How decisions are being made

**Implementation:** Audit logs, visible tool calls, clear agent identification in UI.

### 3. Bias in Agent Decisions

Agents inherit biases from their training data and system prompts:

| Bias Source | Example | Mitigation |
|------------|---------|-----------|
| **Training data** | Model defaults to patterns from majority of training data | Diverse training data, bias testing |
| **System prompt** | Prompt favors certain technologies or approaches | Review prompts for implicit biases |
| **Tool selection** | Agent always picks the same tool/approach | Encourage exploration in system prompt |

### 4. Data Privacy

Agents often need access to sensitive data to be useful:

| Risk | Scenario | Mitigation |
|------|----------|-----------|
| **Data in prompts** | Code with API keys sent to LLM provider | Scrub secrets before sending to LLM |
| **Cross-user leakage** | Agent trained on one user's code helps another | Strict session isolation |
| **Tool access scope** | Agent reads files outside project directory | Sandbox file access to project root |

### 5. Environmental Impact

LLM inference consumes significant compute:

| Consideration | Detail |
|--------------|--------|
| **Energy per query** | A complex agent task can require 10-50+ LLM calls |
| **Carbon footprint** | Depends on data center power source |
| **Scaling impact** | Millions of agent queries daily = significant energy |

**Mitigation:** Model routing (use efficient models when possible), caching, and avoiding unnecessary LLM calls.

## Building Ethically

### Principle 1: Minimal Authority
Give the agent only the permissions it needs. A code review agent doesn't need write access. A search agent doesn't need file system access.

### Principle 2: Transparent Operation
Every agent action should be visible and auditable. Users should be able to understand why the agent did what it did.

### Principle 3: Human Override
Humans should always be able to stop, correct, or reverse agent actions. Rollback capability is not optional.

### Principle 4: Fail Safe
When in doubt, the agent should ask rather than guess. A wrong action is worse than a delayed action.

### Principle 5: Honest Limitations
Agents should communicate what they can't do, not attempt tasks beyond their capability. "I'm not sure about this — please verify" is better than a confident wrong answer.
""", order=2, tags=["ethics", "safety"])

# Final count
internal_cats = set(c['id'] for c in db.categories.find({'internal': True}, {'_id': 0, 'id': 1}))
total = db.documents.count_documents({'deleted': {'$ne': True}, 'category_id': {'$nin': list(internal_cats)}})
print(f"\n=== Batch 2 Complete ===")
print(f"Total public documents: {total}")
