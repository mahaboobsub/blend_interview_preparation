import re
import json

def parse_guide(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # We want to extract questions and answers.
    # Questions start with "#### " followed by a number, a dot, and the question text.
    # The answer is everything until the next "#### " or the end of the file or "### "
    
    questions = []
    
    # Split content by '#### '
    parts = re.split(r'\n#### \d+\.\s*', content)
    
    for part in parts[1:]:
        # The first line of part is the question
        lines = part.split('\n', 1)
        if len(lines) == 2:
            question_text = lines[0].strip()
            # The rest is the answer, but it might contain next section headers like "### "
            answer_text = lines[1]
            answer_text = re.split(r'\n###\s+', answer_text)[0].strip()
            
            has_code = '```' in answer_text
            code_python = ""
            py_match = re.search(r'```python\n(.*?)```', answer_text, re.DOTALL)
            if py_match:
                code_python = py_match.group(1).strip()
                
            questions.append({
                "category": "vidvantu",
                "subcategory": "Vidvantu Architecture & FastAPI",
                "question": question_text,
                "answer": answer_text,
                "is_coding": has_code,
                "code_sql": "",
                "code_java": "",
                "code_python": code_python
            })
            
    return questions

if __name__ == "__main__":
    qs = parse_guide('interview_preparation_guide.md')
    print(f"Parsed {len(qs)} questions")
    
    with open('data/db_vidvantu.py', 'w', encoding='utf-8') as f:
        f.write("# db_vidvantu.py - Vidvantu Project Specific Questions\n\n")
        f.write("VIDVANTU_QUESTIONS = ")
        f.write(json.dumps(qs, indent=2, ensure_ascii=False))
        f.write("\n")
