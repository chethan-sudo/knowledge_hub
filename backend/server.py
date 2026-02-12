from fastapi import FastAPI, APIRouter, HTTPException, Depends, Header
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
import uuid
from datetime import datetime, timezone
import bcrypt
import jwt

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]
JWT_SECRET = os.environ.get('JWT_SECRET', 'fallback_secret')

app = FastAPI()
api_router = APIRouter(prefix="/api")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- Models ---
class UserCreate(BaseModel):
    email: str
    name: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    name: str

class CategoryCreate(BaseModel):
    name: str
    icon: str = "FileText"
    order: int = 0
    parent_id: Optional[str] = None

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    icon: Optional[str] = None
    order: Optional[int] = None

class CategoryResponse(BaseModel):
    id: str
    name: str
    icon: str
    order: int
    parent_id: Optional[str] = None

class DocumentCreate(BaseModel):
    title: str
    content: str = ""
    category_id: str
    order: int = 0

class DocumentUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category_id: Optional[str] = None
    order: Optional[int] = None

class DocumentResponse(BaseModel):
    id: str
    title: str
    content: str
    category_id: str
    author_id: str
    created_at: str
    updated_at: str
    order: int

class BookmarkResponse(BaseModel):
    id: str
    user_id: str
    document_id: str
    created_at: str

# --- Auth Helpers ---
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def create_token(user_id: str, email: str) -> str:
    return jwt.encode({"user_id": user_id, "email": email}, JWT_SECRET, algorithm="HS256")

async def get_current_user(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    token = authorization.split(" ")[1]
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user = await db.users.find_one({"id": payload["user_id"]}, {"_id": 0})
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# --- Auth Routes ---
@api_router.post("/auth/register")
async def register(data: UserCreate):
    existing = await db.users.find_one({"email": data.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user_id = str(uuid.uuid4())
    user_doc = {
        "id": user_id,
        "email": data.email,
        "name": data.name,
        "password_hash": hash_password(data.password),
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    await db.users.insert_one(user_doc)
    token = create_token(user_id, data.email)
    return {"token": token, "user": {"id": user_id, "email": data.email, "name": data.name}}

@api_router.post("/auth/login")
async def login(data: UserLogin):
    user = await db.users.find_one({"email": data.email}, {"_id": 0})
    if not user or not verify_password(data.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_token(user["id"], user["email"])
    return {"token": token, "user": {"id": user["id"], "email": user["email"], "name": user["name"]}}

@api_router.get("/auth/me")
async def get_me(user=Depends(get_current_user)):
    return {"id": user["id"], "email": user["email"], "name": user["name"]}

# --- Categories Routes ---
@api_router.get("/categories")
async def get_categories(user=Depends(get_current_user)):
    cats = await db.categories.find({}, {"_id": 0}).sort("order", 1).to_list(1000)
    return cats

@api_router.post("/categories")
async def create_category(data: CategoryCreate, user=Depends(get_current_user)):
    cat_id = str(uuid.uuid4())
    doc = {"id": cat_id, "name": data.name, "icon": data.icon, "order": data.order, "parent_id": data.parent_id}
    await db.categories.insert_one(doc)
    return {"id": cat_id, "name": data.name, "icon": data.icon, "order": data.order, "parent_id": data.parent_id}

# --- Documents Routes ---
@api_router.get("/documents")
async def get_documents(category_id: Optional[str] = None, user=Depends(get_current_user)):
    query = {}
    if category_id:
        query["category_id"] = category_id
    docs = await db.documents.find(query, {"_id": 0}).sort("order", 1).to_list(1000)
    return docs

@api_router.get("/documents/{doc_id}")
async def get_document(doc_id: str, user=Depends(get_current_user)):
    doc = await db.documents.find_one({"id": doc_id}, {"_id": 0})
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc

@api_router.post("/documents")
async def create_document(data: DocumentCreate, user=Depends(get_current_user)):
    doc_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    doc = {
        "id": doc_id, "title": data.title, "content": data.content,
        "category_id": data.category_id, "author_id": user["id"],
        "created_at": now, "updated_at": now, "order": data.order
    }
    await db.documents.insert_one(doc)
    return {k: v for k, v in doc.items() if k != "_id"}

@api_router.put("/documents/{doc_id}")
async def update_document(doc_id: str, data: DocumentUpdate, user=Depends(get_current_user)):
    doc = await db.documents.find_one({"id": doc_id}, {"_id": 0})
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    update = {k: v for k, v in data.model_dump().items() if v is not None}
    update["updated_at"] = datetime.now(timezone.utc).isoformat()
    await db.documents.update_one({"id": doc_id}, {"$set": update})
    updated = await db.documents.find_one({"id": doc_id}, {"_id": 0})
    return updated

@api_router.delete("/documents/{doc_id}")
async def delete_document(doc_id: str, user=Depends(get_current_user)):
    result = await db.documents.delete_one({"id": doc_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Document not found")
    await db.bookmarks.delete_many({"document_id": doc_id})
    return {"status": "deleted"}

# --- Bookmarks Routes ---
@api_router.get("/bookmarks")
async def get_bookmarks(user=Depends(get_current_user)):
    bms = await db.bookmarks.find({"user_id": user["id"]}, {"_id": 0}).to_list(1000)
    doc_ids = [b["document_id"] for b in bms]
    docs = await db.documents.find({"id": {"$in": doc_ids}}, {"_id": 0}).to_list(1000)
    return {"bookmarks": bms, "documents": docs}

@api_router.post("/bookmarks/{doc_id}")
async def toggle_bookmark(doc_id: str, user=Depends(get_current_user)):
    existing = await db.bookmarks.find_one({"user_id": user["id"], "document_id": doc_id})
    if existing:
        await db.bookmarks.delete_one({"user_id": user["id"], "document_id": doc_id})
        return {"bookmarked": False}
    bm = {"id": str(uuid.uuid4()), "user_id": user["id"], "document_id": doc_id, "created_at": datetime.now(timezone.utc).isoformat()}
    await db.bookmarks.insert_one(bm)
    return {"bookmarked": True}

# --- Search Route ---
@api_router.get("/search")
async def search_documents(q: str = "", user=Depends(get_current_user)):
    if not q or len(q) < 2:
        return []
    query = {"$or": [
        {"title": {"$regex": q, "$options": "i"}},
        {"content": {"$regex": q, "$options": "i"}}
    ]}
    docs = await db.documents.find(query, {"_id": 0, "content": 0}).to_list(50)
    return docs

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
        await db.documents.insert_one(dict(doc))
    await db.categories.create_index("parent_id")
    await db.documents.create_index("category_id")
    await db.documents.create_index([("title", "text"), ("content", "text")])
    return {"status": "seeded", "categories": len(CATEGORIES), "documents": len(DOCUMENTS)}

@api_router.get("/")
async def root():
    return {"message": "Emergent Document Hub API"}

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
