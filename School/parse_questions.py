#!/usr/bin/env python3
"""Parse 毛中特题库.md and generate questions.json"""

import re
import json

def parse_questions(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split by chapter headers to get chapter info
    chapters = []
    current_chapter = ""

    # Find all chapter headers
    chapter_pattern = re.compile(r'^##\s+(.+)$', re.MULTILINE)
    chapter_matches = list(chapter_pattern.finditer(content))

    # Split content by chapter
    chapter_ranges = []
    for i, m in enumerate(chapter_matches):
        start = m.end()
        end = chapter_matches[i+1].start() if i+1 < len(chapter_matches) else len(content)
        chapter_ranges.append((m.group(1).strip(), start, end))

    all_questions = []
    qid = 0

    for chapter_name, start, end in chapter_ranges:
        chapter_content = content[start:end].strip()

        # Split into question blocks
        # Questions start with a number followed by ". "
        blocks = re.split(r'\n(?=\d+\.\s)', chapter_content)

        for block in blocks:
            block = block.strip()
            if not block:
                continue

            qid += 1

            # Extract question lines
            lines = block.split('\n')

            # First line is "N. question text"
            first_line = lines[0].strip()
            match = re.match(r'^\d+\.\s+(.*)', first_line)
            if not match:
                continue
            question_text = match.group(1).strip()

            # Parse remaining fields
            options = []
            question_type = ""
            answer = ""
            explanation = ""
            source = ""

            explanation_lines = []
            in_explanation = False

            for line in lines[1:]:
                line_stripped = line.strip()

                if not line_stripped:
                    continue

                # Option lines
                opt_match = re.match(r'^([A-F])\.\s+(.*)', line_stripped)
                if opt_match:
                    options.append({
                        'key': opt_match.group(1),
                        'text': opt_match.group(2).strip()
                    })
                    continue

                # Type
                if line_stripped.startswith('题型:'):
                    question_type = line_stripped.replace('题型:', '').strip()
                    continue

                # Answer
                if line_stripped.startswith('答案:'):
                    answer = line_stripped.replace('答案:', '').strip()
                    continue

                # Explanation
                if line_stripped.startswith('解析:'):
                    in_explanation = True
                    explanation_lines.append(line_stripped.replace('解析:', '').strip())
                    continue

                # Source
                if line_stripped.startswith('来源:'):
                    source = line_stripped.replace('来源:', '').strip()
                    continue

                # Continuation of explanation
                if in_explanation:
                    explanation_lines.append(line_stripped)

            explanation = ' '.join(explanation_lines)

            # Parse answer: for multi-select, split by 、
            if question_type == '多选':
                answers = [a.strip() for a in answer.replace(' ', '').split('、') if a.strip()]
            else:
                answers = [answer.strip()]

            all_questions.append({
                'id': qid,
                'chapter': chapter_name,
                'type': question_type,
                'question': question_text,
                'options': options,
                'answers': answers,
                'explanation': explanation,
                'source': source
            })

    return all_questions

if __name__ == '__main__':
    questions = parse_questions('毛中特题库.md')
    print(f"Parsed {len(questions)} questions")

    # Count types
    single = sum(1 for q in questions if q['type'] == '单选')
    multi = sum(1 for q in questions if q['type'] == '多选')
    print(f"  单选: {single}")
    print(f"  多选: {multi}")

    with open('questions.json', 'w', encoding='utf-8') as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)

    print("Written to questions.json")
