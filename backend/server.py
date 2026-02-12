from fastapi import FastAPI, APIRouter, HTTPException, Depends, Header, Request, Response, Cookie
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
import re
from pathlib import Path
from pydantic import BaseModel
from typing import List, Optional
import uuid
from datetime import datetime, timezone, timedelta
import httpx

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

ADMIN_EMAIL = "chethan@emergent.sh"
EMERGENT_AUTH_URL = "https://demobackend.emergentagent.com/auth/v1/env/oauth/session-data"

app = FastAPI()
api_router = APIRouter(prefix="/api")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- Models ---
class CategoryCreate(BaseModel):
    name: str
    icon: str = "FileText"
    order: int = 0
    parent_id: Optional[str] = None

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    icon: Optional[str] = None
    order: Optional[int] = None

class DocumentCreate(BaseModel):
    title: str
    content: str = ""
    category_id: str
    order: int = 0
    tags: List[str] = []

class DocumentUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category_id: Optional[str] = None
    order: Optional[int] = None
    tags: Optional[List[str]] = None

class CommentCreate(BaseModel):
    content: str
    parent_id: Optional[str] = None

class ToolCreate(BaseModel):
    name: str
    url: str
    description: str = ""
    category: str = "General"

class ToolUpdate(BaseModel):
    name: Optional[str] = None
    url: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None

# --- Auth Helpers ---
async def get_current_user(request: Request, authorization: str = Header(None)):
    """Check session_token cookie first, then Authorization header."""
    session_token = request.cookies.get("session_token")
    if not session_token and authorization and authorization.startswith("Bearer "):
        session_token = authorization.split(" ")[1]
    if not session_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    session = await db.user_sessions.find_one({"session_token": session_token}, {"_id": 0})
    if not session:
        raise HTTPException(status_code=401, detail="Invalid session")
    expires_at = session.get("expires_at")
    if isinstance(expires_at, str):
        expires_at = datetime.fromisoformat(expires_at)
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    if expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=401, detail="Session expired")
    user = await db.users.find_one({"user_id": session["user_id"]}, {"_id": 0})
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

def is_admin(user: dict) -> bool:
    return user.get("role") == "admin" or user.get("email") == ADMIN_EMAIL

async def require_admin(user=Depends(get_current_user)):
    if not is_admin(user):
        raise HTTPException(status_code=403, detail="Admin access required")
    return user

# --- Auth Routes ---
@api_router.post("/auth/session")
async def create_session(request: Request):
    """Exchange session_id from Emergent Auth for a session_token."""
    body = await request.json()
    session_id = body.get("session_id")
    if not session_id:
        raise HTTPException(status_code=400, detail="session_id required")
    async with httpx.AsyncClient() as hc:
        resp = await hc.get(EMERGENT_AUTH_URL, headers={"X-Session-ID": session_id})
        if resp.status_code != 200:
            raise HTTPException(status_code=401, detail="Invalid session_id")
        data = resp.json()
    email = data.get("email", "")
    name = data.get("name", "")
    picture = data.get("picture", "")
    session_token = data.get("session_token", str(uuid.uuid4()))
    role = "admin" if email == ADMIN_EMAIL else "viewer"
    existing = await db.users.find_one({"email": email}, {"_id": 0})
    if existing:
        user_id = existing["user_id"]
        await db.users.update_one({"email": email}, {"$set": {"name": name, "picture": picture, "role": role}})
    else:
        user_id = f"user_{uuid.uuid4().hex[:12]}"
        await db.users.insert_one({
            "user_id": user_id, "email": email, "name": name, "picture": picture,
            "role": role, "created_at": datetime.now(timezone.utc).isoformat()
        })
    await db.user_sessions.delete_many({"user_id": user_id})
    await db.user_sessions.insert_one({
        "user_id": user_id, "session_token": session_token,
        "expires_at": (datetime.now(timezone.utc) + timedelta(days=7)).isoformat(),
        "created_at": datetime.now(timezone.utc).isoformat()
    })
    response = JSONResponse(content={
        "user": {"user_id": user_id, "email": email, "name": name, "picture": picture, "role": role}
    })
    response.set_cookie(
        key="session_token", value=session_token, path="/",
        httponly=True, secure=True, samesite="none", max_age=7*24*3600
    )
    return response

