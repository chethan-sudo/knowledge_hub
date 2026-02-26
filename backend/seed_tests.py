"""Add remaining quizzes + module tests + learning path tests"""
from pymongo import MongoClient
import uuid

client = MongoClient('mongodb://localhost:27017')
db = client['test_database']
def _id(): return str(uuid.uuid4())

# ============================================================
# 1. Remaining 3 document quizzes
# ============================================================
remaining = {
    "0e138d81-f79c-439d-a6af-b5c58f2f1a26": [  # FAQ
        {"id": _id(), "question": "Who generates the code in an AI agent system?", "options": ["The orchestrator", "The LLM generates it, the orchestrator executes it via tools", "The user", "The database"], "correct": 1, "explanation": "The LLM generates code as text. The orchestrator's tool layer executes it by creating files, running commands, etc."},
        {"id": _id(), "question": "What is sent with every LLM API call?", "options": ["Only the latest message", "System prompt + conversation history + tool definitions", "Just the system prompt", "A database query"], "correct": 1, "explanation": "Every call includes the full system prompt, all conversation history, and all tool definitions. This is why token usage grows each turn."},
    ],
    "e56b29d9-ce8b-42fa-b5f0-e64ea88167c2": [  # Glossary
        {"id": _id(), "question": "What is 'context compaction'?", "options": ["Compressing files", "Summarizing older messages to free up token space", "Deleting old conversations", "Reducing the model size"], "correct": 1, "explanation": "Context compaction summarizes older messages when approaching the LLM's token limit. Key information is preserved but details may be lost."},
        {"id": _id(), "question": "What is the difference between a Tool and a Subagent?", "options": ["They're the same", "A tool is a single action; a subagent is a specialist with its own LLM and tools", "Subagents are faster", "Tools are more expensive"], "correct": 1, "explanation": "A tool executes a single action (read file, run command). A subagent is an independent specialist with its own LLM, system prompt, and tools."},
    ],
    "21505408-c1ef-4a35-939d-50d65fdf1926": [  # UI Guide
        {"id": _id(), "question": "What is the purpose of the debug/observability panel?", "options": ["To write code", "To see raw LLM requests, tool calls, token usage, and timing", "To manage users", "To deploy the app"], "correct": 1, "explanation": "The debug panel shows the internals of every agent interaction — what was sent to the LLM, what tools were called, how many tokens were used."},
        {"id": _id(), "question": "Why use rollback instead of asking the agent to undo changes?", "options": ["It's more expensive", "It's faster and more reliable — reverts to an exact previous state", "The agent can't undo", "Rollback is automatic"], "correct": 1, "explanation": "Rollback reverts to an exact Git checkpoint. Asking the agent to undo is slower and may not perfectly reverse all changes."},
    ],
}

for doc_id, questions in remaining.items():
    db.quizzes.update_one({"document_id": doc_id}, {"$set": {"document_id": doc_id, "questions": questions}}, upsert=True)
print(f"Added quizzes for {len(remaining)} remaining documents")

