# -*- coding: utf-8 -*-
"""v18: ①加载加速重构（按按时长递增加速、95%即冲满跳转、按钮弹出前其位置与提示文字即为热区）
②板块视觉统一：卡片顶部青色渐变分线、MC 指标青边框、查看更多青色、作品图渐变加深"""
path = "index.html"
html = open(path, encoding="utf-8").read()
log = []

def rep(old, new, tag, count=1):
    global html
    if old not in html:
        log.append("FAIL " + tag)
        return False
    html = html.replace(old, new, count)
    log.append("OK   " + tag)
    return True

# ---------- 1. CSS：load-skip 去掉位移（按钮弹出前所在位置即为热区） ----------
rep(
"""  .load-skip {
    margin-top: 20px;
    display: inline-flex; align-items: center; gap: 7px;
    font-size: 12.5px; color: var(--accent);
    border: 1px solid rgba(2,132,199,0.35); background: rgba(2,132,199,0.06);
    border-radius: 999px; padding: 9px 20px; cursor: pointer;
    opacity: 0; transform: translateY(8px);
    transition: opacity 0.35s ease, transform 0.35s ease;
    font-family: inherit; user-select: none; -webkit-user-select: none;
  }
  .load-skip.show { opacity: 1; transform: translateY(0); }""",
"""  .load-skip {
    margin-top: 20px;
    display: inline-flex; align-items: center; gap: 7px;
    font-size: 12.5px; color: var(--accent);
    border: 1px solid rgba(2,132,199,0.35); background: rgba(2,132,199,0.06);
    border-radius: 999px; padding: 9px 20px; cursor: pointer;
    opacity: 0;
    transition: opacity 0.35s ease;
    font-family: inherit; user-select: none; -webkit-user-select: none;
  }
  .load-skip.show { opacity: 1; }""",
"CSS load-skip 无位移")