@api_router.get("/auth/me")
async def get_me(user=Depends(get_current_user)):
    return {
        "user_id": user["user_id"], "email": user["email"], "name": user["name"],
        "picture": user.get("picture", ""), "role": user.get("role", "viewer")
    }

@api_router.post("/auth/logout")
async def logout(request: Request):
    session_token = request.cookies.get("session_token")
    if session_token:
        await db.user_sessions.delete_many({"session_token": session_token})
    response = JSONResponse(content={"status": "logged out"})
    response.delete_cookie(key="session_token", path="/", samesite="none", secure=True)
    return response

# --- Categories Routes ---
@api_router.get("/categories")
async def get_categories(user=Depends(get_current_user)):
    cats = await db.categories.find({}, {"_id": 0}).sort("order", 1).to_list(1000)
    return cats

@api_router.post("/categories")
async def create_category(data: CategoryCreate, user=Depends(require_admin)):
    cat_id = str(uuid.uuid4())
    doc = {"id": cat_id, "name": data.name, "icon": data.icon, "order": data.order, "parent_id": data.parent_id}
    await db.categories.insert_one(doc)
    return {"id": cat_id, "name": data.name, "icon": data.icon, "order": data.order, "parent_id": data.parent_id}

@api_router.put("/categories/{cat_id}")
async def update_category(cat_id: str, data: CategoryUpdate, user=Depends(require_admin)):
    cat = await db.categories.find_one({"id": cat_id}, {"_id": 0})
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")
    update = {k: v for k, v in data.model_dump().items() if v is not None}
    if not update:
        return cat
    await db.categories.update_one({"id": cat_id}, {"$set": update})
    updated = await db.categories.find_one({"id": cat_id}, {"_id": 0})
    return updated

@api_router.delete("/categories/{cat_id}")
async def delete_category(cat_id: str, user=Depends(require_admin)):
    cat = await db.categories.find_one({"id": cat_id}, {"_id": 0})
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")
    children = await db.categories.count_documents({"parent_id": cat_id})
    docs = await db.documents.count_documents({"category_id": cat_id, "deleted": {"$ne": True}})
    if children > 0 or docs > 0:
        raise HTTPException(status_code=400, detail="Category has children or documents. Remove them first.")
    await db.categories.delete_one({"id": cat_id})
    return {"status": "deleted"}

# --- Documents Routes ---
@api_router.get("/documents")
async def get_documents(category_id: Optional[str] = None, user=Depends(get_current_user)):
    query = {"deleted": {"$ne": True}}
    if category_id:
        query["category_id"] = category_id
    docs = await db.documents.find(query, {"_id": 0}).sort("order", 1).to_list(1000)
    return docs

@api_router.get("/documents/{doc_id}")
async def get_document(doc_id: str, user=Depends(get_current_user)):
    doc = await db.documents.find_one({"id": doc_id, "deleted": {"$ne": True}}, {"_id": 0})
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc

@api_router.post("/documents")
async def create_document(data: DocumentCreate, user=Depends(require_admin)):
    doc_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    doc = {
        "id": doc_id, "title": data.title, "content": data.content,
        "category_id": data.category_id, "author_id": user["user_id"],
        "created_at": now, "updated_at": now, "order": data.order,
        "tags": data.tags, "deleted": False
    }
    await db.documents.insert_one(doc)
    return {k: v for k, v in doc.items() if k != "_id"}

@api_router.put("/documents/{doc_id}")
async def update_document(doc_id: str, data: DocumentUpdate, user=Depends(require_admin)):
    doc = await db.documents.find_one({"id": doc_id, "deleted": {"$ne": True}}, {"_id": 0})
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    version = {
        "id": str(uuid.uuid4()), "document_id": doc_id,
        "title": doc.get("title", ""), "content": doc.get("content", ""),
        "edited_by": user["user_id"], "created_at": datetime.now(timezone.utc).isoformat()
    }
    await db.doc_versions.insert_one(version)
    update = {k: v for k, v in data.model_dump().items() if v is not None}
    update["updated_at"] = datetime.now(timezone.utc).isoformat()
    await db.documents.update_one({"id": doc_id}, {"$set": update})
    updated = await db.documents.find_one({"id": doc_id}, {"_id": 0})
    return updated

