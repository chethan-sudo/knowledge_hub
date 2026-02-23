"""Complete E1/Emergent reference removal - ALL documents
Replace with generic AI agent terminology"""

from pymongo import MongoClient
from datetime import datetime, timezone

client = MongoClient('mongodb://localhost:27017')
db = client['test_database']
NOW = datetime.now(timezone.utc).isoformat()

def fix(title, replacements):
    doc = db.documents.find_one({'title': title}, {'_id': 0, 'content': 1})
    if not doc:
        print(f"NOT FOUND: {title}")
        return
    content = doc['content']
    for old, new in replacements:
        content = content.replace(old, new)
    remaining_e1 = content.count('E1')
    remaining_em = content.count('Emergent')
    db.documents.update_one({'title': title}, {'$set': {'content': content, 'updated_at': NOW}})
    status = "CLEAN" if remaining_e1 == 0 and remaining_em == 0 else f"REMAINING E1:{remaining_e1} Emergent:{remaining_em}"
    print(f"  {title}: {status}")

def rename_and_fix(old_title, new_title, replacements):
    doc = db.documents.find_one({'title': old_title}, {'_id': 0, 'content': 1})
    if not doc:
        print(f"NOT FOUND: {old_title}")
        return
    content = doc['content']
    for old, new in replacements:
        content = content.replace(old, new)
    remaining_e1 = content.count('E1')
    remaining_em = content.count('Emergent')
    db.documents.update_one({'title': old_title}, {'$set': {'title': new_title, 'content': content, 'updated_at': NOW}})
    status = "CLEAN" if remaining_e1 == 0 and remaining_em == 0 else f"REMAINING E1:{remaining_e1} Emergent:{remaining_em}"
    print(f"  {old_title} -> {new_title}: {status}")

print("=== Fixing System Architecture Overview ===")
fix("System Architecture Overview", [
    ("A complete map of how the Emergent platform works", "A complete map of how an AI agent platform works"),
    ("E1 Orchestrator", "Agent Orchestrator"),
    ("E1[E1 (The Orchestrator)]", "ORCH[Agent Orchestrator]"),
    ("AS -->|route + store| E1[", "AS -->|route + store| ORCH["),
    ("E1 -->|reason|", "ORCH -->|reason|"),
    ("E1 -->|tools|", "ORCH -->|tools|"),
    ("E1 -->|delegate|", "ORCH -->|delegate|"),
    ("E1 -->|decides|", "ORCH -->|decides|"),
    ("DEC -->|continue| E1", "DEC -->|continue| ORCH"),
    ("POD -->|result| E1", "POD -->|result| ORCH"),
    ("SALLM -->|result| E1", "SALLM -->|result| ORCH"),
    ("E1_INST[E1 Instance]", "AGENT_INST[Agent Instance]"),
    ("AGENTSVC --> E1_INST", "AGENTSVC --> AGENT_INST"),
    ("E1_INST --> LLM_PROXY", "AGENT_INST --> LLM_PROXY"),
    ("E1_INST --> FS", "AGENT_INST --> FS"),
    ("E1_INST --> GIT", "AGENT_INST --> GIT"),
    ("in the Emergent chat interface", "in the chat interface"),
    ("the E1 Orchestrator instance", "the Agent Orchestrator instance"),
    ("E1 Orchestrator processes the message.** E1 is NOT an LLM — it is a software system. It takes", "Agent Orchestrator processes the message.** The orchestrator is NOT an LLM — it is a software system. It takes"),
    ("passes the response back to E1", "passes the response back to the orchestrator"),
    ("E1's Decision Layer parses the response.** If the LLM output contains tool calls → E1 sends them", "The orchestrator's decision layer parses the response.** If the LLM output contains tool calls → it sends them"),
    ("a subagent request → E1 delegates", "a subagent request → the orchestrator delegates"),
    ("If the output is a final answer → E1 formats", "If the output is a final answer → the orchestrator formats"),
    ("results + git diff back to E1", "results + git diff back to the orchestrator"),
    ("E1 decides: continue or done?** After processing tool results or subagent output, E1 decides", "The orchestrator decides: continue or done?** After processing tool results or subagent output, the orchestrator decides"),
    ("The user sees E1's explanation", "The user sees the agent's explanation"),
    ("E1 Orchestrator** | AI agent NOT an LLM", "Agent Orchestrator** | AI agent — NOT an LLM"),
    ("the Emergent platform", "the platform"),
    ("This diagram shows the SIX distinct layers in the Emergent platform", "This diagram shows the SIX distinct layers in the platform"),
    ("navigates to the Emergent platform", "navigates to the platform"),
    ("Agent Service → E1 Instance:** The Agent Service routes the user's message to the E1 Instance assigned to this job. One E1 instance per active job. E1 receives the message",
     "Agent Service → Agent Instance:** The Agent Service routes the user's message to the agent instance assigned to this job. One instance per active job. The orchestrator receives the message"),
    ("E1 Instance → LLM Proxy → External Providers:** When E1 needs to reason", 
     "Agent Instance → LLM Proxy → External Providers:** When the orchestrator needs to reason"),
    ("E1 Instance → Pod Filesystem + Git:** When E1 executes tools", "Agent Instance → Pod Filesystem + Git:** When the orchestrator executes tools"),
    ("This is the development conversation with E1", "This is the development conversation with the agent"),
    ("The app can serve traffic while E1 is simultaneously modifying its code", "The app can serve traffic while the agent is simultaneously modifying its code"),
    ("Every single action E1 takes is logged. If E1 reads a file", "Every single action the agent takes is logged. If the agent reads a file"),
    ("If E1 calls bash", "If the agent calls bash"),
    ("If it sends a message to the LLM, that", "If the agent sends a message to the LLM, that"),
    ("E1 can read and write environment variables", "The agent can read and write environment variables"),
    ("When E1 Delegates To It", "When the Orchestrator Delegates"),
    ("When E1 is stuck in an error loop", "When the orchestrator is stuck in an error loop"),
    ("about Emergent features, billing, GitHub integration", "about platform features, billing, GitHub integration"),
    ("Real time chat between user and E1", "Real time chat between user and agent"),
    ("E1 operates in a continuous loop", "The orchestrator operates in a continuous loop"),
    ("E1 is the orchestrator not an LLM.** It uses an LLM as its reasoning engine but E1 itself is the decision-making agent layer",
     "The orchestrator is not an LLM.** It uses an LLM as its reasoning engine but the orchestrator itself is the decision-making agent layer"),
    ("They have no memory of previous calls. E1 provides full context", "They have no memory of previous calls. The orchestrator provides full context"),
])

