"""Batch 3 — Category Reorganization + Content Deduplication"""
from pymongo import MongoClient
from datetime import datetime, timezone

client = MongoClient('mongodb://localhost:27017')
db = client['test_database']
NOW = datetime.now(timezone.utc).isoformat()

# ============================================================
# 1. Fix model names (GPT-5.2 → remove, use generic or real names)
# ============================================================
print("=== Fixing model name references ===")
internal_cats = set(c['id'] for c in db.categories.find({'internal': True}, {'_id': 0, 'id': 1}))
docs = list(db.documents.find({'deleted': {'$ne': True}, 'category_id': {'$nin': list(internal_cats)}}, {'_id': 0, 'title': 1, 'content': 1}))

for d in docs:
    content = d['content']
    changed = False
    
    # Fix GPT-5.2 (not a real model as of knowledge cutoff)
    if 'GPT-5.2' in content or 'gpt-5.2' in content:
        content = content.replace('GPT-5.2', 'GPT-4o')
        content = content.replace('gpt-5.2', 'gpt-4o')
        changed = True
    
    # Fix Nano Banana (not a standard model name)
    if 'Nano Banana' in content or 'nano banana' in content:
        content = content.replace('Nano Banana', 'Imagen')
        content = content.replace('nano banana', 'imagen')
        changed = True
    
    # Fix claude-sonnet-4-6 (use generic version)
    if 'claude-sonnet-4-6' in content:
        content = content.replace('claude-sonnet-4-6', 'claude-sonnet-4-5')
        changed = True
    
    if changed:
        db.documents.update_one({'title': d['title']}, {'$set': {'content': content, 'updated_at': NOW}})
        print(f"  Fixed model names in: {d['title']}")

# ============================================================
# 2. Deduplicate Universal Key content
# ============================================================
print("\n=== Deduplicating Universal Key references ===")
# Check which docs mention Universal Key
for d in docs:
    if 'Universal Key' in d['content']:
        count = d['content'].count('Universal Key')
        print(f"  {d['title']}: {count} mentions")

# The Universal Key is explained in detail in LLM Proxy Architecture.
# Other docs should reference it briefly, not re-explain.
# Token Economics already has a brief mention. FAQ has a brief mention. These are fine.
# The key dedup issue from the review was about 5 places explaining it in detail.
# Let's check if any doc has excessive duplication:
for d in docs:
    content = d['content']
    if 'Universal Key' in content and d['title'] not in ['LLM Proxy Architecture', 'Token Economics & Billing', 'Frequently Asked Questions']:
        lines_with_uk = [l.strip() for l in content.split('\n') if 'Universal Key' in l]
        if len(lines_with_uk) > 1:
            print(f"  Needs dedup: {d['title']} ({len(lines_with_uk)} lines)")

# ============================================================
# 3. Clean up category ordering for logical flow
# ============================================================
print("\n=== Reordering categories ===")

# Desired order:
# -1: Getting Started
# -0.5: Agent Anatomy (moved up from -0.3)
# 0: Tutorials (moved from -0.5)
# 1: Platform Architecture (was 0)
# 2: LLM Internals (was 1) 
# 3: Infrastructure (was 2)
# 4: Frontend Development (was 3)
# 5: Backend Development (was 4)
# 6: DevOps & Deployment (was 5)
# 7: Security (was 6)
# 8: Data & Storage (was 7)
# 9: Advanced Concepts (was 8)
# 10: Future of AI Agents (was 9)
# 11: Tools & Resources
# 12: Limitations & Constraints
# 13: UI Guide
# 14: FAQ

reorder = {
    "Getting Started": -1,
    "Agent Anatomy": -0.5,
    "Tutorials": 0,
    "Platform Architecture": 1,
    "LLM Internals": 2,
    "Infrastructure": 3,
    "Frontend Development": 4,
    "Backend Development": 5,
    "DevOps & Deployment": 6,
    "Security": 7,
    "Data & Storage": 8,
    "Advanced Concepts": 9,
    "Future of AI Agents": 10,
    "Tools & Resources": 11,
    "Limitations & Constraints": 12,
    "UI Guide": 13,
    "FAQ": 14,
}

for name, order in reorder.items():
    result = db.categories.update_one({"name": name, "parent_id": None}, {"$set": {"order": order}})
    if result.modified_count:
        print(f"  Reordered: {name} → {order}")

# ============================================================
# 4. Final verification
# ============================================================
print("\n=== Final State ===")
internal_cats = set(c['id'] for c in db.categories.find({'internal': True}, {'_id': 0, 'id': 1}))
total_docs = db.documents.count_documents({'deleted': {'$ne': True}, 'category_id': {'$nin': list(internal_cats)}})
total_chars = 0
for d in db.documents.find({'deleted': {'$ne': True}, 'category_id': {'$nin': list(internal_cats)}}, {'content': 1}):
    total_chars += len(d.get('content', ''))

# Check for any remaining problematic references
import re
issues = []
for d in db.documents.find({'deleted': {'$ne': True}, 'category_id': {'$nin': list(internal_cats)}}, {'_id': 0, 'title': 1, 'content': 1}):
    content = d['content']
    if re.search(r'\bE1\b', content) or 'Emergent' in content or 'emergentagent' in content:
        issues.append(d['title'])
    if 'GPT-5.2' in content or 'gpt-5.2' in content:
        issues.append(f"{d['title']} (GPT-5.2)")
    if 'Nano Banana' in content:
        issues.append(f"{d['title']} (Nano Banana)")

print(f"  Total public documents: {total_docs}")
print(f"  Total content: {total_chars:,} characters ({total_chars//1000}K)")
print(f"  Platform reference issues: {len(issues)}")
if issues:
    for i in issues:
        print(f"    - {i}")
else:
    print("  ALL CLEAN!")

# Show final category structure
print("\n=== Category Structure ===")
cats = list(db.categories.find({'internal': {'$ne': True}}, {'_id': 0}))
parents = sorted([c for c in cats if not c.get('parent_id')], key=lambda x: x.get('order', 99))
for p in parents:
    subs = sorted([c for c in cats if c.get('parent_id') == p['id']], key=lambda x: x.get('order', 99))
    doc_count = db.documents.count_documents({'category_id': {'$in': [p['id']] + [s['id'] for s in subs]}, 'deleted': {'$ne': True}})
    print(f"  {p['name']} ({doc_count} docs)")
    for s in subs:
        print(f"    └─ {s['name']}")
