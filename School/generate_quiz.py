#!/usr/bin/env python3
"""Generate a standalone HTML quiz website from questions.json"""

import json

def generate_html(questions_json_path, short_answer_path, output_path):
    with open(questions_json_path, 'r', encoding='utf-8') as f:
        questions = json.load(f)
    with open(short_answer_path, 'r', encoding='utf-8') as f:
        short_answers = json.load(f)

    questions_json = json.dumps(questions, ensure_ascii=False)
    short_answer_json = json.dumps(short_answers, ensure_ascii=False)

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>毛中特题库 - 刷题卡片</title>
<style>
:root {{
    --bg: #f0f2f5;
    --card-bg: #ffffff;
    --text: #1a1a2e;
    --text-secondary: #555;
    --border: #e0e0e0;
    --primary: #4f46e5;
    --primary-light: #eef2ff;
    --correct: #059669;
    --correct-bg: #ecfdf5;
    --correct-border: #a7f3d0;
    --wrong: #dc2626;
    --wrong-bg: #fef2f2;
    --wrong-border: #fecaca;
    --option-hover: #f3f4f6;
    --option-selected: #eef2ff;
    --shadow: 0 4px 24px rgba(0,0,0,0.08);
    --radius: 16px;
    --transition: 0.2s ease;
}}

[data-theme="dark"] {{
    --bg: #111827;
    --card-bg: #1f2937;
    --text: #f1f5f9;
    --text-secondary: #9ca3af;
    --border: #374151;
    --primary: #818cf8;
    --primary-light: #1e1b4b;
    --correct: #34d399;
    --correct-bg: #064e3b;
    --correct-border: #065f46;
    --wrong: #f87171;
    --wrong-bg: #7f1d1d;
    --wrong-border: #991b1b;
    --option-hover: #374151;
    --option-selected: #1e1b4b;
    --shadow: 0 4px 24px rgba(0,0,0,0.3);
}}

* {{ margin: 0; padding: 0; box-sizing: border-box; }}

body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans SC", "PingFang SC", "Microsoft YaHei", sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    transition: background var(--transition), color var(--transition);
}}

/* Top Bar */
.top-bar {{
    position: sticky;
    top: 0;
    z-index: 100;
    background: var(--card-bg);
    border-bottom: 1px solid var(--border);
    padding: 12px 20px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 12px;
    box-shadow: 0 1px 8px rgba(0,0,0,0.05);
}}

.top-bar .brand {{
    font-weight: 700;
    font-size: 1.1rem;
    color: var(--primary);
    white-space: nowrap;
}}

.top-bar .controls {{
    display: flex;
    align-items: center;
    gap: 10px;
    flex-wrap: wrap;
}}

.btn {{
    padding: 8px 16px;
    border: 1px solid var(--border);
    border-radius: 8px;
    background: var(--card-bg);
    color: var(--text);
    cursor: pointer;
    font-size: 0.875rem;
    transition: all var(--transition);
    white-space: nowrap;
    font-family: inherit;
}}

