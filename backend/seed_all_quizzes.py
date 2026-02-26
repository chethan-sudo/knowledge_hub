"""Add quizzes to ALL remaining 42 documents"""
from pymongo import MongoClient
import uuid

client = MongoClient('mongodb://localhost:27017')
db = client['test_database']

def _id(): return str(uuid.uuid4())

def add_quiz(doc_id, questions):
    db.quizzes.update_one({"document_id": doc_id}, {"$set": {"document_id": doc_id, "questions": questions}}, upsert=True)

quizzes = {
    # System Architecture
    "82ae6221-0508-422e-a7ff-b84201cd1a9e": [
        {"id": _id(), "question": "What is the role of the LLM in an agent system?", "options": ["It executes tools", "It manages the database", "It reasons and generates responses", "It stores conversation history"], "correct": 2, "explanation": "The LLM is the reasoning engine. It generates text and tool call proposals. The orchestration layer handles everything else."},
        {"id": _id(), "question": "What does the LLM Proxy do?", "options": ["Generates code", "Routes LLM calls, tracks tokens, handles billing and failover", "Manages user sessions", "Runs tests"], "correct": 1, "explanation": "The LLM Proxy sits between agents and LLM providers, handling routing, authentication, cost tracking, and failover."},
        {"id": _id(), "question": "Why are there two separate paths for app traffic and AI chat?", "options": ["For security", "They use different databases", "The app runs independently while the agent modifies its code", "They require different programming languages"], "correct": 2, "explanation": "Path A (app traffic) and Path B (AI chat) are independent. The app can serve users while the agent simultaneously modifies its code."},
    ],
    # What Is an AI Agent Orchestrator?
    "77e90317-8337-4613-ba2c-877322e28445": [
        {"id": _id(), "question": "What does the Decision Layer do?", "options": ["Trains the model", "Parses LLM output and routes to tools, subagents, or user", "Stores files", "Manages the database"], "correct": 1, "explanation": "The Decision Layer parses each LLM response and decides the next action: execute a tool, delegate to a subagent, or respond to the user."},
        {"id": _id(), "question": "Why does the orchestrator clarify requirements on the first message?", "options": ["To be polite", "To prevent wasted work from ambiguous instructions", "Because the LLM requires it", "To test the user"], "correct": 1, "explanation": "Clarifying upfront prevents building the wrong thing. It's encoded as a rule in the system prompt."},
        {"id": _id(), "question": "What is the Tool Registry?", "options": ["A database of user accounts", "A catalog of available tools with their schemas", "A list of LLM models", "A version control system"], "correct": 1, "explanation": "The Tool Registry catalogs all available tools with their names, parameters, and descriptions. The LLM uses these schemas to generate structured tool calls."},
    ],
    # The Subagent System
    "cf9a2943-0dee-4dde-b9fe-fbb6473406ed": [
        {"id": _id(), "question": "Why are subagents stateless?", "options": ["To save memory", "They do one specialized job and don't need previous context", "Because LLMs can't remember", "For security reasons"], "correct": 1, "explanation": "Subagents are specialized. They do one job well and return results. The orchestrator provides full context each time."},
        {"id": _id(), "question": "When does the orchestrator call the troubleshoot agent?", "options": ["On every error", "After 2+ failed fix attempts", "Before starting any task", "When the user asks"], "correct": 1, "explanation": "The troubleshoot agent is escalation. It's called when the main agent is stuck after multiple failed attempts, providing a fresh diagnostic perspective."},
        {"id": _id(), "question": "What does the testing agent return?", "options": ["A new version of the code", "A JSON test report plus git diff of any fixes", "A list of features", "Nothing"], "correct": 1, "explanation": "The testing agent returns a structured test report (pass/fail per test) and a git diff showing any code changes it made during testing."},
    ],
    # Tool Execution Engine
    "a7588bb9-ed8f-45a2-a712-977f1dd65ea4": [
        {"id": _id(), "question": "Why can some tool calls run in parallel?", "options": ["All tools always run in parallel", "Independent operations (like creating separate files) don't depend on each other", "Parallel is always faster", "The LLM requires it"], "correct": 1, "explanation": "Independent operations can safely parallelize. But dependent operations (install package THEN import it) must be sequential."},
        {"id": _id(), "question": "What happens when a bash command exceeds the timeout?", "options": ["Nothing", "The process is terminated and partial output is captured", "The entire agent crashes", "It runs forever"], "correct": 1, "explanation": "Commands have a timeout (typically 1-2 minutes). When exceeded, the process is killed and whatever output was captured is returned to the agent."},
    ],
    # LLM Proxy
    "0a7bdb8d-de13-4312-b13f-fca914ed5bcb": [
        {"id": _id(), "question": "Why use a centralized LLM proxy?", "options": ["To make requests slower", "To centralize auth, billing, rate limiting, and failover in one place", "Because LLMs require it", "For debugging only"], "correct": 1, "explanation": "Without a proxy, every component needs its own API keys, billing logic, and error handling. The proxy centralizes all of this."},
        {"id": _id(), "question": "What happens if the primary LLM provider is down?", "options": ["The agent stops working", "The proxy routes to a fallback provider", "The user is asked to try again", "The request is cached"], "correct": 1, "explanation": "The proxy has failover logic that automatically routes to an alternative provider if the primary is unavailable."},
        {"id": _id(), "question": "How does provider routing work?", "options": ["Random selection", "Based on the model name in the request", "Always uses the cheapest", "The user chooses manually"], "correct": 1, "explanation": "The model parameter in the request determines the provider. 'gpt-4o' routes to OpenAI, 'claude-sonnet' to Anthropic, etc."},
    ],
    # LLM Training Stages
    "4f3a3853-7a6a-4cfe-bce4-883a27e5b1ec": [
        {"id": _id(), "question": "What does pre-training teach the model?", "options": ["To follow instructions", "To predict the next token given all previous tokens", "To refuse harmful requests", "To use tools"], "correct": 1, "explanation": "Pre-training is next-token prediction on trillions of tokens. It teaches language, facts, code, and reasoning patterns."},
        {"id": _id(), "question": "What is the purpose of RLHF?", "options": ["To make the model faster", "To align the model with human preferences for helpfulness and safety", "To reduce costs", "To add new knowledge"], "correct": 1, "explanation": "RLHF (Reinforcement Learning from Human Feedback) teaches the model which responses humans prefer, making it helpful, harmless, and honest."},
        {"id": _id(), "question": "Why is fine-tuning data smaller than pre-training data?", "options": ["Budget constraints", "Fine-tuning teaches behavior patterns, not knowledge — quality matters more than quantity", "The model can't handle more", "It's the same size"], "correct": 1, "explanation": "Pre-training needs trillions of tokens for knowledge. Fine-tuning only needs thousands-millions of high-quality instruction-response pairs to shape behavior."},
    ],
    # Token Economics
    "42b2fa04-0630-4bbe-8399-4d0b40324345": [
        {"id": _id(), "question": "Why do output tokens cost more than input tokens?", "options": ["They're longer", "Generation is more compute-intensive than processing input", "They're more valuable", "They require more storage"], "correct": 1, "explanation": "Generating each output token requires a full forward pass through the model. Processing input can be batched and is cheaper per token."},
        {"id": _id(), "question": "What is the 'fixed cost' per message in an agent system?", "options": ["$0.01", "System prompt + tool definitions sent with every call", "The user subscription fee", "Database storage"], "correct": 1, "explanation": "The system prompt (~15K tokens) and tool definitions (~8K tokens) are sent with every single LLM call, creating a ~23K token baseline cost per message."},
    ],
    # Docker
    "430d0d99-6cb6-4fe4-a4f8-db4e9d8960d9": [
        {"id": _id(), "question": "How are containers different from virtual machines?", "options": ["They're the same thing", "Containers share the host kernel while VMs run their own OS", "VMs are faster", "Containers need more memory"], "correct": 1, "explanation": "Containers use Linux namespaces for isolation while sharing the host kernel. VMs virtualize entire hardware including a separate OS kernel."},
        {"id": _id(), "question": "Why copy requirements.txt before the application code in a Dockerfile?", "options": ["Alphabetical order", "Requirements file is smaller", "Layer caching — dependencies change less often than code", "Docker requires this order"], "correct": 2, "explanation": "Docker caches layers. If requirements.txt hasn't changed, the pip install layer is cached even when code changes. This makes builds much faster."},
    ],
    # Kubernetes
    "edd57e39-a25c-4e9b-a262-3b8740ffd119": [
        {"id": _id(), "question": "What is a Kubernetes Pod?", "options": ["A virtual machine", "The smallest deployable unit, containing one or more containers", "A database", "A network cable"], "correct": 1, "explanation": "A Pod is Kubernetes' smallest deployable unit. It contains one or more containers that share networking and storage."},
        {"id": _id(), "question": "What happens when a container in a pod crashes?", "options": ["The entire cluster shuts down", "Kubernetes automatically restarts it", "The user must manually restart", "Nothing"], "correct": 1, "explanation": "Kubernetes has self-healing capabilities. If a container crashes, it's automatically restarted with exponential backoff."},
    ],
    # Hot Reload
    "73a500c3-910c-43a8-ad42-3341baa73611": [
        {"id": _id(), "question": "When do you need to manually restart a service?", "options": ["After every code change", "Only after .env changes or dependency installations", "Every hour", "Never"], "correct": 1, "explanation": "Hot reload handles code changes automatically. Manual restart is only needed for environment variable changes or new package installations."},
        {"id": _id(), "question": "What does Supervisor do?", "options": ["Writes code", "Manages and auto-restarts processes", "Deploys to production", "Runs tests"], "correct": 1, "explanation": "Supervisor (supervisord) manages all processes — frontend, backend, database. If any crash, it automatically restarts them."},
    ],
    # React
    "bc48cfdf-5403-4017-b6d9-229485d3fea5": [
        {"id": _id(), "question": "Why are stable keys important in React lists?", "options": ["For styling", "They let React track items across re-renders without destroying/recreating them", "React requires them", "For accessibility"], "correct": 1, "explanation": "Without stable keys, React destroys and recreates every list item on re-render. With stable keys, it only updates items that actually changed."},
        {"id": _id(), "question": "When should you use useCallback?", "options": ["Always", "When passing callbacks to memoized child components", "Never", "Only for API calls"], "correct": 1, "explanation": "useCallback prevents creating a new function reference every render, which would cause React.memo'd children to re-render unnecessarily."},
        {"id": _id(), "question": "What is the React anti-pattern of 'state that should be derived'?", "options": ["Using too many components", "Storing a value as state when it can be computed from other state", "Using hooks", "Having too many props"], "correct": 1, "explanation": "If a value can be computed from existing state (e.g., count = items.length), it shouldn't be separate state. This avoids synchronization bugs."},
    ],
    # FastAPI
    "59c72443-acaa-4172-873a-8ced3bdbffcd": [
        {"id": _id(), "question": "What HTTP status code does Pydantic validation failure return?", "options": ["400", "401", "422", "500"], "correct": 2, "explanation": "FastAPI returns 422 Unprocessable Entity when the request body doesn't match the Pydantic model, with detailed field-level error messages."},
        {"id": _id(), "question": "What is Dependency Injection in FastAPI?", "options": ["A security vulnerability", "A way to share reusable logic (auth, DB) across routes via Depends()", "A database pattern", "A testing framework"], "correct": 1, "explanation": "FastAPI's Depends() lets you define reusable functions that run before your route handler — perfect for authentication, database connections, and authorization."},
    ],
    # MongoDB
    "d666695b-7238-4aeb-9506-e87ff7ae3fd3": [
        {"id": _id(), "question": "Why must you always exclude _id from MongoDB query projections?", "options": ["It's a security risk", "ObjectId is not JSON serializable — it will crash your API", "It's too large", "MongoDB requires it"], "correct": 1, "explanation": "MongoDB's _id field is an ObjectId type that Python can't serialize to JSON. Always use {'_id': 0} in projections to exclude it."},
        {"id": _id(), "question": "What does insert_one() do to the dictionary you pass it?", "options": ["Nothing", "Mutates it by adding an _id field", "Copies it", "Validates it"], "correct": 1, "explanation": "insert_one() adds the generated _id field to your input dictionary. If you reuse that dict in your response, it will contain an unserializable ObjectId."},
    ],
    # JWT & OAuth
    "a8ba52c1-fbb3-42ba-9dda-81283861b0fd": [
        {"id": _id(), "question": "Are JWTs encrypted?", "options": ["Yes", "No — they are encoded (Base64) but anyone can read the payload", "Only the signature is encrypted", "Depends on the algorithm"], "correct": 1, "explanation": "JWTs are encoded, not encrypted. The payload is Base64-encoded, which anyone can decode. Never put passwords or sensitive data in a JWT."},
        {"id": _id(), "question": "What is the purpose of the JWT signature?", "options": ["To encrypt the data", "To prove the token hasn't been tampered with", "To compress the token", "To make it shorter"], "correct": 1, "explanation": "The signature is an HMAC of the header + payload using a secret key. If anyone modifies the payload, the signature won't match and the token is rejected."},
    ],
    # Deployment
    "6d80151d-b337-4d53-bfc6-1ff2ea7a3135": [
        {"id": _id(), "question": "Why should production apps NOT use allow_origins=['*'] with credentials?", "options": ["It's slower", "It's a CORS security risk — any origin can make authenticated requests", "It's not valid syntax", "It costs more"], "correct": 1, "explanation": "Wildcard origins with credentials enabled means any website can make authenticated requests to your API. In production, restrict to your specific domain."},
        {"id": _id(), "question": "What is the purpose of a health check endpoint?", "options": ["To show documentation", "To verify the app and its dependencies (DB, etc.) are running", "To reset the server", "To count users"], "correct": 1, "explanation": "Health check endpoints verify the app is running and its dependencies (database, etc.) are connected. Used by monitoring systems and load balancers."},
    ],
    # Git
    "30c18c0c-78c0-4f30-aa6a-0f31d051cdd4": [
        {"id": _id(), "question": "Does Git store diffs or complete snapshots?", "options": ["Only diffs", "Complete snapshots — every commit has a full snapshot of all files", "Both", "Neither"], "correct": 1, "explanation": "Every commit contains a complete snapshot (tree). Git manages disk space through compression and deduplication — same content = same blob hash."},
        {"id": _id(), "question": "What is the git reflog?", "options": ["A bug report", "A log of every position HEAD has been at — your safety net for recovering 'lost' commits", "A list of branches", "A deployment log"], "correct": 1, "explanation": "The reflog keeps entries for 30 days showing every state HEAD has been in. Even after hard reset, old commits are still there."},
    ],
    # Rate Limiting
    "cbc7b591-8536-4da8-ad73-213c7984cf1e": [
        {"id": _id(), "question": "If you get a 429 error with a plain HTML page, which layer blocked you?", "options": ["Your application", "The web server (Nginx)", "The database", "The LLM provider"], "correct": 1, "explanation": "A 429 with HTML (not JSON) means the web server/proxy blocked the request before it reached your application. Your app returns JSON errors."},
        {"id": _id(), "question": "Why use sliding windows instead of fixed windows for rate limiting?", "options": ["They're simpler", "They prevent burst at window boundaries", "They use less memory", "They're faster"], "correct": 1, "explanation": "Fixed windows allow a burst at the boundary (e.g., 100 requests at 11:59 and 100 at 12:00). Sliding windows distribute the limit evenly."},
    ],
    # SSL/TLS & CORS
    "408ce019-490a-486e-b5cb-a0393614fbf1": [
        {"id": _id(), "question": "Why does 'it works in Postman but not in my app' almost always mean CORS?", "options": ["Postman is faster", "CORS is a browser-only mechanism — curl and Postman don't enforce same-origin policy", "Postman uses a different network", "The API is broken"], "correct": 1, "explanation": "CORS is enforced by browsers, not servers. Postman, curl, and server-to-server calls don't have origins, so they're never blocked by CORS."},
        {"id": _id(), "question": "Where does TLS terminate in a typical cloud setup?", "options": ["In your application code", "At the load balancer/ingress — your app only sees plain HTTP", "In the browser", "In the database"], "correct": 1, "explanation": "TLS terminates at the load balancer or ingress controller. Internal traffic between services is plain HTTP, so your app code never handles certificates."},
    ],
    # Session Lifecycle
    "b2f69bb6-38fb-441e-a8cc-c856747a6d90": [
        {"id": _id(), "question": "What data survives when a cloud development environment is recycled?", "options": ["Everything", "Only database records and committed Git — filesystem is lost", "Nothing", "Only environment variables"], "correct": 1, "explanation": "Database data persists because it's on persistent storage. Git commits survive because they're pushed to remote. Ephemeral filesystem (temp files, uncommitted code) is lost."},
        {"id": _id(), "question": "What should you use for user preferences like theme?", "options": ["Database", "localStorage (browser-side)", "Environment variables", "Cookies"], "correct": 1, "explanation": "User preferences are best in localStorage — instant access, no API call needed, persists across page refreshes, and stored in the user's browser."},
    ],
    # Assets
    "0799b23d-3e8b-4fde-acf3-50df40b1dee5": [
        {"id": _id(), "question": "Why should you NOT manually set Content-Type when uploading files with FormData?", "options": ["It's not required", "The browser automatically sets it with the correct multipart boundary — manual setting breaks it", "It's too long", "For security"], "correct": 1, "explanation": "When using FormData, the browser sets Content-Type to multipart/form-data with a unique boundary string. Setting it manually omits the boundary, breaking the upload."},
    ],
    # Observability
    "6bde53b6-a3a5-45e9-9fd4-36d2d7c2ee1b": [
        {"id": _id(), "question": "Why does every debug entry look nearly identical at first glance?", "options": ["The LLM generates the same thing", "The system prompt (~60-70% of the payload) is constant — dynamic content is buried below it", "It's a bug", "The logs are cached"], "correct": 1, "explanation": "The system prompt and tool definitions are sent with every call and don't change. They dominate the view. You need to scroll past them to find the dynamic content."},
        {"id": _id(), "question": "If an agent interaction takes 30+ seconds, what should you check first?", "options": ["The network cable", "Input token count — large context windows are expensive and slow", "The database", "The frontend code"], "correct": 1, "explanation": "High latency usually means the context window is very large (150K+ tokens). Starting a new session or being more targeted in requests reduces this."},
    ],
    # RAG (already has quiz, skip)
    # Agent Frameworks
    "d89835e2-3a1d-4e5e-ab1d-08564363d945": [
        {"id": _id(), "question": "What is MCP (Model Context Protocol)?", "options": ["A programming language", "A standard protocol for how AI agents interact with tools", "A database system", "A testing framework"], "correct": 1, "explanation": "MCP, by Anthropic, standardizes how agents discover and call tools — making tools portable across different agent frameworks."},
        {"id": _id(), "question": "When should you choose CrewAI over a single agent?", "options": ["Always", "When your problem naturally breaks into distinct roles (researcher, writer, reviewer)", "For simple tasks", "When you need speed"], "correct": 1, "explanation": "CrewAI is designed for multi-agent collaboration where each agent has a distinct role. It's overkill for tasks a single agent can handle."},
    ],
    # Prompt Engineering
    "365341b4-bcda-490c-826c-ed2d73bbbe55": [
        {"id": _id(), "question": "Why are few-shot examples more effective than abstract instructions?", "options": ["They're shorter", "LLMs pattern-match from examples — they learn the convention without explicit rules", "They cost fewer tokens", "They're required by the API"], "correct": 1, "explanation": "Given 'login-form-submit-button' as an example, the LLM generates 'signup-form-email-input' — following the pattern without being told the naming convention explicitly."},
        {"id": _id(), "question": "What is the purpose of negative instructions ('Don'ts')?", "options": ["To be strict", "To prevent known failure modes where the LLM does 'helpful' but destructive things", "To make the prompt longer", "They don't help"], "correct": 1, "explanation": "LLMs tend toward 'helpful' behaviors that can be destructive (restarting servers, deleting configs). Negative instructions explicitly prevent these."},
    ],
    # Browser Rendering
    "f37650ff-3257-4184-80b9-3776892ddd3a": [
        {"id": _id(), "question": "What triggers a browser reflow (layout recalculation)?", "options": ["Changing colors", "Changing dimensions, position, or adding/removing elements", "Changing opacity", "Changing text color"], "correct": 1, "explanation": "Reflow recalculates the layout of elements. It's triggered by changes to dimensions, position, margin, padding, or adding/removing DOM elements."},
    ],
    # Error Recovery
    "51d33940-574a-4071-81b4-5a0fc99e9ea5": [
        {"id": _id(), "question": "What is the 'blind retry' anti-pattern?", "options": ["Retrying with different parameters", "Repeating the same failed action expecting different results", "Asking the user for help", "Skipping the step"], "correct": 1, "explanation": "Blind retry means repeating the exact same action without changing anything. The fix: max retry count + require a different approach after N failures."},
        {"id": _id(), "question": "When should an agent escalate to the user?", "options": ["On every error", "After 2-3 failed attempts with different approaches", "Never", "Only for permission issues"], "correct": 1, "explanation": "Escalation is appropriate after the agent has tried multiple approaches and failed. It's better than infinite retrying or giving up silently."},
    ],
    # Ethical Considerations
    "417e0794-ef30-41c1-bec7-6021777f1b35": [
        {"id": _id(), "question": "At what autonomy level do most production agents operate?", "options": ["Fully autonomous", "Level 2-3 (supervised to semi-autonomous)", "Advisory only", "No autonomy"], "correct": 1, "explanation": "Most production agents operate at supervised (human approves critical actions) or semi-autonomous (acts freely within bounds, escalates edge cases) level."},
    ],
    # Evaluation
    "29cc06bb-7fbb-4fd6-ba28-69c011198919": [
        {"id": _id(), "question": "Why is evaluating agents harder than traditional software?", "options": ["Agents are slower", "Agents are non-deterministic — same input can produce different results", "Agents are more expensive", "It's not harder"], "correct": 1, "explanation": "Traditional software is deterministic (same input → same output). Agents may take different actions and produce different results each time."},
        {"id": _id(), "question": "What is LLM-as-Judge?", "options": ["Using an LLM to run the agent", "Using another LLM to evaluate the agent's output quality", "A legal concept", "A debugging tool"], "correct": 1, "explanation": "LLM-as-Judge uses a separate LLM to score an agent's output on criteria like correctness, code quality, and completeness. It scales better than human review."},
    ],
    # Multi-Agent
    "6969126d-1369-4e9a-8516-761a9aeac367": [
        {"id": _id(), "question": "What is the Blackboard pattern?", "options": ["Agents write on a physical whiteboard", "Agents share a common knowledge base, each reading and writing to it", "Agents communicate in sequence", "A debugging tool"], "correct": 1, "explanation": "In the Blackboard pattern, all agents read from and write to a shared knowledge base. Each agent picks up relevant information and contributes its results."},
        {"id": _id(), "question": "How do MCP and A2A protocols differ?", "options": ["They're the same", "MCP is agent↔tool communication, A2A is agent↔agent communication", "MCP is newer", "A2A is by Anthropic"], "correct": 1, "explanation": "MCP (Anthropic) standardizes how agents use tools. A2A (Google) standardizes how agents communicate with each other. They solve different problems."},
    ],
    # Fine-Tuning vs Prompting vs RAG
    "2a5515f0-e724-4b19-8fc7-d265e95c3154": [
        {"id": _id(), "question": "When should you try prompting before fine-tuning?", "options": ["Never", "Always — prompting is free and faster to iterate", "Only for simple tasks", "Only for complex tasks"], "correct": 1, "explanation": "Prompting costs nothing extra and can be iterated instantly. Fine-tuning is expensive ($100-$10,000+) and slow. Always try prompting first."},
        {"id": _id(), "question": "What does RAG add latency for?", "options": ["Model inference", "Embedding the query and searching the vector database (100-500ms)", "User authentication", "Rendering results"], "correct": 1, "explanation": "RAG adds latency for embedding the query and performing vector similarity search. Typically 100-500ms depending on the knowledge base size."},
    ],
    # Cost Optimization
    "c5def112-62e1-47a8-9f8a-4e5a9c8513bf": [
        {"id": _id(), "question": "What is the highest-leverage cost optimization?", "options": ["Use shorter system prompts", "Model routing — use cheap models for easy tasks, expensive for hard ones", "Reduce output length", "Cache everything"], "correct": 1, "explanation": "Model routing can reduce costs 50-80%. A classification task using GPT-4o-mini instead of Claude Sonnet costs 20x less with similar quality."},
        {"id": _id(), "question": "Why does context grow more expensive with each message?", "options": ["Tokens get more expensive over time", "The full conversation history is sent with every call, growing each turn", "The model slows down", "The database grows"], "correct": 1, "explanation": "Every LLM call includes the full conversation history. Turn 1 might be 15K tokens, but Turn 30 could be 100K+ tokens — all billed as input tokens."},
    ],
    # Real-World Case Studies
    "d14121c2-b664-4df8-b2b6-2a22d5e639ce": [
        {"id": _id(), "question": "What makes Cursor's agent different from other coding agents?", "options": ["It uses a bigger model", "It indexes the entire codebase for context-aware suggestions", "It's open source", "It only works with Python"], "correct": 1, "explanation": "Cursor indexes your entire codebase, letting the agent understand project structure. This makes tool choices more accurate than agents that start blind."},
        {"id": _id(), "question": "What safety pattern does Claude Code implement?", "options": ["No safety measures", "Permission-gated tool use — asks before destructive actions", "Only runs in read-only mode", "Requires admin approval for everything"], "correct": 1, "explanation": "Claude Code asks for permission before destructive actions (deleting files, running risky commands). This is a practical human-in-the-loop safety pattern."},
    ],
    # Building REST API
    "c6ea5927-451c-46c9-a5ff-d970942371e1": [
        {"id": _id(), "question": "Why use UUID strings instead of MongoDB ObjectIds for document IDs?", "options": ["They're shorter", "UUIDs are JSON serializable — ObjectIds are not", "MongoDB requires UUIDs", "They're faster"], "correct": 1, "explanation": "UUID strings serialize to JSON naturally. MongoDB's ObjectId type is not JSON serializable and will crash your API if returned in a response."},
        {"id": _id(), "question": "What is the soft delete pattern?", "options": ["Deleting data permanently", "Setting a 'deleted' flag instead of actually removing the record", "Deleting after 30 days", "Moving to a different database"], "correct": 1, "explanation": "Soft delete marks records as deleted without actually removing them. This allows recovery (undelete) and preserves referential integrity."},
    ],
    # Debugging 500
    "e3a78a63-314a-4c0d-9418-51e61a1c96c3": [
        {"id": _id(), "question": "What is the FIRST thing you should do when debugging a 500 error?", "options": ["Restart the server", "Check the error logs", "Rewrite the code", "Ask for help"], "correct": 1, "explanation": "Always check logs first. The traceback tells you the exact file, line, function, and error type. This is faster and more reliable than guessing."},
        {"id": _id(), "question": "Why should you reproduce the error before fixing it?", "options": ["To waste time", "To understand exactly what triggers it and verify the fix works", "It's required by the framework", "To document it"], "correct": 1, "explanation": "Reproducing ensures you understand the root cause (not just a symptom) and gives you a reliable way to verify the fix actually works."},
    ],
    # Choosing the Right LLM
    "c70d2179-aa23-470d-bb40-4c697c17c340": [
        {"id": _id(), "question": "When should you use Gemini Flash over Claude Sonnet?", "options": ["For complex code review", "When speed and cost matter more than maximum quality", "For creative writing", "For long documents"], "correct": 1, "explanation": "Gemini Flash is optimized for speed and cost. Use it for high-volume, simpler tasks. Use Claude Sonnet when the task requires deep reasoning and code quality."},
    ],
    # MongoDB vs PostgreSQL
    "d8447fae-a2fe-4f05-94f3-c27c600fd18b": [
        {"id": _id(), "question": "When should you choose PostgreSQL over MongoDB?", "options": ["Always", "When you have complex relationships and need JOINs, strict constraints, or SQL analytics", "For prototyping", "For document storage"], "correct": 1, "explanation": "PostgreSQL excels at relational data (JOINs), strict data integrity (constraints, foreign keys), and complex analytics queries (SQL)."},
    ],
    # Where AI Agents Are Heading
    "be3ebcad-8294-4cb0-b7cb-4943262bb210": [
        {"id": _id(), "question": "What is the 'verification problem' for autonomous agents?", "options": ["Verifying the user's identity", "As agents build complex systems, how do humans verify the output is correct?", "Verifying the model version", "Checking the network connection"], "correct": 1, "explanation": "As agents become more autonomous and build more complex systems, humans can't read every line of generated code. Verification at scale is an unsolved challenge."},
    ],
    # First AI Coding Session
    "faa447ea-8011-4636-b9f2-92bb8baa9d11": [
        {"id": _id(), "question": "What is the most productive pattern for working with an AI coding agent?", "options": ["Write detailed specs first", "Rapid iteration — describe, review, adjust, repeat", "Let the agent work autonomously", "Only use it for debugging"], "correct": 1, "explanation": "The most productive pattern is rapid iteration: describe what you want, review the result, describe changes, repeat. Each cycle takes 2-5 minutes."},
    ],
    # Communicating with AI Agents
    "1f1cb4f8-b5ed-45d8-9db0-1b4268c97bbf": [
        {"id": _id(), "question": "What makes a good bug report to an AI agent?", "options": ["Just say 'it's broken'", "What you did, what happened, what you expected, and any error messages", "A screenshot only", "The file path"], "correct": 1, "explanation": "A good bug report includes: what you did, what happened, what you expected, error messages, and when it started. This gives the agent enough context to investigate."},
    ],
    # AI Limitations
    "0e478094-8b66-40e0-9c35-17af77e9b64a": [
        {"id": _id(), "question": "Why can't LLMs know about very recent events?", "options": ["They choose not to", "They have a training data cutoff — knowledge only goes up to the training date", "They forget recent things", "The API filters them out"], "correct": 1, "explanation": "LLMs are trained on a fixed dataset with a cutoff date. Events after that date are unknown to the model unless retrieved via tools like web search."},
    ],
}

count = 0
for doc_id, questions in quizzes.items():
    add_quiz(doc_id, questions)
    count += 1

print(f"Added/updated quizzes for {count} documents")
total = db.quizzes.count_documents({})
print(f"Total quizzes in DB: {total}")
