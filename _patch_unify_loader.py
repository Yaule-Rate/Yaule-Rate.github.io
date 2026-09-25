# -*- coding: utf-8 -*-
"""统一加载遮罩为「进入日志」样式：Y 一笔画 + Yaule 名字 + 8 秒进度条一体。
- 移除独立 pageLoader，开屏与跳转共用 loadingOverlay（changelog 同款）
- CSS：实底 --bg、Y/名字动画、进度条 300px/0.2s
- JS：startLoading 每次激活重播 Y 动画；playSplash 统一为 startLoading('') 无跳转
"""
path = "index.html"
html = open(path, encoding="utf-8").read()
log = []

def rep(old, new, tag):
    global html
    if old not in html:
        log.append("FAIL " + tag)
        return
    html = html.replace(old, new, 1)
    log.append("OK   " + tag)

# ========== A. CSS：loadingOverlay 改为 changelog 同款 ==========
rep("""  /* ===== 伪进度条加载遮罩 ===== */
  .loading-overlay {
    position: fixed;
    inset: 0;
    background: var(--overlay);
    backdrop-filter: blur(12px);
    z-index: 9999;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.3s ease;
  }
  .loading-overlay.active {
    opacity: 1;
    pointer-events: all;
  }
  .loading-overlay .load-title {
    font-family: "Noto Serif SC", Georgia, serif;
    font-size: 24px;
    font-weight: 600;
    color: var(--ink);
    margin-bottom: 32px;
  }
  .loading-bar {
    width: 320px;
    height: 4px;
    background: var(--line);
    border-radius: 999px;
    overflow: hidden;
    position: relative;
  }
  .loading-bar-fill {
    position: absolute;
    left: 0;
    top: 0;
    height: 100%;
    width: 0%;
    background: linear-gradient(90deg, var(--accent), #38bdf8);
    border-radius: 999px;
    transition: width 0.3s ease;
  }
  .loading-percent {
    margin-top: 16px;
    font-size: 14px;
    color: var(--ink-2);
    font-variant-numeric: tabular-nums;
  }
  .loading-hint {
    margin-top: 24px;
    font-size: 13px;
    color: var(--ink-2);
    opacity: 0.6;
    cursor: pointer;
    user-select: none;
    -webkit-user-select: none;
    transition: color 0.2s;
  }
  .loading-hint:active { color: var(--accent); }""",
"""  /* ===== 加载遮罩（统一为「进入日志」样式：Y 一笔画 + 名字 + 8 秒进度条） ===== */
  .loading-overlay {
    position: fixed;
    inset: 0;
    background: var(--bg);
    z-index: 9999;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 18px;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.3s ease;
  }
  .loading-overlay.active {
    opacity: 1;
    pointer-events: all;
  }
  .loading-overlay .loader-svg { width: 84px; height: 84px; color: var(--accent); }
  .loading-overlay .loader-path {
    stroke-dasharray: 100;
    stroke-dashoffset: 100;
    animation: loaderDraw 1.1s ease forwards;
  }
  .loading-overlay .loader-name {
    font-family: "Noto Serif SC", Georgia, serif;
    font-size: 20px;
    font-weight: 700;
    letter-spacing: 0.24em;
    color: var(--ink);
    opacity: 0;
    transform: translateY(6px);
    animation: loaderName 0.6s ease 0.55s forwards;
  }
  @keyframes loaderDraw { to { stroke-dashoffset: 0; } }
  @keyframes loaderName { to { opacity: 1; transform: translateY(0); } }
  .loading-bar {
    width: 300px;
    height: 4px;
    background: var(--line);
    border-radius: 999px;
    overflow: hidden;
    position: relative;
    margin-top: 14px;
  }
  .loading-bar-fill {
    position: absolute;
    left: 0;
    top: 0;
    height: 100%;
    width: 0%;
    background: linear-gradient(90deg, var(--accent), var(--accent-2));
    border-radius: 999px;
    transition: width 0.2s ease;
  }
  .loading-percent {
    margin-top: 16px;
    font-size: 14px;
    color: var(--ink-2);
    font-variant-numeric: tabular-nums;
  }
  .loading-hint {
    margin-top: 16px;
    font-size: 13px;
    color: var(--ink-2);
    opacity: 0.65;
    cursor: pointer;
    user-select: none;
    -webkit-user-select: none;
    transition: color 0.2s;
  }
  .loading-hint:active { color: var(--accent); }""",
"CSS overlay 改日志样式")

# ========== B. CSS：移除独立 pageLoader 块 ==========
rep("""  /* ===== 页面加载动画：青色 Y 一笔画 ===== */
  .page-loader {
    position: fixed;
    inset: 0;
    z-index: 9999;
    background: var(--bg);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 18px;
    transition: opacity 0.5s ease, visibility 0.5s ease;
  }
  .page-loader.done { opacity: 0; visibility: hidden; }
  .loader-svg { width: 84px; height: 84px; color: var(--accent); }
  .loader-path {
    stroke-dasharray: 100;
    stroke-dashoffset: 100;
    animation: loaderDraw 1.1s ease forwards;
  }
  @keyframes loaderDraw { to { stroke-dashoffset: 0; } }
  .loader-name {
    font-family: "Noto Serif SC", Georgia, serif;
    font-size: 20px;
    font-weight: 700;
    letter-spacing: 0.24em;
    color: var(--ink);
    opacity: 0;
    transform: translateY(6px);
    animation: loaderName 0.6s ease 0.55s forwards;
  }
  @keyframes loaderName { to { opacity: 1; transform: translateY(0); } }""",
"""  /* ===== （旧独立开屏动画已合并进 loadingOverlay，见上方加载遮罩样式） ===== */""",
"移除 pageLoader CSS")

