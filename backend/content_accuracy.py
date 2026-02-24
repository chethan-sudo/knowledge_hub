"""Deep accuracy pass - Frame architecture docs as reference architecture,
fix FAQ, fix UI Guide, fix Limitations, fix remaining docs"""

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
# 1. System Architecture Overview - add reference framing
# ============================================================
# Read current content and add framing
doc = db.documents.find_one({'title': 'System Architecture Overview'}, {'_id': 0, 'content': 1})
content = doc['content']
# Replace the opening line
content = content.replace(
    "A complete map of how an AI agent platform works — every component, every data flow, every service.",
    "A reference architecture for AI agent platforms — the components, data flows, and services that make up a production agent system. The specifics may vary across implementations, but this captures the common architectural patterns."
)
# Fix the DB schema section - frame as example
content = content.replace(
    "MongoDB stores ALL platform data:\n\n| Collection | Purpose | Key Fields |",
    "A typical agent platform stores data in collections like:\n\n| Collection (Example) | Purpose | Typical Fields |"
)
# Fix specific token count claim
content = content.replace("~15,000 tokens of rules", "thousands of tokens of rules")
content = content.replace("~15,000+ tokens", "thousands of tokens")
content = content.replace("~15,000 tokens", "thousands of tokens")
db.documents.update_one({'title': 'System Architecture Overview'}, {'$set': {'content': content, 'updated_at': NOW}})
print(f"UPDATED: System Architecture Overview ({len(content)} chars)")

# ============================================================
# 2. What Is an AI Agent Orchestrator - add reference framing
# ============================================================
doc = db.documents.find_one({'title': 'What Is an AI Agent Orchestrator?'}, {'_id': 0, 'content': 1})
content = doc['content']
content = content.replace(
    "An AI Agent Orchestrator is **not an LLM**. It is a **software orchestration system** that uses an LLM as one of its components. The distinction is critical.",
    "An AI Agent Orchestrator is **not an LLM**. It is a **software orchestration system** that uses an LLM as one of its components. The distinction is critical.\n\n> This document describes the general architecture pattern used by AI coding agents. Specific implementations vary, but the core concepts apply broadly."
)
content = content.replace("(~15,000+ tokens)", "(typically thousands of tokens)")
db.documents.update_one({'title': 'What Is an AI Agent Orchestrator?'}, {'$set': {'content': content, 'updated_at': NOW}})
print(f"UPDATED: What Is an AI Agent Orchestrator? ({len(content)} chars)")

# ============================================================
# 3. The Subagent System - add reference framing
# ============================================================
doc = db.documents.find_one({'title': 'The Subagent System'}, {'_id': 0, 'content': 1})
content = doc['content']
content = content.replace(
    "## What Are Subagents?\n\nSubagents are specialized AI agents",
    "## What Are Subagents?\n\n> This describes a common multi-agent architecture pattern. Specific tool names and workflows vary by platform.\n\nSubagents are specialized AI agents"
)
db.documents.update_one({'title': 'The Subagent System'}, {'$set': {'content': content, 'updated_at': NOW}})
print(f"UPDATED: The Subagent System ({len(content)} chars)")

# ============================================================
# 4. Tool Execution Engine - add reference framing
# ============================================================
doc = db.documents.find_one({'title': 'Tool Execution Engine'}, {'_id': 0, 'content': 1})
content = doc['content']
content = content.replace(
    "## What Are Tools?\n\nTools give the orchestrator",
    "## What Are Tools?\n\n> Tool names and capabilities described here represent common patterns across AI agent platforms.\n\nTools give the orchestrator"
)
db.documents.update_one({'title': 'Tool Execution Engine'}, {'$set': {'content': content, 'updated_at': NOW}})
print(f"UPDATED: Tool Execution Engine ({len(content)} chars)")

# ============================================================
# 5. LLM Proxy Architecture - add reference framing
# ============================================================
doc = db.documents.find_one({'title': 'LLM Proxy Architecture'}, {'_id': 0, 'content': 1})
content = doc['content']
content = content.replace(
    "The LLM Proxy is one of the most critical infrastructure components in the platform.",
    "The LLM Proxy is a common infrastructure pattern in AI agent platforms."
)
db.documents.update_one({'title': 'LLM Proxy Architecture'}, {'$set': {'content': content, 'updated_at': NOW}})
print(f"UPDATED: LLM Proxy Architecture ({len(content)} chars)")

