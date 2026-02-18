from fastapi import FastAPI, APIRouter, HTTPException, Depends, Header, Request, Response, Cookie, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
import re
import json
import asyncio
from pathlib import Path
from pydantic import BaseModel
from typing import List, Optional, Dict, Set
import uuid
from datetime import datetime, timezone, timedelta

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

ADMIN_EMAIL = "chethan@emergent.sh"

app = FastAPI()
api_router = APIRouter(prefix="/api")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- WebSocket Collaboration Manager ---
class CollabManager:
    def __init__(self):
        # doc_id -> {user_id: {"ws": WebSocket, "name": str, "color": str, "mode": str, "cursor": int}}
        self.rooms: Dict[str, Dict[str, dict]] = {}

    async def connect(self, doc_id: str, user_id: str, user_name: str, color: str, ws: WebSocket):
        await ws.accept()
        if doc_id not in self.rooms:
            self.rooms[doc_id] = {}
        self.rooms[doc_id][user_id] = {"ws": ws, "name": user_name, "color": color, "mode": "viewing", "cursor": 0}
        await self.broadcast_presence(doc_id)

    def disconnect(self, doc_id: str, user_id: str):
        if doc_id in self.rooms:
            self.rooms[doc_id].pop(user_id, None)
            if not self.rooms[doc_id]:
                del self.rooms[doc_id]

    def get_presence(self, doc_id: str) -> list:
        if doc_id not in self.rooms:
            return []
        return [{"user_id": uid, "name": u["name"], "color": u["color"], "mode": u["mode"], "cursor": u["cursor"]}
                for uid, u in self.rooms[doc_id].items()]

    async def broadcast_presence(self, doc_id: str):
        presence = self.get_presence(doc_id)
        await self._broadcast(doc_id, {"type": "presence", "users": presence})

    async def broadcast_content(self, doc_id: str, sender_id: str, content: str, cursor: int):
        if doc_id in self.rooms and sender_id in self.rooms[doc_id]:
            self.rooms[doc_id][sender_id]["cursor"] = cursor
        msg = {"type": "content_update", "sender_id": sender_id, "content": content, "cursor": cursor}
        await self._broadcast(doc_id, msg, exclude=sender_id)

    async def broadcast_cursor(self, doc_id: str, sender_id: str, cursor: int, selection_end: int):
        if doc_id in self.rooms and sender_id in self.rooms[doc_id]:
            self.rooms[doc_id][sender_id]["cursor"] = cursor
        msg = {"type": "cursor_update", "sender_id": sender_id, "cursor": cursor, "selection_end": selection_end}
        await self._broadcast(doc_id, msg, exclude=sender_id)

    async def set_mode(self, doc_id: str, user_id: str, mode: str):
        if doc_id in self.rooms and user_id in self.rooms[doc_id]:
            self.rooms[doc_id][user_id]["mode"] = mode
            await self.broadcast_presence(doc_id)

    async def broadcast_saved(self, doc_id: str, sender_id: str):
        await self._broadcast(doc_id, {"type": "doc_saved", "sender_id": sender_id})

    async def _broadcast(self, doc_id: str, message: dict, exclude: str = None):
        if doc_id not in self.rooms:
            return
        dead = []
        for uid, u in self.rooms[doc_id].items():
            if uid == exclude:
                continue
            try:
                await u["ws"].send_json(message)
            except Exception:
                dead.append(uid)
        for uid in dead:
            self.rooms[doc_id].pop(uid, None)

collab = CollabManager()

# --- Models ---
class UserRegister(BaseModel):
    email: str
    name: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

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

class InviteCreate(BaseModel):
    email: str
    role: str = "viewer"

class UserRoleUpdate(BaseModel):
    role: str

# --- Auth Helpers (no login required) ---
DEFAULT_USER = {"user_id": "default", "email": "admin@emergent.sh", "name": "Admin", "role": "admin", "picture": ""}

async def get_current_user(request: Request = None, authorization: str = Header(None)):
    return DEFAULT_USER

def is_admin(user: dict) -> bool:
    return True

async def require_admin(user=Depends(get_current_user)):
    return user

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