@api_router.delete("/documents/{doc_id}")
async def soft_delete_document(doc_id: str, user=Depends(require_admin)):
    doc = await db.documents.find_one({"id": doc_id, "deleted": {"$ne": True}}, {"_id": 0})
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    await db.documents.update_one({"id": doc_id}, {"$set": {
        "deleted": True, "deleted_at": datetime.now(timezone.utc).isoformat(),
        "deleted_by": user["user_id"]
    }})
    return {"status": "moved to trash"}

@api_router.get("/trash")
async def get_trash(user=Depends(require_admin)):
    docs = await db.documents.find({"deleted": True}, {"_id": 0}).sort("deleted_at", -1).to_list(200)
    return docs

@api_router.post("/trash/{doc_id}/restore")
async def restore_document(doc_id: str, user=Depends(require_admin)):
    doc = await db.documents.find_one({"id": doc_id, "deleted": True}, {"_id": 0})
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found in trash")
    await db.documents.update_one({"id": doc_id}, {"$set": {"deleted": False}, "$unset": {"deleted_at": "", "deleted_by": ""}})
    return {"status": "restored"}

@api_router.delete("/trash/{doc_id}")
async def permanent_delete(doc_id: str, user=Depends(require_admin)):
    result = await db.documents.delete_one({"id": doc_id, "deleted": True})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Document not found in trash")
    await db.bookmarks.delete_many({"document_id": doc_id})
    await db.doc_versions.delete_many({"document_id": doc_id})
    await db.comments.delete_many({"document_id": doc_id})
    return {"status": "permanently deleted"}

@api_router.get("/documents/{doc_id}/versions")
async def get_document_versions(doc_id: str, user=Depends(get_current_user)):
    versions = await db.doc_versions.find({"document_id": doc_id}, {"_id": 0}).sort("created_at", -1).to_list(50)
    return versions

@api_router.get("/tags")
async def get_all_tags(user=Depends(get_current_user)):
    docs = await db.documents.find({"tags": {"$exists": True, "$ne": []}, "deleted": {"$ne": True}}, {"_id": 0, "tags": 1}).to_list(1000)
    all_tags = set()
    for d in docs:
        all_tags.update(d.get("tags", []))
    return sorted(list(all_tags))

# --- Comments Routes (Threaded) ---
@api_router.get("/documents/{doc_id}/comments")
async def get_comments(doc_id: str, user=Depends(get_current_user)):
    comments = await db.comments.find({"document_id": doc_id}, {"_id": 0}).sort("created_at", 1).to_list(500)
    return comments

@api_router.post("/documents/{doc_id}/comments")
async def add_comment(doc_id: str, data: CommentCreate, user=Depends(get_current_user)):
    comment_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    comment = {
        "id": comment_id, "document_id": doc_id, "content": data.content,
        "parent_id": data.parent_id, "user_id": user["user_id"],
        "user_name": user["name"], "user_picture": user.get("picture", ""),
        "upvotes": [], "created_at": now, "updated_at": now
    }
    await db.comments.insert_one(comment)
    return {k: v for k, v in comment.items() if k != "_id"}

@api_router.post("/comments/{comment_id}/upvote")
async def toggle_upvote(comment_id: str, user=Depends(get_current_user)):
    comment = await db.comments.find_one({"id": comment_id}, {"_id": 0})
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    upvotes = comment.get("upvotes", [])
    uid = user["user_id"]
    if uid in upvotes:
        upvotes.remove(uid)
    else:
        upvotes.append(uid)
    await db.comments.update_one({"id": comment_id}, {"$set": {"upvotes": upvotes}})
    return {"upvotes": upvotes}

@api_router.delete("/comments/{comment_id}")
async def delete_comment(comment_id: str, user=Depends(get_current_user)):
    comment = await db.comments.find_one({"id": comment_id}, {"_id": 0})
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if comment["user_id"] != user["user_id"] and not is_admin(user):
        raise HTTPException(status_code=403, detail="Can only delete your own comments")
    await db.comments.delete_one({"id": comment_id})
    await db.comments.delete_many({"parent_id": comment_id})
    return {"status": "deleted"}

