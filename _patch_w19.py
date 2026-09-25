# -*- coding: utf-8 -*-
"""v19 index.html：①作品卡分享按钮(微博/QQ带文案) ②加载标语随机轮换 ③22:00-06:00自动深色(手动优先) ④SEO title/description 加长"""
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

# ---------- 1. SEO：title / description 加长 ----------
rep('<title>Yaule · 欢迎你的到来</title>',
    '<title>Yaule · 欢迎你的到来 | 个人主页 · 失眠夜空间 · 作品与日常</title>',
    "title 加长")
rep('''<meta name="description" content="欢迎来到 Yaule 的个人主页。这里记录着咖啡、音乐、游戏与作品，还有全世界的「欢迎你的到来」。">''',
    '''<meta name="description" content="欢迎来到 Yaule 的个人主页（失眠夜空间）：记录着咖啡、音乐、游戏与作品，精选校园工具到游戏辅助的自研项目，还有全世界的「欢迎你的到来」。在这里可以看到开源仓库、技能雷达、人生清单与详细更新日志。">''',
    "description 加长")

# ---------- 2. CSS：分享按钮与浮层 + 标语行 ----------
rep("  .card { cursor: pointer; }",
"""  /* ===== v19 分享按钮 ===== */
  .card-foot {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    margin-top: 4px;
  }
  .card-share {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    font-size: 12px;
    color: var(--ink-2);
    background: var(--soft);
    border: 1px solid var(--line);
    border-radius: 999px;
    padding: 4px 12px;
    cursor: pointer;
    font-family: inherit;
    transition: all 0.15s ease;
  }
  .card-share:hover { color: var(--accent); border-color: var(--accent); background: rgba(2,132,199,0.08); }
  .card-share svg { width: 13px; height: 13px; }
  .share-pop {
    position: absolute;
    right: 12px;
    bottom: 46px;
    display: flex;
    gap: 8px;
    background: var(--card-bg);
    border: 1px solid rgba(2,132,199,0.3);
    border-radius: 12px;
    padding: 8px 10px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.14);
    opacity: 0;
    transform: translateY(6px) scale(0.96);
    pointer-events: none;
    transition: opacity 0.18s ease, transform 0.18s ease;
    z-index: 5;
  }
  .share-pop.show { opacity: 1; transform: translateY(0) scale(1); pointer-events: all; }
  .share-pop a {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    font-size: 12px;
    color: var(--ink-2);
    text-decoration: none;
    border-radius: 999px;
    padding: 5px 12px;
    border: 1px solid var(--line);
    transition: all 0.15s ease;
  }
  .share-pop a:hover { color: #fff; text-decoration: none; }
  .share-pop .sp-wb { background: rgba(255,112,67,0.08); }
  .share-pop .sp-wb:hover { background: #ff7043; border-color: #ff7043; }
  .share-pop .sp-qq { background: rgba(18,183,245,0.08); }
  .share-pop .sp-qq:hover { background: #12b7f5; border-color: #12b7f5; }
  .share-pop a svg { width: 12px; height: 12px; }
  .card { cursor: pointer; }""",
"CSS 分享按钮/浮层")

# ---------- 3. JS：startLoading 标语轮换 ----------
rep("""    loadTitle.textContent = title || '正在进入';
    overlay.classList.add('active');""",
"""    loadTitle.textContent = title || '正在进入';
    overlay.classList.add('active');
    var LOAD_LINES = [
      '正在泡咖啡…', '正在数星星…', '正在整理作品…', '正在点亮灯笼…',
      '正在问候全世界…', '正在翻今天的日记…', '正在检查进度条…', '正在等你…'
    ];
    if (loadHint) loadHint.textContent = LOAD_LINES[Math.floor(Math.random() * LOAD_LINES.length)];""",
"加载标语轮换")

# ---------- 4. JS：主题自动深色（手动优先） ----------
rep("""  /* ========== 主题切换（深色 / 浅色） ========== */
  (function () {
    var toggle = document.getElementById('themeToggle');
    var root = document.documentElement;
    try {
      if (localStorage.getItem('yaule-theme') === 'dark') root.setAttribute('data-theme', 'dark');
    } catch (e) {}
    toggle.addEventListener('click', function () {
      if (root.getAttribute('data-theme') === 'dark') {
        root.removeAttribute('data-theme');
        try { localStorage.setItem('yaule-theme', 'light'); } catch (e) {}
      } else {
        root.setAttribute('data-theme', 'dark');
        try { localStorage.setItem('yaule-theme', 'dark'); } catch (e) {}
      }
    });
  })();""",
"""  /* ========== 主题切换（深色 / 浅色；22:00–06:00 自动深色，手动选择优先） ========== */
  (function () {
    var toggle = document.getElementById('themeToggle');
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
    setInterval(applyTheme, 1800000);
    toggle.addEventListener('click', function () {
      if (root.getAttribute('data-theme') === 'dark') {
        root.removeAttribute('data-theme');
        try { localStorage.setItem('yaule-theme', 'light'); } catch (e) {}
      } else {
        root.setAttribute('data-theme', 'dark');
        try { localStorage.setItem('yaule-theme', 'dark'); } catch (e) {}
      }
    });
  })();""",
"主题自动深色")