print("\n=== Fixing What Is E1? ===")
rename_and_fix("What Is E1?", "What Is an AI Agent Orchestrator?", [
    ("# What Is E1?", "# What Is an AI Agent Orchestrator?"),
    ("E1 is **not an LLM**. E1 is an **AI Agent** — a software orchestration system built by Emergent Labs that uses an LLM as one of its components.",
     "An AI Agent Orchestrator is **not an LLM**. It is a **software orchestration system** that uses an LLM as one of its components."),
    ("## E1 vs an LLM", "## Orchestrator vs an LLM"),
    ("E1 is the **orchestration layer**", "The orchestrator is the **orchestration layer**"),
    ('subgraph E1["E1 (The Orchestrator)"]', 'subgraph ORCH["Agent Orchestrator"]'),
    ("**Flow Explanation — What is inside E1:**", "**Flow Explanation — What is inside an AI Agent Orchestrator:**"),
    ("This diagram shows the internal architecture of E1 — it is NOT a single LLM but a multi-component software system",
     "This diagram shows the internal architecture of an agent orchestrator — it is NOT a single LLM but a multi-component software system"),
    ("governs E1's behavior", "governs the agent's behavior"),
    ("When E1 decides to act", "When the orchestrator decides to act"),
    ("E1 delegates to these when", "The orchestrator delegates to these when"),
    ("Why this architecture?** Because LLMs alone cannot act. They can only generate text. E1 wraps the LLM",
     "Why this architecture?** Because LLMs alone cannot act. They can only generate text. The orchestrator wraps the LLM"),
    ("| Capability | LLM (Claude/GPT) | E1 (The Agent) |", "| Capability | LLM (Claude/GPT) | Agent Orchestrator |"),
    ("## How E1 Makes Decisions", "## How the Orchestrator Makes Decisions"),
    ("E1 follows a structured decision-making process", "The orchestrator follows a structured decision-making process"),
    ("This diagram shows exactly how E1 decides", "This diagram shows how the orchestrator decides"),
    ("E1 calls ask_human to clarify", "the orchestrator calls ask_human to clarify"),
    ("about Emergent capabilities", "about platform capabilities"),
    ("E1 delegates to support_agent", "the orchestrator delegates to support_agent"),
    ("E1 follows a strict sequence", "the orchestrator follows a strict sequence"),
    ("E1 first reproduces the issue", "the orchestrator first reproduces the issue"),
    ("E1 reads the relevant files first", "the orchestrator reads the relevant files first"),
])

