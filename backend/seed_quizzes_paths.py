"""Seed quizzes and learning paths into MongoDB"""
from pymongo import MongoClient
from datetime import datetime, timezone
import uuid

client = MongoClient('mongodb://localhost:27017')
db = client['test_database']

def _id():
    return str(uuid.uuid4())

# ============================================================
# QUIZZES — 3-5 questions per key document
# ============================================================
quizzes = [
    {
        "document_id": "f53aecbb-3b19-478c-9912-66d82827f402",  # What Is an AI Agent?
        "questions": [
            {"id": _id(), "question": "What is the key difference between a chatbot and an AI agent?", "options": ["An agent uses a bigger model", "An agent can take actions through tools", "An agent is always right", "An agent doesn't use an LLM"], "correct": 1, "explanation": "The core difference is that an agent can execute actions (create files, run commands, call APIs) through tools, while a chatbot can only generate text."},
            {"id": _id(), "question": "What role does the LLM play in an AI agent?", "options": ["It executes code directly", "It stores conversation history", "It reasons and generates text/tool calls", "It manages the database"], "correct": 2, "explanation": "The LLM is the reasoning engine — it generates text and proposes tool calls. The orchestration layer actually executes actions."},
            {"id": _id(), "question": "Which is NOT one of the three pillars of an AI agent?", "options": ["Reasoning (the LLM)", "Tools (the hands)", "Memory (the context)", "Training data (the knowledge)"], "correct": 3, "explanation": "The three pillars are Reasoning (LLM), Tools (execution capabilities), and Memory (context management). Training data is part of the LLM itself, not a separate agent pillar."},
            {"id": _id(), "question": "In the agent loop, what happens after the agent 'Acts'?", "options": ["It stops", "It observes the result", "It asks the user", "It retrains the model"], "correct": 1, "explanation": "After acting (executing a tool), the agent observes the result and feeds it back to the LLM for the next reasoning step."},
        ]
    },
    {
        "document_id": "6c753d08-d469-4e3f-8f3b-017d11c365c0",  # The Agent Loop
        "questions": [
            {"id": _id(), "question": "What is the correct order of the agent loop?", "options": ["Act → Think → Observe → Perceive", "Perceive → Think → Decide → Act → Observe", "Think → Act → Perceive → Observe", "Observe → Perceive → Think → Act"], "correct": 1, "explanation": "The universal agent loop is: Perceive (receive input) → Think (LLM reasoning) → Decide (choose action) → Act (execute tool) → Observe (see result) → repeat."},
            {"id": _id(), "question": "Why do agents sometimes get stuck in infinite loops?", "options": ["The LLM is too slow", "They keep retrying the same failed approach without adapting", "The tools are broken", "The user gave bad instructions"], "correct": 1, "explanation": "The most common cause is the agent retrying the same failed approach. Good agents detect this pattern and try alternative approaches or escalate to the user."},
            {"id": _id(), "question": "How many iterations might a full application build take?", "options": ["1-2", "3-5", "30-60+", "1000+"], "correct": 2, "explanation": "Building a full application typically requires 30-60+ iterations of the agent loop, each involving an LLM call plus tool executions."},
        ]
    },
    {
        "document_id": "b1abbfef-70c7-4c36-a5ed-11bc7b237d9c",  # Agent Memory Systems
        "questions": [
            {"id": _id(), "question": "Why do LLMs need external memory management?", "options": ["They're too expensive", "They're stateless — no memory between API calls", "They can't read files", "They run too slowly"], "correct": 1, "explanation": "LLMs are stateless. Each API call is independent. The agent's orchestration layer must manage all memory externally."},
            {"id": _id(), "question": "What is the most reliable form of long-term agent memory?", "options": ["Conversation history", "In-memory variables", "Persistent files (like PRD.md)", "The LLM's training data"], "correct": 2, "explanation": "Persistent files survive session restarts, context compaction, and even agent upgrades. They're the most reliable way to store critical decisions."},
            {"id": _id(), "question": "What happens during context compaction?", "options": ["The model is retrained", "Older messages are summarized to free up token space", "Files are deleted", "The agent starts a new session"], "correct": 1, "explanation": "Context compaction summarizes older messages into shorter form, preserving key information while freeing up tokens for new conversation."},
            {"id": _id(), "question": "Which memory type uses vector embeddings for retrieval?", "options": ["Short-term memory", "Working memory", "Semantic memory (RAG)", "Episodic memory"], "correct": 2, "explanation": "Semantic memory uses RAG — documents are embedded as vectors and retrieved based on similarity to the user's query."},
        ]
    },
    {
        "document_id": "c5c16dd0-8607-4576-a4d0-5ed296cd5980",  # Planning & Reasoning
        "questions": [
            {"id": _id(), "question": "What does ReAct stand for?", "options": ["Reactive Agents", "Reasoning + Acting", "Real-time Actions", "Recursive Architecture"], "correct": 1, "explanation": "ReAct stands for Reasoning + Acting — the agent alternates between thinking (reasoning) and doing (acting with tools)."},
            {"id": _id(), "question": "When should you use Tree-of-Thought over ReAct?", "options": ["For simple tasks", "When you need to explore multiple approaches before committing", "When speed is critical", "For bug fixes"], "correct": 1, "explanation": "Tree-of-Thought explores multiple possible approaches and evaluates them before committing to one. It's best for design decisions with multiple valid options."},
            {"id": _id(), "question": "What is the main weakness of Plan-and-Execute?", "options": ["It's too fast", "Plans can become stale as context changes", "It can't use tools", "It requires multiple LLMs"], "correct": 1, "explanation": "Plans are created upfront but may not survive contact with reality. If Step 3 reveals something unexpected, a rigid plan may not adapt."},
        ]
    },
    {
        "document_id": "007b573a-9065-4c3a-b835-1c7e8dc19591",  # Agent Design Patterns
        "questions": [
            {"id": _id(), "question": "In the Orchestrator-Worker pattern, who makes the decisions?", "options": ["The workers decide together", "Each worker decides for itself", "The orchestrator decides and delegates", "The user decides everything"], "correct": 2, "explanation": "The orchestrator controls all coordination. Workers are specialized — they receive tasks, execute them, and return results. They never talk to each other directly."},
            {"id": _id(), "question": "What is the Reflexion pattern?", "options": ["The agent reflects on its own output and improves it", "The agent asks the user for feedback", "The agent runs tests", "The agent searches the web"], "correct": 0, "explanation": "Reflexion is when the agent evaluates its own output and iteratively improves it. It catches mistakes that single-pass generation misses, but doubles the token cost."},
            {"id": _id(), "question": "Which anti-pattern describes an agent retrying the same failure forever?", "options": ["Over-delegation", "Blind retry", "Premature completion", "No observation"], "correct": 1, "explanation": "Blind retry means repeating the same action expecting different results. The fix is a max retry count plus requiring a different approach after N failures."},
        ]
    },
    {
        "document_id": "a6248371-7ced-4bb6-8343-fb7c2a31a2ae",  # How Transformers Work
        "questions": [
            {"id": _id(), "question": "What does a transformer predict?", "options": ["The user's intent", "The next token", "The best tool to use", "The answer to a question"], "correct": 1, "explanation": "Transformers are fundamentally next-token predictors. Given all previous tokens, they predict the probability distribution of the next token."},
            {"id": _id(), "question": "What is the purpose of self-attention?", "options": ["To compress the input", "To let each token 'look at' every other token for context", "To generate images", "To store memory"], "correct": 1, "explanation": "Self-attention allows each token to consider every other token in the sequence, enabling the model to understand context (e.g., 'bank' near 'river' vs 'bank' near 'loan')."},
            {"id": _id(), "question": "What does temperature=0 mean in sampling?", "options": ["The model is off", "Always pick the most likely token (deterministic)", "Maximum creativity", "The model runs faster"], "correct": 1, "explanation": "Temperature=0 means greedy/deterministic — always pick the highest probability token. Higher temperature increases randomness and creativity."},
        ]
    },
    {
        "document_id": "78d7bf49-291b-484f-91bd-bdeb670f449f",  # Function Calling
        "questions": [
            {"id": _id(), "question": "Who actually executes a function call?", "options": ["The LLM executes it directly", "The user runs it manually", "The agent's tool execution layer", "The cloud provider"], "correct": 2, "explanation": "The LLM generates a structured JSON tool call. The agent's execution layer parses it and actually runs the function. The LLM never executes anything."},
            {"id": _id(), "question": "What is tool_choice='required' used for?", "options": ["The LLM must call at least one tool", "The tool is optional", "No tools can be used", "The user must approve"], "correct": 0, "explanation": "tool_choice='required' forces the LLM to output at least one tool call. Use it when you always need an action, not a text response."},
            {"id": _id(), "question": "How are tools defined for the LLM?", "options": ["Natural language descriptions", "JSON schemas with name, description, and parameters", "Python function decorators", "Binary protocols"], "correct": 1, "explanation": "Tools are defined using JSON schemas that specify the function name, description, and parameter types. The LLM uses these schemas to generate correctly structured calls."},
        ]
    },
    {
        "document_id": "837d44b6-b59f-441b-bda4-37a5bf5b53e5",  # Guardrails & Safety
        "questions": [
            {"id": _id(), "question": "Why is agent safety harder than LLM safety?", "options": ["Agents are smarter", "Agents can take real actions that affect the world", "Agents cost more", "Agents are newer"], "correct": 1, "explanation": "An LLM generating wrong text is annoying. An agent executing wrong commands (deleting files, running destructive code) is actually dangerous."},
            {"id": _id(), "question": "What is prompt injection?", "options": ["Adding more examples to the prompt", "Tricking the agent into ignoring its instructions", "Making the prompt longer", "A way to speed up responses"], "correct": 1, "explanation": "Prompt injection is when a user (or data) tricks the agent into overriding its system prompt instructions, potentially causing it to take unauthorized actions."},
            {"id": _id(), "question": "What is the 'human-in-the-loop' pattern?", "options": ["Humans write all the code", "The agent asks for approval before critical actions", "Humans review after deployment", "The agent is turned off"], "correct": 1, "explanation": "Human-in-the-loop means the agent pauses and asks for human approval before critical actions like deployments, database changes, or payments."},
        ]
    },
    {
        "document_id": "9d1d8932-abb7-4ae1-8243-6ecebffc9165",  # RAG
        "questions": [
            {"id": _id(), "question": "What problem does RAG solve?", "options": ["Making LLMs faster", "Giving LLMs access to private or current data they weren't trained on", "Reducing costs", "Training new models"], "correct": 1, "explanation": "RAG lets LLMs answer questions about data that isn't in their training data — your company's docs, recent information, private databases."},
            {"id": _id(), "question": "Why is chunk overlap important in RAG?", "options": ["It makes search faster", "Facts split across chunk boundaries won't be lost", "It reduces storage", "It improves model quality"], "correct": 1, "explanation": "Without overlap, a fact split across two chunks might never be retrieved. 50-100 token overlap ensures boundary content appears in at least one chunk."},
            {"id": _id(), "question": "When should you NOT use RAG?", "options": ["When you have private data", "When data changes frequently", "When you have a very small knowledge base (<10 docs)", "When you need citations"], "correct": 2, "explanation": "For very small knowledge bases, you can include all documents directly in the prompt. RAG adds unnecessary complexity when the data fits in the context window."},
        ]
    },
]

