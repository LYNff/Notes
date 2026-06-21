---
cssclasses:
  - home-page
  - hide-properties
obsidianUIMode: preview
---

```dataviewjs
// ============================================================
//  Timeline Sidebar — reads Calendar/Schedule.md
//  Smart date parsing:
//    "24 | event"          → current month + day
//    "7-12 | event"        → month + day, current year
//    "2026-06-18 | event"  → full date as-is
//    "下午 | event"        → today + time-of-day
//    "明天上午 | event"    → tomorrow morning
//    "24 下午 | event"     → day + time-of-day
// ============================================================

const content = await dv.io.load("Calendar/Schedule.md");
const today = new Date();
today.setHours(0, 0, 0, 0);

const curYear = today.getFullYear();
const curMonth = today.getMonth();
const WEEKDAYS = ["周日", "周一", "周二", "周三", "周四", "周五", "周六"];
const MONTHS = ["一月", "二月", "三月", "四月", "五月", "六月",
                "七月", "八月", "九月", "十月", "十一月", "十二月"];

function parseDate(raw) {
    raw = raw.trim();
    let m;

    // 1. Full date: YYYY-MM-DD
    m = raw.match(/^(\d{4})-(\d{1,2})-(\d{1,2})$/);
    if (m) return { date: new Date(+m[1], +m[2] - 1, +m[3]), time: null };

    // 2. Month-Day with optional time: M-D [上午/下午/...]
    m = raw.match(/^(\d{1,2})-(\d{1,2})\s*(上午|中午|下午|傍晚|晚上)?$/);
    if (m) return { date: new Date(curYear, +m[1] - 1, +m[2]), time: m[3] || null };

    // 3. Day-only with optional time: D [上午/下午/...]
    m = raw.match(/^(\d{1,2})\s*(上午|中午|下午|傍晚|晚上)?$/);
    if (m) return { date: new Date(curYear, curMonth, +m[1]), time: m[2] || null };

    // 4. Relative day + optional time: 明天/后天/大后天 [上午/...]
    const offsets = { '明天': 1, '后天': 2, '大后天': 3 };
    for (const [kw, off] of Object.entries(offsets)) {
        m = raw.match(new RegExp(`^${kw}\\s*(上午|中午|下午|傍晚|晚上)?$`));
        if (m) {
            const d = new Date(today); d.setDate(d.getDate() + off);
            return { date: d, time: m[1] || null };
        }
    }

    // 5. "今天" + optional time
    m = raw.match(/^今天\s*(上午|中午|下午|傍晚|晚上)?$/);
    if (m) return { date: new Date(today), time: m[1] || null };

    // 6. Time-only → today
    m = raw.match(/^(上午|中午|下午|傍晚|晚上)$/);
    if (m) return { date: new Date(today), time: m[1] };

    return null;
}

const TIME_ICONS = { '上午': '🌅', '中午': '☀️', '下午': '🌤️', '傍晚': '🌆', '晚上': '🌙' };
const TIME_CLASSES = { '上午': 'tl-time-morning', '中午': 'tl-time-noon', '下午': 'tl-time-afternoon', '傍晚': 'tl-time-dusk', '晚上': 'tl-time-night' };

const lineRe = /^\s*(.+?)\s*\|\s*(.+?)\s*$/gm;
let events = [];
let match;
while ((match = lineRe.exec(content)) !== null) {
    const parsed = parseDate(match[1]);
    const title = match[2];
    if (parsed && parsed.date && !isNaN(parsed.date.getTime())) {
        events.push({ date: parsed.date, time: parsed.time, title });
    }
}

// ── Auto-expand time-only entries ──
// "下午 | task" → "19 下午 | task" so the date sticks and won't shift tomorrow
let fixedContent = content;
const timeOnlyLineRe = /^(\s*)(上午|中午|下午|傍晚|晚上)(\s*\|\s*.+)$/gm;
let expanded = false;
fixedContent = fixedContent.replace(timeOnlyLineRe, (_m, sp, time, rest) => {
    expanded = true;
    return `${sp}${today.getDate()} ${time}${rest}`;
});
if (expanded) {
    const sFile = app.vault.getAbstractFileByPath("Calendar/Schedule.md");
    if (sFile) {
        await app.vault.modify(sFile, fixedContent);
        // Re-parse with expanded content
        events = [];
        while ((match = lineRe.exec(fixedContent)) !== null) {
            const parsed = parseDate(match[1]);
            const title = match[2];
            if (parsed && parsed.date && !isNaN(parsed.date.getTime())) {
                events.push({ date: parsed.date, time: parsed.time, title });
            }
        }
    }
}

// ── Move finished items to Finished Schedule.md ──
const scheduleFile = app.vault.getAbstractFileByPath("Calendar/Schedule.md");
if (scheduleFile) {
    const rawContent = await app.vault.read(scheduleFile);
    const rawLines = rawContent.split('\n');

    const TIME_END = { '上午': 12*60, '中午': 13*60, '下午': 18*60, '傍晚': 19*60, '晚上': 23*60+59 };
    const now = new Date();
    const nowMinutes = now.getHours() * 60 + now.getMinutes();
    const singleRe = /^\s*(.+?)\s*\|\s*(.+?)\s*$/;

    const activeLines = [];
    const finishedLines = [];

    for (const line of rawLines) {
        const m = line.match(singleRe);
        if (!m) { activeLines.push(line); continue; }

        const parsed = parseDate(m[1]);
        const title = m[2];
        if (!parsed || !parsed.date || isNaN(parsed.date.getTime())) {
            activeLines.push(line); continue;
        }

        const diff = daysBetween(today, parsed.date);
        let finished = false;

        if (diff < 0) {
            // Date already passed
            finished = true;
        } else if (diff === 0 && parsed.time) {
            // Today + time label: check if the time period has passed
            const endMin = TIME_END[parsed.time];
            if (endMin !== undefined && nowMinutes > endMin) {
                finished = true;
            }
        }

        if (finished) {
            const timeStr = parsed.time ? ` ${parsed.time}` : '';
            finishedLines.push(`${fmtDate(parsed.date)}${timeStr} | ${title}`);
        } else {
            activeLines.push(line);
        }
    }

    if (finishedLines.length > 0) {
        // Write back active lines to Schedule.md
        await app.vault.modify(scheduleFile, activeLines.join('\n'));

        // Append to Finished Schedule.md
        const finishedFile = app.vault.getAbstractFileByPath("Calendar/Finished Schedule.md");
        if (finishedFile) {
            const existing = (await app.vault.read(finishedFile)).trimEnd();
            const sep = existing ? '\n' : '';
            await app.vault.modify(finishedFile, existing + sep + finishedLines.join('\n'));
        } else {
            await app.vault.create("Calendar/Finished Schedule.md", finishedLines.join('\n'));
        }

        // Re-parse events from updated Schedule.md
        events = [];
        const newContent = activeLines.join('\n');
        const parseRe = /^\s*(.+?)\s*\|\s*(.+?)\s*$/gm;
        let m2;
        while ((m2 = parseRe.exec(newContent)) !== null) {
            const p2 = parseDate(m2[1]);
            const t2 = m2[2];
            if (p2 && p2.date && !isNaN(p2.date.getTime())) {
                events.push({ date: p2.date, time: p2.time, title: t2 });
            }
        }
    }
}

events.sort((a, b) => a.date - b.date);

function fmtDate(d) {
    const mm = String(d.getMonth() + 1).padStart(2, '0');
    const dd = String(d.getDate()).padStart(2, '0');
    return `${d.getFullYear()}-${mm}-${dd}`;
}

function daysBetween(a, b) {
    return Math.round((b - a) / 86400000);
}

// --- Render timeline content ---
dv.container.classList.add('hp-timeline-sidebar');

const titleEl = dv.el('div', '📅 日程时间轴');
titleEl.classList.add('hp-sidebar-title');

if (events.length === 0) {
    const emptyEl = dv.el('div', '');
    emptyEl.innerHTML = '<div class="timeline-sidebar"><div class="timeline-empty">📭 暂无 upcoming 日程</div></div>';
} else {
    let html = `<div class="timeline-sidebar">`;
    let lastMonth = -1;

    for (const ev of events) {
        const d = ev.date;
        const monthIdx = d.getMonth();
        const diff = daysBetween(today, d);
        const isToday = diff === 0;
        const isPast = diff < 0;
        if (isPast) continue;

        if (monthIdx !== lastMonth) {
            lastMonth = monthIdx;
            html += `<div class="timeline-month">${MONTHS[monthIdx]} ${d.getFullYear()}</div>`;
        }

        let dotClass = "upcoming";
        if (isToday) dotClass = "today";
        else if (isPast) dotClass = "past";

        let dateClass = isToday ? " today" : "";

        // Time-of-day badge
        let timeBadgeHTML = "";
        if (ev.time) {
            const icon = TIME_ICONS[ev.time] || '';
            const cls = TIME_CLASSES[ev.time] || '';
            timeBadgeHTML = `<span class="timeline-time ${cls}">${icon} ${ev.time}</span>`;
        }

        let countdownHTML = "";
        if (isToday) {
            countdownHTML = `<span class="timeline-countdown urgent">今天</span>`;
        } else if (diff > 0 && diff <= 7) {
            countdownHTML = `<span class="timeline-countdown urgent">${diff}天后</span>`;
        } else if (diff > 7 && diff <= 30) {
            countdownHTML = `<span class="timeline-countdown">${diff}天后</span>`;
        }

        html += `
            <div class="timeline-event">
                <div class="timeline-dot ${dotClass}"></div>
                <div class="timeline-card">
                    <span class="timeline-date${dateClass}">${fmtDate(d)}</span>
                    ${timeBadgeHTML}
                    ${countdownHTML}
                    <span class="timeline-title">${ev.title}</span>
                </div>
            </div>`;
    }
    html += `</div>`;

    const tlEl = dv.el('div', '');
    tlEl.innerHTML = html;
}

// --- Project Summary: render below timeline in the sidebar ---
const projects = dv.pages().where(p => p.type === "project");
const doing   = projects.where(p => p.status === "Doing");
const planned = projects.where(p => p.status === "plan");
const done    = projects.where(p => p.status === "Done");

if (doing.length + planned.length + done.length > 0) {
    const projDiv = dv.el('div', '');
    projDiv.classList.add('hp-projects');
    let pHtml = '<div class="hp-sidebar-divider"></div>';
    pHtml += '<a data-href="project" href="project" class="internal-link hp-proj-title-link" style="display:block;text-decoration:none !important;color:inherit;"><div class="hp-sidebar-title" style="margin-top:4px;">📂 阶段项目</div></a>';

    function renderProject(p) {
        const name = p.file.name;
        const prog = Number(p.progress) || Number(p.进展) || 0;
        let item = `<a data-href="${name}" href="${name}" class="internal-link hp-proj-link">${name}</a>`;
        if (prog > 0) {
            const pct = Math.min(100, Math.max(0, prog));
            item += `<div class="hp-progress-wrap"><div class="hp-progress-bar"><div class="hp-progress-fill" style="width:${pct}%"></div></div><span class="hp-progress-pct">${pct}%</span></div>`;
        }
        return item;
    }

    if (doing.length > 0) {
        pHtml += '<div class="hp-proj-group"><span class="hp-proj-dot doing"></span>进行中</div>';
        for (const p of doing) pHtml += renderProject(p);
    }
    if (planned.length > 0) {
        pHtml += '<div class="hp-proj-group"><span class="hp-proj-dot planned"></span>未开始</div>';
        for (const p of planned) pHtml += renderProject(p);
    }
    if (done.length > 0) {
        pHtml += '<div class="hp-proj-group"><span class="hp-proj-dot done"></span>已完成</div>';
        for (const p of done) pHtml += renderProject(p);
    }

    projDiv.innerHTML = pHtml;
}

// --- Two-column layout: inject !important CSS + fixed timeline ---
setTimeout(() => {
    let tlBlock = dv.container;
    while (tlBlock && tlBlock.parentElement && !tlBlock.classList.contains('block-language-dataviewjs')) {
        tlBlock = tlBlock.parentElement;
    }
    if (!tlBlock || !tlBlock.parentElement) return;
    if (tlBlock.dataset.hpDone) return;
    tlBlock.dataset.hpDone = '1';

    // Inject CSS to shrink content (covers multiple Obsidian internal selectors)
    const style = document.createElement('style');
    style.id = 'hp-layout-style';
    style.textContent = `
      .home-page .markdown-preview-view,
      .home-page .markdown-preview-sizer,
      .home-page .markdown-preview-section {
        max-width: calc(100% - 360px) !important;
        margin-left: 0 !important;
        margin-right: 360px !important;
      }
      .home-page .markdown-reading-view {
        padding-right: 360px !important;
      }
    `;
    document.head.appendChild(style);

    // Pin timeline to viewport right
    tlBlock.classList.add('hp-timeline-block');
    tlBlock.style.position = 'fixed';
    tlBlock.style.top = '68px';
    tlBlock.style.right = '24px';
    tlBlock.style.width = '320px';
    tlBlock.style.maxHeight = 'calc(100vh - 100px)';
    tlBlock.style.overflowY = 'auto';
    tlBlock.style.zIndex = '5';
}, 200);
```