# ============================================================
# 2. Module-level tests (per category final exams)
# ============================================================
module_tests = [
    {
        "id": _id(), "category_id": "ff182579-9490-422f-9d69-30ce642cf662",
        "title": "Getting Started — Final Test", "category_name": "Getting Started",
        "questions": [
            {"id": _id(), "question": "What is the fundamental loop every AI agent follows?", "options": ["Train → Deploy → Monitor", "Perceive → Think → Decide → Act → Observe", "Read → Write → Test", "Plan → Code → Ship"], "correct": 1, "explanation": "The universal agent loop: Perceive input → Think (LLM reasons) → Decide action → Act (execute tool) → Observe result → repeat."},
            {"id": _id(), "question": "What is the best way to report a bug to an AI agent?", "options": ["Say 'it's broken'", "Describe what you did, what happened, what you expected, and any error messages", "Send a screenshot only", "Restart the session"], "correct": 1, "explanation": "A complete bug report gives the agent enough context to investigate without guessing."},
            {"id": _id(), "question": "What does 'context window' mean?", "options": ["The browser window", "The maximum tokens an LLM can process in one request", "The visible part of the code", "The chat history display area"], "correct": 1, "explanation": "The context window is the LLM's token limit. Everything — system prompt, history, tools, your message — must fit within it."},
            {"id": _id(), "question": "What is the most productive pattern for working with an AI coding agent?", "options": ["Write detailed specs then wait", "Rapid iteration: describe → review → adjust → repeat", "Let it work completely autonomously", "Only use it for debugging"], "correct": 1, "explanation": "Rapid iteration (2-5 min cycles) is the most productive pattern. Describe, review, adjust, repeat."},
            {"id": _id(), "question": "What is a 'handoff summary'?", "options": ["A meeting agenda", "A structured document passed between sessions with context about completed work and decisions", "An error report", "A user manual"], "correct": 1, "explanation": "Handoff summaries preserve context across sessions — problem statement, completed work, pending issues, architecture decisions."},
        ]
    },
    {
        "id": _id(), "category_id": "a2a89675-2987-4313-b6a8-4690d7f330e3",
        "title": "Agent Anatomy — Final Test", "category_name": "Agent Anatomy",
        "questions": [
            {"id": _id(), "question": "In the ReAct pattern, what does the agent do between Thought and Observation?", "options": ["Sleeps", "Takes an Action (executes a tool)", "Asks the user", "Retrains the model"], "correct": 1, "explanation": "ReAct = Reasoning + Acting. The agent thinks (Thought), acts (executes a tool), then observes the result."},
            {"id": _id(), "question": "What is the most reliable form of long-term agent memory?", "options": ["Conversation history", "Persistent files (like PRD.md)", "The LLM's training data", "In-memory variables"], "correct": 1, "explanation": "Persistent files survive session restarts, context compaction, and agent upgrades."},
            {"id": _id(), "question": "What is prompt injection?", "options": ["Adding examples to a prompt", "Tricking the agent into ignoring its system prompt instructions", "Making prompts longer", "A debugging technique"], "correct": 1, "explanation": "Prompt injection tricks the agent into overriding its instructions, potentially causing unauthorized actions."},
            {"id": _id(), "question": "In the Orchestrator-Worker pattern, how do workers communicate?", "options": ["Workers talk to each other directly", "Workers only communicate through the orchestrator", "Workers share a database", "Workers use email"], "correct": 1, "explanation": "In Orchestrator-Worker (hub-and-spoke), workers never talk to each other. All communication goes through the orchestrator."},
            {"id": _id(), "question": "What is the 'blind retry' anti-pattern?", "options": ["Trying a different approach", "Repeating the exact same failed action expecting different results", "Asking for help", "Logging the error"], "correct": 1, "explanation": "Blind retry means not changing anything between attempts. Fix: max retry count + require a different approach after N failures."},
            {"id": _id(), "question": "Why should agents verify results after every action?", "options": ["To be slow", "To detect failures and adapt — the agent 'learns' from its own actions within a session", "It's required by the API", "For billing purposes"], "correct": 1, "explanation": "Verification catches errors immediately. Without it, the agent might build on a broken foundation."},
        ]
    },
    {
        "id": _id(), "category_id": "52c88f91-c6d7-401b-8b56-c29a8a639a56",
        "title": "LLM Internals — Final Test", "category_name": "LLM Internals",
        "questions": [
            {"id": _id(), "question": "What does self-attention allow in a transformer?", "options": ["Faster training", "Each token to consider every other token for context", "Smaller model size", "Fewer parameters"], "correct": 1, "explanation": "Self-attention lets 'bank' attend to 'river' or 'loan' to determine its meaning from context."},
            {"id": _id(), "question": "What is the difference between pre-training and fine-tuning?", "options": ["They're the same", "Pre-training teaches language from data; fine-tuning teaches behavior from instructions", "Fine-tuning is cheaper", "Pre-training is faster"], "correct": 1, "explanation": "Pre-training = next-token prediction on trillions of tokens (knowledge). Fine-tuning = instruction-response pairs (behavior)."},
            {"id": _id(), "question": "Why do output tokens cost more than input tokens?", "options": ["They're longer", "Generation requires a full forward pass per token — more compute", "They're stored differently", "Provider markup"], "correct": 1, "explanation": "Each output token requires a complete forward pass. Input processing can be batched, making it cheaper per token."},
            {"id": _id(), "question": "What does the LLM Proxy handle?", "options": ["Code generation", "Routing, auth, billing, rate limiting, and failover for all LLM calls", "File storage", "User management"], "correct": 1, "explanation": "The LLM Proxy is a centralized gateway that handles provider routing, Universal Key auth, token billing, rate limits, and automatic failover."},
            {"id": _id(), "question": "What is function calling in the context of LLMs?", "options": ["The LLM runs functions directly", "The LLM outputs structured JSON requesting a tool execution, which the agent then runs", "A programming technique", "Calling the LLM API"], "correct": 1, "explanation": "Function calling = the LLM generates structured tool call JSON. The agent's execution layer actually runs the function."},
        ]
    },
    {
        "id": _id(), "category_id": "a7aa2f11-d978-48e1-b5cd-2af037632309",
        "title": "Advanced Concepts — Final Test", "category_name": "Advanced Concepts",
        "questions": [
            {"id": _id(), "question": "When should you use RAG instead of fine-tuning?", "options": ["Always", "When you need access to private or frequently changing data", "When speed is critical", "When the model is too large"], "correct": 1, "explanation": "RAG is ideal for private data and frequently changing content. Fine-tuning is for consistent style/behavior changes."},
            {"id": _id(), "question": "What is MCP (Model Context Protocol)?", "options": ["A messaging app", "A standard protocol for how AI agents discover and use tools", "A database format", "A testing framework"], "correct": 1, "explanation": "MCP by Anthropic standardizes agent-tool interaction, making tools portable across frameworks."},
            {"id": _id(), "question": "Why are few-shot examples more effective than abstract rules in prompts?", "options": ["They're shorter", "LLMs pattern-match from concrete examples better than interpreting abstract rules", "They cost fewer tokens", "They're required"], "correct": 1, "explanation": "LLMs learn conventions from examples ('login-form-submit-button') better than from rules ('use descriptive kebab-case IDs')."},
            {"id": _id(), "question": "What is chunk overlap in RAG and why does it matter?", "options": ["It wastes space", "Facts at chunk boundaries would be lost without overlap between adjacent chunks", "It speeds up search", "It reduces costs"], "correct": 1, "explanation": "Without overlap, a fact split across two chunks might never be retrieved. 50-100 token overlap prevents this."},
        ]
    },
    {
        "id": _id(), "category_id": "f73c6407-fa1a-4887-89bf-b57a3f38269f",
        "title": "Tutorials — Final Test", "category_name": "Tutorials",
        "questions": [
            {"id": _id(), "question": "What is the highest-leverage cost optimization for AI agents?", "options": ["Shorter prompts", "Model routing — cheap models for easy tasks, expensive for hard ones", "Reducing output length", "Caching everything"], "correct": 1, "explanation": "Model routing can reduce costs 50-80%. Use GPT-4o-mini for classification, Claude Sonnet for complex code."},
            {"id": _id(), "question": "What should you always check FIRST when debugging a 500 error?", "options": ["The frontend code", "The error logs (tail backend.err.log)", "The database", "The network"], "correct": 1, "explanation": "Logs tell you the exact file, line, and error type. Always check logs before touching code."},
            {"id": _id(), "question": "When should you start with MongoDB over PostgreSQL?", "options": ["Never", "When prototyping and you need schema flexibility", "When you have complex JOINs", "When data integrity is critical"], "correct": 1, "explanation": "MongoDB's flexible schema means no migrations during rapid prototyping. Switch to PostgreSQL when you need strict constraints or complex JOINs."},
            {"id": _id(), "question": "What safety pattern does Claude Code implement?", "options": ["No safety", "Permission-gated tool use — asks before destructive actions", "Read-only mode only", "Full approval for everything"], "correct": 1, "explanation": "Claude Code asks before destructive actions (delete, deploy). This is a practical human-in-the-loop pattern."},
        ]
    },
]