# ============================================================
# 6. FAQ - rewrite to be general/accurate
# ============================================================
update_doc("Frequently Asked Questions", """# Frequently Asked Questions

Common questions about AI agent architecture, answered with technical detail.

## How does an agent communicate with the LLM?

The agent does NOT chat with the LLM the way you chat with ChatGPT. It uses **function calling / tool use** — a structured API mode.

The agent sends three things in every API call:

1. **System prompt** — thousands of tokens of rules, constraints, and workflow instructions
2. **Conversation history** — every previous message, tool call, and result from the session
3. **Tool definitions** — JSON schemas describing every available tool (name, parameters, description)

The LLM responds with either:
- **Text** — an explanation or answer for the user
- **Tool calls** — structured JSON specifying which tool to invoke and with what parameters

The orchestrator then executes the tool and feeds the result back to the LLM for the next decision.

## Who generates the code — the agent or the LLM?

**The LLM generates the code.** The orchestrator does NOT generate code itself. It decides what needs to be done, then asks the LLM to generate the code. The LLM outputs a tool call with the code as a parameter (e.g., `create_file` with the file content). The orchestrator's tool engine then executes that tool call to actually create the file.

So the orchestrator is the **decision maker** and the LLM is the **text/code generator**.

## How does the agent decide which tool to use?

**The LLM proposes it**, guided by **the system prompt**. The system prompt contains rules like:

- "Read files before editing them"
- "Use search_replace for existing files, create_file for new ones"
- "Run tests after implementing features"
- "Check logs before debugging"

These rules steer the LLM toward correct tool choices. The LLM outputs a structured tool call, and the orchestrator executes it.

## For edits, does the agent send the whole file to the LLM?

**No.** Typical approaches include:

- The relevant file content (read via a view_file tool)
- The user's request for the change
- Previous tool results showing the current state

The LLM then generates a targeted edit (e.g., a search-and-replace operation), not a rewrite of the entire file. This is both cheaper (fewer tokens) and safer (less chance of accidentally breaking unrelated code).

## What is a Universal LLM Key?

A single API key that works across multiple LLM providers through a proxy layer:

| Model Requested | Routed To |
|----------------|-----------|
| `gpt-4o`, `gpt-4o-mini` | OpenAI |
| `claude-sonnet-4-5`, `claude-haiku-4-5` | Anthropic |
| `gemini-3-flash`, `gemini-3-pro` | Google |

The proxy handles authentication, token counting, billing, and provider failover transparently.

## How does third-party integration work?

When integrating external services like Stripe, Twilio, or email APIs:

1. The orchestrator typically delegates to an **integration specialist subagent**
2. The subagent returns a verified playbook with exact code and setup steps
3. The orchestrator asks the user for required API keys
4. The orchestrator implements the integration following the playbook

This pattern exists because SDK versions and APIs change frequently — a specialized subagent can look up current documentation rather than relying on potentially outdated training data.

## What data does the platform store?

A typical AI agent platform stores:

| Data | Purpose |
|------|---------|
| **Conversation history** | Every message between user and agent |
| **Tool call logs** | Every tool invocation with parameters and results |
| **Token usage** | Input/output tokens per LLM call for billing |
| **Session metadata** | Which model was used, timestamps, status |
| **User data** | Account info, preferences, API keys |
| **Git history** | Automatic commits for rollback capability |

## What does "latency" mean in the debug panel?

Latency typically measures the time the LLM provider takes to generate a response:

| Latency | Interpretation |
|---------|---------------|
| 1,000 - 5,000 ms | Fast — small context, simple response |
| 5,000 - 15,000 ms | Normal — typical coding task |
| 15,000 - 30,000 ms | Expected for complex reasoning |
| 30,000 - 60,000 ms | Slow — very large context |
| > 60,000 ms | Possible provider issues |

This does NOT include tool execution time, network latency, or the agent's decision-making overhead. It only measures the LLM provider's response time.

## What is a system prompt?

The system prompt is the set of instructions that defines an agent's behavior. It typically includes:

| Section | What It Contains |
|---------|-----------------|
| Role definition | Who the agent is and what it specializes in |
| Environment info | Available tools, services, ports, URLs |
| Workflow rules | Step-by-step process for different task types |
| Constraints | What the agent must NOT do |
| Output format | How to structure responses |
| Examples | Concrete demonstrations of desired behavior |

The system prompt is sent with every LLM call. It's the same every time — it doesn't change between messages. This is why it appears repetitive in debug/observability tools.

## How does the agent handle long conversations?

As conversations grow, the total token count increases with every message. When approaching the LLM's context window limit:

1. **Context compaction** — older messages may be summarized to free up space
2. **Memory files** — critical decisions can be persisted to files (like PRD.md) that survive across sessions
3. **New session** — starting a fresh session with a handoff summary resets the context while preserving key information

The tradeoff: compaction preserves space but may lose details. That's why persisting important decisions to files is recommended for long projects.
""")

