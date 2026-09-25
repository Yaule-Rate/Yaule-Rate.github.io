# -*- coding: utf-8 -*-
"""changelog.html 改版：VSCode 风格渲染 + 全量数据与主页同步（从 index.html 提取 YAULE_CHANGELOG）"""
import re

idx = open("index.html", encoding="utf-8").read()
chg = open("changelog.html", encoding="utf-8").read()
log = []

m = re.search(r"var YAULE_CHANGELOG = \[.*?\];", idx, re.S)
if not m:
    print("FAIL 提取 YAULE_CHANGELOG")
    raise SystemExit
data = m.group(0)

# 1. FALLBACK_LOGS 替换为全量数据
old = re.search(r"var FALLBACK_LOGS = \[.*?\];", chg, re.S)
if old:
    chg = chg.replace(old.group(0), data.replace("YAULE_CHANGELOG", "FALLBACK_LOGS"), 1)
    log.append("OK   FALLBACK_LOGS 同步全量数据")

# 2. 渲染函数 -> VSCode 风格（渲染全部版本）
m2 = re.search(r"var lvClass = \{.*?\nrender\(\);", chg, re.S)
if not m2:
    print("FAIL 渲染函数匹配失败")
    raise SystemExit
new_render = """var lvClass = { "[ADD]": "cat-add", "[INFO]": "cat-info", "[FIX]": "cat-fix", "[DEL]": "cat-del", "[WARN]": "cat-warn" };
function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
function rowHtml(item) {
  var cls = lvClass[item.lv] || 'cat-info';
  return '<div class="vs-row ' + cls + '"><span class="vs-dot"></span><span class="vs-time">' + esc(item.time || '') + '</span><span class="vs-tag">' + esc(item.lv || '') + '</span><span class="vs-text">' + esc(item.text || '') + '</span></div>';
}
function verHtml(v) {
  var rows = (v.list || []).map(rowHtml).join('');
  return '<div class="vs-ver' + (v.current ? ' current' : '') + '"><div class="vs-ver-head"><span class="vs-ver-tab">' + esc(v.ver) + '</span><span class="vs-ver-date">' + esc(v.date) + '</span>' + (v.current ? '<span class="vs-ver-badge">当前版本</span>' : '') + '</div><div class="vs-rows">' + rows + '</div></div>';
}
function render() {
  var box = document.getElementById('mcLog');
  if (!box) return;
  box.innerHTML = logs.map(verHtml).join('');
  var note = document.getElementById('syncNote');
  note.textContent = synced
    ? '已读取主页同步的最新日志（' + logs.length + ' 个版本）。每次打开主页都会自动更新本页。'
    : '尚未在本机打开过主页，当前展示内置日志。打开主页后会自动同步为最新记录。';
}
render();"""
chg = chg.replace(m2.group(0), new_render, 1)
log.append("OK   渲染函数 VSCode 风格")

# 3. 容器 class
chg = chg.replace('<div class="mc-log" id="mcLog"></div>', '<div class="vs-log" id="mcLog"></div>', 1)
log.append("OK   vs-log 容器")

# 4. CSS：MC -> VSCode（47-92 行区域）
mcss = re.search(r"  \.mc-log \{ display: flex; flex-direction: column; gap: 14px; \}.*?\.mc-ver-list li\.cat-fix::before \{ background: #f97316; \}", chg, re.S)
if mcss:
    new_css = """  .vs-log { display: flex; flex-direction: column; gap: 16px; }
  .vs-ver {
    background: #0d1117;
    border: 1px solid #30363d;
    border-radius: 10px;
    overflow: hidden;
    font-family: ui-monospace, "Cascadia Code", Consolas, "SF Mono", monospace;
  }
  .vs-ver-head {
    display: flex; align-items: center; gap: 12px;
    padding: 10px 16px;
    background: #161b22;
    border-bottom: 1px solid #30363d;
    flex-wrap: wrap;
  }
  .vs-ver-tab {
    display: inline-flex; align-items: center; gap: 8px;
    font-size: 12.5px; font-weight: 700; color: #e6edf3;
    letter-spacing: 0.04em;
  }
  .vs-ver-tab::before {
    content: ""; width: 3px; height: 14px; border-radius: 2px;
    background: linear-gradient(180deg, var(--accent), var(--accent-2));
  }
  .vs-ver-date {
    font-size: 11px; color: #8b949e; letter-spacing: 0.02em;
  }
  .vs-ver-badge {
    margin-left: auto; font-size: 10.5px; color: #3fb950;
    border: 1px solid rgba(63,185,80,0.35); background: rgba(63,185,80,0.08);
    border-radius: 999px; padding: 2px 9px; letter-spacing: 0.05em;
  }
  .vs-rows { padding: 8px 0 10px; }
  .vs-row {
    display: flex; align-items: baseline; gap: 10px;
    padding: 4.5px 16px;
    font-size: 12.5px; line-height: 1.6;
  }
  .vs-row:hover { background: rgba(56,139,253,0.06); }
  .vs-dot {
    flex: none; width: 7px; height: 7px; border-radius: 50%;
    transform: translateY(-1px);
    background: #8b949e;
  }
  .vs-time {
    flex: none; font-size: 11px; color: #8b949e; letter-spacing: 0.02em;
  }
  .vs-tag {
    flex: none; font-size: 10.5px; font-weight: 700; letter-spacing: 0.04em;
  }
  .vs-text { color: #c9d1d9; }
  .vs-row.cat-add .vs-dot { background: #3fb950; }
  .vs-row.cat-add .vs-tag { color: #3fb950; }
  .vs-row.cat-info .vs-dot { background: #58a6ff; }
  .vs-row.cat-info .vs-tag { color: #58a6ff; }
  .vs-row.cat-fix .vs-dot { background: #f97316; }
  .vs-row.cat-fix .vs-tag { color: #f97316; }
  .vs-row.cat-del .vs-dot { background: #f85149; }
  .vs-row.cat-del .vs-tag { color: #f85149; }
  .vs-row.cat-warn .vs-dot { background: #e3b341; }
  .vs-row.cat-warn .vs-tag { color: #e3b341; }"""
    chg = chg.replace(mcss.group(0), new_css, 1)
    log.append("OK   CSS VSCode 风格")
else:
    log.append("FAIL CSS 匹配失败")

open("changelog.html", "w", encoding="utf-8").write(chg)
for l in log:
    print(l)
print("DONE")