## 🗓️ 任务看板 

>[!multi-column]
>
>> [!success] ☀️ 今日计划
>> ```tasks
>> not done
>> due today
>> # 隐藏多余的标记让界面更整洁
>> hide due date
>> hide task count
>> hide backlink
>> ```
>
>> [!warning] ⏳ 延期计划
>> ```tasks
>> not done
>> due before today
>> # 按过期天数排序，先解决拖延最久的
>> sort by due
>> hide task count
>> hide backlink
>> ```

---
## 🏅 任务复盘 (To-Do List)

> [!multi-column]
>
>> [!success] 🌟 本周完成任务
>> ```tasks
>> done this week
>> hide due date
>> hide backlink
>> hide task count
>> ```
>
>> [!info] 🏆 本月完成任务
>> ```tasks
>> done this month
>> hide due date
>> hide backlink
>> hide task count
>> ```

---
## 🦺 DDL

> [!multi-column]
>
>> [!important] 🚨 DDL 
>> ```tasks
>> not done
>> has due date
>> path includes To do list
>> sort by due
>> hide backlink
>> ```
>
>> [!todo] 📥 To do
>> ```tasks
>> not done
>> no due date
>> no start date
>> no scheduled date
>> sort by priority
>> hide backlink
>> ```

---
## 📊 贡献图
```contributionGraph
title: Words Contributions
graphType: default
dateRangeValue: 365
dateRangeType: LATEST_DAYS
startOfWeek: 1
showCellRuleIndicators: true
titleStyle:
  textAlign: center
  fontSize: 15px
  fontWeight: normal
dataSource:
  type: PAGE
  value: ""
  dateField:
    type: FILE_MTIME
fillTheScreen: true
enableMainContainerShadow: false
cellStyleRules:
  - id: Ocean_a
    color: "#8dd1e2"
    min: 1
    max: 2
  - id: Ocean_b
    color: "#63a1be"
    min: 2
    max: 3
  - id: Ocean_c
    color: "#376d93"
    min: 3
    max: 5
  - id: Ocean_d
    color: "#012f60"
    min: 5
    max: 9999

```