# ============================================================
# 7. AI Agent Platform UI Guide - generalize
# ============================================================
update_doc("AI Agent Platform UI Guide", """# AI Agent Platform UI Guide

A walkthrough of the typical UI elements in an AI agent development platform. While specific layouts vary across platforms, these are the common components.

## The Message Panel

The message panel is the primary interaction area — the central pane where you communicate with the agent.

| Element | Location | Purpose |
|---------|----------|---------|
| **Message input** | Bottom of panel | Text area where you type instructions. Enter to send, Shift+Enter for new line |
| **Message history** | Scrollable area above input | Full conversation between you and the agent |
| **Agent responses** | In message history | The agent replies with text, code blocks, and tool call results |
| **Tool call indicators** | Inline in responses | Shows when the agent is executing tools — displays tool name, status, and expandable output |
| **Thinking indicator** | Below last message | Shows the agent is processing your request |
| **Attachments** | Near message input | Upload images or files for the agent to analyze |

## The File Browser

| Element | Purpose |
|---------|---------|
| **File tree** | Shows all project files in a collapsible tree structure |
| **File viewer** | Click any file to view its contents with syntax highlighting |
| **Line numbers** | Left margin of editor — the agent references these when explaining code |
| **Diff indicators** | Shows which lines were added, modified, or deleted |

## The Preview Panel

| Element | Purpose |
|---------|---------|
| **Live preview** | Your running application rendered in an iframe |
| **Preview URL** | The URL where your app is accessible |
| **Refresh** | Reload the preview after changes |

## Version Control / Rollback

Every significant code change creates an automatic checkpoint (git commit). You can revert to any of these.

| Element | Purpose |
|---------|---------|
| **Checkpoint list** | Timeline of all auto-commits with descriptions |
| **Rollback button** | Revert the codebase to a selected checkpoint |
| **Diff view** | See what changed between checkpoints |

## Settings & Configuration

| Setting | Purpose |
|---------|---------|
| **Model selection** | Choose which LLM the agent uses (e.g., Claude, GPT, Gemini) |
| **API keys** | Configure keys for third-party services |
| **Universal LLM Key** | A single key that works across multiple LLM providers through a proxy |
| **Balance** | Your remaining token budget for LLM calls |

## Debug / Observability Panel

The debug panel shows the raw internals of every agent interaction:

| Element | What It Shows |
|---------|-------------|
| **LLM requests** | Full payload sent to the LLM (system prompt + messages + tools) |
| **LLM responses** | Raw response with tool calls and reasoning |
| **Token counts** | Input and output tokens per call |
| **Timing** | Duration of each LLM call and tool execution |
| **Tool results** | Output of every tool call (bash output, file contents, screenshots) |

## Keyboard Shortcuts (Common)

| Shortcut | Action |
|----------|--------|
| `Enter` | Send message |
| `Shift + Enter` | New line in message |
| `Ctrl/Cmd + K` | Focus search |
| `Escape` | Close panels/dialogs |

## Tips for Effective Use

| Tip | Why |
|-----|-----|
| Keep the preview panel open while developing | See changes in real-time |
| Use the debug panel when the agent makes unexpected decisions | Understand the reasoning |
| Check the file browser after complex changes | Verify all files look correct |
| Use rollback rather than asking the agent to undo | Faster and more reliable |
""")

