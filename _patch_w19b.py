# -*- coding: utf-8 -*-
"""v19 changelog.html：①title/description 加长 ②加载标语轮换(新增 loading-hint) ③22:00-06:00 自动深色(手动优先)"""
path = "changelog.html"
html = open(path, encoding="utf-8").read()
log = []

def rep(old, new, tag):
    global html
    if old not in html:
        log.append("FAIL " + tag)
        return
    html = html.replace(old, new, 1)
    log.append("OK   " + tag)

# 1. title / description
rep("<title>详细日志 · Yaule 失眠夜空间</title>",
    "<title>更新日志 · Yaule 失眠夜空间 | 完整版本记录与详细时间戳</title>",
    "title 加长")
rep('<meta name="description" content="Yaule 失眠夜空间的完整更新日志，包含全部版本记录与时间戳。">',
    '<meta name="description" content="Yaule 失眠夜空间的完整更新日志：收录 v1 到当前版本的全部改动记录，每条均带完整时间戳与新增 / 信息 / 修复标签，与主页实时同步。">',
    "description 加长")

# 2. loading-hint CSS（放在 loading-percent 样式后）
rep("""  .loading-percent { font-size: 13px; color: var(--ink-2); font-variant-numeric: tabular-nums; }""",
"""  .loading-percent { font-size: 13px; color: var(--ink-2); font-variant-numeric: tabular-nums; }
  .loading-hint {
    margin-top: 16px;
    font-size: 13px;
    color: var(--ink-2);
    opacity: 0.65;
    user-select: none;
    -webkit-user-select: none;
  }""",
"CSS loading-hint")

# 3. loading-hint 元素（进度百分比之后、按钮之前）
rep("""  <p class="loading-percent" id="loadPercent">0%</p>
  <button class="load-skip" id="loadSkip" type="button">""",
"""  <p class="loading-percent" id="loadPercent">0%</p>
  <p class="loading-hint" id="loadHint">正在读取日志…</p>
  <button class="load-skip" id="loadSkip" type="button">""",
"HTML loading-hint 元素")

# 4. 加载标语轮换（在加载 IIFE 顶部设置）
rep("""  var skipTimer = setTimeout(function () { if (skip) skip.classList.add('show'); }, 3000);""",
"""  var hint = document.getElementById('loadHint');
  if (hint) {
    var LOAD_LINES = ['正在泡咖啡…', '正在数星星…', '正在整理日志…', '正在点亮灯笼…', '正在问候全世界…', '正在翻今天的日记…'];
    hint.textContent = LOAD_LINES[Math.floor(Math.random() * LOAD_LINES.length)];
  }
  var skipTimer = setTimeout(function () { if (skip) skip.classList.add('show'); }, 3000);""",
"标语轮换 JS")

# 5. 主题自动深色
rep("""  var toggle = document.getElementById('themeToggle');
  var root = document.documentElement;
  try {
    if (localStorage.getItem('yaule-theme') === 'dark') root.setAttribute('data-theme', 'dark');
  } catch (e) {}""",
"""  var toggle = document.getElementById('themeToggle');
  var root = document.documentElement;
  function applyTheme() {
    var saved = null;
    try { saved = localStorage.getItem('yaule-theme'); } catch (e) {}
    if (saved === 'dark') { root.setAttribute('data-theme', 'dark'); return; }
    if (saved === 'light') { root.removeAttribute('data-theme'); return; }
    var h = new Date().getHours();
    if (h >= 22 || h < 6) root.setAttribute('data-theme', 'dark');
    else root.removeAttribute('data-theme');
  }
  applyTheme();
  setInterval(applyTheme, 1800000);""",
"主题自动深色")

open(path, "w", encoding="utf-8").write(html)
for l in log:
    print(l)
print("DONE")
