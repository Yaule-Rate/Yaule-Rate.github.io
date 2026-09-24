# -*- coding: utf-8 -*-
"""v13: 今年进度环 + 一言自动轮播/点击复制 + 页面加载一笔画动画"""
path = "index.html"
html = open(path, encoding="utf-8").read()
changed = []

# ---------- 1. CSS ----------
# 1a. now-grid 改 3 列
old = """.now-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
  }"""
new = """.now-grid {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 20px;
  }"""
if old in html:
    html = html.replace(old, new, 1); changed.append("grid 3col")
else:
    print("FAIL grid")

# 1b. 追加：进度环 / 一言过渡 / 加载动画样式（插在 .now-card .weather-temp 之后）
anchor = """  @media (max-width: 640px) {
    .now-grid { grid-template-columns: 1fr; }
  }
"""
add_css = """  /* ===== 今年进度环 ===== */
  .now-progress { display: flex; flex-direction: column; align-items: center; justify-content: center; }
  .ring-wrap { position: relative; width: 126px; height: 126px; }
  .ring-wrap svg { width: 100%; height: 100%; }
  .ring-fg { transition: stroke-dashoffset 1.2s ease; }
  .ring-center { position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; }
  .ring-pct { font-size: 30px; font-weight: 800; color: var(--ink); font-family: "Noto Serif SC", Georgia, serif; line-height: 1; }
  .ring-label { font-size: 11px; color: var(--ink-2); letter-spacing: 0.14em; margin-top: 5px; }
  .ring-foot { margin-top: 14px; font-size: 13px; color: var(--ink-2); }

  /* ===== 一言过渡 ===== */
  #quoteText { transition: opacity 0.22s ease; }

  /* ===== 页面加载动画：青色 Y 一笔画 ===== */
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
  @keyframes loaderName { to { opacity: 1; transform: translateY(0); } }
  @media (prefers-reduced-motion: reduce) {
    .page-loader { display: none; }
  }

  @media (max-width: 640px) {
    .now-grid { grid-template-columns: 1fr; }
  }
"""
if anchor in html:
    html = html.replace(anchor, add_css, 1); changed.append("css add")
else:
    print("FAIL css add")

# ---------- 2. HTML：加载动画（body 最前） ----------
old_body = """<body>
<!-- 伪进度条加载遮罩 -->"""
new_body = """<body>
<!-- 页面加载动画：青色 Y 一笔画 -->
<div class="page-loader" id="pageLoader">
  <svg class="loader-svg" viewBox="0 0 120 120" fill="none" stroke="currentColor" stroke-width="7" stroke-linecap="round" stroke-linejoin="round">
    <path class="loader-path" pathLength="100" d="M22 18 L60 54 L98 18 M60 54 L60 102"/>
  </svg>
  <p class="loader-name">Yaule</p>
</div>
<!-- 伪进度条加载遮罩 -->"""
if old_body in html:
    html = html.replace(old_body, new_body, 1); changed.append("loader html")
else:
    print("FAIL loader html")

# ---------- 3. HTML：今年进度环卡片（now-grid 末尾） ----------
old_now = """      <div class="now-card">
        <p class="weather-row" id="weatherRow">
          <svg id="weatherIcon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17.5 19H9a7 7 0 1 1 6.71-9h1.79a4.5 4.5 0 1 1 0 9Z"/></svg>
          <span id="weatherText">衢州 · 正在读取天气…</span>
        </p>
      </div>
    </div>
  </div>
</section>"""
new_now = """      <div class="now-card">
        <p class="weather-row" id="weatherRow">
          <svg id="weatherIcon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17.5 19H9a7 7 0 1 1 6.71-9h1.79a4.5 4.5 0 1 1 0 9Z"/></svg>
          <span id="weatherText">衢州 · 正在读取天气…</span>
        </p>
      </div>
      <div class="now-card now-progress">
        <div class="ring-wrap">
          <svg viewBox="0 0 100 100" fill="none" stroke-linecap="round">
            <circle cx="50" cy="50" r="42" stroke="var(--line)" stroke-width="7"/>
            <circle class="ring-fg" id="yearRing" cx="50" cy="50" r="42" stroke="var(--accent)" stroke-width="7" stroke-dasharray="263.9" stroke-dashoffset="263.9" transform="rotate(-90 50 50)"/>
          </svg>
          <div class="ring-center">
            <span class="ring-pct" id="yearPct">--%</span>
            <span class="ring-label">今年已过</span>
          </div>
        </div>
        <p class="ring-foot" id="yearLeft">2026 年还剩 -- 天</p>
      </div>
    </div>
  </div>
</section>"""
if old_now in html:
    html = html.replace(old_now, new_now, 1); changed.append("ring html")