# ============================================================
# 8. AI Agent Platform Limitations - generalize
# ============================================================
update_doc("AI Agent Platform Limitations", """# AI Agent Platform Limitations

An honest overview of current limitations in AI agent systems — constraints that apply broadly, not just to any specific platform.

## Context Window Limits

| Constraint | Detail |
|-----------|--------|
| **LLM context window** | Each LLM has a maximum token limit (e.g., 200K for Claude, 128K for GPT-4o, 1M for Gemini). Very long conversations may lose early context |
| **Context compaction** | When approaching limits, agents compact context automatically. Some details may be lost |
| **Workaround** | Use persistent files (like PRD.md) to store critical decisions that survive across sessions |

## Execution Constraints

| Constraint | Detail |
|-----------|--------|
| **Command timeout** | Long-running commands typically time out after 1-2 minutes. Background processes are needed for longer tasks |
| **File size** | Very large files (10K+ lines) may be truncated when viewed by the agent |
| **Package availability** | Some system packages may not be available in the container environment |
| **Port restrictions** | Only specific ports are exposed externally (typically frontend and backend ports) |

## LLM Limitations

| Constraint | Detail |
|-----------|--------|
| **Knowledge cutoff** | LLMs have training data cutoffs. They may not know about very recent libraries or APIs |
| **Hallucination risk** | LLMs can generate plausible but incorrect code. Always verify critical logic |
| **Non-deterministic** | Same prompt may produce different results each time |
| **No direct web browsing** | LLMs cannot browse the web. Agents use a web_search tool instead |
| **Token costs** | Every LLM call costs tokens. Complex tasks consume more budget |

## Agent Limitations

| Constraint | Detail |
|-----------|--------|
| **No persistent memory across sessions** | Agents do not remember previous sessions. Each starts fresh |
| **Single-task focus** | Agents work on one task at a time within a session |
| **Subagent isolation** | Subagents have no context from previous calls. Full context must be provided each time |
| **Limited GUI interaction** | Agents cannot click buttons or interact with GUIs directly — they use screenshot and automation tools |
| **Sequential bottleneck** | Some tool calls must be sequential even when parallelism would be faster |

## Infrastructure Limitations

| Constraint | Detail |
|-----------|--------|
| **Environment lifecycle** | Development environments may be recycled after inactivity. Unsaved work in temp directories is lost |
| **Database storage limits** | Storage is not unlimited — clean up unused data |
| **Preview URLs are temporary** | URLs change between sessions |
| **No custom domains** | Typically cannot attach custom domains to preview deployments |

## Integration Limitations

| Constraint | Detail |
|-----------|--------|
| **Universal LLM Key scope** | Universal keys typically only work for LLM text/image generation, not for third-party services like payment processors or email APIs |
| **OAuth** | Platform-managed OAuth may be limited to specific providers |
| **Third-party API keys** | Users must provide their own API keys for non-LLM services |
| **Webhook limitations** | Inbound webhooks require a stable URL, which preview environments don't provide |

## What AI Agents Generally Cannot Do

- Access private repositories or external databases without credentials
- Send emails or SMS without configured services
- Run GPU-intensive workloads (ML training, video rendering)
- Modify their own system prompt or tool definitions
- Access other users' environments or data
- Bypass rate limits or budget constraints
- Maintain state across completely separate sessions
""")

# ============================================================
# 9. Essential Tools & Resources - generalize
# ============================================================
update_doc("Essential Tools & Resources", """# Essential Tools & Resources

A curated list of tools, libraries, and resources commonly used in AI agent platforms and modern web development.

## Frontend Libraries

| Library | Purpose | Link |
|---------|---------|------|
| React | UI component framework | reactjs.org |
| Tailwind CSS | Utility-first CSS framework | tailwindcss.com |
| Shadcn/UI | Pre-built React components | ui.shadcn.com |
| Mermaid | Diagram rendering from text | mermaid.js.org |
| react-markdown | Markdown rendering in React | github.com/remarkjs/react-markdown |
| Lucide React | Icon library | lucide.dev |

## Backend Libraries

| Library | Purpose | Link |
|---------|---------|------|
| FastAPI | Modern Python web framework | fastapi.tiangolo.com |
| Motor | Async MongoDB driver for Python | motor.readthedocs.io |
| Pydantic | Data validation and serialization | docs.pydantic.dev |
| uvicorn | ASGI server for FastAPI | uvicorn.org |

## Database

| Tool | Purpose | Link |
|------|---------|------|
| MongoDB | Document database | mongodb.com |
| MongoDB Compass | GUI for MongoDB | mongodb.com/products/compass |
| Mongosh | MongoDB shell | mongodb.com/docs/mongodb-shell |

## AI / LLM Libraries

| Library | Purpose | Link |
|---------|---------|------|
| OpenAI SDK | GPT models API client | github.com/openai/openai-python |
| Anthropic SDK | Claude models API client | github.com/anthropics/anthropic-sdk-python |
| LangChain | LLM application framework | langchain.com |

## Testing & Quality

| Tool | Purpose | Link |
|------|---------|------|
| Playwright | Browser automation and testing | playwright.dev |
| pytest | Python testing framework | pytest.org |
| ESLint | JavaScript linter | eslint.org |
| Ruff | Fast Python linter | docs.astral.sh/ruff |

## DevOps

| Tool | Purpose | Link |
|------|---------|------|
| Docker | Container platform | docker.com |
| Kubernetes | Container orchestration | kubernetes.io |
| Supervisor | Process manager | supervisord.org |
| Nginx | Reverse proxy and web server | nginx.org |

## Documentation

| Resource | Purpose | Link |
|----------|---------|------|
| MDN Web Docs | Web technology reference | developer.mozilla.org |
| Python Docs | Python standard library reference | docs.python.org |
| Stack Overflow | Community Q&A | stackoverflow.com |
""")

print("\n=== Deep accuracy pass complete ===")
