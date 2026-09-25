# -*- coding: utf-8 -*-
"""详情页 ×6：按钮「开始使用」→「立即体验」；注入与更新日志一致的加载遮罩（Y + 名字 + 8 秒进度条）
点击「立即体验」→ 进度条（可长按加速）→ 跳转作品文件
"""
import re, glob

CSS_BLOCK = """
  /* 加载遮罩（与更新日志一致：Y 一笔画 + 名字 + 8 秒进度条） */
  .page-loader {
    position: fixed; inset: 0; z-index: 9999; background: var(--bg);
    display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 18px;
    opacity: 0; visibility: hidden; transition: opacity 0.3s ease, visibility 0.3s ease;
  }
  .page-loader.show { opacity: 1; visibility: visible; }
  .page-loader .loader-svg { width: 84px; height: 84px; color: var(--accent); }
  .page-loader .loader-path { stroke-dasharray: 100; stroke-dashoffset: 100; animation: loaderDraw 1.1s ease forwards; }
  @keyframes loaderDraw { to { stroke-dashoffset: 0; } }
  .page-loader .loader-name {
    font-family: "Noto Serif SC", Georgia, serif; font-size: 20px; font-weight: 700;
    letter-spacing: 0.24em; color: var(--ink);
    opacity: 0; transform: translateY(6px); animation: loaderName 0.6s ease 0.55s forwards;
  }
  @keyframes loaderName { to { opacity: 1; transform: translateY(0); } }
  .page-loader .loading-bar { width: 300px; height: 4px; background: var(--line); border-radius: 999px; overflow: hidden; margin-top: 14px; }
  .page-loader .loading-bar-fill { height: 100%; width: 0%; background: linear-gradient(90deg, var(--accent), var(--accent-2)); border-radius: 999px; transition: width 0.2s ease; }
  .page-loader .loading-percent { font-size: 13px; color: var(--ink-2); font-variant-numeric: tabular-nums; }
  .page-loader .loading-hint { margin-top: 16px; font-size: 13px; color: var(--ink-2); opacity: 0.65; user-select: none; -webkit-user-select: none; }
  .page-loader .load-skip {
    margin-top: 20px; display: inline-flex; align-items: center; gap: 7px;
    font-size: 12.5px; color: var(--accent);
    border: 1px solid rgba(2,132,199,0.35); background: rgba(2,132,199,0.06);
    border-radius: 999px; padding: 9px 20px; cursor: pointer;
    opacity: 0; transition: opacity 0.35s ease;
    font-family: inherit; user-select: none; -webkit-user-select: none;
  }
  .page-loader .load-skip.show { opacity: 1; }
  .page-loader .load-skip svg { width: 14px; height: 14px; }
  .page-loader .load-skip:active { background: rgba(2,132,199,0.16); }
  .page-loader .load-skip small { font-size: 11px; opacity: 0.75; }
"""

