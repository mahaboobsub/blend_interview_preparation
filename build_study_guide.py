# build_study_guide.py - Master compiler
# Imports all modular databases + parses questions.txt → deduplicates → outputs JS + MD files

import os, json, sys, re

# Add data directory to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data'))

from db_sql import SQL_QUESTIONS
from db_dsa import DSA_QUESTIONS
from db_ml import ML_QUESTIONS
from db_dl import DL_QUESTIONS
from db_genai import GENAI_QUESTIONS
from db_fullstack import FULLSTACK_QUESTIONS
from db_projects import PROJECT_QUESTIONS

CATEGORIES = {
    "sql_db": "SQL, DB Design & DBMS Deep Concepts",
    "dsa": "Data Structures & Algorithms (DSA)",
    "ml_stats": "Machine Learning & Statistics",
    "dl_cv": "Deep Learning & Computer Vision",
    "genai_rag": "Generative AI, RAG & Agents",
    "fullstack": "Fullstack Development (JS/Python/REST)",
    "devops_projects": "DevOps, System Design & Projects"
}

# ─── Parse questions.txt ─────────────────────────────────────
def parse_questions_txt(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    SUBJECT_MAP = {
        "LANGCHAIN": ("genai_rag", "LangChain & Agentic AI"),
        "RAG": ("genai_rag", "RAG & Vector Databases"),
        "PROMPT ENGINEERING": ("genai_rag", "Prompt Engineering & Cost Optimization"),
        "AI FUNDAMENTALS": ("dl_cv", "Deep Learning Architectures"),
        "DEEP LEARNING": ("dl_cv", "Deep Learning Architectures"),
        "MACHINE LEARNING": ("ml_stats", "ML Algorithms"),
        "DATA ANALYSIS": ("ml_stats", "Data Analysis & SQL"),
    }

    subject_blocks = re.split(r'={10,}\nSUBJECT \d+: (.+?)\n={10,}', content)
    questions = []

    for i in range(1, len(subject_blocks), 2):
        subject_title = subject_blocks[i].strip()
        subject_body = subject_blocks[i+1] if i+1 < len(subject_blocks) else ""

        cat, subcat = "genai_rag", subject_title.title()
        for key, (c, s) in SUBJECT_MAP.items():
            if key in subject_title.upper():
                cat, subcat = c, s
                break

        qa_pattern = re.compile(r'Q\d+:\s*(.+?)\nA\d+:\n(.*?)(?=\nQ\d+:|\Z)', re.DOTALL)
        for question_text, answer_text in qa_pattern.findall(subject_body):
            question_text = question_text.strip().strip('"')
            answer_text = answer_text.strip()
            has_code = '```' in answer_text
            code_python = ""
            py_match = re.search(r'```python\n(.*?)```', answer_text, re.DOTALL)
            if py_match:
                code_python = py_match.group(1).strip()

            questions.append({
                "category": cat,
                "subcategory": subcat,
                "question": question_text,
                "answer": answer_text,
                "is_coding": has_code,
                "code_sql": "",
                "code_java": "",
                "code_python": code_python
            })
    return questions

# ─── Merge & Deduplicate ─────────────────────────────────────
def normalize(text):
    """Normalize question text for dedup comparison."""
    return re.sub(r'[^a-z0-9 ]', '', text.lower()).strip()

ALL_QUESTIONS = []
seen_questions = set()
id_counter = 1

def add_batch(q_list, source_name):
    global id_counter
    added = 0
    for q in q_list:
        norm = normalize(q['question'])
        # Skip if too similar to an existing question (first 60 chars match)
        key = norm[:80]
        if key in seen_questions:
            continue
        seen_questions.add(key)
        q['id'] = id_counter
        ALL_QUESTIONS.append(q)
        id_counter += 1
        added += 1
    print(f"  {source_name}: added {added} (skipped {len(q_list) - added} duplicates)")

# Add module questions first (they have detailed, structured answers)
print("Adding module questions...")
add_batch(SQL_QUESTIONS, "db_sql")
add_batch(DSA_QUESTIONS, "db_dsa")
add_batch(ML_QUESTIONS, "db_ml")
add_batch(DL_QUESTIONS, "db_dl")
add_batch(GENAI_QUESTIONS, "db_genai")
add_batch(FULLSTACK_QUESTIONS, "db_fullstack")
add_batch(PROJECT_QUESTIONS, "db_projects")

# Parse and add questions.txt (these also have detailed answers)
workspace = os.path.dirname(os.path.abspath(__file__))
txt_path = os.path.join(workspace, "questions.txt")
if os.path.exists(txt_path):
    print("\nParsing questions.txt...")
    txt_qs = parse_questions_txt(txt_path)
    add_batch(txt_qs, "questions.txt")

# ─── Output ──────────────────────────────────────────────────
print(f"\n{'='*60}")
print(f"TOTAL UNIQUE QUESTIONS: {len(ALL_QUESTIONS)}")
print(f"{'='*60}")

# Category breakdown
cats = {}
for q in ALL_QUESTIONS:
    cats[q['category']] = cats.get(q['category'], 0) + 1
for k, v in sorted(cats.items()):
    name = CATEGORIES.get(k, k)
    print(f"  {name}: {v}")

# 1. Write questions_data.js
js_path = os.path.join(workspace, "questions_data.js")
with open(js_path, 'w', encoding='utf-8') as f:
    f.write("// questions_data.js — Auto-generated, do not edit manually\n")
    f.write("window.QUESTIONS_DATA = ")
    f.write(json.dumps(ALL_QUESTIONS, indent=2, ensure_ascii=False))
    f.write(";\n")
print(f"\nGenerated {js_path}")

# 2. Write updated markdown files
def write_md(file_path, title, cat_ids):
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(f"# {title}\n\n")
        f.write("> Compiled with detailed answers. Duplicates removed.\n\n---\n\n")
        for cid in cat_ids:
            cname = CATEGORIES.get(cid, cid)
            cat_qs = [q for q in ALL_QUESTIONS if q['category'] == cid]
            if not cat_qs:
                continue
            f.write(f"## {cname}\n\n")
            for q in cat_qs:
                f.write(f"### Q: {q['question']}\n\n")
                f.write(f"**A:** {q['answer']}\n\n")
                if q.get('is_coding'):
                    for lang, key in [('sql', 'code_sql'), ('java', 'code_java'), ('python', 'code_python')]:
                        if q.get(key):
                            f.write(f"```{lang}\n{q[key]}\n```\n\n")
                f.write("---\n\n")

write_md(
    os.path.join(workspace, "question&dsainjavapython.md"),
    "Interview Question Bank — Assessment Aligned",
    ["sql_db", "dsa", "ml_stats"]
)
print("Updated question&dsainjavapython.md")

write_md(
    os.path.join(workspace, "Resume-based additional interview questions covering all gaps.md"),
    "Resume-Based Interview Questions — Edge Case Coverage",
    ["dl_cv", "genai_rag", "fullstack", "devops_projects"]
)
print("Updated Resume-based additional interview questions covering all gaps.md")

print("\nBuild complete!")
