#!/usr/bin/env python3
"""Parse 毛概简答题.md into short_answer.json"""

import re
import json

def parse_short_answers(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split by blank lines between questions
    # Questions start with "N. "
    blocks = re.split(r'\n(?=\d+\.\s)', content.strip())

    questions = []
    for i, block in enumerate(blocks):
        block = block.strip()
        if not block:
            continue

        lines = block.split('\n')
        # First line: "N. question text"
        first = lines[0].strip()
        m = re.match(r'^\d+\.\s+(.*)', first)
        if not m:
            continue

        question_text = m.group(1).strip()

        # Remaining lines are answer bullets (starting with "- " or "  - ")
        answer_points = []
        for line in lines[1:]:
            stripped = line.strip()
            if stripped.startswith('- '):
                answer_points.append(stripped[2:].strip())
            elif stripped.startswith('-'):
                answer_points.append(stripped[1:].strip())

        questions.append({
            'id': i + 1,
            'question': question_text,
            'answer': answer_points
        })

    return questions

if __name__ == '__main__':
    qs = parse_short_answers('毛概简答题.md')
    print(f"Parsed {len(qs)} short-answer questions")
    with open('short_answer.json', 'w', encoding='utf-8') as f:
        json.dump(qs, f, ensure_ascii=False, indent=2)
    print("Written to short_answer.json")