JS_BLOCK = """
<script>
(function () {
  var overlay = document.getElementById('pageLoader');
  var bar = document.getElementById('loadBar');
  var pct = document.getElementById('loadPercent');
  var skip = document.getElementById('loadSkip');
  var hint = document.getElementById('loadHint');
  var btn = document.querySelector('.btn-primary');
  if (!overlay || !bar || !btn) return;
  var target = btn.getAttribute('href');
  var timer = null, skipTimer = null, endTimer = null, boostTimer = null;
  var boostStart = 0, progress = 0, finished = false;
  function replay() {
    var p = overlay.querySelector('.loader-path');
    if (p) { var c = p.cloneNode(true); p.parentNode.replaceChild(c, p); }
    var n = overlay.querySelector('.loader-name');
    if (n) { var c2 = n.cloneNode(true); n.parentNode.replaceChild(c2, n); }
  }
  function stopAll() {
    if (timer) { clearInterval(timer); timer = null; }
    if (skipTimer) { clearTimeout(skipTimer); skipTimer = null; }
    if (endTimer) { clearTimeout(endTimer); endTimer = null; }
    if (boostTimer) { clearInterval(boostTimer); boostTimer = null; }
  }
  function finish() {
    if (finished) return;
    finished = true;
    stopAll();
    bar.style.width = '100%';
    pct.textContent = '100%';
    setTimeout(function () { window.location.href = target; }, 250);
  }
  function start() {
    finished = false; progress = 0;
    stopAll();
    overlay.classList.add('show');
    replay();
    bar.style.width = '0%';
    pct.textContent = '0%';
    if (skip) skip.classList.remove('show');
    var LINES = ['正在泡咖啡…', '正在数星星…', '正在打开作品…', '正在点亮灯笼…', '正在问候全世界…', '正在检查进度条…'];
    if (hint) hint.textContent = LINES[Math.floor(Math.random() * LINES.length)];
    timer = setInterval(function () {
      progress += Math.random() * 2.2;
      if (progress > 95) progress = 95;
      bar.style.width = progress + '%';
      pct.textContent = Math.floor(progress) + '%';
    }, 100);
    skipTimer = setTimeout(function () { if (skip) skip.classList.add('show'); }, 3000);
    endTimer = setTimeout(finish, 8000);
  }
  function startBoost() {
    if (boostTimer) return;
    boostStart = Date.now();
    boostTimer = setInterval(function () {
      var hold = (Date.now() - boostStart) / 1000;
      var inc = 2 + hold * 4;
      progress += inc;
      if (progress >= 95) { progress = 95; bar.style.width = '95%'; pct.textContent = '95%'; finish(); return; }
      bar.style.width = progress + '%';
      pct.textContent = Math.floor(progress) + '%';
    }, 70);
  }
  function stopBoost() { if (boostTimer) { clearInterval(boostTimer); boostTimer = null; } }
  [skip, hint].forEach(function (el) {
    if (!el) return;
    el.addEventListener('mousedown', startBoost);
    el.addEventListener('touchstart', startBoost, { passive: true });
    ['mouseup', 'mouseleave', 'touchend', 'touchcancel'].forEach(function (ev) {
      el.addEventListener(ev, stopBoost);
    });
  });
  btn.addEventListener('click', function (e) { e.preventDefault(); start(); });
})();
</script>
"""

def get_work_name(path):
    s = open(path, encoding="utf-8").read()
    m = re.search(r"<h1>(.*?)</h1>", s)
    return m.group(1).strip() if m else "Yaule"

def get_try_href(path):
    s = open(path, encoding="utf-8").read()
    m = re.search(r'class="btn btn-primary" href="([^"]+)"', s)
    return m.group(1) if m else "index.html"

for f in sorted(glob.glob("works/*.html")):
    html = open(f, encoding="utf-8").read()
    name = get_work_name(f)
    log = []
    # 1. 按钮改名
    if "开始使用" in html:
        html = html.replace("开始使用", "立即体验", 1)
        log.append("按钮→立即体验")
    # 2. 注入 CSS
    if ".page-loader" not in html:
        html = html.replace("</style>", CSS_BLOCK + "\n</style>", 1)
        log.append("CSS 遮罩")
    # 3. 注入 HTML（body 后）
    if 'id="pageLoader"' not in html:
        loader_html = (
            '<!-- 加载遮罩（点击「立即体验」后显示，与更新日志一致） -->\n'
            '<div class="page-loader" id="pageLoader">\n'
            '  <svg class="loader-svg" viewBox="0 0 120 120" fill="none" stroke="currentColor" stroke-width="7" stroke-linecap="round" stroke-linejoin="round">\n'
            '    <path class="loader-path" pathLength="100" d="M22 18 L60 54 L98 18 M60 54 L60 102"/>\n'
            '  </svg>\n'
            '  <p class="loader-name">%s</p>\n'
            '  <div class="loading-bar"><div class="loading-bar-fill" id="loadBar"></div></div>\n'
            '  <p class="loading-percent" id="loadPercent">0%%</p>\n'
            '  <p class="loading-hint" id="loadHint">正在打开作品…</p>\n'
            '  <button class="load-skip" id="loadSkip" type="button">\n'
            '    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>\n'
            '    长按加速 <small>按住不放，加载更快</small>\n'
            '  </button>\n'
            '</div>\n'
        ) % name
        html = html.replace("<body>", "<body>\n" + loader_html, 1)
        log.append("HTML 遮罩")
    # 4. 注入 JS（</body> 前）
    if "btn-primary" in html and "pageLoader" in JS_BLOCK:
        if "document.querySelector('.btn-primary')" not in html:
            html = html.replace("</body>", JS_BLOCK + "\n</body>", 1)
            log.append("JS 进度条")
    open(f, "w", encoding="utf-8").write(html)
    print("OK  ", f, "->", " / ".join(log), "| 作品:", name, "| href:", get_try_href(f))
print("DONE")