else:
    print("FAIL ring html")

# ---------- 4. JS：一言自动轮播 + 点击复制 ----------
old_quote = """    // 初始化：先显示本地每日一句，联网成功则替换为实时句子
    pickLocal(false);
    fetchNet(function (q) { if (q) render(q); });
    next.addEventListener('click', function () {
      fetchNet(function (q) { if (q) { render(q); } else { pickLocal(true); } });
    });
  })();"""
new_quote = """    // 一言：每 3 秒自动换（联网优先，失败本地随机）；点击复制
    function fallbackCopy(t) {
      var ta = document.createElement('textarea');
      ta.value = t;
      ta.style.position = 'fixed';
      ta.style.opacity = '0';
      document.body.appendChild(ta);
      ta.select();
      try { document.execCommand('copy'); } catch (e) {}
      document.body.removeChild(ta);
    }
    var qTimer = null;
    function fadeSwap(fn) {
      text.style.opacity = '0';
      setTimeout(function () { fn(); text.style.opacity = '1'; }, 220);
    }
    function nextQuote() {
      fetchNet(function (q) {
        if (q) { fadeSwap(function () { render(q); }); }
        else { fadeSwap(function () { pickLocal(true); }); }
      });
    }
    function restartAuto() {
      if (qTimer) clearInterval(qTimer);
      qTimer = setInterval(nextQuote, 3000);
    }
    pickLocal(false);
    fetchNet(function (q) { if (q) render(q); });
    next.addEventListener('click', function () { nextQuote(); restartAuto(); });
    restartAuto();
    text.style.cursor = 'pointer';
    text.title = '点击复制一言';
    text.addEventListener('click', function () {
      var t = text.textContent.replace(/^“|”$/g, '');
      function done() { showToast('一言已复制'); }
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(t).then(done).catch(function () { fallbackCopy(t); done(); });
      } else { fallbackCopy(t); done(); }
    });
  })();"""
if old_quote in html:
    html = html.replace(old_quote, new_quote, 1); changed.append("quote js")
else:
    print("FAIL quote js")

# ---------- 5. JS：今年进度 + 加载动画移除（script 末尾 </script> 前） ----------
tail = "  })();\n</script>"
add_tail = """  })();

  /* ========== 今年进度环 ========== */
  (function () {
    var ring = document.getElementById('yearRing');
    var pctEl = document.getElementById('yearPct');
    var leftEl = document.getElementById('yearLeft');
    if (!ring || !pctEl) return;
    function update() {
      var now = new Date();
      var y = now.getFullYear();
      var start = new Date(y, 0, 1);
      var end = new Date(y + 1, 0, 1);
      var total = Math.round((end - start) / 86400000);
      var elapsed = Math.floor((now - start) / 86400000) + 1;
      var pct = Math.min(100, Math.round((elapsed / total) * 100));
      var left = Math.max(0, total - elapsed);
      var C = 2 * Math.PI * 42;
      ring.setAttribute('stroke-dasharray', C.toFixed(1));
      ring.setAttribute('stroke-dashoffset', (C * (1 - pct / 100)).toFixed(1));
      pctEl.textContent = pct + '%';
      leftEl.textContent = y + ' 年还剩 ' + left + ' 天';
    }
    update();
    setInterval(update, 60000);
  })();

  /* ========== 页面加载动画移除 ========== */
  (function () {
    var loader = document.getElementById('pageLoader');
    if (!loader) return;
    setTimeout(function () {
      loader.classList.add('done');
      setTimeout(function () {
        if (loader.parentNode) loader.parentNode.removeChild(loader);
      }, 600);
    }, 1700);
  })();
</script>"""
if tail in html:
    html = html.replace(tail, add_tail, 1); changed.append("year/loader js")
else:
    print("FAIL tail")

open(path, "w", encoding="utf-8").write(html)
print("CHANGED:", changed)
