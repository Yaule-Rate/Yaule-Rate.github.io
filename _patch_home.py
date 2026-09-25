# -*- coding: utf-8 -*-
"""主页三改：
A. 恢复 v19.3 简笔画开屏（pageLoader：Y 一笔画 + Yaule，1.7s 淡出）——首次进入 / bfcache 返回
B. 作品卡统一：点击一次 -> 详情页（移除 a.card-image 的 data-loading 直开作品；卡片 JS 简化为进详情）
C. loadingOverlay 保留 v19.4（Y+进度条一体）用于 data-loading 跳转（进入个人空间 / 查看更多）
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

# ===== A1. CSS：恢复 pageLoader（简笔画开屏） =====
rep("""  /* ===== （旧独立开屏动画已合并进 loadingOverlay，见上方加载遮罩样式） ===== */""",
"""  /* ===== 开屏简笔画：青色 Y 一笔画 + Yaule（首次进入 / 返回主页时播放，约 1.7 秒） ===== */
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
"恢复 pageLoader CSS")

# ===== A2. HTML：恢复 pageLoader =====
rep("""<!-- 加载遮罩（统一为「进入日志」样式：Y 一笔画 + 名字 + 8 秒进度条） -->
<div class="loading-overlay" id="loadingOverlay">""",
"""<!-- 开屏简笔画：青色 Y 一笔画 + Yaule -->
<div class="page-loader" id="pageLoader">
  <svg class="loader-svg" viewBox="0 0 120 120" fill="none" stroke="currentColor" stroke-width="7" stroke-linecap="round" stroke-linejoin="round">
    <path class="loader-path" pathLength="100" d="M22 18 L60 54 L98 18 M60 54 L60 102"/>
  </svg>
  <p class="loader-name">Yaule</p>
</div>
<!-- 跳转进度条（统一为「进入日志」样式：Y 一笔画 + 名字 + 8 秒进度条） -->
<div class="loading-overlay" id="loadingOverlay">""",
"恢复 pageLoader HTML")

# ===== A3. JS：playSplash 恢复简笔画版 =====
rep("""  /* ========== 每次进入本站自动播放开屏（Y 一笔画 + 8 秒进度条，与进入日志一致；含返回 / 浏览器后退） ========== */
  function playSplash() {
    window.scrollTo(0, 0);
    startLoading('', '', false);
  }
  playSplash();""",
"""  /* ========== 开屏简笔画：每次进入本站（含作品页 / 日志返回、浏览器后退）播放 Y 一笔画 ========== */
  var splashTimer = null;
  function playSplash() {
    if (splashTimer) { clearTimeout(splashTimer); splashTimer = null; }
    window.scrollTo(0, 0);
    var loader = document.getElementById('pageLoader');
    if (!loader) {
      // bfcache 返回时原 loader 已从 DOM 移除：重建并播放
      loader = document.createElement('div');
      loader.className = 'page-loader';
      loader.id = 'pageLoader';
      loader.innerHTML = '<svg class="loader-svg" viewBox="0 0 120 120" fill="none" stroke="currentColor" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"><path class="loader-path" pathLength="100" d="M22 18 L60 54 L98 18 M60 54 L60 102"/></svg><p class="loader-name">Yaule</p>';
      document.body.insertBefore(loader, document.body.firstChild);
    } else {
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
  playSplash();""",
"playSplash 恢复简笔画")

# ===== B1. 移除 6 处 a.card-image 的 data-loading =====
for _ in range(6):
    rep('rel="noopener" data-loading="正在加载作品"',
        'rel="noopener"',
        "移除 data-loading（第 %d 处）" % (6 - _))

# ===== B2. 卡片点击 JS 简化 =====
rep("""  // 作品卡片：点卡片展开预览；点「查看详情」打开作品；下载按钮除外
  document.querySelectorAll('.card').forEach(function (card) {
    card.addEventListener('click', function (e) {
      if (e.target.closest('.card-dl')) return;
      if (e.target.closest('a.card-image')) {
        e.preventDefault();
        this.classList.toggle('expanded');
        return;
      }
      if (e.target.closest('.meta')) {
        var dd = this.getAttribute('data-detail');
        if (dd) { window.location.href = dd; return; }
        var link = this.querySelector('a.card-image');
        if (link) link.click();
        return;
      }
      this.classList.toggle('expanded');
    });
    card.addEventListener('keydown', function (e) {
      if ((e.key === 'Enter' || e.key === ' ') && e.target === card) {
        e.preventDefault();
        this.classList.toggle('expanded');
      }
    });
  });""",
"""  // 作品卡片：点击一次即进入详情页（下载 / 分享按钮除外）；详情页内再点「立即体验」进入作品
  document.querySelectorAll('.card').forEach(function (card) {
    card.addEventListener('click', function (e) {
      if (e.target.closest('.card-dl')) return;
      if (e.target.closest('.card-share')) return;
      e.preventDefault();
      var dd = this.getAttribute('data-detail');
      if (dd) { window.location.href = dd; }
    });
    card.addEventListener('keydown', function (e) {
      if ((e.key === 'Enter' || e.key === ' ') && e.target === card) {
        e.preventDefault();
        var dd = this.getAttribute('data-detail');
        if (dd) { window.location.href = dd; }
      }
    });
  });""",
"卡片点击统一进详情页")

open(path, "w", encoding="utf-8").write(html)
for l in log:
    print(l)
print("DONE")