# Insert quizzes
db.quizzes.drop()
for q in quizzes:
    db.quizzes.insert_one(q)
print(f"Inserted {len(quizzes)} quizzes")

# ============================================================
# LEARNING PATHS
# ============================================================
paths = [
    {
        "id": _id(),
        "title": "Beginner: Understanding AI Agents",
        "description": "Start from zero. Learn what agents are, how they think, and why they matter.",
        "icon": "Rocket",
        "difficulty": "beginner",
        "estimated_time": "45 min",
        "order": 0,
        "steps": [
            {"document_id": "f53aecbb-3b19-478c-9912-66d82827f402", "title": "What Is an AI Agent?", "description": "The foundation — chatbots vs assistants vs agents"},
            {"document_id": "6c753d08-d469-4e3f-8f3b-017d11c365c0", "title": "The Agent Loop", "description": "The universal Perceive → Think → Act cycle"},
            {"document_id": "b1abbfef-70c7-4c36-a5ed-11bc7b237d9c", "title": "Agent Memory Systems", "description": "How agents remember and forget"},
            {"document_id": "a6248371-7ced-4bb6-8343-fb7c2a31a2ae", "title": "How Transformers Work", "description": "The AI engine under the hood"},
            {"document_id": "faa447ea-8011-4636-b9f2-92bb8baa9d11", "title": "Your First AI Coding Session", "description": "Put it into practice"},
        ]
    },
    {
        "id": _id(),
        "title": "Builder: Agent Architecture Deep Dive",
        "description": "For developers who want to understand how to design and build agent systems.",
        "icon": "Layers",
        "difficulty": "intermediate",
        "estimated_time": "90 min",
        "order": 1,
        "steps": [
            {"document_id": "77e90317-8337-4613-ba2c-877322e28445", "title": "What Is an AI Agent Orchestrator?", "description": "The orchestration layer explained"},
            {"document_id": "c5c16dd0-8607-4576-a4d0-5ed296cd5980", "title": "Planning & Reasoning Patterns", "description": "ReAct, CoT, ToT, Plan-and-Execute"},
            {"document_id": "007b573a-9065-4c3a-b835-1c7e8dc19591", "title": "Agent Design Patterns", "description": "ReAct, MRKL, Reflexion, Orchestrator-Worker"},
            {"document_id": "78d7bf49-291b-484f-91bd-bdeb670f449f", "title": "Function Calling & Tool Use", "description": "How agents interact with the world"},
            {"document_id": "cf9a2943-0dee-4dde-b9fe-fbb6473406ed", "title": "The Subagent System", "description": "Multi-agent delegation and coordination"},
            {"document_id": "6969126d-1369-4e9a-8516-761a9aeac367", "title": "Multi-Agent Communication", "description": "MCP, A2A, and communication patterns"},
            {"document_id": "837d44b6-b59f-441b-bda4-37a5bf5b53e5", "title": "Guardrails & Safety", "description": "Building agents you can trust"},
        ]
    },
    {
        "id": _id(),
        "title": "LLM Foundations",
        "description": "Understand the AI engine that powers every agent — from transformers to tokens to training.",
        "icon": "Cpu",
        "difficulty": "intermediate",
        "estimated_time": "60 min",
        "order": 2,
        "steps": [
            {"document_id": "a6248371-7ced-4bb6-8343-fb7c2a31a2ae", "title": "How Transformers Work", "description": "The neural network architecture"},
            {"document_id": "4f3a3853-7a6a-4cfe-bce4-883a27e5b1ec", "title": "LLM Training Stages", "description": "From data to deployment"},
            {"document_id": "42b2fa04-0630-4bbe-8399-4d0b40324345", "title": "Token Economics & Billing", "description": "Understanding costs"},
            {"document_id": "c70d2179-aa23-470d-bb40-4c697c17c340", "title": "Choosing the Right LLM", "description": "Model selection guide"},
            {"document_id": "365341b4-bcda-490c-826c-ed2d73bbbe55", "title": "Prompt Engineering Techniques", "description": "Crafting effective prompts"},
            {"document_id": "9d1d8932-abb7-4ae1-8243-6ecebffc9165", "title": "Retrieval Augmented Generation", "description": "Grounding LLMs in real data"},
        ]
    },
    {
        "id": _id(),
        "title": "Practitioner: Building Real Applications",
        "description": "Hands-on tutorials and real-world patterns for building production systems.",
        "icon": "Telescope",
        "difficulty": "advanced",
        "estimated_time": "75 min",
        "order": 3,
        "steps": [
            {"document_id": "c6ea5927-451c-46c9-a5ff-d970942371e1", "title": "Building a REST API from Scratch", "description": "Step-by-step API tutorial"},
            {"document_id": "e3a78a63-314a-4c0d-9418-51e61a1c96c3", "title": "Debugging a 500 Error", "description": "Systematic debugging approach"},
            {"document_id": "c5def112-62e1-47a8-9f8a-4e5a9c8513bf", "title": "Cost Optimization for AI Agents", "description": "Reduce costs without losing quality"},
            {"document_id": "29cc06bb-7fbb-4fd6-ba28-69c011198919", "title": "Evaluation & Observability", "description": "Measuring agent performance"},
            {"document_id": "d14121c2-b664-4df8-b2b6-2a22d5e639ce", "title": "Real-World AI Agents: Case Studies", "description": "Learn from Devin, Cursor, Claude Code"},
            {"document_id": "2a5515f0-e724-4b19-8fc7-d265e95c3154", "title": "Fine-Tuning vs Prompting vs RAG", "description": "When to use which approach"},
        ]
    },
]

db.learning_paths.drop()
for p in paths:
    db.learning_paths.insert_one(p)
print(f"Inserted {len(paths)} learning paths")
