---
cssclasses:
  - project-dashboard
obsidianUIMode: preview
projects:
  - name: Leetcode Hot 100
    type: 算法刷题
    progress: 40
    status: Doing
    notes: hot100
  - name: CSAPP
    type: 课程学习
    progress: 45
    status: Doing
    notes: CSAPP
  - name: ICSPA
    type: 课程学习
    progress: 0
    status: plan
    notes: ICSPA
  - name: CS231n
    type: 课程学习
    progress: 0
    status: plan
    notes: CS231n
  - name: NJUOJ
    type: 课程学习
    progress: 0
    status: plan
    notes: ""
  - name: CS336
    type: 课程学习
    progress: 0
    status: plan
    notes: ""
  - name: hello agent
    type: 项目
    progress: 0
    status: plan
    notes: ""
  - name: 科研
    type: 科研
    progress: 0
    status: plan
    notes: ""
  - name: 吴恩达机器学习
    type: 课程学习
    progress: 100
    status: Done
    notes: 吴恩达机器学习
---

# 📂 项目面板

```dataviewjs
const C = dv.container;

// ---- Load ----
const fm = dv.current();
let projects = Array.isArray(fm.projects)
  ? fm.projects.map((p, i) => ({ ...p, _idx: i }))
  : [];

const fp = fm.file.path;
const TFile = app.vault.getAbstractFileByPath(fp);

// ---- Helpers ----
const clamp = (v, lo, hi) => Math.max(lo, Math.min(hi, v));
const esc = s => (s == null) ? "" : String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
const pc = v => v >= 100 ? "#16a34a" : v >= 70 ? "#22c55e" : v >= 30 ? "#f59e0b" : "#ef4444";
const STATUS = ["plan", "Doing", "Done"];
const SL = { plan: "未开始", Doing: "进行中", Done: "已完成" };
let filter = "all"; // current filter: "all", "plan", "Doing", "Done"
function isActive(f) { return filter === f ? "box-shadow:inset 0 0 0 2px var(--interactive-accent);" : ""; }
function statusStyle(s) {
  if (s === "Doing") return "background:#dcfce7;color:#16a34a;";
  if (s === "Done")  return "background:#f3f4f6;color:#6b7280;";
  return "background:#fef9c3;color:#ca8a04;";
}

// ---- Auto-status (bidirectional) ----
function autoStatus(p) {
  const v = Number(p.progress) || 0;
  if (v > 0 && p.status === "plan")   p.status = "Doing";
  if (v >= 100 && p.status === "Doing") p.status = "Done";
  if (v < 100 && p.status === "Done")  p.status = "Doing";
  if (v === 0 && p.status === "Doing") p.status = "plan";
}

// ---- Save ----
async function save() {
  const clean = projects.map(({ _idx, ...r }) => r);
  await app.fileManager.processFrontMatter(TFile, fm2 => { fm2.projects = clean; });
}

// ---- Note link renderer ----
function noteLink(raw) {
  if (!raw || !raw.trim()) return '<span class="pd-notes-empty">—</span>';
  const t = raw.trim();
  const m = t.match(/^\[\[([^\]]+)\]\]$/);
  const target = m ? m[1] : t;
  return `<a data-href="${esc(target)}" href="${esc(target)}" class="pd-notes internal-link" data-tooltip-position="top">${esc(target)}</a>`;
}

// ====================================================================
function render() {
  C.empty();
  const wrap = dv.el("div");

  const total = projects.length;
  const doing = projects.filter(p => p.status === "Doing").length;
  const plan  = projects.filter(p => p.status === "plan").length;
  const done  = projects.filter(p => p.status === "Done").length;

  let h = "";

  // ── Summary cards ──
  h += `<div style="display:flex;gap:12px;margin-bottom:20px;">`;
  h += `<div class="pd-filter-card" data-filter="all" style="flex:1;background:var(--background-primary-alt);border-radius:10px;padding:14px 18px;text-align:center;cursor:pointer;transition:box-shadow 0.15s;${isActive("all")}"><div style="font-size:1.8em;font-weight:700;">${total}</div><div style="font-size:0.8em;color:var(--text-muted);margin-top:2px;">总项目</div></div>`;
  h += `<div class="pd-filter-card" data-filter="Doing" style="flex:1;background:var(--background-primary-alt);border-radius:10px;padding:14px 18px;text-align:center;cursor:pointer;transition:box-shadow 0.15s;${isActive("Doing")}"><div style="font-size:1.8em;font-weight:700;color:#16a34a;">${doing}</div><div style="font-size:0.8em;color:var(--text-muted);margin-top:2px;">进行中</div></div>`;
  h += `<div class="pd-filter-card" data-filter="plan" style="flex:1;background:var(--background-primary-alt);border-radius:10px;padding:14px 18px;text-align:center;cursor:pointer;transition:box-shadow 0.15s;${isActive("plan")}"><div style="font-size:1.8em;font-weight:700;color:#ca8a04;">${plan}</div><div style="font-size:0.8em;color:var(--text-muted);margin-top:2px;">未开始</div></div>`;
  h += `<div class="pd-filter-card" data-filter="Done" style="flex:1;background:var(--background-primary-alt);border-radius:10px;padding:14px 18px;text-align:center;cursor:pointer;transition:box-shadow 0.15s;${isActive("Done")}"><div style="font-size:1.8em;font-weight:700;color:#6b7280;">${done}</div><div style="font-size:0.8em;color:var(--text-muted);margin-top:2px;">已完成</div></div>`;
  h += `</div>`;

  // ── Table header ──
  h += `<div class="pd-header" style="display:flex;align-items:center;gap:8px;padding:8px 12px;font-size:0.82em;font-weight:700;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.05em;border-bottom:2px solid var(--background-modifier-border);">
    <span style="width:18px;flex:0 0 auto;"></span>
    <span style="flex:2;min-width:80px;">项目名称</span>
    <span style="width:30px;flex:0 0 auto;"></span>
    <span style="flex:1;min-width:60px;text-align:center;">类型</span>
    <span style="flex:1;min-width:50px;text-align:center;">状态</span>
    <span style="flex:3;min-width:100px;text-align:center;">进度</span>
    <span style="flex:2;min-width:80px;text-align:center;">关联笔记</span>
    <span style="width:24px;flex:0 0 auto;"></span>
    <span style="width:28px;flex:0 0 auto;"></span>
  </div>`;

  // ── Project rows ──
  const filtered = filter === "all" ? projects : projects.filter(p => p.status === filter);
  if (filtered.length === 0) {
    h += `<div class="pd-empty">📋 ${filter === "all" ? "暂无项目" : "暂无" + (SL[filter] || "") + "项目"}</div>`;
  } else {
    for (const p of filtered) {
      const idx = p._idx;
      const pct = clamp(Number(p.progress) || 0, 0, 100);
      const sl = SL[p.status] || p.status;
      const ss = statusStyle(p.status);

      h += `<div class="pd-row" data-idx="${idx}" style="display:flex;align-items:center;gap:8px;padding:6px 12px;border-bottom:1px solid var(--background-modifier-border);font-size:0.95em;line-height:1.3;transition:background 0.15s;">`;

      // Drag handle
      h += `<span class="pd-grip" data-idx="${idx}" style="width:18px;flex:0 0 auto;color:var(--text-faint);cursor:grab;user-select:none;font-size:0.8em;text-align:center;letter-spacing:-1px;" title="拖拽排序">⋮⋮</span>`;

      // Name
      h += `<span class="pd-ed" data-field="name" data-idx="${idx}" style="flex:2;min-width:80px;font-weight:600;color:var(--text-normal);cursor:text;outline:none;padding:2px 4px;border-radius:3px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;" title="双击编辑">${esc(p.name)}</span>`;

      // Spacer
      h += `<span style="width:30px;flex:0 0 auto;"></span>`;

      // Type
      h += `<span class="pd-ed pd-type" data-field="type" data-idx="${idx}" style="flex:1;min-width:60px;text-align:center;display:inline-block;padding:2px 8px;border-radius:10px;font-size:0.82em;background:var(--background-modifier-hover);color:var(--text-muted);cursor:text;outline:none;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;" title="双击编辑">${esc(p.type || "—")}</span>`;

      // Status
      h += `<span class="pd-st" data-idx="${idx}" style="flex:1;min-width:50px;text-align:center;display:inline-block;padding:3px 0;border-radius:12px;font-size:0.78em;font-weight:600;cursor:pointer;user-select:none;${ss}">${sl}</span>`;

      // Progress — centered bar group
      h += `<div style="flex:3;min-width:100px;display:flex;align-items:center;justify-content:center;padding:0 4px;">`;
      h += `<div style="display:flex;align-items:center;gap:5px;width:100%;">`;
      h += `<button class="pd-minus" data-idx="${idx}" style="width:20px;height:20px;flex:0 0 auto;font-size:0.8em;font-weight:700;cursor:pointer;display:inline-flex;align-items:center;justify-content:center;padding:0;">−</button>`;
      h += `<div class="pd-bar" data-idx="${idx}" style="flex:1;min-width:40px;height:8px;overflow:hidden;cursor:ew-resize;">`;
      h += `<div class="pd-fill" style="width:${pct}%;height:100%;background:${pc(pct)};"></div>`;
      h += `</div>`;
      h += `<span class="pd-ed" data-field="progress" data-idx="${idx}" style="font-size:0.82em;font-weight:600;color:var(--text-muted);min-width:32px;text-align:center;cursor:text;outline:none;padding:1px 2px;border-radius:3px;">${pct}%</span>`;
      h += `<button class="pd-plus" data-idx="${idx}" style="width:20px;height:20px;flex:0 0 auto;font-size:0.8em;font-weight:700;cursor:pointer;display:inline-flex;align-items:center;justify-content:center;padding:0;">+</button>`;
      h += `</div></div>`;

      // Notes
      h += `<span class="pd-ed" data-field="notes" data-idx="${idx}" style="flex:2;min-width:80px;text-align:center;cursor:text;outline:none;padding:2px 4px;border-radius:3px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;font-size:0.9em;" title="双击编辑">${noteLink(p.notes)}</span>`;

      // Edit row button
      h += `<button class="pd-edit" data-idx="${idx}" style="width:24px;flex:0 0 auto;height:24px;" title="编辑整行">✎</button>`;

      // Delete
      h += `<button class="pd-del" data-idx="${idx}" style="width:28px;flex:0 0 auto;height:24px;cursor:pointer;font-size:0.95em;padding:0;" title="删除">🗑</button>`;

      h += `</div>`;
    }
  }

  // ── Add button ──
  h += `<div style="margin-top:14px;">
    <button class="pd-add-btn" style="padding:8px 22px;font-size:0.92em;font-weight:600;cursor:pointer;">＋ 添加项目</button>
    <div class="pd-add-form" style="display:none;margin-top:12px;padding:16px;background:var(--background-primary-alt);border:1px solid var(--background-modifier-border);border-radius:10px;max-width:440px;">
      <div style="font-weight:600;margin-bottom:10px;color:var(--text-normal);">添加新项目</div>
      <input class="pd-add-name" placeholder="项目名称" style="display:block;width:100%;padding:7px 10px;margin-bottom:8px;border-radius:6px;border:1px solid #d1d5db;font-size:0.9em;outline:none;color:var(--text-normal);background:var(--background-primary);">
      <input class="pd-add-type" placeholder="项目类型（如：课程学习）" style="display:block;width:100%;padding:7px 10px;margin-bottom:8px;border-radius:6px;border:1px solid #d1d5db;font-size:0.9em;outline:none;color:var(--text-normal);background:var(--background-primary);">
      <input class="pd-add-notes" placeholder="关联笔记（可选，输入笔记文件名）" style="display:block;width:100%;padding:7px 10px;margin-bottom:12px;border-radius:6px;border:1px solid #d1d5db;font-size:0.9em;outline:none;color:var(--text-normal);background:var(--background-primary);">
      <div style="display:flex;gap:8px;justify-content:flex-end;">
        <button class="pd-add-cancel" style="padding:5px 16px;border:1px solid #d1d5db;border-radius:6px;background:transparent;cursor:pointer;font-size:0.85em;color:var(--text-muted);">取消</button>
        <button class="pd-add-ok" style="padding:5px 20px;border:none;border-radius:6px;background:var(--interactive-accent);color:#fff;cursor:pointer;font-weight:600;font-size:0.85em;">添加</button>
      </div>
    </div>
  </div>`;

  wrap.innerHTML = h;

  // ============ BIND EVENTS ============

  // Filter cards
  wrap.querySelectorAll(".pd-filter-card").forEach(card => {
    card.addEventListener("click", () => {
      filter = card.dataset.filter;
      render();
    });
  });

  // +/- buttons
  wrap.querySelectorAll(".pd-minus").forEach(btn => {
    btn.addEventListener("click", async () => {
      const p = projects.find(p => p._idx === Number(btn.dataset.idx));
      if (p) { p.progress = clamp((Number(p.progress) || 0) - 5, 0, 100); autoStatus(p); await save(); render(); }
    });
  });
  wrap.querySelectorAll(".pd-plus").forEach(btn => {
    btn.addEventListener("click", async () => {
      const p = projects.find(p => p._idx === Number(btn.dataset.idx));
      if (p) { p.progress = clamp((Number(p.progress) || 0) + 5, 0, 100); autoStatus(p); await save(); render(); }
    });
  });

  // Status toggle
  wrap.querySelectorAll(".pd-st").forEach(el => {
    el.addEventListener("click", async () => {
      const p = projects.find(p => p._idx === Number(el.dataset.idx));
      if (p) { p.status = STATUS[(STATUS.indexOf(p.status) + 1) % STATUS.length]; await save(); render(); }
    });
  });

  // Edit row toggle
  wrap.querySelectorAll(".pd-edit").forEach(btn => {
    btn.addEventListener("click", async () => {
      const row = btn.closest(".pd-row");
      if (!row) return;
      const idx = Number(btn.dataset.idx);
      const p = projects.find(p => p._idx === idx);
      if (!p) return;
      const fields = row.querySelectorAll(".pd-ed");
      const isEditing = btn.classList.contains("active");

      if (isEditing) {
        // Save all fields at once
        let changed = false;
        fields.forEach(el => {
          el.contentEditable = "false";
          el.style.outline = "";
          const field = el.dataset.field;
          const newVal = el.textContent.trim();
          const oldVal = el.dataset.old || "";
          if (newVal === oldVal) { el.textContent = oldVal; return; }
          changed = true;
          if (field === "progress") {
            const n = clamp(parseInt(newVal, 10), 0, 100);
            if (!isNaN(n)) p.progress = n;
          } else if (field === "notes") {
            const m = newVal.match(/^\[\[([^\]]+)\]\]$/);
            p.notes = m ? m[1] : newVal;
          } else {
            p[field] = newVal;
          }
        });
        btn.classList.remove("active");
        btn.textContent = "✎";
        if (changed) { autoStatus(p); await save(); render(); }
      } else {
        // Enter edit mode on all fields
        fields.forEach(el => {
          el.contentEditable = "true";
          el.dataset.old = el.textContent.trim();
          el.style.outline = "1px solid var(--interactive-accent)";
          el.style.borderRadius = "3px";
        });
        btn.classList.add("active");
        btn.textContent = "✓";
        if (fields.length > 0) fields[0].focus();
      }
    });
  });

  // Delete
  wrap.querySelectorAll(".pd-del").forEach(btn => {
    let timer = null;
    btn.addEventListener("click", async () => {
      const p = projects.find(p => p._idx === Number(btn.dataset.idx));
      if (!p) return;
      if (btn.dataset.confirm !== "1") {
        btn.textContent = "?";
        btn.style.color = "#ef4444";
        btn.style.fontWeight = "700";
        btn.dataset.confirm = "1";
        if (timer) clearTimeout(timer);
        timer = setTimeout(() => { btn.textContent = "🗑"; btn.style.color = ""; btn.style.fontWeight = ""; btn.dataset.confirm = ""; }, 3000);
        return;
      }
      if (timer) clearTimeout(timer);
      projects = projects.filter(p => p._idx !== Number(btn.dataset.idx));
      await save(); render();
    });
  });

  // Progress field: single-click to edit directly
  wrap.querySelectorAll('.pd-ed[data-field="progress"]').forEach(el => {
    el.addEventListener("click", () => {
      if (el.contentEditable === "true") return; // already editing
      el.contentEditable = "true";
      el.dataset.old = el.textContent.trim();
      el.focus();
      // Select just the number (strip the % sign)
      const txt = el.textContent.trim();
      const m = txt.match(/^\d+/);
      if (m) {
        const range = document.createRange();
        range.setStart(el.firstChild, 0);
        range.setEnd(el.firstChild, m[0].length);
        const sel = window.getSelection();
        sel.removeAllRanges();
        sel.addRange(range);
      }
      el.style.outline = "1px solid var(--interactive-accent)";
      el.style.borderRadius = "3px";
    });
  });

  // ContentEditable (double-click to edit)
  wrap.querySelectorAll(".pd-ed").forEach(el => {
    const idx = Number(el.dataset.idx);
    const field = el.dataset.field;

    el.addEventListener("dblclick", () => {
      el.contentEditable = "true";
      el.dataset.old = el.textContent.trim();
      el.focus();
      el.style.outline = "1px solid var(--interactive-accent)";
      el.style.borderRadius = "3px";
    });
    el.addEventListener("keydown", e => {
      if (e.key === "Enter") { e.preventDefault(); el.blur(); }
      if (e.key === "Escape") { el.textContent = el.dataset.old || ""; el.blur(); }
    });
    el.addEventListener("blur", async () => {
      el.contentEditable = "false";
      el.style.outline = "";
      const newVal = el.textContent.trim();
      const oldVal = el.dataset.old || "";
      el.dataset.old = "";
      if (newVal === oldVal) { el.textContent = oldVal; return; }
      const p = projects.find(p => p._idx === idx);
      if (!p) return;
      if (field === "progress") {
        const n = clamp(parseInt(newVal, 10), 0, 100);
        if (!isNaN(n)) { p.progress = n; autoStatus(p); } else { el.textContent = oldVal; return; }
      } else if (field === "notes") {
        const m = newVal.match(/^\[\[([^\]]+)\]\]$/);
        p.notes = m ? m[1] : newVal;
      } else {
        p[field] = newVal;
      }
      await save(); render();
    });
  });

  // Add project
  const addBtn = wrap.querySelector(".pd-add-btn");
  const addForm = wrap.querySelector(".pd-add-form");
  if (addBtn && addForm) {
    addBtn.addEventListener("click", () => { addForm.style.display = "block"; addBtn.style.display = "none"; addForm.querySelector(".pd-add-name").focus(); });
    addForm.querySelector(".pd-add-cancel").addEventListener("click", () => { addForm.style.display = "none"; addBtn.style.display = ""; });
    addForm.querySelector(".pd-add-ok").addEventListener("click", async () => {
      const name = addForm.querySelector(".pd-add-name").value.trim();
      if (!name) return;
      const type = addForm.querySelector(".pd-add-type").value.trim() || "未分类";
      const notes = addForm.querySelector(".pd-add-notes").value.trim();
      const max = projects.reduce((m, p) => Math.max(m, p._idx), -1);
      projects.push({ _idx: max + 1, name, type, progress: 0, status: "plan", notes });
      addForm.querySelector(".pd-add-name").value = "";
      addForm.querySelector(".pd-add-type").value = "";
      addForm.querySelector(".pd-add-notes").value = "";
      addForm.style.display = "none"; addBtn.style.display = "";
      await save(); render();
    });
  }

  // Progress bar click
  wrap.querySelectorAll(".pd-bar").forEach(bar => {
    bar.addEventListener("click", async (e) => {
      const p = projects.find(p => p._idx === Number(bar.dataset.idx));
      if (!p) return;
      const r = bar.getBoundingClientRect();
      p.progress = clamp(Math.round((e.clientX - r.left) / r.width * 100), 0, 100);
      autoStatus(p); await save(); render();
    });
  });

  // ── Drag-to-reorder ──
  wrap.querySelectorAll(".pd-grip").forEach(grip => {
    grip.addEventListener("mousedown", (e) => {
      const row = grip.closest(".pd-row");
      if (!row) return;
      // Find the current wrap (may be stale after re-render, but this handler only lives for one render cycle)
      const currentWrap = wrap;

      row.style.opacity = "0.4";
      row.style.background = "var(--background-modifier-hover)";
      let dragEl = row;

      function onMove(ev) {
        const rows = [...currentWrap.querySelectorAll(".pd-row")];
        rows.forEach(r => r.style.borderTop = "");
        for (const r of rows) {
          if (r === dragEl) continue;
          const rect = r.getBoundingClientRect();
          if (ev.clientY > rect.top && ev.clientY < rect.bottom) {
            r.style.borderTop = "2px solid #4b63fb";
            break;
          }
        }
      }

      async function onUp(ev) {
        document.removeEventListener("mousemove", onMove);
        document.removeEventListener("mouseup", onUp);
        const rows = [...currentWrap.querySelectorAll(".pd-row")];
        const fromIdx = rows.indexOf(dragEl);

        let toIdx = fromIdx;
        for (let i = 0; i < rows.length; i++) {
          if (rows[i].style.borderTop) { toIdx = i; break; }
        }

        rows.forEach(r => { r.style.opacity = ""; r.style.background = ""; r.style.borderTop = ""; });

        if (toIdx !== fromIdx && toIdx >= 0 && toIdx < rows.length) {
          const [moved] = projects.splice(fromIdx, 1);
          const target = toIdx > fromIdx ? toIdx - 1 : toIdx;
          projects.splice(target, 0, moved);
          projects.forEach((p, i) => { p._idx = i; });
          await save(); render();
        }
        dragEl = null;
      }

      document.addEventListener("mousemove", onMove);
      document.addEventListener("mouseup", onUp);
      e.preventDefault();
    });
  });
}

render();
```