# ========== C. CSS：reduced-motion 里删 page-loader ==========
rep("""  @media (prefers-reduced-motion: reduce) {
    .page-loader { display: none; }
  }""",
"""  @media (prefers-reduced-motion: reduce) {
    .loading-overlay { transition: opacity 0.15s ease; }
  }""",
"reduced-motion 调整")

# ========== D. HTML：移除独立 pageLoader ==========
rep("""<!-- 页面加载动画：青色 Y 一笔画 -->
<div class="page-loader" id="pageLoader">
  <svg class="loader-svg" viewBox="0 0 120 120" fill="none" stroke="currentColor" stroke-width="7" stroke-linecap="round" stroke-linejoin="round">
    <path class="loader-path" pathLength="100" d="M22 18 L60 54 L98 18 M60 54 L60 102"/>
  </svg>
  <p class="loader-name">Yaule</p>
</div>
<!-- 伪进度条加载遮罩 -->
<div class="loading-overlay" id="loadingOverlay">
  <p class="load-title" id="loadTitle">正在进入</p>
  <div class="loading-bar">
    <div class="loading-bar-fill" id="loadBar"></div>
  </div>""",
"""<!-- 加载遮罩（统一为「进入日志」样式：Y 一笔画 + 名字 + 8 秒进度条） -->
<div class="loading-overlay" id="loadingOverlay">
  <svg class="loader-svg" viewBox="0 0 120 120" fill="none" stroke="currentColor" stroke-width="7" stroke-linecap="round" stroke-linejoin="round">
    <path class="loader-path" pathLength="100" d="M22 18 L60 54 L98 18 M60 54 L60 102"/>
  </svg>
  <p class="loader-name">Yaule</p>
  <div class="loading-bar">
    <div class="loading-bar-fill" id="loadBar"></div>
  </div>""",
"HTML overlay 改为日志样式并移除 pageLoader")

# ========== E. JS：移除 loadTitle 引用 ==========
rep("""  var loadTitle = document.getElementById('loadTitle');
  var loadSkip = document.getElementById('loadSkip');""",
"""  var loadSkip = document.getElementById('loadSkip');""",
"移除 loadTitle 变量")

# ========== F. JS：startLoading 重播 Y 动画 ==========
rep("""  function startLoading(targetUrl, title, openInNew) {
    loadTitle.textContent = title || '正在进入';
    overlay.classList.add('active');""",
"""  function startLoading(targetUrl, title, openInNew) {
    // 每次激活遮罩都重播 Y 一笔画与名字动画（与进入日志一致）
    var lp = overlay.querySelector('.loader-path');
    if (lp) { var lc = lp.cloneNode(true); lp.parentNode.replaceChild(lc, lp); }
    var ln = overlay.querySelector('.loader-name');
    if (ln) { var lc2 = ln.cloneNode(true); ln.parentNode.replaceChild(lc2, ln); }
    overlay.classList.add('active');""",
"startLoading 重播 Y")

# ========== G. JS：playSplash 统一 ==========
rep("""  /* ========== 开屏动画：青色 Y 一笔画（每次进入本站均播放，含作品页返回 / 浏览器后退） ========== */
  var splashTimer = null;
  function playSplash(restart) {
    if (splashTimer) { clearTimeout(splashTimer); splashTimer = null; }
    var loader = document.getElementById('pageLoader');
    if (!loader) {
      // bfcache 返回时原 loader 已从 DOM 移除：重建并播放
      loader = document.createElement('div');
      loader.className = 'page-loader';
      loader.id = 'pageLoader';
      loader.innerHTML = '<svg class="loader-svg" viewBox="0 0 120 120" fill="none" stroke="currentColor" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"><path class="loader-path" pathLength="100" d="M22 18 L60 54 L98 18 M60 54 L60 102"/></svg><p class="loader-name">Yaule</p>';
      document.body.insertBefore(loader, document.body.firstChild);
    } else if (restart) {
      // 重播：克隆路径与名字节点以重新触发 CSS 动画
      var path = loader.querySelector('.loader-path');
      if (path) { var c1 = path.cloneNode(true); path.parentNode.replaceChild(c1, path); }
      var name = loader.querySelector('.loader-name');
      if (name) { var c2 = name.cloneNode(true); name.parentNode.replaceChild(c2, name); }
      loader.classList.remove('done');
    }
    splashTimer = setTimeout(function () {
      loader.classList.add('done');
    }, 1700);
  }
  playSplash(false);""",
"""  /* ========== 每次进入本站自动播放开屏（Y 一笔画 + 8 秒进度条，与进入日志一致；含返回 / 浏览器后退） ========== */
  function playSplash() {
    window.scrollTo(0, 0);
    startLoading('', '', false);
  }
  playSplash();""",
"playSplash 统一")

# ========== H. JS：pageshow 调用无参 ==========
rep("""  window.addEventListener('pageshow', function (e) {
    if (e.persisted) { playSplash(true); return; }
    if (overlay.classList.contains('active')) hideLoading();
  });""",
"""  window.addEventListener('pageshow', function (e) {
    if (e.persisted) { playSplash(); return; }
    if (overlay.classList.contains('active')) hideLoading();
  });""",
"pageshow 无参调用")

open(path, "w", encoding="utf-8").write(html)
for l in log:
    print(l)
print("DONE")