# ---------- 5. JS：作品卡分享按钮注入 ----------
rep("""  /* ========== 下载按钮（不触发进度条，直接下载） ========== */""",
"""  /* ========== 作品卡分享按钮（微博 / QQ 带文案） ========== */
  (function () {
    var base = location.origin + location.pathname;
    function closeShares() {
      document.querySelectorAll('.share-pop.show').forEach(function (p) { p.classList.remove('show'); });
    }
    document.querySelectorAll('.card').forEach(function (card) {
      var meta = card.querySelector('.meta');
      var h3 = card.querySelector('h3');
      if (!meta || !h3) return;
      var name = h3.textContent.trim() || '作品';
      var detail = card.getAttribute('data-detail') || '';
      var shareUrl = detail
        ? base.replace(/\\/[^/]*$/, '/') + detail
        : base;
      var text = '来自 Yaule 的作品「' + name + '」——失眠夜个人空间';
      var foot = document.createElement('div');
      foot.className = 'card-foot';
      meta.parentNode.insertBefore(foot, meta);
      foot.appendChild(meta);
      var btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'card-share';
      btn.title = '分享作品';
      btn.setAttribute('aria-label', '分享作品');
      btn.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/></svg>分享';
      foot.appendChild(btn);
      var pop = document.createElement('div');
      pop.className = 'share-pop';
      pop.innerHTML =
        '<a class="sp-wb" target="_blank" rel="noopener" href="https://service.weibo.com/share/share.php?url=' + encodeURIComponent(shareUrl) + '&title=' + encodeURIComponent(text) + '"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M10.5 11.5c-.8-.3-1.7-1.5-1.5-2.5.2-1 .9-1.4 1.6-1 .7.4 1 1.3.6 2-.3.6-.5 1.2-.7 1.5zm3-1.2c.5 0 .8-.4.8-1s-.4-1-.8-1c-.5 0-.8.4-.8 1s.3 1 .8 1zm-1.2 2.1c-.5-.4-1.7-1.8-1.6-3 .1-1.1.8-1.8 1.7-1.4 1 .4 1.4 1.7.9 3.1-.1.4-.6 1.2-1 1.3zM19 13c0 4.4-3.6 8-8 8s-8-3.6-8-8 3.6-8 8-8 8 3.6 8 8z"/></svg>微博</a>' +
        '<a class="sp-qq" target="_blank" rel="noopener" href="https://connect.qq.com/widget/shareqq/index.html?url=' + encodeURIComponent(shareUrl) + '&title=' + encodeURIComponent(text) + '&summary=' + encodeURIComponent('点开看看这个作品') + '"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.5 2 2 6 2 10.9c0 2.6 1.3 4.9 3.4 6.4-.2.8-.5 1.6-.5 2.2 0 .6.5 1.1 1.2 1.1 1 0 2.2-.7 3.2-1.5 1.5.4 3.1.7 4.7.7s3.2-.2 4.7-.7c1 .8 2.2 1.5 3.2 1.5.7 0 1.2-.5 1.2-1.1 0-.6-.3-1.4-.5-2.2 2.1-1.5 3.4-3.8 3.4-6.4C22 6 17.5 2 12 2z"/></svg>QQ</a>';
      foot.appendChild(pop);
      btn.addEventListener('click', function (e) {
        e.stopPropagation();
        if (pop.classList.contains('show')) { pop.classList.remove('show'); return; }
        closeShares();
        pop.classList.add('show');
      });
      pop.addEventListener('click', function (e) { e.stopPropagation(); });
      card.addEventListener('click', closeShares);
    });
    document.addEventListener('click', closeShares);
  })();

  /* ========== 下载按钮（不触发进度条，直接下载） ========== */""",
"分享按钮 JS")

open(path, "w", encoding="utf-8").write(html)
for l in log:
    print(l)
print("DONE")