.btn:hover {{ border-color: var(--primary); color: var(--primary); }}
.btn.active {{ background: var(--primary); color: #fff; border-color: var(--primary); }}

.btn-icon {{
    width: 36px; height: 36px;
    padding: 0;
    display: flex; align-items: center; justify-content: center;
    border-radius: 50%;
    font-size: 1.1rem;
}}

select.btn {{
    appearance: none;
    padding-right: 28px;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2'%3E%3Cpath d='m6 9 6 6 6-6'/%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position: right 10px center;
}}

/* Stats */
.stats {{
    display: flex;
    gap: 16px;
    align-items: center;
    font-size: 0.875rem;
    color: var(--text-secondary);
}}

.stat-item {{
    display: flex;
    align-items: center;
    gap: 4px;
}}

.stat-num {{ font-weight: 700; color: var(--text); }}

/* Progress bar */
.progress-wrap {{
    padding: 16px 20px 0;
    max-width: 760px;
    margin: 0 auto;
}}

.progress-bar {{
    height: 6px;
    background: var(--border);
    border-radius: 3px;
    overflow: hidden;
}}

.progress-fill {{
    height: 100%;
    background: var(--primary);
    border-radius: 3px;
    transition: width 0.4s ease;
}}

/* Main Container */
.container {{
    max-width: 760px;
    margin: 0 auto;
    padding: 20px;
}}

/* Card */
.card {{
    background: var(--card-bg);
    border-radius: var(--radius);
    box-shadow: var(--shadow);
    padding: 32px;
    margin-bottom: 20px;
    transition: all var(--transition);
    animation: fadeIn 0.3s ease;
}}

@keyframes fadeIn {{
    from {{ opacity: 0; transform: translateY(12px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}

.card-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 20px;
    flex-wrap: wrap;
    gap: 8px;
}}

.badge {{
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
}}

.badge-chapter {{
    background: var(--primary-light);
    color: var(--primary);
}}

.badge-type {{
    background: #fef3c7;
    color: #92400e;
}}

[data-theme="dark"] .badge-type {{
    background: #78350f;
    color: #fcd34d;
}}

.question-num {{
    font-size: 0.85rem;
    color: var(--text-secondary);
    font-weight: 500;
}}

.question-text {{
    font-size: 1.15rem;
    font-weight: 600;
    line-height: 1.7;
    margin-bottom: 24px;
    color: var(--text);
}}

/* Options */
.options {{
    display: flex;
    flex-direction: column;
    gap: 10px;
}}

.option {{
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 14px 18px;
    border: 2px solid var(--border);
    border-radius: 12px;
    cursor: pointer;
    transition: all var(--transition);
    font-size: 0.95rem;
    line-height: 1.5;
    user-select: none;
}}

.option:hover {{ border-color: var(--primary); background: var(--option-hover); }}

.option-key {{
    width: 32px; height: 32px;
    border-radius: 50%;
    background: var(--option-hover);
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 0.9rem;
    flex-shrink: 0;
    transition: all var(--transition);
}}

.option.selected {{
    border-color: var(--primary);
    background: var(--option-selected);
}}

.option.selected .option-key {{
    background: var(--primary);
    color: #fff;
}}

.option.correct {{
    border-color: var(--correct-border);
    background: var(--correct-bg);
}}

.option.correct .option-key {{
    background: var(--correct);
    color: #fff;
}}

.option.wrong {{
    border-color: var(--wrong-border);
    background: var(--wrong-bg);
}}

.option.wrong .option-key {{
    background: var(--wrong);
    color: #fff;
}}

.option.disabled {{
    pointer-events: none;
    opacity: 0.7;
}}

.option.disabled.incorrect-choice {{
    opacity: 1;
}}

.option-icon {{
    margin-left: auto;
    font-size: 1.2rem;
}}

/* Submit button for multi-select */
.submit-row {{
    margin-top: 16px;
    display: flex;
    gap: 10px;
}}

.btn-submit {{
    padding: 12px 32px;
    background: var(--primary);
    color: #fff;
    border: none;
    border-radius: 10px;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all var(--transition);
    font-family: inherit;
}}

.btn-submit:hover {{ opacity: 0.9; transform: translateY(-1px); }}
.btn-submit:disabled {{ opacity: 0.4; cursor: not-allowed; transform: none; }}

/* Explanation */
.explanation {{
    margin-top: 20px;
    padding: 20px;
    background: var(--bg);
    border-radius: 12px;
    border-left: 4px solid var(--primary);
    animation: slideDown 0.3s ease;
}}

@keyframes slideDown {{
    from {{ opacity: 0; transform: translateY(-8px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}

.explanation-title {{
    font-weight: 700;
    font-size: 0.95rem;
    margin-bottom: 8px;
    color: var(--text);
}}

.explanation-text {{
    font-size: 0.9rem;
    line-height: 1.7;
    color: var(--text-secondary);
}}

.result-banner {{
    text-align: center;
    padding: 16px;
    border-radius: 12px;
    margin-bottom: 16px;
    font-weight: 700;
    font-size: 1.05rem;
}}

.result-banner.correct {{
    background: var(--correct-bg);
    color: var(--correct);
}}

.result-banner.wrong {{
    background: var(--wrong-bg);
    color: var(--wrong);
}}

/* Navigation */
.nav-row {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 12px;
    margin-top: 20px;
}}

.btn-nav {{
    padding: 12px 28px;
    font-size: 0.95rem;
    font-weight: 600;
    border-radius: 10px;
    font-family: inherit;
}}

.btn-nav.primary {{
    background: var(--primary);
    color: #fff;
    border: none;
}}

/* Summary Page */
.summary {{
    text-align: center;
    padding: 40px 0;
}}

.summary h2 {{
    font-size: 1.8rem;
    margin-bottom: 8px;
}}

.summary .big-score {{
    font-size: 4rem;
    font-weight: 800;
    background: linear-gradient(135deg, var(--primary), #7c3aed);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}}

.summary-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    gap: 16px;
    margin: 24px 0;
}}

.summary-card {{
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px;
    text-align: center;
}}

.summary-card .num {{
    font-size: 1.8rem;
    font-weight: 700;
    color: var(--text);
}}

.summary-card .label {{
    font-size: 0.8rem;
    color: var(--text-secondary);
    margin-top: 4px;
}}

/* Chapter review */
.review-table {{
    width: 100%;
    border-collapse: collapse;
    margin: 24px 0;
    font-size: 0.85rem;
    text-align: left;
}}

.review-table th, .review-table td {{
    padding: 10px 14px;
    border-bottom: 1px solid var(--border);
}}

.review-table th {{
    font-weight: 600;
    color: var(--text-secondary);
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}

.review-icon {{
    font-size: 1.2rem;
}}

/* Responsive */
@media (max-width: 600px) {{
    .card {{ padding: 20px; }}
    .top-bar {{ padding: 10px 14px; gap: 8px; }}
    .top-bar .brand {{ font-size: 0.95rem; }}
    .btn {{ padding: 6px 12px; font-size: 0.8rem; }}
    .question-text {{ font-size: 1.05rem; }}
    .option {{ padding: 12px 14px; font-size: 0.9rem; }}
    .summary .big-score {{ font-size: 3rem; }}
    .stats {{ font-size: 0.8rem; gap: 10px; }}
}}

/* Empty state */
.empty-state {{
    text-align: center;
    padding: 80px 20px;
    color: var(--text-secondary);
}}

.empty-state .emoji {{ font-size: 3rem; margin-bottom: 12px; }}

.hidden {{ display: none !important; }}

/* Review Mode */
.review-bar {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 10px;
    margin-bottom: 20px;
    padding: 16px 20px;
    background: var(--card-bg);
    border-radius: var(--radius);
    box-shadow: var(--shadow);
}}

.review-bar .title {{
    font-weight: 700;
    font-size: 1.05rem;
    color: var(--text);
}}

.review-bar .info {{
    font-size: 0.85rem;
    color: var(--text-secondary);
}}

.review-card {{
    background: var(--card-bg);
    border-radius: var(--radius);
    box-shadow: var(--shadow);
    padding: 28px;
    margin-bottom: 16px;
    animation: fadeIn 0.3s ease;
    border-left: 4px solid var(--wrong);
}}

.review-card .correct-answer-note {{
    display: inline-block;
    padding: 6px 14px;
    background: var(--correct-bg);
    color: var(--correct);
    border-radius: 8px;
    font-weight: 700;
    font-size: 0.9rem;
    margin-top: 12px;
    margin-bottom: 12px;
}}

/* Exam Mode */
.exam-mode #chapterFilter,
.exam-mode #reviewBtn,
.exam-mode #shuffleBtn,
.exam-mode #resetBtn {{ opacity: 0.35; pointer-events: none; }}
.exam-mode .progress-wrap {{ display: none; }}
.exam-mode .stats {{ opacity: 0.5; }}

.exam-timer {{
    text-align: center;
    margin-bottom: 12px;
}}

.exam-timer .time-display {{
    font-size: 2rem;
    font-weight: 700;
    font-family: "SF Mono", "Fira Code", "Consolas", monospace;
    color: var(--text);
}}

.exam-timer .time-label {{
    font-size: 0.8rem;
    color: var(--text-secondary);
}}

.exam-card {{
    background: var(--card-bg);
    border-radius: var(--radius);
    box-shadow: var(--shadow);
    padding: 36px;
    margin-bottom: 20px;
    animation: fadeIn 0.3s ease;
    position: relative;
    overflow: hidden;
}}

.exam-card::before {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 4px;
    background: linear-gradient(90deg, var(--primary), #7c3aed, #f59e0b);
}}

.exam-progress {{
    display: flex;
    gap: 4px;
    margin-bottom: 24px;
}}

.exam-progress .dot {{
    width: 100%;
    height: 4px;
    background: var(--border);
    border-radius: 2px;
    transition: background 0.3s;
}}

.exam-progress .dot.done-correct {{ background: var(--correct); }}
.exam-progress .dot.done-wrong {{ background: var(--wrong); }}
.exam-progress .dot.current {{ background: var(--primary); }}

.exam-feedback {{
    text-align: center;
    padding: 14px;
    border-radius: 10px;
    font-weight: 700;
    font-size: 1.1rem;
    margin-top: 16px;
    animation: fadeIn 0.2s ease;
}}

.exam-feedback.correct {{ background: var(--correct-bg); color: var(--correct); }}
.exam-feedback.wrong {{ background: var(--wrong-bg); color: var(--wrong); }}

.btn-exam {{
    padding: 10px 22px;
    background: linear-gradient(135deg, #f59e0b, #ef4444);
    color: #fff;
    border: none;
    border-radius: 10px;
    font-size: 0.9rem;
    font-weight: 700;
    cursor: pointer;
    transition: all var(--transition);
    font-family: inherit;
    white-space: nowrap;
}}

.btn-exam:hover {{ opacity: 0.9; transform: translateY(-1px); box-shadow: 0 4px 12px rgba(239,68,68,0.3); }}

/* Exam summary */
.exam-result {{
    text-align: center;
    padding: 20px;
}}

.exam-result .big-grade {{
    font-size: 3.5rem;
    font-weight: 800;
    margin: 8px 0;
}}

.exam-result .grade-a {{ color: var(--correct); }}
.exam-result .grade-b {{ color: #f59e0b; }}
.exam-result .grade-c {{ color: #f97316; }}
.exam-result .grade-d {{ color: var(--wrong); }}

/* Flashcard Mode */
.flashcard-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
    padding: 10px 0;
}}

.flashcard {{
    perspective: 1000px;
    height: 280px;
    cursor: pointer;
}}

.flashcard-inner {{
    position: relative;
    width: 100%;
    height: 100%;
    transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    transform-style: preserve-3d;
}}

.flashcard.flipped .flashcard-inner {{
    transform: rotateY(180deg);
}}

.flashcard-face {{
    position: absolute;
    width: 100%;
    height: 100%;
    backface-visibility: hidden;
    border-radius: var(--radius);
    box-shadow: var(--shadow);
    padding: 24px;
    display: flex;
    flex-direction: column;
    overflow: hidden;
}}

.flashcard-front {{
    background: var(--card-bg);
    border: 2px solid var(--border);
    justify-content: center;
    align-items: center;
    text-align: center;
}}

.flashcard-front .card-num {{
    font-size: 2.5rem;
    font-weight: 800;
    color: var(--primary);
    opacity: 0.3;
    margin-bottom: 12px;
}}

.flashcard-front .card-question {{
    font-size: 1.05rem;
    font-weight: 600;
    line-height: 1.6;
    color: var(--text);
}}

.flashcard-front .card-hint {{
    font-size: 0.75rem;
    color: var(--text-secondary);
    margin-top: 12px;
    opacity: 0.6;
}}

.flashcard-back {{
    background: var(--card-bg);
    border: 2px solid var(--primary);
    transform: rotateY(180deg);
    overflow-y: auto;
}}

.flashcard-back .back-title {{
    font-weight: 700;
    font-size: 0.9rem;
    color: var(--primary);
    margin-bottom: 12px;
    padding-bottom: 8px;
    border-bottom: 1px solid var(--border);
}}

.flashcard-back .answer-list {{
    list-style: none;
    padding: 0;
    margin: 0;
}}

.flashcard-back .answer-list li {{
    position: relative;
    padding: 6px 0 6px 20px;
    font-size: 0.88rem;
    line-height: 1.6;
    color: var(--text-secondary);
}}

.flashcard-back .answer-list li::before {{
    content: '•';
    position: absolute;
    left: 4px;
    color: var(--primary);
    font-weight: 700;
}}

.flashcard-back .answer-list li + li {{
    border-top: 1px solid var(--border);
}}

/* Flashcard controls */
.flashcard-controls {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 10px;
    margin-bottom: 20px;
}}

.flashcard-controls .fc-title {{
    font-weight: 700;
    font-size: 1.05rem;
    color: var(--text);
}}

.flashcard-controls .fc-actions {{
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
}}

@media (max-width: 600px) {{
    .flashcard-grid {{
        grid-template-columns: 1fr;
    }}
    .flashcard {{
        height: 240px;
    }}
}}

/* Flashcard status badges */
.flashcard-status {{
    position: absolute;
    top: 10px;
    right: 10px;
    z-index: 5;
    font-size: 1.4rem;
    pointer-events: none;
}}

/* Study Mode */
.study-container {{
    max-width: 640px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 20px;
}}

.study-progress {{
    width: 100%;
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 0.9rem;
    color: var(--text-secondary);
}}

.study-progress-bar {{
    flex: 1;
    height: 6px;
    background: var(--border);
    border-radius: 3px;
    overflow: hidden;
}}

.study-progress-fill {{
    height: 100%;
    background: var(--primary);
    border-radius: 3px;
    transition: width 0.4s ease;
}}

.study-card {{
    perspective: 1000px;
    width: 100%;
    height: 420px;
    cursor: pointer;
}}

.study-card-inner {{
    position: relative;
    width: 100%;
    height: 100%;
    transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    transform-style: preserve-3d;
}}

.study-card.flipped .study-card-inner {{
    transform: rotateY(180deg);
}}

.study-card-face {{
    position: absolute;
    width: 100%;
    height: 100%;
    backface-visibility: hidden;
    border-radius: var(--radius);
    box-shadow: var(--shadow);
    padding: 36px;
    display: flex;
    flex-direction: column;
    overflow: hidden;
}}

.study-card-front {{
    background: var(--card-bg);
    border: 2px solid var(--border);
    justify-content: center;
    align-items: center;
    text-align: center;
}}

.study-card-front .study-num {{
    font-size: 4rem;
    font-weight: 800;
    color: var(--primary);
    opacity: 0.2;
    margin-bottom: 16px;
}}

.study-card-front .study-question {{
    font-size: 1.25rem;
    font-weight: 600;
    line-height: 1.7;
    color: var(--text);
}}

.study-card-front .study-hint {{
    font-size: 0.85rem;
    color: var(--text-secondary);
    margin-top: 16px;
    opacity: 0.5;
}}

.study-card-back {{
    background: var(--card-bg);
    border: 2px solid var(--primary);
    transform: rotateY(180deg);
    overflow-y: auto;
}}

.study-card-back .study-back-title {{
    font-weight: 700;
    font-size: 1rem;
    color: var(--primary);
    margin-bottom: 16px;
    padding-bottom: 10px;
    border-bottom: 1px solid var(--border);
}}

.study-card-back .study-answer-list {{
    list-style: none;
    padding: 0;
    margin: 0;
}}

.study-card-back .study-answer-list li {{
    position: relative;
    padding: 8px 0 8px 22px;
    font-size: 0.95rem;
    line-height: 1.7;
    color: var(--text-secondary);
}}

.study-card-back .study-answer-list li::before {{
    content: '•';
    position: absolute;
    left: 4px;
    color: var(--primary);
    font-weight: 700;
}}

.study-card-back .study-answer-list li + li {{
    border-top: 1px solid var(--border);
}}

.study-actions {{
    display: flex;
    gap: 16px;
    width: 100%;
    max-width: 640px;
}}

.study-actions button {{
    flex: 1;
    padding: 16px 24px;
    border-radius: 12px;
    font-size: 1.05rem;
    font-weight: 700;
    cursor: pointer;
    transition: all var(--transition);
    font-family: inherit;
    border: none;
}}

.btn-remember {{
    background: var(--correct-bg);
    color: var(--correct);
    border: 2px solid var(--correct-border) !important;
}}

.btn-remember:hover {{
    background: var(--correct);
    color: #fff;
    transform: translateY(-2px);
    box-shadow: 0 4px 16px rgba(5,150,105,0.3);
}}

.btn-forget {{
    background: var(--wrong-bg);
    color: var(--wrong);
    border: 2px solid var(--wrong-border) !important;
}}

.btn-forget:hover {{
    background: var(--wrong);
    color: #fff;
    transform: translateY(-2px);
    box-shadow: 0 4px 16px rgba(220,38,38,0.3);
}}

.study-summary {{
    text-align: center;
    padding: 40px 20px;
}}

.study-summary .big-num {{
    font-size: 3rem;
    font-weight: 800;
}}

@media (max-width: 600px) {{
    .study-card {{
        height: 340px;
    }}
    .study-card-face {{
        padding: 24px;
    }}
    .study-card-front .study-num {{
        font-size: 2.5rem;
    }}
    .study-card-front .study-question {{
        font-size: 1.1rem;
    }}
    .study-actions {{
        flex-direction: column;
    }}
}}
</style>
</head>
<body id="appBody">

<div class="top-bar">
    <span class="brand">📚 毛中特题库</span>
    <div class="stats">
        <span class="stat-item">✅ <span class="stat-num" id="correctCount">0</span></span>
        <span class="stat-item">❌ <span class="stat-num" id="wrongCount">0</span></span>
        <span class="stat-item">📝 <span class="stat-num" id="remainCount">0</span></span>
    </div>
    <div class="controls">
        <select id="chapterFilter" class="btn">
            <option value="all">全部章节</option>
        </select>
        <button id="reviewBtn" class="btn hidden" title="浏览所有错题及解析">📝 错题回顾</button>
        <button id="examBtn" class="btn-exam" title="随机20题模拟考试（10单选+10多选）">⚡ 考前突击</button>
        <button id="flashcardBtn" class="btn" title="简答题闪光卡记忆">🃏 简答题</button>
        <button id="shuffleBtn" class="btn" title="随机打乱题目顺序">🔀 乱序</button>
        <button id="resetBtn" class="btn" title="重置所有进度">🔄 重置</button>
        <button id="themeBtn" class="btn btn-icon" title="切换暗色模式">🌙</button>
    </div>
</div>

<div class="progress-wrap">
    <div class="progress-bar">
        <div class="progress-fill" id="progressFill" style="width:0%"></div>
    </div>
</div>

<div class="container" id="mainContainer">
    <!-- Dynamic content -->
</div>

<script>
const ALL_QUESTIONS = {questions_json};
const SHORT_ANSWERS = {short_answer_json};

// State
let questions = [];
let currentIndex = 0;
let answered = {{}};  // {{ qid: 'correct'|'wrong' }}
let isShuffled = false;
let reviewMode = false;  // true when browsing wrong answers
let theme = localStorage.getItem('quiz-theme') || 'light';

// Exam mode state
let examMode = false;
let examQuestions = [];      // shuffled questions with shuffled options
let examIndex = 0;
let examResults = [];        // {{ correct: bool }}
let examTimer = null;
let examStartTime = 0;
let examElapsed = 0;

// Flashcard mode state
let flashcardMode = false;
let flashcardExpandedAll = false;

// Study mode state
let studyMode = false;
let studyIndex = 0;
let studyFlipped = false;
let studyQueue = [];              // ordered array of card IDs to study
let studyMemorized = new Set();     // card IDs marked as remembered
let studyNotMemorized = new Set();  // card IDs marked as not remembered

// Initialize
function init() {{
    applyTheme();
    populateChapterFilter();
    resetState();
    render();
}}

function applyTheme() {{
    document.documentElement.setAttribute('data-theme', theme);
    document.getElementById('themeBtn').textContent = theme === 'dark' ? '☀️' : '🌙';
    localStorage.setItem('quiz-theme', theme);
}}

function toggleTheme() {{
    theme = theme === 'dark' ? 'light' : 'dark';
    applyTheme();
}}

function populateChapterFilter() {{
    const chapters = [...new Set(ALL_QUESTIONS.map(q => q.chapter))];
    const select = document.getElementById('chapterFilter');
    chapters.forEach(ch => {{
        const opt = document.createElement('option');
        opt.value = ch;
        opt.textContent = ch;
        select.appendChild(opt);
    }});
}}

function resetState() {{
    const chapter = document.getElementById('chapterFilter').value;
    let pool = chapter === 'all'
        ? [...ALL_QUESTIONS]
        : ALL_QUESTIONS.filter(q => q.chapter === chapter);

    if (isShuffled) {{
        shuffleArray(pool);
    }}

    questions = pool;
    currentIndex = 0;
    answered = {{}};
    updateStats();
}}

function shuffleArray(arr) {{
    for (let i = arr.length - 1; i > 0; i--) {{
        const j = Math.floor(Math.random() * (i + 1));
        [arr[i], arr[j]] = [arr[j], arr[i]];
    }}
}}

function updateStats() {{
    const correct = Object.values(answered).filter(v => v === 'correct').length;
    const wrong = Object.values(answered).filter(v => v === 'wrong').length;
    const total = questions.length;
    document.getElementById('correctCount').textContent = correct;
    document.getElementById('wrongCount').textContent = wrong;
    document.getElementById('remainCount').textContent = total - correct - wrong;

    const done = correct + wrong;
    const pct = total > 0 ? (done / total * 100) : 0;
    document.getElementById('progressFill').style.width = pct + '%';

    // Show/hide review button based on wrong count
    const reviewBtn = document.getElementById('reviewBtn');
    if (wrong > 0) {{
        reviewBtn.classList.remove('hidden');
        reviewBtn.textContent = `📝 错题回顾 (${{wrong}})`;
    }} else {{
        reviewBtn.classList.add('hidden');
    }}
}}

function render() {{
    const container = document.getElementById('mainContainer');

    if (flashcardMode) {{
        if (studyMode) {{
            renderStudy();
        }} else {{
            renderFlashcards();
        }}
        return;
    }}

    if (examMode) {{
        renderExam();
        return;
    }}

    if (reviewMode) {{
        renderReview();
        return;
    }}

    if (questions.length === 0) {{
        container.innerHTML = `<div class="empty-state"><div class="emoji">📭</div><h3>该章节暂无题目</h3></div>`;
        return;
    }}

    if (currentIndex >= questions.length) {{
        renderSummary();
        return;
    }}

    const q = questions[currentIndex];
    const qNum = currentIndex + 1;
    const total = questions.length;
    const isMulti = q.type === '多选';
    const state = answered[q.id];

    container.innerHTML = renderCard(q, qNum, total, isMulti, state);
    bindCardEvents(q, isMulti, state);
    window.scrollTo({{ top: 0, behavior: 'smooth' }});
}}

function renderCard(q, qNum, total, isMulti, state) {{
    const typeLabel = isMulti ? '多选题' : '单选题';
    const typeBadge = isMulti ? 'badge-type' : 'badge-chapter';
    const hintText = isMulti ? '（可多选，点击选项选中后提交）' : '（点击选项直接作答）';

    let optionsHTML = q.options.map((opt, idx) => {{
        let cls = '';
        let iconHTML = '';

        if (state) {{
            cls = 'disabled';
            const isCorrectAnswer = q.answers.includes(opt.key);
            const wasSelected = (state === 'correct' && isCorrectAnswer) ||
                (isMulti && isCorrectAnswer) ||
                (!isMulti && opt.key === q.answers[0]);

            if (isCorrectAnswer) {{
                cls += ' correct';
                iconHTML = '<span class="option-icon">✓</span>';
            }} else if (state === 'wrong' && !isCorrectAnswer) {{
                // Keep default appearance for unselected wrong options
            }}
        }}

        return `
            <div class="option ${{cls}}" data-key="${{opt.key}}">
                <span class="option-key">${{opt.key}}</span>
                <span class="option-text">${{opt.text}}</span>
                ${{iconHTML}}
            </div>`;
    }}).join('');

    let resultHTML = '';
    if (state) {{
        const isCorrect = state === 'correct';
        resultHTML = `
            <div class="result-banner ${{isCorrect ? 'correct' : 'wrong'}}">
                ${{isCorrect ? '🎉 回答正确！' : '😞 回答错误'}}
            </div>
            <div class="explanation">
                <div class="explanation-title">📖 解析</div>
                <div class="explanation-text">${{q.explanation}}</div>
            </div>`;
    }}

    let submitHTML = '';
    if (isMulti && !state) {{
        submitHTML = `
            <div class="submit-row">
                <button class="btn-submit" id="submitBtn" disabled>确认提交</button>
                <span style="font-size:0.8rem;color:var(--text-secondary);align-self:center;">请选择至少一个选项</span>
            </div>`;
    }}

    return `
        <div class="card">
            <div class="card-header">
                <span class="question-num">第 ${{qNum}} / ${{total}} 题</span>
                <span class="badge ${{typeBadge}}">${{typeLabel}}</span>
                <span class="badge badge-chapter">${{q.chapter}}</span>
            </div>
            <div class="question-text">${{q.question}}</div>
            <div style="font-size:0.8rem;color:var(--text-secondary);margin-bottom:12px;">${{hintText}}</div>
            <div class="options" id="optionsContainer">
                ${{optionsHTML}}
            </div>
            ${{submitHTML}}
            ${{resultHTML}}
            <div class="nav-row">
                <button class="btn btn-nav" id="prevBtn" ${{currentIndex === 0 ? 'disabled' : ''}}>⬅ 上一题</button>
                <span style="font-size:0.85rem;color:var(--text-secondary);">${{q.id}}</span>
                <button class="btn btn-nav primary" id="nextBtn">
                    ${{currentIndex >= questions.length - 1 ? '🏁 查看结果' : '下一题 ➡'}}
                </button>
            </div>
        </div>`;
}}

function bindCardEvents(q, isMulti, state) {{
    // Single choice: click to answer
    if (!isMulti && !state) {{
        document.querySelectorAll('#optionsContainer .option').forEach(optEl => {{
            optEl.addEventListener('click', () => {{
                const key = optEl.dataset.key;
                const isCorrect = q.answers.includes(key);
                answered[q.id] = isCorrect ? 'correct' : 'wrong';

                // Show the correct answer highlight
                document.querySelectorAll('#optionsContainer .option').forEach(el => {{
                    el.classList.add('disabled');
                    if (q.answers.includes(el.dataset.key)) {{
                        el.classList.add('correct');
                        el.innerHTML += '<span class="option-icon">✓</span>';
                    }} else if (el.dataset.key === key && !isCorrect) {{
                        el.classList.add('wrong');
                        el.classList.add('incorrect-choice');
                        el.innerHTML += '<span class="option-icon">✗</span>';
                    }}
                }});

                updateStats();
                showResult(q, isCorrect);
            }});
        }});
    }}

    // Multi-select: toggle options
    if (isMulti && !state) {{
        const selected = new Set();
        const submitBtn = document.getElementById('submitBtn');

        document.querySelectorAll('#optionsContainer .option').forEach(optEl => {{
            optEl.addEventListener('click', () => {{
                const key = optEl.dataset.key;
                if (selected.has(key)) {{
                    selected.delete(key);
                    optEl.classList.remove('selected');
                }} else {{
                    selected.add(key);
                    optEl.classList.add('selected');
                }}
                submitBtn.disabled = selected.size === 0;
            }});
        }});

        submitBtn.addEventListener('click', () => {{
            const userAnswers = [...selected].sort().join('');
            const correctAnswers = [...q.answers].sort().join('');
            const isCorrect = userAnswers === correctAnswers;
            answered[q.id] = isCorrect ? 'correct' : 'wrong';

            document.querySelectorAll('#optionsContainer .option').forEach(el => {{
                el.classList.add('disabled');
                if (q.answers.includes(el.dataset.key)) {{
                    el.classList.add('correct');
                    if (!el.querySelector('.option-icon')) {{
                        el.innerHTML += '<span class="option-icon">✓</span>';
                    }}
                }} else if (selected.has(el.dataset.key) && !q.answers.includes(el.dataset.key)) {{
                    el.classList.add('wrong');
                    el.classList.add('incorrect-choice');
                    el.innerHTML += '<span class="option-icon">✗</span>';
                }}
            }});

            document.getElementById('submitBtn').remove();
            updateStats();
            showResult(q, isCorrect);
        }});
    }}

    // Navigation
    document.getElementById('prevBtn').addEventListener('click', () => {{
        if (currentIndex > 0) {{
            currentIndex--;
            render();
        }}
    }});

    document.getElementById('nextBtn').addEventListener('click', () => {{
        if (currentIndex < questions.length) {{
            currentIndex++;
            render();
        }}
    }});
}}

function showResult(q, isCorrect) {{
    // Re-render to show result banner and explanation
    const container = document.getElementById('mainContainer');
    const qNum = currentIndex + 1;
    const total = questions.length;
    const isMulti = q.type === '多选';
    const state = answered[q.id];

    // Update the card in place with animation
    container.innerHTML = renderCard(q, qNum, total, isMulti, state);
    bindCardEvents(q, isMulti, state);

    // Scroll to show the explanation
    const explanation = document.querySelector('.explanation');
    if (explanation) {{
        explanation.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
    }}
}}

function renderSummary() {{
    const container = document.getElementById('mainContainer');
    const correct = Object.values(answered).filter(v => v === 'correct').length;
    const wrong = Object.values(answered).filter(v => v === 'wrong').length;
    const total = questions.length;
    const answeredCount = correct + wrong;
    const accuracy = answeredCount > 0 ? Math.round(correct / answeredCount * 100) : 0;

    // Chapter breakdown
    const chapterStats = {{}};
    questions.forEach(q => {{
        if (!chapterStats[q.chapter]) chapterStats[q.chapter] = {{ total: 0, correct: 0, wrong: 0 }};
        chapterStats[q.chapter].total++;
        if (answered[q.id] === 'correct') chapterStats[q.chapter].correct++;
        if (answered[q.id] === 'wrong') chapterStats[q.chapter].wrong++;
    }});

    let chapterRows = Object.entries(chapterStats).map(([ch, stats]) => {{
        const chAccuracy = stats.total > 0 ? Math.round((stats.correct / Math.max(1, stats.correct + stats.wrong)) * 100) : '-';
        return `
            <tr>
                <td>${{ch}}</td>
                <td>${{stats.total}}</td>
                <td>${{stats.correct}}</td>
                <td>${{stats.wrong}}</td>
                <td>${{chAccuracy === '-' ? '-' : chAccuracy + '%'}}</td>
            </tr>`;
    }}).join('');

    let emoji = accuracy >= 90 ? '🏆' : accuracy >= 70 ? '👍' : accuracy >= 50 ? '📖' : '💪';

    container.innerHTML = `
        <div class="card summary">
            <h2>${{emoji}} 答题完成！</h2>
            <div class="big-score">${{accuracy}}%</div>
            <p style="color:var(--text-secondary);">正确率</p>
            <div class="summary-grid">
                <div class="summary-card">
                    <div class="num">${{total}}</div>
                    <div class="label">总题数</div>
                </div>
                <div class="summary-card">
                    <div class="num">${{answeredCount}}</div>
                    <div class="label">已作答</div>
                </div>
                <div class="summary-card">
                    <div class="num" style="color:var(--correct)">${{correct}}</div>
                    <div class="label">✅ 正确</div>
                </div>
                <div class="summary-card">
                    <div class="num" style="color:var(--wrong)">${{wrong}}</div>
                    <div class="label">❌ 错误</div>
                </div>
            </div>

            <h3 style="margin-top:24px;margin-bottom:12px;">📊 章节统计</h3>
            <div style="overflow-x:auto;">
                <table class="review-table">
                    <thead>
                        <tr><th>章节</th><th>题数</th><th>✅ 正确</th><th>❌ 错误</th><th>正确率</th></tr>
                    </thead>
                    <tbody>${{chapterRows}}</tbody>
                </table>
            </div>

            <div class="nav-row" style="justify-content:center;gap:16px;">
                <button class="btn btn-nav primary" id="retryWrongBtn">🔄 重做错题</button>
                <button class="btn btn-nav" id="reviewAllBtn">📋 浏览全部</button>
            </div>
        </div>`;

    document.getElementById('retryWrongBtn').addEventListener('click', retryWrong);
    document.getElementById('reviewAllBtn').addEventListener('click', reviewAll);
}}

function enterReviewMode() {{
    reviewMode = true;
    // Hide chapter filter and shuffle during review
    document.getElementById('chapterFilter').disabled = true;
    document.getElementById('shuffleBtn').disabled = true;
    document.getElementById('reviewBtn').classList.add('active');
    render();
}}

function exitReviewMode() {{
    reviewMode = false;
    document.getElementById('chapterFilter').disabled = false;
    document.getElementById('shuffleBtn').disabled = false;
    document.getElementById('reviewBtn').classList.remove('active');
    render();
}}

function renderReview() {{
    const container = document.getElementById('mainContainer');
    const wrongEntries = Object.entries(answered).filter(([, v]) => v === 'wrong').map(([id]) => parseInt(id));
    const wrongQuestions = ALL_QUESTIONS.filter(q => wrongEntries.includes(q.id));

    if (wrongQuestions.length === 0) {{
        container.innerHTML = `
            <div class="card" style="text-align:center;padding:60px 20px;">
                <div class="emoji" style="font-size:3rem;">🎉</div>
                <h3 style="margin:12px 0;">暂无错题</h3>
                <p style="color:var(--text-secondary);margin-bottom:20px;">继续保持，去答题吧！</p>
                <button class="btn btn-nav primary" onclick="exitReviewMode()">返回答题</button>
            </div>`;
        return;
    }}

    let cardsHTML = wrongQuestions.map((q, idx) => {{
        const isMulti = q.type === '多选';
        const typeLabel = isMulti ? '多选题' : '单选题';
        const correctAnswersStr = q.answers.join('、');

        let optionsHTML = q.options.map(opt => {{
            const isCorrectAnswer = q.answers.includes(opt.key);
            let cls = isCorrectAnswer ? 'correct' : '';
            let icon = isCorrectAnswer ? '<span class="option-icon">✓</span>' : '';
            return `
                <div class="option disabled ${{cls}}" data-key="${{opt.key}}">
                    <span class="option-key">${{opt.key}}</span>
                    <span class="option-text">${{opt.text}}</span>
                    ${{icon}}
                </div>`;
        }}).join('');

        return `
            <div class="review-card">
                <div class="card-header">
                    <span class="badge badge-chapter">${{q.chapter}}</span>
                    <span class="badge badge-type">${{typeLabel}}</span>
                    <span class="question-num">#${{q.id}}</span>
                </div>
                <div class="question-text">${{q.question}}</div>
                <div class="options" style="margin-bottom:12px;">
                    ${{optionsHTML}}
                </div>
                <div class="correct-answer-note">
                    ✅ 正确答案：${{correctAnswersStr}}
                </div>
                <div class="explanation">
                    <div class="explanation-title">📖 解析</div>
                    <div class="explanation-text">${{q.explanation}}</div>
                </div>
            </div>`;
    }}).join('');

    container.innerHTML = `
        <div class="review-bar">
            <div>
                <span class="title">📝 错题回顾</span>
                <span class="info" style="margin-left:12px;">共 ${{wrongQuestions.length}} 道错题</span>
            </div>
            <div style="display:flex;gap:8px;">
                <button class="btn" onclick="retryWrong()">🔄 重做这些题</button>
                <button class="btn btn-nav primary" onclick="exitReviewMode()">← 返回答题</button>
            </div>
        </div>
        ${{cardsHTML}}
        <div class="review-bar" style="justify-content:center;">
            <button class="btn btn-nav primary" onclick="exitReviewMode()">← 返回继续答题</button>
        </div>`;

    window.scrollTo({{ top: 0, behavior: 'smooth' }});
}}

function retryWrong() {{
    reviewMode = false;
    document.getElementById('chapterFilter').disabled = false;
    document.getElementById('shuffleBtn').disabled = false;
    document.getElementById('reviewBtn').classList.remove('active');

    const wrongIds = Object.entries(answered)
        .filter(([, v]) => v === 'wrong')
        .map(([id]) => parseInt(id));
    if (wrongIds.length === 0) {{
        alert('没有错题，太棒了！🎉');
        return;
    }}
    questions = ALL_QUESTIONS.filter(q => wrongIds.includes(q.id));
    if (isShuffled) shuffleArray(questions);
    currentIndex = 0;
    answered = {{}};
    updateStats();
    render();
}}

function reviewAll() {{
    questions = [...ALL_QUESTIONS];
    if (isShuffled) shuffleArray(questions);
    currentIndex = 0;
    answered = {{}};
    updateStats();
    render();
}}

// ========== Exam Mode ==========

function startExam() {{
    // Pick 10 single + 10 multi
    const singlePool = ALL_QUESTIONS.filter(q => q.type === '单选');
    const multiPool = ALL_QUESTIONS.filter(q => q.type === '多选');

    const pickRandom = (pool, n) => {{
        const shuffled = [...pool];
        shuffleArray(shuffled);
        return shuffled.slice(0, n);
    }};

    let selected = [
        ...pickRandom(singlePool, 10),
        ...pickRandom(multiPool, 10)
    ];

    // Shuffle question order
    shuffleArray(selected);

    // Shuffle options within each question, reassign display keys as A/B/C/D
    const KEY_LABELS = ['A','B','C','D','E','F','G','H'];
    examQuestions = selected.map(q => {{
        const shuffledContent = [...q.options];
        shuffleArray(shuffledContent);
        // Map original keys to shuffled positions
        const keyMap = {{}};  // displayLabel -> originalKey
        const shuffledOptions = shuffledContent.map((opt, i) => {{
            keyMap[KEY_LABELS[i]] = opt.key;
            return {{
                ...opt,
                displayKey: KEY_LABELS[i]
            }};
        }});
        return {{
            ...q,
            shuffledOptions,
            keyMap
        }};
    }});

    examIndex = 0;
    examResults = [];
    examMode = true;
    examStartTime = Date.now();
    examElapsed = 0;

    document.getElementById('appBody').classList.add('exam-mode');
    document.getElementById('examBtn').textContent = '🛑 退出突击';
    document.getElementById('examBtn').classList.add('active');

    // Start timer
    examTimer = setInterval(() => {{
        examElapsed = Math.floor((Date.now() - examStartTime) / 1000);
        const timerEl = document.getElementById('examTimerDisplay');
        if (timerEl) {{
            timerEl.textContent = formatTime(examElapsed);
        }}
    }}, 200);

    render();
}}

function exitExam() {{
    if (examTimer) clearInterval(examTimer);
    examMode = false;
    examQuestions = [];
    examIndex = 0;
    examResults = [];
    document.getElementById('appBody').classList.remove('exam-mode');
    document.getElementById('examBtn').textContent = '⚡ 考前突击';
    document.getElementById('examBtn').classList.remove('active');
    render();
}}

function formatTime(seconds) {{
    const m = Math.floor(seconds / 60);
    const s = seconds % 60;
    return `${{String(m).padStart(2,'0')}}:${{String(s).padStart(2,'0')}}`;
}}

function renderExam() {{
    const container = document.getElementById('mainContainer');

    if (examIndex >= examQuestions.length) {{
        renderExamResult();
        return;
    }}

    const q = examQuestions[examIndex];
    const total = examQuestions.length;
    const isMulti = q.type === '多选';
    const feedback = examResults[examIndex];  // undefined = not answered, true/false

    // Progress dots
    let dotsHTML = examQuestions.map((_, i) => {{
        let cls = '';
        if (i < examResults.length) {{
            cls = examResults[i] ? 'done-correct' : 'done-wrong';
        }} else if (i === examIndex) {{
            cls = 'current';
        }}
        return `<div class="dot ${{cls}}"></div>`;
    }}).join('');

    // Timer
    const timeStr = formatTime(examElapsed);

    // Options
    let optionsHTML = q.shuffledOptions.map(opt => {{
        let cls = '';
        let iconHTML = '';
        if (feedback !== undefined) {{
            cls = 'disabled';
            const origKey = q.keyMap[opt.displayKey];
            if (q.answers.includes(origKey)) {{
                cls += ' correct';
                iconHTML = '<span class="option-icon">✓</span>';
            }}
        }}
        return `
            <div class="option ${{cls}}" data-display-key="${{opt.displayKey}}">
                <span class="option-key">${{opt.displayKey}}</span>
                <span class="option-text">${{opt.text}}</span>
                ${{iconHTML}}
            </div>`;
    }}).join('');

    let feedbackHTML = '';
    if (feedback !== undefined) {{
        feedbackHTML = `
            <div class="exam-feedback ${{feedback ? 'correct' : 'wrong'}}">
                ${{feedback ? '✅ 正确！' : '❌ 错误'}}
            </div>`;
    }}

    let submitHTML = '';
    if (isMulti && feedback === undefined) {{
        submitHTML = `
            <div class="submit-row">
                <button class="btn-submit" id="examSubmitBtn" disabled>确认提交</button>
            </div>`;
    }}

    let navHTML = '';
    if (feedback !== undefined) {{
        const isLast = examIndex >= total - 1;
        navHTML = `
            <div class="nav-row">
                <span></span>
                <button class="btn btn-nav primary" id="examNextBtn">
                    ${{isLast ? '🏁 查看成绩' : '下一题 ➡'}}
                </button>
            </div>`;
    }}

    container.innerHTML = `
        <div class="exam-card">
            <div class="exam-progress">${{dotsHTML}}</div>
            <div class="exam-timer">
                <div class="time-display" id="examTimerDisplay">${{timeStr}}</div>
                <div class="time-label">⏱ 用时</div>
            </div>
            <div class="card-header">
                <span class="question-num">第 ${{examIndex + 1}} / ${{total}} 题</span>
                <span class="badge ${{isMulti ? 'badge-type' : 'badge-chapter'}}">${{isMulti ? '多选题' : '单选题'}}</span>
                <span class="badge badge-chapter">${{q.chapter}}</span>
            </div>
            <div class="question-text">${{q.question}}</div>
            <div class="options" id="examOptionsContainer">
                ${{optionsHTML}}
            </div>
            ${{submitHTML}}
            ${{feedbackHTML}}
            ${{navHTML}}
        </div>`;

    bindExamEvents(q, isMulti, feedback);
}}

function bindExamEvents(q, isMulti, feedback) {{
    // Helper: get original key from display key
    const origKey = (dk) => q.keyMap[dk];

    // Single choice: click to answer
    if (!isMulti && feedback === undefined) {{
        document.querySelectorAll('#examOptionsContainer .option').forEach(optEl => {{
            optEl.addEventListener('click', () => {{
                const displayKey = optEl.dataset.displayKey;
                const realKey = origKey(displayKey);
                const isCorrect = q.answers.includes(realKey);
                examResults[examIndex] = isCorrect;

                document.querySelectorAll('#examOptionsContainer .option').forEach(el => {{
                    el.classList.add('disabled');
                    const elRealKey = origKey(el.dataset.displayKey);
                    if (q.answers.includes(elRealKey)) {{
                        el.classList.add('correct');
                        el.innerHTML += '<span class="option-icon">✓</span>';
                    }} else if (el.dataset.displayKey === displayKey && !isCorrect) {{
                        el.classList.add('wrong');
                        el.innerHTML += '<span class="option-icon">✗</span>';
                    }}
                }});

                // Re-render to show feedback + next button
                renderExam();
            }});
        }});
    }}

    // Multi-select
    if (isMulti && feedback === undefined) {{
        const selected = new Set();  // stores display keys
        const submitBtn = document.getElementById('examSubmitBtn');

        document.querySelectorAll('#examOptionsContainer .option').forEach(optEl => {{
            optEl.addEventListener('click', () => {{
                const displayKey = optEl.dataset.displayKey;
                if (selected.has(displayKey)) {{
                    selected.delete(displayKey);
                    optEl.classList.remove('selected');
                }} else {{
                    selected.add(displayKey);
                    optEl.classList.add('selected');
                }}
                submitBtn.disabled = selected.size === 0;
            }});
        }});

        submitBtn.addEventListener('click', () => {{
            const userAnswers = [...selected].map(dk => origKey(dk)).sort().join('');
            const correctAnswers = [...q.answers].sort().join('');
            const isCorrect = userAnswers === correctAnswers;
            examResults[examIndex] = isCorrect;

            document.querySelectorAll('#examOptionsContainer .option').forEach(el => {{
                el.classList.add('disabled');
                const elRealKey = origKey(el.dataset.displayKey);
                if (q.answers.includes(elRealKey)) {{
                    el.classList.add('correct');
                    if (!el.querySelector('.option-icon')) {{
                        el.innerHTML += '<span class="option-icon">✓</span>';
                    }}
                }} else if (selected.has(el.dataset.displayKey) && !q.answers.includes(elRealKey)) {{
                    el.classList.add('wrong');
                    el.innerHTML += '<span class="option-icon">✗</span>';
                }}
            }});

            renderExam();
        }});
    }}

    // Next button
    if (feedback !== undefined) {{
        document.getElementById('examNextBtn').addEventListener('click', () => {{
            examIndex++;
            renderExam();
        }});
    }}
}}

function renderExamResult() {{
    if (examTimer) clearInterval(examTimer);
    const container = document.getElementById('mainContainer');
    const total = examQuestions.length;
    const correct = examResults.filter(r => r).length;
    const wrong = total - correct;
    const accuracy = Math.round(correct / total * 100);
    const timeStr = formatTime(examElapsed);

    let grade, gradeClass;
    if (accuracy >= 90) {{ grade = 'A'; gradeClass = 'grade-a'; }}
    else if (accuracy >= 75) {{ grade = 'B'; gradeClass = 'grade-b'; }}
    else if (accuracy >= 60) {{ grade = 'C'; gradeClass = 'grade-c'; }}
    else {{ grade = 'D'; gradeClass = 'grade-d'; }}

    const emoji = accuracy >= 90 ? '🏆' : accuracy >= 75 ? '👍' : accuracy >= 60 ? '📖' : '💪';

    // Question-by-question breakdown
    let breakdownHTML = examQuestions.map((q, i) => {{
        const isCorrect = examResults[i];
        const isMulti = q.type === '多选';
        const typeLabel = isMulti ? '多选' : '单选';
        const correctAnswers = q.answers.join('、');
        return `
            <div class="review-card" style="border-left-color:${{isCorrect ? 'var(--correct)' : 'var(--wrong)'}};">
                <div class="card-header">
                    <span class="question-num">#${{i + 1}} ${{isCorrect ? '✅' : '❌'}}</span>
                    <span class="badge badge-chapter">${{q.chapter}}</span>
                    <span class="badge ${{isMulti ? 'badge-type' : 'badge-chapter'}}">${{typeLabel}}</span>
                </div>
                <div class="question-text" style="font-size:1rem;">${{q.question}}</div>
                <div class="correct-answer-note">正确答案：${{correctAnswers}}</div>
                <div class="explanation">
                    <div class="explanation-title">📖 解析</div>
                    <div class="explanation-text">${{q.explanation}}</div>
                </div>
            </div>`;
    }}).join('');

    container.innerHTML = `
        <div class="card exam-result">
            <h2>${{emoji}} 突击完成！</h2>
            <div class="big-grade ${{gradeClass}}">${{grade}}</div>
            <p style="color:var(--text-secondary);font-size:1rem;">等级评定</p>
            <div class="summary-grid" style="margin-top:20px;">
                <div class="summary-card">
                    <div class="num">${{correct}}/${{total}}</div>
                    <div class="label">正确率 ${{accuracy}}%</div>
                </div>
                <div class="summary-card">
                    <div class="num">${{timeStr}}</div>
                    <div class="label">⏱ 用时</div>
                </div>
                <div class="summary-card">
                    <div class="num" style="color:var(--correct)">${{correct}}</div>
                    <div class="label">✅ 正确</div>
                </div>
                <div class="summary-card">
                    <div class="num" style="color:var(--wrong)">${{wrong}}</div>
                    <div class="label">❌ 错误</div>
                </div>
            </div>

            <div class="nav-row" style="justify-content:center;gap:12px;margin-top:24px;">
                <button class="btn btn-nav primary" onclick="startExam()">🔄 再来一组</button>
                <button class="btn btn-nav" onclick="exitExam()">← 返回主页</button>
            </div>
        </div>

        <h3 style="margin:24px 0 12px;color:var(--text);">📋 逐题回顾</h3>
        ${{breakdownHTML}}

        <div class="nav-row" style="justify-content:center;margin-bottom:40px;">
            <button class="btn btn-nav primary" onclick="startExam()">🔄 再来一组新题</button>
            <button class="btn btn-nav" onclick="exitExam()">← 返回主页</button>
        </div>`;

    window.scrollTo({{ top: 0, behavior: 'smooth' }});
}}

// ========== Flashcard Mode ==========

// ----- Study Mode (one card at a time) -----

function enterStudyMode() {{
    studyMode = true;
    studyIndex = 0;
    studyFlipped = false;
    studyQueue = SHORT_ANSWERS.map(q => q.id);
    render();
}}

function exitStudyMode() {{
    studyMode = false;
    studyFlipped = false;
    render();
}}

function renderStudy() {{
    const container = document.getElementById('mainContainer');
    const total = studyQueue.length;

    if (studyIndex >= total) {{
        renderStudySummary();
        return;
    }}

    const cardId = studyQueue[studyIndex];
    const q = SHORT_ANSWERS.find(q => q.id === cardId);
    if (!q) {{ studyIndex++; renderStudy(); return; }}
    const memorized = studyMemorized.has(q.id);
    const notMemorized = studyNotMemorized.has(q.id);
    const isClassified = memorized || notMemorized;

    // Progress — based on current queue position, not global sets
    const done = studyIndex;
    const pct = total > 0 ? (done / total * 100) : 0;

    let actionsHTML = '';
    if (studyFlipped) {{
        actionsHTML = `
            <div class="study-actions">
                <button class="btn-remember" onclick="markRemembered(${{q.id}})">
                    ${{memorized ? '✅ 已记住 ✓' : '✅ 记住了'}}
                </button>
                <button class="btn-forget" onclick="markNotRemembered(${{q.id}})">
                    ${{notMemorized ? '🔄 已标记没记住 ✓' : '❌ 没记住'}}
                </button>
            </div>`;
    }}

    container.innerHTML = `
        <div class="study-container">
            <div class="flashcard-controls" style="width:100%;">
                <span class="fc-title">📖 阅读模式 <span style="color:var(--text-secondary);font-weight:400;">(${{studyIndex + 1}}/${{total}})</span></span>
                <div class="fc-actions">
                    <button class="btn" onclick="exitStudyMode()">🃏 返回网格</button>
                </div>
            </div>
            <div class="study-progress">
                <span>进度</span>
                <div class="study-progress-bar">
                    <div class="study-progress-fill" style="width:${{pct}}%"></div>
                </div>
                <span>${{done}}/${{total}}</span>
                <span style="font-size:0.8rem;">✅${{studyMemorized.size}} 🔄${{studyNotMemorized.size}}</span>
            </div>
            <div class="study-card ${{studyFlipped ? 'flipped' : ''}}" id="studyCard" onclick="flipStudyCard()">
                <div class="study-card-inner">
                    <div class="study-card-face study-card-front">
                        ${{isClassified ? `<div class="flashcard-status" style="top:16px;right:16px;font-size:2rem;">${{memorized ? '✅' : '🔄'}}</div>` : ''}}
                        <div class="study-num">${{String(q.id).padStart(2,'0')}}</div>
                        <div class="study-question">${{q.question}}</div>
                        <div class="study-hint">👆 点击卡片翻转查看答案</div>
                    </div>
                    <div class="study-card-face study-card-back">
                        <div class="study-back-title">📖 答案要点</div>
                        <ul class="study-answer-list">
                            ${{q.answer.map(a => `<li>${{a}}</li>`).join('')}}
                        </ul>
                    </div>
                </div>
            </div>
            ${{actionsHTML}}
        </div>`;

    window.scrollTo({{ top: 0, behavior: 'smooth' }});
}}

function flipStudyCard() {{
    studyFlipped = true;
    renderStudy();
}}

function markRemembered(id) {{
    studyMemorized.add(id);
    studyNotMemorized.delete(id);
    advanceStudy();
}}

function markNotRemembered(id) {{
    studyNotMemorized.add(id);
    studyMemorized.delete(id);
    advanceStudy();
}}

function advanceStudy() {{
    studyIndex++;
    studyFlipped = false;
    if (studyIndex >= studyQueue.length) {{
        renderStudySummary();
    }} else {{
        renderStudy();
    }}
}}

function renderStudySummary() {{
    const container = document.getElementById('mainContainer');
    const total = SHORT_ANSWERS.length;
    const remembered = studyMemorized.size;
    const notRemembered = studyNotMemorized.size;
    const unclassified = total - remembered - notRemembered;

    container.innerHTML = `
        <div class="card study-summary">
            <h2>🎉 阅读完成！</h2>
            <div class="summary-grid">
                <div class="summary-card">
                    <div class="num" style="color:var(--correct)">${{remembered}}</div>
                    <div class="label">✅ 记住了</div>
                </div>
                <div class="summary-card">
                    <div class="num" style="color:var(--wrong)">${{notRemembered}}</div>
                    <div class="label">🔄 没记住</div>
                </div>
                <div class="summary-card">
                    <div class="num" style="color:var(--text-secondary)">${{unclassified}}</div>
                    <div class="label">📝 未分类</div>
                </div>
            </div>
            <div class="nav-row" style="justify-content:center;gap:12px;margin-top:20px;">
                ${{notRemembered > 0 ? `<button class="btn btn-nav primary" onclick="retryNotRemembered()">🔄 重做没记住的 (${{notRemembered}})</button>` : ''}}
                <button class="btn btn-nav" onclick="resetStudyAndRestart()">🔁 重新开始</button>
                <button class="btn btn-nav" onclick="exitStudyMode()">🃏 返回网格</button>
            </div>
        </div>`;

    window.scrollTo({{ top: 0, behavior: 'smooth' }});
}}

function retryNotRemembered() {{
    studyIndex = 0;
    studyFlipped = false;
    // Build queue from only not-remembered cards
    const idsToRetry = [...studyNotMemorized];
    studyQueue = idsToRetry;
    // Clear not-remembered and memorized for these cards (fresh start)
    idsToRetry.forEach(id => {{
        studyNotMemorized.delete(id);
        studyMemorized.delete(id);
    }});
    renderStudy();
}}

function resetStudyAndRestart() {{
    studyIndex = 0;
    studyFlipped = false;
    studyQueue = SHORT_ANSWERS.map(q => q.id);
    studyMemorized.clear();
    studyNotMemorized.clear();
    renderStudy();
}}

function enterFlashcardMode() {{
    flashcardMode = true;
    flashcardExpandedAll = false;
    document.getElementById('flashcardBtn').classList.add('active');
    // Disable other controls
    document.getElementById('chapterFilter').disabled = true;
    document.getElementById('shuffleBtn').disabled = true;
    document.getElementById('reviewBtn').classList.add('hidden');
    document.getElementById('examBtn').style.display = 'none';
    if (examMode) exitExam();
    if (reviewMode) exitReviewMode();
    render();
}}

function exitFlashcardMode() {{
    flashcardMode = false;
    flashcardExpandedAll = false;
    document.getElementById('flashcardBtn').classList.remove('active');
    document.getElementById('chapterFilter').disabled = false;
    document.getElementById('shuffleBtn').disabled = false;
    document.getElementById('examBtn').style.display = '';
    updateStats();  // restores reviewBtn visibility
    render();
}}

function renderFlashcards() {{
    const container = document.getElementById('mainContainer');
    const cards = [...SHORT_ANSWERS];

    const cardsHTML = cards.map(q => {{
        let statusBadge = '';
        if (studyMemorized.has(q.id)) {{
            statusBadge = '<div class="flashcard-status">✅</div>';
        }} else if (studyNotMemorized.has(q.id)) {{
            statusBadge = '<div class="flashcard-status">🔄</div>';
        }}
        return `
        <div class="flashcard" id="fc-${{q.id}}" onclick="toggleFlashcard(${{q.id}})">
            ${{statusBadge}}
            <div class="flashcard-inner">
                <div class="flashcard-face flashcard-front">
                    <div class="card-num">${{String(q.id).padStart(2,'0')}}</div>
                    <div class="card-question">${{q.question}}</div>
                    <div class="card-hint">👆 点击翻转查看答案</div>
                </div>
                <div class="flashcard-face flashcard-back">
                    <div class="back-title">📖 答案要点</div>
                    <ul class="answer-list">
                        ${{q.answer.map(a => `<li>${{a}}</li>`).join('')}}
                    </ul>
                </div>
            </div>
        </div>`;
    }}).join('');

    container.innerHTML = `
        <div class="flashcard-controls">
            <span class="fc-title">🃏 简答题闪光卡 <span style="color:var(--text-secondary);font-weight:400;">(${{cards.length}} 张)</span></span>
            <div class="fc-actions">
                <button class="btn btn-nav primary" onclick="enterStudyMode()">📖 阅读模式</button>
                <button class="btn" onclick="expandAllFlashcards()">📖 全部展开</button>
                <button class="btn" onclick="collapseAllFlashcards()">🔄 全部翻转</button>
                <button class="btn" onclick="shuffleFlashcards()">🔀 随机排序</button>
                <button class="btn btn-nav primary" onclick="exitFlashcardMode()">← 返回选择题</button>
            </div>
        </div>
        <div class="flashcard-grid" id="flashcardGrid">
            ${{cardsHTML}}
        </div>`;

    // If expandedAll was true, flip all
    if (flashcardExpandedAll) {{
        document.querySelectorAll('.flashcard').forEach(el => el.classList.add('flipped'));
    }}

    window.scrollTo({{ top: 0, behavior: 'smooth' }});
}}

function toggleFlashcard(id) {{
    const card = document.getElementById('fc-' + id);
    if (card) {{
        card.classList.toggle('flipped');
    }}
}}

function expandAllFlashcards() {{
    flashcardExpandedAll = true;
    document.querySelectorAll('.flashcard').forEach(el => el.classList.add('flipped'));
}}

function collapseAllFlashcards() {{
    flashcardExpandedAll = false;
    document.querySelectorAll('.flashcard').forEach(el => el.classList.remove('flipped'));
}}

function shuffleFlashcards() {{
    const grid = document.getElementById('flashcardGrid');
    if (!grid) return;
    const cards = Array.from(grid.children);
    // Fisher-Yates shuffle
    for (let i = cards.length - 1; i > 0; i--) {{
        const j = Math.floor(Math.random() * (i + 1));
        grid.appendChild(cards[j]);
    }}
    // Scroll to top
    window.scrollTo({{ top: 0, behavior: 'smooth' }});
}}

// Event Listeners
document.getElementById('flashcardBtn').addEventListener('click', () => {{
    if (flashcardMode) {{
        exitFlashcardMode();
    }} else {{
        enterFlashcardMode();
    }}
}});

document.getElementById('examBtn').addEventListener('click', () => {{
    if (examMode) {{
        if (confirm('确定要退出考前突击吗？当前进度将丢失。')) {{
            exitExam();
        }}
    }} else {{
        if (reviewMode) {{
            reviewMode = false;
            document.getElementById('reviewBtn').classList.remove('active');
            document.getElementById('chapterFilter').disabled = false;
            document.getElementById('shuffleBtn').disabled = false;
        }}
        startExam();
    }}
}});

document.getElementById('reviewBtn').addEventListener('click', () => {{
    if (reviewMode) {{
        exitReviewMode();
    }} else {{
        enterReviewMode();
    }}
}});

document.getElementById('chapterFilter').addEventListener('change', () => {{
    if (examMode || flashcardMode) return;
    reviewMode = false;
    document.getElementById('reviewBtn').classList.remove('active');
    document.getElementById('chapterFilter').disabled = false;
    document.getElementById('shuffleBtn').disabled = false;
    resetState();
    render();
}});

document.getElementById('shuffleBtn').addEventListener('click', () => {{
    if (examMode || flashcardMode) return;
    reviewMode = false;
    document.getElementById('reviewBtn').classList.remove('active');
    document.getElementById('chapterFilter').disabled = false;
    document.getElementById('shuffleBtn').disabled = false;
    isShuffled = !isShuffled;
    document.getElementById('shuffleBtn').classList.toggle('active', isShuffled);
    resetState();
    render();
}});

document.getElementById('resetBtn').addEventListener('click', () => {{
    if (examMode || flashcardMode) return;
    if (confirm('确定要重置当前进度吗？所有作答记录将被清除。')) {{
        reviewMode = false;
        document.getElementById('reviewBtn').classList.remove('active');
        document.getElementById('chapterFilter').disabled = false;
        document.getElementById('shuffleBtn').disabled = false;
        resetState();
        render();
    }}
}});

document.getElementById('themeBtn').addEventListener('click', toggleTheme);

// Keyboard navigation
document.addEventListener('keydown', (e) => {{
    if (flashcardMode) return;
    if (examMode) {{
        if (e.key === 'ArrowRight' && examResults[examIndex] !== undefined && examIndex < examQuestions.length) {{
            e.preventDefault();
            examIndex++;
            renderExam();
        }}
        return;
    }}
    if (e.key === 'ArrowLeft' && currentIndex > 0 && !reviewMode) {{
        e.preventDefault();
        currentIndex--;
        render();
    }} else if (e.key === 'ArrowRight' && !reviewMode) {{
        e.preventDefault();
        if (currentIndex < questions.length) {{
            currentIndex++;
            render();
        }}
    }}
}});

// Start
init();
</script>
</body>
</html>'''

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"Generated {output_path}")
    print(f"Total questions: {len(questions)}")
    import os
    size_kb = os.path.getsize(output_path) / 1024
    print(f"File size: {size_kb:.1f} KB")

if __name__ == '__main__':
    generate_html('questions.json', 'short_answer.json', 'quiz.html')