print("\n=== Fixing The Subagent System ===")
fix("The Subagent System", [
    ("E1 delegates work to", "the primary orchestrator delegates work to"),
    ("E1 spawns them", "the orchestrator spawns them"),
    ("E1[E1 Orchestrator]", "ORCH[Agent Orchestrator]"),
    ("E1 -->|", "ORCH -->|"),
    ("-->|report| E1", "-->|report| ORCH"),
    ("-->|guidelines| E1", "-->|guidelines| ORCH"),
    ("-->|playbook| E1", "-->|playbook| ORCH"),
    ("-->|fix| E1", "-->|fix| ORCH"),
    ("-->|answer| E1", "-->|answer| ORCH"),
    ("-->|status| E1", "-->|status| ORCH"),
    ("every subagent E1 can delegate to", "every subagent the orchestrator can delegate to"),
    ("When does E1 delegate?** E1 delegates", "When does the orchestrator delegate?** It delegates"),
    ("Called AFTER E1 implements features or fixes bugs. E1 sends",
     "Called AFTER the orchestrator implements features or fixes bugs. The orchestrator sends"),
    ("Called BEFORE building UI. E1 sends", "Called BEFORE building UI. The orchestrator sends"),
    ("Called after E1 fails to fix a bug", "Called after the orchestrator fails to fix a bug"),
    ("E1 passes the response directly to the user", "The orchestrator passes the response directly to the user"),
    ("E1 must package all relevant context", "The orchestrator must package all relevant context"),
    ("participant E1 as E1 Orchestrator", "participant ORCH as Agent Orchestrator"),
    ("E1->>AS:", "ORCH->>AS:"),
    ("AS->>E1:", "AS->>ORCH:"),
    ("E1->>E1:", "ORCH->>ORCH:"),
    ("when E1 delegates to a subagent", "when the orchestrator delegates to a subagent"),
    ("E1 packages context:** E1 creates", "The orchestrator packages context:** It creates"),
    ("E1 receives both", "The orchestrator receives both"),
    ("E1 processes results:** E1 reads the test report", "The orchestrator processes results:** It reads the test report"),
    ("subagent changed (via git diff), and decides next steps. If tests failed, E1 fixes the bugs",
     "subagent changed (via git diff), and decides next steps. If tests failed, the orchestrator fixes the bugs"),
    ("E1 provides full context each time", "the orchestrator provides full context each time"),
])

print("\n=== Fixing Tool Execution Engine ===")
fix("Tool Execution Engine", [
    ("Tools give E1 the ability", "Tools give the orchestrator the ability"),
    ("The LLM inside E1 can only generate text", "The LLM can only generate text"),
    ("E1[E1 decides to use a tool]", "ORCH[Orchestrator decides to use a tool]"),
    ("E1_2[E1 processes result]", "ORCH2[Orchestrator processes result]"),
    ("E1_2 -->|decides next| E1", "ORCH2 -->|decides next| ORCH"),
    ("how a tool call travels from E1's decision", "how a tool call travels from the orchestrator's decision"),
    ("E1 decides:** During the orchestration loop", "The orchestrator decides:** During the orchestration loop"),
    ("E1's decision layer", "The orchestrator's decision layer"),
    ("Results are fed back to E1", "Results are fed back to the orchestrator"),
    ("how E1 actually builds software. Each iteration — think, act, observe — gets E1 closer",
     "how the agent actually builds software. Each iteration — think, act, observe — gets it closer"),
    ("which tool operations E1 can safely run", "which tool operations can safely run"),
    ("If E1 needs to create 5 files", "If the agent needs to create 5 files"),
])

print("\n=== Fixing LLM Proxy Architecture ===")
fix("LLM Proxy Architecture", [
    ("in the Emergent platform", "in the platform"),
    ("between the E1 orchestrator", "between the agent orchestrator"),
    ("all requests route through the Emergent proxy", "all requests route through the proxy"),
    ("E1[E1 Orchestrator]", "ORCH[Agent Orchestrator]"),
    ("between all Emergent agents", "between all agents"),
    ("E1 Orchestrator:** The main agent", "Agent Orchestrator:** The main agent"),
    ("E1 doesn't get stuck", "the agent doesn't get stuck"),
    ("also called \"Emergent LLM Key\"", "also called the \"Universal LLM Key\""),
    ("E1 decides** to call an LLM", "The orchestrator decides** to call an LLM"),
    ("to E1 or subagent", "to the orchestrator or subagent"),
    ("participant E1 as E1 Orchestrator", "participant ORCH as Agent Orchestrator"),
    ("E1->>LP:", "ORCH->>LP:"),
    ("LP-->>E1:", "LP-->>ORCH:"),
    ("E1 sends request:** E1 makes", "The orchestrator sends request:** It makes"),
    ("so E1 doesn't have to wait", "so the agent doesn't have to wait"),
    ("E1 can start processing", "The agent can start processing"),
    ("return a clear error to E1", "return a clear error to the orchestrator"),
])