# --- Collaboration Presence ---
@api_router.get("/documents/{doc_id}/presence")
async def get_document_presence(doc_id: str):
    return collab.get_presence(doc_id)

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
    # Log search query for analytics
    await db.search_logs.insert_one({"query": q, "searched_at": datetime.now(timezone.utc).isoformat()})
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
    context_parts = []
    # If on a specific doc, include its FULL content
    if data.doc_id:
        doc = await db.documents.find_one({"id": data.doc_id, "deleted": {"$ne": True}}, {"_id": 0})
        if doc:
            context_parts.append(f"CURRENT DOCUMENT: {doc['title']}\n{doc['content'][:6000]}")
    # Search for relevant docs using individual keywords from the message
    keywords = [w for w in data.message.split() if len(w) > 2]
    matched_ids = set()
    for kw in keywords[:8]:
        escaped_kw = re.escape(kw)
        query = {"deleted": {"$ne": True}, "$or": [
            {"title": {"$regex": escaped_kw, "$options": "i"}},
            {"content": {"$regex": escaped_kw, "$options": "i"}}
        ]}
        docs = await db.documents.find(query, {"_id": 0, "id": 1, "title": 1, "content": 1}).to_list(5)
        for d in docs:
            if d["id"] not in matched_ids:
                matched_ids.add(d["id"])
                context_parts.append(f"RELATED DOC: {d['title']}\n{d['content'][:4000]}")
            if len(matched_ids) >= 5:
                break
        if len(matched_ids) >= 5:
            break
    # If still no context, provide doc titles as overview
    if not context_parts:
        all_docs = await db.documents.find({"deleted": {"$ne": True}}, {"_id": 0, "title": 1, "content": 1}).to_list(100)
        for d in all_docs[:10]:
            context_parts.append(f"DOC: {d['title']}\n{d['content'][:2000]}")
    context = "\n\n---\n\n".join(context_parts[:6])
    system = f"""You are the Emergent Knowledge Hub AI assistant. You have deep knowledge of the Emergent platform documentation.

IMPORTANT RULES:
- Answer ONLY based on the documentation context provided below
- Be detailed and thorough - include specific technical details from the docs
- Reference document names when citing information
- If the docs contain mermaid diagrams or tables, describe them in text
- If asked about system architecture, explain the FULL flow: User -> Frontend -> Agent Service -> E1 Orchestrator -> LLM/Tools/Subagents -> Response
- Never make up information not in the docs

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

# --- Invite / User Management ---
@api_router.get("/users")
async def list_users(user=Depends(require_admin)):
    users = await db.users.find({}, {"_id": 0, "user_id": 1, "email": 1, "name": 1, "role": 1, "picture": 1, "created_at": 1}).to_list(500)
    return users

@api_router.post("/invite")
async def invite_user(data: InviteCreate, user=Depends(require_admin)):
    existing = await db.users.find_one({"email": data.email}, {"_id": 0})
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")
    if data.role not in ("admin", "viewer"):
        raise HTTPException(status_code=400, detail="Role must be admin or viewer")
    user_id = f"user_{uuid.uuid4().hex[:12]}"
    new_user = {
        "user_id": user_id, "email": data.email, "name": data.email.split("@")[0],
        "picture": "", "role": data.role, "invited_by": user["user_id"],
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    await db.users.insert_one(new_user)
    return {k: v for k, v in new_user.items() if k != "_id"}

@api_router.put("/users/{user_id}/role")
async def update_user_role(user_id: str, data: UserRoleUpdate, user=Depends(require_admin)):
    target = await db.users.find_one({"user_id": user_id}, {"_id": 0})
    if not target:
        raise HTTPException(status_code=404, detail="User not found")
    if data.role not in ("admin", "viewer"):
        raise HTTPException(status_code=400, detail="Role must be admin or viewer")
    await db.users.update_one({"user_id": user_id}, {"$set": {"role": data.role}})
    return {"user_id": user_id, "role": data.role}

@api_router.delete("/users/{user_id}")
async def remove_user(user_id: str, user=Depends(require_admin)):
    if user_id == user["user_id"]:
        raise HTTPException(status_code=400, detail="Cannot remove yourself")
    result = await db.users.delete_one({"user_id": user_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    await db.user_sessions.delete_many({"user_id": user_id})
    return {"status": "removed"}

# --- Document Templates ---
TEMPLATES = [
    {"id": "api-doc", "name": "API Documentation", "icon": "Server",
     "content": "# API Name\n\n## Overview\nBrief description of the API.\n\n## Base URL\n`https://api.example.com/v1`\n\n## Authentication\nDescribe auth method.\n\n## Endpoints\n\n### GET /resource\n**Description:** Fetch resource.\n\n| Parameter | Type | Required | Description |\n|-----------|------|----------|-------------|\n| id | string | yes | Resource ID |\n\n**Response:**\n```json\n{\"id\": \"123\", \"name\": \"example\"}\n```\n\n## Error Codes\n\n| Code | Description |\n|------|-------------|\n| 400 | Bad request |\n| 401 | Unauthorized |\n| 404 | Not found |\n| 500 | Server error |\n"},
    {"id": "runbook", "name": "Runbook", "icon": "Rocket",
     "content": "# Runbook: Service Name\n\n## Overview\nWhat this runbook covers.\n\n## Prerequisites\n- Access to production environment\n- Required permissions\n\n## Procedure\n\n### Step 1: Verify the Issue\n1. Check monitoring dashboard\n2. Review recent deployments\n3. Check error logs\n\n### Step 2: Diagnose\n1. SSH into the affected server\n2. Run diagnostic commands\n3. Identify root cause\n\n### Step 3: Remediate\n1. Apply the fix\n2. Verify the fix\n3. Monitor for 15 minutes\n\n## Rollback Plan\nIf the fix fails:\n1. Revert the change\n2. Notify on-call team\n3. Escalate if needed\n\n## Contacts\n| Role | Name | Contact |\n|------|------|---------|\n| On-call | TBD | TBD |\n| Escalation | TBD | TBD |\n"},
    {"id": "rca", "name": "Root Cause Analysis", "icon": "Search",
     "content": "# RCA: Incident Title\n\n## Incident Summary\n| Field | Detail |\n|-------|--------|\n| Date | YYYY-MM-DD |\n| Duration | X hours |\n| Severity | P1/P2/P3 |\n| Impact | Description of impact |\n\n## Timeline\n| Time | Event |\n|------|-------|\n| HH:MM | Issue detected |\n| HH:MM | Investigation started |\n| HH:MM | Root cause identified |\n| HH:MM | Fix deployed |\n| HH:MM | Resolved |\n\n## Root Cause\nDetailed explanation of what went wrong.\n\n## Contributing Factors\n- Factor 1\n- Factor 2\n\n## Resolution\nWhat was done to fix the issue.\n\n## Action Items\n| Action | Owner | Due Date | Status |\n|--------|-------|----------|--------|\n| Action 1 | TBD | TBD | Open |\n| Action 2 | TBD | TBD | Open |\n\n## Lessons Learned\n- Lesson 1\n- Lesson 2\n"},
    {"id": "meeting-notes", "name": "Meeting Notes", "icon": "MessageSquare",
     "content": "# Meeting: Title\n\n## Details\n| Field | Value |\n|-------|-------|\n| Date | YYYY-MM-DD |\n| Attendees | Name 1, Name 2 |\n| Facilitator | Name |\n\n## Agenda\n1. Topic 1\n2. Topic 2\n3. Topic 3\n\n## Discussion Notes\n\n### Topic 1\n- Key point discussed\n- Decision made\n\n### Topic 2\n- Key point discussed\n- Decision made\n\n## Action Items\n| Action | Owner | Due Date |\n|--------|-------|----------|\n| Action 1 | Name | Date |\n| Action 2 | Name | Date |\n\n## Next Meeting\nDate and time of next meeting.\n"},
    {"id": "test-plan", "name": "Test Plan", "icon": "Check",
     "content": "# Test Plan: Feature Name\n\n## Objective\nWhat this test plan covers.\n\n## Scope\n- In scope: Feature X, Feature Y\n- Out of scope: Feature Z\n\n## Test Cases\n\n### TC-001: Basic Flow\n| Field | Detail |\n|-------|--------|\n| Priority | High |\n| Preconditions | User is logged in |\n\n**Steps:**\n1. Navigate to page\n2. Perform action\n3. Verify result\n\n**Expected Result:** Description of expected outcome.\n\n### TC-002: Error Handling\n| Field | Detail |\n|-------|--------|\n| Priority | Medium |\n| Preconditions | User is logged in |\n\n**Steps:**\n1. Navigate to page\n2. Trigger error condition\n3. Verify error handling\n\n**Expected Result:** Appropriate error message shown.\n\n## Test Environment\n- Browser: Chrome latest\n- OS: macOS/Windows\n- Backend: Staging\n"},
]

@api_router.get("/templates")
async def get_templates(user=Depends(get_current_user)):
    return TEMPLATES

# --- Tag Suggestions ---
@api_router.get("/tags/suggestions")
async def get_tag_suggestions(q: str = "", user=Depends(get_current_user)):
    all_tags = await get_all_tags(user)
    if not q:
        return all_tags[:20]
    q_lower = q.lower()
    return [t for t in all_tags if q_lower in t.lower()][:10]

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

# --- Document View Tracking ---
@api_router.post("/documents/{doc_id}/view")
async def track_document_view(doc_id: str):
    doc = await db.documents.find_one({"id": doc_id, "deleted": {"$ne": True}}, {"_id": 0, "title": 1})
    await db.doc_views.insert_one({
        "document_id": doc_id,
        "title": doc.get("title", "Unknown") if doc else "Unknown",
        "viewed_at": datetime.now(timezone.utc).isoformat()
    })
    return {"status": "tracked"}

# --- Analytics ---
@api_router.get("/analytics/overview")
async def analytics_overview(user=Depends(require_admin)):
    total_docs = await db.documents.count_documents({"deleted": {"$ne": True}})
    total_categories = await db.categories.count_documents({})
    total_views = await db.doc_views.count_documents({})
    total_chats = await db.chat_messages.count_documents({})
    total_searches = await db.search_logs.count_documents({})
    total_comments = await db.comments.count_documents({})
    # Views in last 7 days
    week_ago = (datetime.now(timezone.utc) - timedelta(days=7)).isoformat()
    views_7d = await db.doc_views.count_documents({"viewed_at": {"$gte": week_ago}})
    chats_7d = await db.chat_messages.count_documents({"created_at": {"$gte": week_ago}})
    return {
        "total_docs": total_docs, "total_categories": total_categories,
        "total_views": total_views, "total_chats": total_chats,
        "total_searches": total_searches, "total_comments": total_comments,
        "views_7d": views_7d, "chats_7d": chats_7d
    }

@api_router.get("/analytics/popular-docs")
async def analytics_popular_docs(user=Depends(require_admin)):
    pipeline = [
        {"$group": {"_id": "$document_id", "views": {"$sum": 1}, "stored_title": {"$first": "$title"}}},
        {"$sort": {"views": -1}},
        {"$limit": 15}
    ]
    results = await db.doc_views.aggregate(pipeline).to_list(15)
    # Enrich with current doc titles, fallback to stored title
    doc_ids = [r["_id"] for r in results]
    docs = await db.documents.find({"id": {"$in": doc_ids}}, {"_id": 0, "id": 1, "title": 1, "category_id": 1}).to_list(100)
    doc_map = {d["id"]: d for d in docs}
    output = []
    for r in results:
        doc_id = r["_id"]
        if doc_id in doc_map:
            # Document exists - use current title
            output.append({"doc_id": doc_id, "views": r["views"],
                          "title": doc_map[doc_id].get("title", "Unknown"),
                          "category_id": doc_map[doc_id].get("category_id", "")})
        else:
            # Document deleted/doesn't exist - show "[Deleted document]"
            stored = r.get("stored_title")
            title = "[Deleted document]" if not stored or stored == "Unknown" else stored
            output.append({"doc_id": doc_id, "views": r["views"],
                          "title": title, "category_id": ""})
    return output

@api_router.get("/analytics/searches")
async def analytics_searches(user=Depends(require_admin)):
    pipeline = [
        {"$group": {"_id": "$query", "count": {"$sum": 1}, "last_searched": {"$max": "$searched_at"}}},
        {"$sort": {"count": -1}},
        {"$limit": 20}
    ]
    results = await db.search_logs.aggregate(pipeline).to_list(20)
    return [{"query": r["_id"], "count": r["count"], "last_searched": r.get("last_searched", "")} for r in results]

@api_router.get("/analytics/chatbot")
async def analytics_chatbot(user=Depends(require_admin)):
    total = await db.chat_messages.count_documents({})
    # Group by day for last 14 days
    two_weeks_ago = (datetime.now(timezone.utc) - timedelta(days=14)).isoformat()
    pipeline = [
        {"$match": {"created_at": {"$gte": two_weeks_ago}}},
        {"$project": {"day": {"$substr": ["$created_at", 0, 10]}}},
        {"$group": {"_id": "$day", "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}}
    ]
    daily = await db.chat_messages.aggregate(pipeline).to_list(14)
    # Recent questions
    recent = await db.chat_messages.find({}, {"_id": 0, "user_message": 1, "created_at": 1, "doc_id": 1}).sort("created_at", -1).to_list(10)
    return {"total": total, "daily": [{"date": d["_id"], "count": d["count"]} for d in daily],
            "recent": [{"question": r.get("user_message", ""), "asked_at": r.get("created_at", ""), "doc_id": r.get("doc_id")} for r in recent]}

@api_router.get("/analytics/activity")
async def analytics_activity(user=Depends(require_admin)):
    # Recent document changes
    recent_docs = await db.documents.find({"deleted": {"$ne": True}}, {"_id": 0, "id": 1, "title": 1, "updated_at": 1, "created_at": 1}).sort("updated_at", -1).to_list(10)
    # Recent comments
    recent_comments = await db.comments.find({}, {"_id": 0, "id": 1, "content": 1, "user_name": 1, "document_id": 1, "created_at": 1}).sort("created_at", -1).to_list(10)
    return {"recent_docs": recent_docs, "recent_comments": recent_comments}

@api_router.get("/")
async def root():
    return {"message": "Emergent Knowledge Hub API"}

app.include_router(api_router)

# --- WebSocket Collaboration Endpoint (must be on app, not router) ---
@app.websocket("/api/ws/collab/{doc_id}")
async def ws_collab(ws: WebSocket, doc_id: str):
    user_id = ws.query_params.get("user_id", str(uuid.uuid4()))
    user_name = ws.query_params.get("name", "Anonymous")
    color = ws.query_params.get("color", "#6366f1")
    await collab.connect(doc_id, user_id, user_name, color, ws)
    try:
        while True:
            data = await ws.receive_json()
            msg_type = data.get("type")
            if msg_type == "content_update":
                await collab.broadcast_content(doc_id, user_id, data.get("content", ""), data.get("cursor", 0))
            elif msg_type == "cursor_update":
                await collab.broadcast_cursor(doc_id, user_id, data.get("cursor", 0), data.get("selection_end", 0))
            elif msg_type == "mode_change":
                await collab.set_mode(doc_id, user_id, data.get("mode", "viewing"))
            elif msg_type == "save":
                # Auto-save: persist to DB
                content = data.get("content")
                title = data.get("title")
                if content is not None or title is not None:
                    doc = await db.documents.find_one({"id": doc_id, "deleted": {"$ne": True}}, {"_id": 0})
                    if doc:
                        version = {"id": str(uuid.uuid4()), "document_id": doc_id,
                                   "title": doc.get("title", ""), "content": doc.get("content", ""),
                                   "edited_by": user_id, "created_at": datetime.now(timezone.utc).isoformat()}
                        await db.doc_versions.insert_one(version)
                        update = {"updated_at": datetime.now(timezone.utc).isoformat()}
                        if content is not None:
                            update["content"] = content
                        if title is not None:
                            update["title"] = title
                        await db.documents.update_one({"id": doc_id}, {"$set": update})
                        await collab.broadcast_saved(doc_id, user_id)
    except WebSocketDisconnect:
        pass
    except Exception as e:
        logger.error(f"WebSocket error for doc {doc_id}: {e}")
    finally:
        collab.disconnect(doc_id, user_id)
        await collab.broadcast_presence(doc_id)

# CORS: When credentials are used, origin must not be wildcard
origins = os.environ.get('CORS_ORIGINS', '*').split(',')
if origins == ['*']:
    # Raw ASGI middleware to handle CORS without breaking WebSocket
    from starlette.types import ASGIApp, Receive, Scope, Send
    from starlette.responses import Response as StarletteResponse

    class DynamicCORSMiddleware:
        def __init__(self, app: ASGIApp):
            self.app = app

        async def __call__(self, scope: Scope, receive: Receive, send: Send):
            if scope["type"] == "websocket":
                await self.app(scope, receive, send)
                return
            if scope["type"] != "http":
                await self.app(scope, receive, send)
                return
            headers_list = dict(scope.get("headers", []))  # noqa: F841
            origin = ""
            for k, v in scope.get("headers", []):
                if k == b"origin":
                    origin = v.decode()
                    break
            method = scope.get("method", "")
            if method == "OPTIONS":
                resp = StarletteResponse(status_code=200)
                resp.headers["Access-Control-Allow-Origin"] = origin or "*"
                resp.headers["Access-Control-Allow-Credentials"] = "true"
                resp.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS, HEAD, PATCH"
                resp.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, Cookie"
                await resp(scope, receive, send)
                return

            async def send_with_cors(message):
                if message["type"] == "http.response.start":
                    headers = dict(message.get("headers", []))  # noqa: F841
                    extra = [
                        (b"access-control-allow-origin", (origin or "*").encode()),
                        (b"access-control-allow-credentials", b"true"),
                        (b"access-control-allow-methods", b"GET, POST, PUT, DELETE, OPTIONS, HEAD, PATCH"),
                        (b"access-control-allow-headers", b"Content-Type, Authorization, Cookie"),
                    ]
                    message["headers"] = list(message.get("headers", [])) + extra
                await send(message)

            await self.app(scope, receive, send_with_cors)

    app.add_middleware(DynamicCORSMiddleware)
else:
    app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_origins=origins,
        allow_methods=["*"],
        allow_headers=["*"],
    )

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