# --- Public Sharing ---
@api_router.post("/documents/{doc_id}/share")
async def toggle_share(doc_id: str, user=Depends(require_admin)):
    doc = await db.documents.find_one({"id": doc_id, "deleted": {"$ne": True}}, {"_id": 0})
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    share_id = doc.get("share_id")
    if share_id:
        await db.documents.update_one({"id": doc_id}, {"$unset": {"share_id": ""}})
        return {"shared": False, "share_id": None}
    new_share_id = uuid.uuid4().hex[:10]
    await db.documents.update_one({"id": doc_id}, {"$set": {"share_id": new_share_id}})
    return {"shared": True, "share_id": new_share_id}

@api_router.get("/public/{share_id}")
async def get_public_document(share_id: str):
    """No auth required - public endpoint."""
    doc = await db.documents.find_one({"share_id": share_id, "deleted": {"$ne": True}}, {"_id": 0})
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found or not shared")
    return {"title": doc["title"], "content": doc["content"], "tags": doc.get("tags", []),
            "updated_at": doc.get("updated_at", ""), "author_id": doc.get("author_id", "")}

# --- Tools Directory ---
@api_router.get("/tools")
async def get_tools(user=Depends(get_current_user)):
    tools = await db.tools.find({}, {"_id": 0}).sort("category", 1).to_list(200)
    return tools

@api_router.post("/tools")
async def create_tool(data: ToolCreate, user=Depends(require_admin)):
    tool_id = str(uuid.uuid4())
    tool = {"id": tool_id, "name": data.name, "url": data.url, "description": data.description,
            "category": data.category, "created_at": datetime.now(timezone.utc).isoformat()}
    await db.tools.insert_one(tool)
    return {k: v for k, v in tool.items() if k != "_id"}

@api_router.put("/tools/{tool_id}")
async def update_tool(tool_id: str, data: ToolUpdate, user=Depends(require_admin)):
    tool = await db.tools.find_one({"id": tool_id}, {"_id": 0})
    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")
    update = {k: v for k, v in data.model_dump().items() if v is not None}
    await db.tools.update_one({"id": tool_id}, {"$set": update})
    updated = await db.tools.find_one({"id": tool_id}, {"_id": 0})
    return updated

