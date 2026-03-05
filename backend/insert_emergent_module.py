#!/usr/bin/env python3
"""Insert 'How Emergent Actually Works' module into already-seeded MongoDB.

Run: python3 backend/insert_emergent_module.py

This script is idempotent — it checks for existing categories/documents by name
before inserting, so it's safe to run multiple times.
"""
import sys
import os

# Add parent directory to path so we can import seed_data
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pymongo import MongoClient
from seed_data import (
    CATEGORIES, DOCUMENTS,
    CAT_HOW_EMERGENT, SUB_AGENTS_MODELS, SUB_AGENT_LOOP_EM,
    SUB_TOOLS_DELEG, SUB_TRAJ_DEBUG, SUB_FAILURE_RECOVERY,
)

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.environ.get("DB_NAME", "knowledge_hub")

# IDs for the new module
NEW_CATEGORY_IDS = {
    CAT_HOW_EMERGENT, SUB_AGENTS_MODELS, SUB_AGENT_LOOP_EM,
    SUB_TOOLS_DELEG, SUB_TRAJ_DEBUG, SUB_FAILURE_RECOVERY,
}

# Category IDs that new documents belong to
NEW_DOC_CATEGORY_IDS = NEW_CATEGORY_IDS - {CAT_HOW_EMERGENT}  # parent has no docs


def main():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]

    # --- Insert categories ---
    new_cats = [c for c in CATEGORIES if c["id"] in NEW_CATEGORY_IDS]
    cat_inserted = 0
    for cat in new_cats:
        if db.categories.find_one({"name": cat["name"]}):
            print(f"  [skip] Category already exists: {cat['name']}")
        else:
            db.categories.insert_one(dict(cat))
            cat_inserted += 1
            print(f"  [+] Inserted category: {cat['name']}")

    # --- Insert documents ---
    new_docs = [d for d in DOCUMENTS if d["category_id"] in NEW_DOC_CATEGORY_IDS]
    doc_inserted = 0
    for doc in new_docs:
        if db.documents.find_one({"title": doc["title"]}):
            print(f"  [skip] Document already exists: {doc['title']}")
        else:
            db.documents.insert_one(dict(doc))
            doc_inserted += 1
            print(f"  [+] Inserted document: {doc['title']}")

    print(f"\nDone: {cat_inserted} categories inserted, {doc_inserted} documents inserted.")
    print(f"Skipped: {len(new_cats) - cat_inserted} categories, {len(new_docs) - doc_inserted} documents.")
    client.close()


if __name__ == "__main__":
    main()