# ---------- 2. CSS：loading-hint 作为副热区 ----------
rep(
"""  .loading-hint {
    margin-top: 24px;
    font-size: 13px;
    color: var(--ink-2);
    opacity: 0.6;
  }""",
"""  .loading-hint {
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
"CSS loading-hint 热区")

# ---------- 3. JS：加载系统重构 ----------
js_old = """  var overlay = document.getElementById('loadingOverlay');
  var loadBar = document.getElementById('loadBar');
  var loadPercent = document.getElementById('loadPercent');
  var loadTitle = document.getElementById('loadTitle');
  var loadSkip = document.getElementById('loadSkip');
  var loadTimer = null;
  var skipTimer = null;
  var endTimer = null;
  var boostTimer = null;
  var progress = 0;

  function hideLoading() {
    overlay.classList.remove('active');
    if (loadTimer) { clearInterval(loadTimer); loadTimer = null; }
    if (skipTimer) { clearTimeout(skipTimer); skipTimer = null; }
    if (endTimer) { clearTimeout(endTimer); endTimer = null; }
    if (boostTimer) { clearInterval(boostTimer); boostTimer = null; }
    loadBar.style.width = '0%';
    loadPercent.textContent = '0%';
    if (loadSkip) loadSkip.classList.remove('show');
  }

  function startLoading(targetUrl, title, openInNew) {
    loadTitle.textContent = title || '正在进入';
    overlay.classList.add('active');
    progress = 0;
    loadBar.style.width = '0%';
    loadPercent.textContent = '0%';
    if (loadSkip) loadSkip.classList.remove('show');
    // 常速推进：8 秒全程
    loadTimer = setInterval(function () {
      progress += Math.random() * 2.2;
      if (progress > 95) progress = 95;
      loadBar.style.width = progress + '%';
      loadPercent.textContent = Math.floor(progress) + '%';
    }, 100);
    // 第 3 秒弹出「长按加速」按钮
    skipTimer = setTimeout(function () { if (loadSkip) loadSkip.classList.add('show'); }, 3000);
    endTimer = setTimeout(function () {
      clearInterval(loadTimer); loadTimer = null;
      clearTimeout(skipTimer); skipTimer = null;
      loadBar.style.width = '100%';
      loadPercent.textContent = '100%';
      setTimeout(function () {
        if (openInNew) {
          window.open(targetUrl, '_blank');
          hideLoading();
          showToast('已在新标签页打开');
        } else {
          window.location.href = targetUrl;
        }
      }, 300);
    }, 8000);
  }

  // 长按加速：按住不放，每 70ms 前进 6%
  if (loadSkip) {
    function startBoost() {
      if (boostTimer) return;
      boostTimer = setInterval(function () {
        progress += 6;
        if (progress > 95) progress = 95;
        loadBar.style.width = progress + '%';
        loadPercent.textContent = Math.floor(progress) + '%';
      }, 70);
    }
    function stopBoost() {
      if (boostTimer) { clearInterval(boostTimer); boostTimer = null; }
    }
    loadSkip.addEventListener('mousedown', startBoost);
    loadSkip.addEventListener('touchstart', startBoost, { passive: true });
    ['mouseup', 'mouseleave', 'touchend', 'touchcancel'].forEach(function (ev) {
      loadSkip.addEventListener(ev, stopBoost);
    });
  }
"""

js_new = """  var overlay = document.getElementById('loadingOverlay');
  var loadBar = document.getElementById('loadBar');
  var loadPercent = document.getElementById('loadPercent');
  var loadTitle = document.getElementById('loadTitle');
  var loadSkip = document.getElementById('loadSkip');
  var loadHint = document.querySelector('.loading-hint');
  var loadTimer = null;
  var skipTimer = null;
  var endTimer = null;
  var boostTimer = null;
  var progress = 0;
  var finished = false;
  var pendingUrl = '';
  var pendingNew = false;

  function hideLoading() {
    overlay.classList.remove('active');
    if (loadTimer) { clearInterval(loadTimer); loadTimer = null; }
    if (skipTimer) { clearTimeout(skipTimer); skipTimer = null; }
    if (endTimer) { clearTimeout(endTimer); endTimer = null; }
    if (boostTimer) { clearInterval(boostTimer); boostTimer = null; }
    loadBar.style.width = '0%';
    loadPercent.textContent = '0%';
    if (loadSkip) loadSkip.classList.remove('show');
  }

  // 收尾：进度冲到 100% 并执行跳转（常速 8 秒到点 / 长按提前冲满 都会走到这里）
  function completeLoading() {
    if (finished) return;
    finished = true;
    if (loadTimer) { clearInterval(loadTimer); loadTimer = null; }
    if (skipTimer) { clearTimeout(skipTimer); skipTimer = null; }
    if (boostTimer) { clearInterval(boostTimer); boostTimer = null; }
    if (endTimer) { clearTimeout(endTimer); endTimer = null; }
    loadBar.style.width = '100%';
    loadPercent.textContent = '100%';
    setTimeout(function () {
      if (pendingNew) {
        window.open(pendingUrl, '_blank');
        hideLoading();
        showToast('已在新标签页打开');
      } else {
        window.location.href = pendingUrl;
      }
    }, 250);
  }

  function startLoading(targetUrl, title, openInNew) {
    loadTitle.textContent = title || '正在进入';
    overlay.classList.add('active');
    progress = 0;
    finished = false;
    pendingUrl = targetUrl;
    pendingNew = openInNew;
    loadBar.style.width = '0%';
    loadPercent.textContent = '0%';
    if (loadSkip) loadSkip.classList.remove('show');
    // 常速推进：8 秒全程
    loadTimer = setInterval(function () {
      progress += Math.random() * 2.2;
      if (progress > 95) progress = 95;
      loadBar.style.width = progress + '%';
      loadPercent.textContent = Math.floor(progress) + '%';
    }, 100);
    // 第 3 秒弹出「长按加速」按钮
    skipTimer = setTimeout(function () { if (loadSkip) loadSkip.classList.add('show'); }, 3000);
    endTimer = setTimeout(function () { completeLoading(); }, 8000);
  }

  // 长按加速：按得越久加载越快（0 秒约 57%/s，每秒递增约 12%/70ms）；到 95% 直接冲满并立即进入
  var boostStart = 0;
  function startBoost() {
    if (boostTimer) return;
    boostStart = Date.now();
    boostTimer = setInterval(function () {
      var hold = (Date.now() - boostStart) / 1000;
      var inc = 4 + hold * 12;
      progress += inc;
      if (progress >= 95) {
        progress = 95;
        loadBar.style.width = '95%';
        loadPercent.textContent = '95%';
        completeLoading();
        return;
      }
      loadBar.style.width = progress + '%';
      loadPercent.textContent = Math.floor(progress) + '%';
    }, 70);
  }
  function stopBoost() {
    if (boostTimer) { clearInterval(boostTimer); boostTimer = null; }
  }
  // 热区 = 加速按钮 + 提示文字：按钮第 3 秒才出现，但它的位置和提示文字从第 0 秒就可按住加速
  if (loadSkip) {
    loadSkip.addEventListener('mousedown', startBoost);
    loadSkip.addEventListener('touchstart', startBoost, { passive: true });
    ['mouseup', 'mouseleave', 'touchend', 'touchcancel'].forEach(function (ev) {
      loadSkip.addEventListener(ev, stopBoost);
    });
  }
  if (loadHint) {
    loadHint.addEventListener('mousedown', startBoost);
    loadHint.addEventListener('touchstart', startBoost, { passive: true });
    ['mouseup', 'mouseleave', 'touchend', 'touchcancel'].forEach(function (ev) {
      loadHint.addEventListener(ev, stopBoost);
    });
  }
"""
rep(js_old, js_new, "JS 加载系统重构")

# ---------- 4. 视觉统一：MC 指标青色 ----------
rep("border: 1.5px solid #17181C;", "border: 1.5px solid rgba(2,132,199,0.38);", "mc-metric 青边框")
rep(":root[data-theme=\"dark\"] .mc-metric { border-color: #E8EAED; }",
    ":root[data-theme=\"dark\"] .mc-metric { border-color: rgba(56,189,248,0.42); }",
    "mc-metric dark 青边框")
rep(".mc-metric .m-val { color: #17181C; }", ".mc-metric .m-val { color: var(--accent); }", "mc-metric 数值青色")
rep(":root[data-theme=\"dark\"] .mc-metric .m-val { color: #E8EAED; }",
    ":root[data-theme=\"dark\"] .mc-metric .m-val { color: #7dd3fc; }",
    "mc-metric dark 数值青色")

# ---------- 5. 视觉统一：查看更多按钮青色 ----------
rep(
"""  .btn-more {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 14px 32px;
    border: 1px solid var(--line);
    border-radius: 999px;
    background: var(--card-bg);
    color: var(--ink);
    font-size: 15px;
    font-weight: 500;
    cursor: pointer;
    transition: all .15s;
    font-family: inherit;
  }
  .btn-more:hover { border-color: var(--accent); color: var(--accent); }""",
"""  .btn-more {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 14px 32px;
    border: 1px solid rgba(2,132,199,0.35);
    border-radius: 999px;
    background: rgba(2,132,199,0.05);
    color: var(--accent);
    font-size: 15px;
    font-weight: 500;
    cursor: pointer;
    transition: all .15s;
    font-family: inherit;
  }
  .btn-more:hover { border-color: var(--accent); color: var(--accent); background: rgba(2,132,199,0.12); }""",
"btn-more 青色")

# ---------- 6. 视觉统一：作品图渐变加深青色 ----------
rep("--card-image: linear-gradient(135deg, #e0f2fe, #bae6fd);",
    "--card-image: linear-gradient(135deg, #d7effc, #9fd9f3);",
    "card-image 青渐变加深")

# ---------- 7. 视觉统一：卡片顶部青色分线（作品/仓库/日志/此刻/清单） ----------
rep("  /* ===== 人生清单 ===== */",
"""  /* ===== v18 视觉统一：下方板块注入青色血脉（顶部渐变分线） ===== */
  .card, .repo-card, .mc-ver, .now-card, .bucket-item { position: relative; }
  .card::before, .repo-card::before, .mc-ver::before, .now-card::before, .bucket-item::before {
    content: "";
    position: absolute; top: 0; left: 0; right: 0; height: 3px;
    border-radius: 999px 999px 0 0;
    background: linear-gradient(90deg, var(--accent), var(--accent-2));
    opacity: 0.9;
    pointer-events: none;
    z-index: 1;
  }
  .bucket-item { transition: border-color 0.15s, transform 0.15s; }
  .bucket-item:hover { border-color: rgba(2,132,199,0.45); transform: translateY(-2px); }

  /* ===== 人生清单 ===== */""",
"卡片顶部青色分线")

open(path, "w", encoding="utf-8").write(html)
for l in log:
    print(l)
print("DONE")