@api_router.delete("/tools/{tool_id}")
async def delete_tool(tool_id: str, user=Depends(require_admin)):
    result = await db.tools.delete_one({"id": tool_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Tool not found")
    return {"status": "deleted"}

# --- Bookmarks Routes ---
@api_router.get("/bookmarks")
async def get_bookmarks(user=Depends(get_current_user)):
    bms = await db.bookmarks.find({"user_id": user["user_id"]}, {"_id": 0}).to_list(1000)
    doc_ids = [b["document_id"] for b in bms]
    docs = await db.documents.find({"id": {"$in": doc_ids}, "deleted": {"$ne": True}}, {"_id": 0}).to_list(1000)
    return {"bookmarks": bms, "documents": docs}

@api_router.post("/bookmarks/{doc_id}")
async def toggle_bookmark(doc_id: str, user=Depends(get_current_user)):
    existing = await db.bookmarks.find_one({"user_id": user["user_id"], "document_id": doc_id})
    if existing:
        await db.bookmarks.delete_one({"user_id": user["user_id"], "document_id": doc_id})
        return {"bookmarked": False}
    bm = {"id": str(uuid.uuid4()), "user_id": user["user_id"], "document_id": doc_id,
          "created_at": datetime.now(timezone.utc).isoformat()}
    await db.bookmarks.insert_one(bm)
    return {"bookmarked": True}

# --- Search Route (fuzzy, case-insensitive, searches headings too) ---
@api_router.get("/search")
async def search_documents(q: str = "", user=Depends(get_current_user)):
    if not q or len(q) < 1:
        return []
    escaped = re.escape(q)
    fuzzy_pattern = ".*".join(list(escaped))
    query = {"deleted": {"$ne": True}, "$or": [
        {"title": {"$regex": fuzzy_pattern, "$options": "i"}},
        {"content": {"$regex": fuzzy_pattern, "$options": "i"}}
    ]}
    docs = await db.documents.find(query, {"_id": 0}).to_list(50)
    results = []
    for d in docs:
        snippet = ""
        content = d.get("content", "")
        # Search in headings and content
        lines = content.split("\n")
        heading_match = None
        for line in lines:
            if line.startswith("#") and q.lower() in line.lower():
                heading_match = line.lstrip("#").strip()
                break
        if heading_match:
            snippet = f"Section: {heading_match}"
        else:
            idx = content.lower().find(q.lower())
            if idx >= 0:
                start = max(0, idx - 60)
                end = min(len(content), idx + len(q) + 60)
                snippet = ("..." if start > 0 else "") + content[start:end].replace("\n", " ") + ("..." if end < len(content) else "")
        results.append({"id": d["id"], "title": d["title"], "category_id": d.get("category_id", ""), "snippet": snippet, "tags": d.get("tags", [])})
    return results

# --- AI Chatbot ---
class ChatRequest(BaseModel):
    message: str
    session_id: str
    doc_id: Optional[str] = None

@api_router.post("/chat")
async def chat_with_ai(data: ChatRequest, user=Depends(get_current_user)):
    from emergentintegrations.llm.chat import LlmChat, UserMessage
    # Build context from documents
    context_parts = []
    if data.doc_id:
        doc = await db.documents.find_one({"id": data.doc_id, "deleted": {"$ne": True}}, {"_id": 0})
        if doc:
            context_parts.append(f"Current document: {doc['title']}\n{doc['content'][:3000]}")
    # Also get top relevant docs via keyword search from message
    words = data.message.split()[:5]
    search_q = " ".join(words)
    if search_q:
        query = {"deleted": {"$ne": True}, "$or": [
            {"title": {"$regex": search_q, "$options": "i"}},
            {"content": {"$regex": search_q, "$options": "i"}}
        ]}
        related = await db.documents.find(query, {"_id": 0, "title": 1, "content": 1}).to_list(3)
        for r in related:
            context_parts.append(f"Related doc: {r['title']}\n{r['content'][:1500]}")
    if not context_parts:
        all_docs = await db.documents.find({"deleted": {"$ne": True}}, {"_id": 0, "title": 1}).to_list(100)
        titles = ", ".join([d["title"] for d in all_docs])
        context_parts.append(f"Available documents: {titles}")
    context = "\n\n---\n\n".join(context_parts)
    system = f"""You are the Emergent Knowledge Hub AI assistant. Answer questions about the documentation.
Be concise, accurate, and helpful. Reference specific document names when possible.
If you don't know something, say so honestly.

Documentation context:
{context}"""
    try:
        api_key = os.environ.get("EMERGENT_LLM_KEY")
        chat = LlmChat(api_key=api_key, session_id=data.session_id, system_message=system)
        chat.with_model("anthropic", "claude-sonnet-4-5-20250929")
        user_msg = UserMessage(text=data.message)
        response = await chat.send_message(user_msg)
        # Store in DB for history
        chat_msg_id = str(uuid.uuid4())
        await db.chat_messages.insert_one({
            "id": chat_msg_id,
            "session_id": data.session_id, "user_id": user["user_id"],
            "user_message": data.message, "ai_response": response,
            "doc_id": data.doc_id, "created_at": datetime.now(timezone.utc).isoformat()
        })
        return {"response": response}
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/chat/history/{session_id}")
async def get_chat_history(session_id: str, user=Depends(get_current_user)):
    messages = await db.chat_messages.find({"session_id": session_id, "user_id": user["user_id"]}, {"_id": 0}).sort("created_at", 1).to_list(100)
    return messages

# --- Seed Route ---
@api_router.post("/seed")
async def seed_data():
    existing = await db.categories.count_documents({})
    if existing > 0:
        return {"status": "already_seeded", "categories": existing}
    from seed_data import CATEGORIES, DOCUMENTS
    for cat in CATEGORIES:
        await db.categories.insert_one(dict(cat))
    for doc in DOCUMENTS:
        d = dict(doc)
        d["deleted"] = False
        await db.documents.insert_one(d)
    await db.categories.create_index("parent_id")
    await db.documents.create_index("category_id")
    return {"status": "seeded", "categories": len(CATEGORIES), "documents": len(DOCUMENTS)}

@api_router.get("/")
async def root():
    return {"message": "Emergent Knowledge Hub API"}

app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