# Insert module tests
db.module_tests.drop()
for mt in module_tests:
    db.module_tests.insert_one(mt)
print(f"Created {len(module_tests)} module tests")

# ============================================================
# 3. Learning path final tests
# ============================================================
paths = list(db.learning_paths.find({}, {'_id': 0}))
path_tests = []
for path in paths:
    # Gather questions from all docs in this path
    all_qs = []
    for step in path.get('steps', []):
        quiz = db.quizzes.find_one({'document_id': step['document_id']}, {'_id': 0})
        if quiz and quiz.get('questions'):
            # Take 1 question from each doc
            all_qs.append(quiz['questions'][0])
    if all_qs:
        path_tests.append({
            "id": _id(),
            "path_id": path['id'],
            "title": f"{path['title']} — Final Assessment",
            "questions": all_qs[:8]  # Max 8 questions per path test
        })

db.path_tests.drop()
for pt in path_tests:
    db.path_tests.insert_one(pt)
print(f"Created {len(path_tests)} learning path tests")

# Total quiz count
total_quizzes = db.quizzes.count_documents({})
total_questions = sum(len(q.get('questions', [])) for q in db.quizzes.find({}, {'_id': 0}))
total_module_qs = sum(len(m.get('questions', [])) for m in db.module_tests.find({}, {'_id': 0}))
total_path_qs = sum(len(p.get('questions', [])) for p in db.path_tests.find({}, {'_id': 0}))
print(f"\nTotal: {total_quizzes} doc quizzes ({total_questions} questions)")
print(f"       {len(module_tests)} module tests ({total_module_qs} questions)")
print(f"       {len(path_tests)} path tests ({total_path_qs} questions)")
