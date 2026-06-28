# parse_questions_txt.py
# Parses the structured questions.txt file and outputs a Python list of dicts.

import re, json, os

def parse_questions_txt(filepath):
    """Parse the questions.txt file and return a list of question dicts."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Map subject headers to categories
    SUBJECT_MAP = {
        "LANGCHAIN": "genai_rag",
        "RAG": "genai_rag",
        "PROMPT ENGINEERING": "genai_rag",
        "AI FUNDAMENTALS": "dl_cv",
        "DEEP LEARNING": "dl_cv",
        "MACHINE LEARNING": "ml_stats",
        "DATA ANALYSIS": "ml_stats",
    }

    SUBJECT_SUBCAT_MAP = {
        "LANGCHAIN": "LangChain & Agentic AI",
        "RAG": "RAG & Vector Databases",
        "PROMPT ENGINEERING": "Prompt Engineering & Cost Optimization",
        "AI FUNDAMENTALS": "Deep Learning Architectures",
        "DEEP LEARNING": "Deep Learning Architectures",
        "MACHINE LEARNING": "ML Algorithms & Architecttic",
        "DATA ANALYSIS": "Data Analysis & SQL",
    }

    # Split into subjects
    subject_blocks = re.split(r'={10,}\nSUBJECT \d+: (.+?)\n={10,}', content)
    
    questions = []
    
    # First block is header, skip it
    for i in range(1, len(subject_blocks), 2):
        subject_title = subject_blocks[i].strip()
        subject_body = subject_blocks[i+1] if i+1 < len(subject_blocks) else ""
        
        # Determine category from subject title
        cat = "genai_rag"
        subcat = subject_title.title()
        for key, val in SUBJECT_MAP.items():
            if key in subject_title.upper():
                cat = val
                subcat = SUBJECT_SUBCAT_MAP.get(key, subject_title.title())
                break
        
        # Extract Q/A pairs within this subject
        qa_pattern = re.compile(r'Q\d+:\s*(.+?)\nA\d+:\n(.*?)(?=\nQ\d+:|\Z)', re.DOTALL)
        matches = qa_pattern.findall(subject_body)
        
        for question_text, answer_text in matches:
            question_text = question_text.strip().strip('"')
            answer_text = answer_text.strip()
            
            # Check if it has code blocks
            has_code = '```' in answer_text
            code_python = ""
            code_sql = ""
            
            if has_code:
                py_match = re.search(r'```python\n(.*?)```', answer_text, re.DOTALL)
                if py_match:
                    code_python = py_match.group(1).strip()
                sql_match = re.search(r'```sql\n(.*?)```', answer_text, re.DOTALL)
                if sql_match:
                    code_sql = sql_match.group(1).strip()
            
            questions.append({
                "category": cat,
                "subcategory": subcat,
                "question": question_text,
                "answer": answer_text,
                "is_coding": has_code,
                "code_sql": code_sql,
                "code_java": "",
                "code_python": code_python
            })
    
    return questions

if __name__ == "__main__":
    workspace = os.path.dirname(os.path.abspath(__file__))
    qs = parse_questions_txt(os.path.join(workspace, "questions.txt"))
    print(f"Parsed {len(qs)} questions from questions.txt")
    # Print category breakdown
    cats = {}
    for q in qs:
        cats[q['category']] = cats.get(q['category'], 0) + 1
    for k, v in sorted(cats.items()):
        print(f"  {k}: {v}")
    
    # Save as JSON for verification
    with open(os.path.join(workspace, "data", "parsed_txt.json"), "w", encoding="utf-8") as f:
        json.dump(qs, f, indent=2)
    print("Saved to data/parsed_txt.json")