print("\n=== Fixing Essential Tools & Resources ===")
fix("Essential Tools & Resources", [
    ("used across the Emergent platform", "used across the platform"),
    ("## Emergent-Specific Libraries", "## Platform Libraries"),
])

print("\n=== Fixing Platform Limitations ===")
rename_and_fix("Platform Limitations", "AI Agent Platform Limitations", [
    ("# Emergent Platform Limitations", "# AI Agent Platform Limitations"),
    ("E1 compacts context automatically", "the agent compacts context automatically"),
    ("E1 uses web_search tool instead", "agents use a web_search tool instead"),
    ("E1 does not remember across separate sessions", "Agents do not remember across separate sessions"),
    ("E1 cannot click buttons or interact with GUI apps directly", "Agents cannot click buttons or interact with GUI apps directly"),
    ("**Emergent LLM Key**", "**Universal LLM Key**"),
    ("Emergent-managed Google Auth", "platform-managed Google Auth"),
    ("## What E1 Cannot Do", "## Common Agent Limitations"),
])

print("\n=== Fixing Complete UI Guide ===")
rename_and_fix("Complete UI Guide", "AI Agent Platform UI Guide", [
    ("# Emergent Platform UI Guide", "# AI Agent Platform UI Guide"),
    ("the Emergent development platform", "an AI agent development platform"),
    ("you communicate with E1", "you communicate with the agent"),
    ("you type instructions to E1", "you type instructions to the agent"),
    ("between you and E1", "between you and the agent"),
    ("E1 replies with text", "The agent replies with text"),
    ("when E1 is executing tools", "when the agent is executing tools"),
    ("E1 is processing your request", "the agent is processing your request"),
    ("for E1 to analyze", "for the agent to analyze"),
    ("E1 references these when explaining code", "The agent references these when explaining code"),
    ("E1 makes creates an automatic checkpoint", "the agent makes creates an automatic checkpoint"),
    ("Your Emergent LLM API key", "Your universal LLM API key"),
    ("through the Emergent proxy", "through the proxy"),
    ("sk-emergent-xxx", "sk-xxx"),
    ("E1 will use the integration playbook", "the agent uses the integration playbook"),
])

print("\n=== Fixing Frequently Asked Questions ===")
fix("Frequently Asked Questions", [
    ("from the Emergent team", "about AI agent architecture"),
    ("## How does E1 communicate with the LLM?", "## How does the agent communicate with the LLM?"),
    ("E1 does NOT chat with the LLM", "The agent does NOT chat with the LLM"),
    ("E1 sends the LLM three things", "The agent sends the LLM three things"),
    ("E1 then executes the tool", "The orchestrator then executes the tool"),
    ("## Who writes the code — E1 or the LLM?", "## Who generates the code — the agent or the LLM?"),
    ("E1 does NOT generate code. E1 decides what needs to be done (orchestration), then asks the LLM to generate the code.",
     "The orchestrator does NOT generate code. It decides what needs to be done, then asks the LLM to generate the code."),
    ("So E1 is the **decision maker**", "So the orchestrator is the **decision maker**"),
    ("guided by **E1's system prompt**", "guided by **the system prompt**"),
    ("## If there's an edit, does E1 send the whole code to the LLM?", "## For edits, does the agent send the whole file to the LLM?"),
    ("**No.** E1 sends:", "**No.** The agent sends:"),
    ("sk-emergent-xxx", "sk-xxx"),
    ("through Emergent's proxy", "through the platform's proxy"),
    ("When you ask E1 to integrate", "When you ask the agent to integrate"),
    ("E1 calls the **Integration Playbook Expert** subagent", "The orchestrator calls the **Integration Playbook Expert** subagent"),
    ("E1 asks you for the required API keys", "The orchestrator asks you for the required API keys"),
    ("E1 implements the code exactly", "The orchestrator implements the code exactly"),
    ("Every message between user and E1", "Every message between user and agent"),
    ("or E1's decision-making time", "or the agent's decision-making time"),
])

# Final check
print("\n=== FINAL VERIFICATION ===")
internal_cats = set(c['id'] for c in db.categories.find({'internal': True}, {'_id': 0, 'id': 1}))
docs = list(db.documents.find({'deleted': {'$ne': True}}, {'_id': 0, 'title': 1, 'content': 1, 'category_id': 1}))
problems = []
for d in docs:
    if d.get('category_id') in internal_cats:
        continue
    e1 = d['content'].count('E1')
    em = d['content'].count('Emergent')
    if e1 > 0 or em > 0:
        problems.append(f"  {d['title']:50} E1:{e1:>3}  Emergent:{em:>3}")

if problems:
    print("DOCUMENTS STILL WITH REFERENCES:")
    for p in problems:
        print(p)
else:
    print("ALL PUBLIC DOCUMENTS ARE CLEAN!")
