"""Update path tests to 25 questions each for beginner, intermediate, advanced"""
from pymongo import MongoClient
import uuid

client = MongoClient('mongodb://localhost:27017')
db = client['test_database']
def _id(): return str(uuid.uuid4())

# Get all paths
paths = list(db.learning_paths.find({}, {'_id': 0}))

# Gather ALL quiz questions from the database
all_quizzes = list(db.quizzes.find({}, {'_id': 0}))
all_module_tests = list(db.module_tests.find({}, {'_id': 0}))

# Build a pool of all available questions
question_pool = []
for q in all_quizzes:
    question_pool.extend(q.get('questions', []))
for mt in all_module_tests:
    question_pool.extend(mt.get('questions', []))

print(f"Total question pool: {len(question_pool)}")

# For each path, create 25 questions by:
# 1. Taking questions from the path's documents
# 2. Filling remaining from related topic questions
db.path_tests.drop()

for path in paths:
    path_qs = []
    # First: questions from docs in this path
    for step in path.get('steps', []):
        quiz = db.quizzes.find_one({'document_id': step['document_id']}, {'_id': 0})
        if quiz and quiz.get('questions'):
            path_qs.extend(quiz['questions'])
    
    # Deduplicate by question text
    seen = set()
    unique_qs = []
    for q in path_qs:
        if q['question'] not in seen:
            seen.add(q['question'])
            unique_qs.append(q)
    
    # Fill to 25 from pool
    for q in question_pool:
        if len(unique_qs) >= 25:
            break
        if q['question'] not in seen:
            seen.add(q['question'])
            unique_qs.append(q)
    
    # Ensure each has a unique ID
    for q in unique_qs:
        q['id'] = _id()
    
    test = {
        "id": _id(),
        "path_id": path['id'],
        "title": f"{path['title']} — Final Assessment",
        "questions": unique_qs[:25]
    }
    db.path_tests.insert_one(test)
    print(f"  {path['title']}: {len(unique_qs[:25])} questions")

print("\nDone!")
