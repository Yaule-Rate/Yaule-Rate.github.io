# -*- coding: utf-8 -*-
"""v14: RSS/Atom 订阅 + 访问计数(不蒜子) + SEO 增强 + 视差滚动 + 作品展开预览 + favicon 呼吸 + 幸运今日"""
path = "index.html"
html = open(path, encoding="utf-8").read()
changed = []

# ---------- 1. SEO 增强 ----------
old_seo = """<meta name="description" content="欢迎来到 Yaule 的个人主页。这里记录着咖啡、音乐、游戏与作品。">
<meta name="author" content="Yaule">
<link rel="canonical" href="https://Yaule-Rate.github.io/">
<meta property="og:type" content="website">
<meta property="og:title" content="Yaule · 欢迎你的到来">
<meta property="og:url" content="https://Yaule-Rate.github.io/">"""
new_seo = """<meta name="description" content="欢迎来到 Yaule 的个人主页。这里记录着咖啡、音乐、游戏与作品，还有全世界的「欢迎你的到来」。">
<meta name="keywords" content="Yaule,个人主页,个人空间,欢迎你的到来,博客,作品集,GitHub Pages,失眠夜">
<meta name="author" content="Yaule">
<link rel="canonical" href="https://Yaule-Rate.github.io/">
<link rel="alternate" type="application/atom+xml" title="Yaule 的个人空间" href="https://Yaule-Rate.github.io/atom.xml">
<meta property="og:type" content="website">
<meta property="og:title" content="Yaule · 欢迎你的到来">
<meta property="og:description" content="欢迎来到 Yaule 的个人主页。这里记录着咖啡、音乐、游戏与作品。">
<meta property="og:url" content="https://Yaule-Rate.github.io/">
<meta property="og:site_name" content="Yaule 的个人空间">
<meta property="og:locale" content="zh_CN">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="Yaule · 欢迎你的到来">
<meta name="twitter:description" content="欢迎来到 Yaule 的个人主页。这里记录着咖啡、音乐、游戏与作品。">"""
if old_seo in html:
    html = html.replace(old_seo, new_seo, 1); changed.append("seo")
else:
    print("FAIL seo")

# ---------- 2. CSS ----------
anchor = """  @media (prefers-reduced-motion: reduce) {
    .page-loader { display: none; }
  }
"""
add_css = """  /* ===== 作品展开预览 ===== */
  .card-preview {
    max-height: 0;
    overflow: hidden;
    opacity: 0;
    transition: max-height 0.35s ease, opacity 0.35s ease, margin-top 0.35s ease;
    font-size: 13.5px;
    color: var(--ink-2);
    line-height: 1.7;
  }
  .card.expanded .card-preview { max-height: 180px; opacity: 1; margin-top: 10px; }
  .card-tags { display: inline-flex; gap: 6px; flex-wrap: wrap; }
  .card-tags span {
    font-size: 11px;
    color: var(--accent);
    border: 1px solid rgba(2, 132, 199, 0.3);
    background: rgba(2, 132, 199, 0.05);
    border-radius: 999px;
    padding: 2px 10px;
  }
  .card { cursor: pointer; }
  .card .meta { transition: color 0.2s ease; }
  .card.expanded .meta { color: var(--accent); }

  /* ===== 页脚新增项 ===== */
  .footer-bottom .visit b { color: var(--accent-2); font-weight: 600; }
  .footer-bottom .lucky b { font-weight: 600; }
  .footer-bottom .lucky { white-space: nowrap; }

  @media (prefers-reduced-motion: reduce) {
    .page-loader { display: none; }
  }
"""
if anchor in html:
    html = html.replace(anchor, add_css, 1); changed.append("css")
else:
    print("FAIL css")

# ---------- 3. 作品预览 HTML（6 个） ----------
previews = [
    ("兴华中学广播站系统",
     "广播排班、播放日程、站点信息一站式维护，从零开发并投入校园日常使用。",
     ["广播", "管理"]),
    ("自助记账系统",
     "收支流水、分类统计、报表导出，让每一笔账都清清楚楚。",
     ["记账", "工具"]),
    ("代码编写系统",
     "代码编写辅助工作台，模板化快速生成，让日常编码更顺手。",
     ["编码", "效率"]),
    ("表情转图片转换器",
     "把文字图案一键转成 Emoji 图片，分享出来更有趣。",
     ["趣味", "图像"]),
    ("CS 灵敏度校准",
     "FPS 游戏鼠标灵敏度科学校准，找到真正属于自己的手感。",
     ["游戏", "外设"]),
    ("棋类合集",
     "象棋与五子棋同页双开，约上好友面对面来一局。",
     ["游戏", "对战"]),
]
for name, desc, tags in previews:
    old_block = '<h3>%s</h3>\n          <p>' % name
    i = html.find(old_block)
    if i == -1:
        print("FAIL preview:", name); continue
    p_end = html.find('</p>', i)
    meta_start = html.find('<span class="meta">', p_end)
    if meta_start == -1:
        print("FAIL meta:", name); continue
    tags_html = "".join("<span>%s</span>" % t for t in tags)
    preview = ('<div class="card-preview">\n'
               '            <p>%s</p>\n'
               '            <span class="card-tags">%s</span>\n'
               '          </div>\n          ') % (desc, tags_html)
    html = html[:meta_start] + preview + html[meta_start:]
    changed.append("preview: " + name)

# ---------- 4. 卡片点击：展开/收起 + 查看详情跳转 ----------
old_click = """  // 作品卡片：整卡可点击（单击卡片任意处打开作品，下载按钮除外）
  document.querySelectorAll('.card').forEach(function (card) {
    card.addEventListener('click', function (e) {
      if (e.target.closest('.card-dl')) return;
      var link = this.querySelector('a.card-image');
      if (link && !e.target.closest('a.card-image')) {
        link.click();
      }
    });
    card.addEventListener('keydown', function (e) {
      if ((e.key === 'Enter' || e.key === ' ') && e.target === card) {
        e.preventDefault();
        var link = this.querySelector('a.card-image');
        if (link) link.click();
      }
    });
  });"""
new_click = """  // 作品卡片：点卡片展开预览；点「查看详情」打开作品；下载按钮除外
  document.querySelectorAll('.card').forEach(function (card) {
    card.addEventListener('click', function (e) {
      if (e.target.closest('.card-dl')) return;
      var link = this.querySelector('a.card-image');
      if (e.target.closest('a.card-image')) return;
      if (e.target.closest('.meta')) {
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
  });"""
if old_click in html:
    html = html.replace(old_click, new_click, 1); changed.append("card click")
else:
    print("FAIL card click")

# ---------- 5. 页脚：幸运今日 + 访问计数 + RSS 订阅 ----------
old_fb = """    <div class="footer-bottom">
      <span>© <span id="year">2026</span> Yaule. All rights reserved.</span>
      <span class="stay-time" id="stayTime">已停留 0 分 0 秒</span>
      <span>Powered by GitHub Pages</span>
    </div>"""
new_fb = """    <div class="footer-bottom">
      <span>© <span id="year">2026</span> Yaule. All rights reserved.</span>
      <span class="stay-time" id="stayTime">已停留 0 分 0 秒</span>
      <span class="visit">本站访问 <b id="pvCount" class="busuanzi_value_site_pv">--</b> 次</span>
      <span class="lucky" id="luckyToday">今日幸运 · --</span>
      <span>Powered by GitHub Pages</span>
    </div>"""
if old_fb in html:
    html = html.replace(old_fb, new_fb, 1); changed.append("footer bottom")
else:
    print("FAIL footer bottom")

old_rss = """          <li><a href="https://github.com/Yaule-Rate" target="_blank" rel="noopener">GitHub</a></li>
          <li><a href="mailto:1957784559@qq.com">邮箱</a></li>"""
new_rss = """          <li><a href="https://github.com/Yaule-Rate" target="_blank" rel="noopener">GitHub</a></li>
          <li><a href="mailto:1957784559@qq.com">邮箱</a></li>
          <li><a href="atom.xml">RSS 订阅</a></li>"""
if old_rss in html:
    html = html.replace(old_rss, new_rss, 1); changed.append("rss link")
else:
    print("FAIL rss link")

# ---------- 6. 不蒜子脚本（</body> 前） ----------
old_body_end = """<div class="fest-layer" id="festLayer"></div>
<script>"""
new_body_end = """<div class="fest-layer" id="festLayer"></div>
<script async src="https://busuanzi.ibruce.info/busuanzi/2.3/busuanzi.pure.mini.js"></script>
<script>"""
if old_body_end in html:
    html = html.replace(old_body_end, new_body_end, 1); changed.append("busuanzi")
else:
    print("FAIL busuanzi")

# ---------- 7. JS：视差 + favicon 呼吸 + 幸运今日（script 末尾） ----------
tail = "  })();\n</script>"
add_js = """  })();

  /* ========== 视差滚动：首屏随滚动上移淡出 ========== */
  (function () {
    var hero = document.getElementById('hero');
    if (!hero) return;
    var inner = hero.querySelector('.hero-inner');
    if (!inner) return;
    var ticking = false;
    function update() {
      var y = window.pageYOffset || document.documentElement.scrollTop;
      if (y < window.innerHeight) {
        inner.style.transform = 'translateY(' + (y * 0.22) + 'px)';
        inner.style.opacity = String(Math.max(0, 1 - y / 520));
      }
      ticking = false;
    }
    window.addEventListener('scroll', function () {
      if (!ticking) { ticking = true; requestAnimationFrame(update); }
    }, { passive: true });
    update();
  })();

  /* ========== favicon 呼吸 ========== */
  (function () {
    var link = document.querySelector('link[rel="icon"]');
    if (!link) return;
    var cv = document.createElement('canvas');
    cv.width = 32; cv.height = 32;
    var ctx = cv.getContext('2d');
    function roundRect(x, y, w, h, r) {
      ctx.beginPath();
      ctx.moveTo(x + r, y);
      ctx.arcTo(x + w, y, x + w, y + h, r);
      ctx.arcTo(x + w, y + h, x, y + h, r);
      ctx.arcTo(x, y + h, x, y, r);
      ctx.arcTo(x, y, x + w, y, r);
      ctx.closePath();
    }
    var t = 0;
    function draw() {
      t += 0.12;
      var a = 0.45 + 0.55 * (Math.sin(t) * 0.5 + 0.5);
      ctx.clearRect(0, 0, 32, 32);
      ctx.fillStyle = 'rgba(2,132,199,' + a.toFixed(3) + ')';
      roundRect(1, 1, 30, 30, 7); ctx.fill();
      ctx.strokeStyle = '#ffffff'; ctx.lineWidth = 2.4; ctx.lineCap = 'round'; ctx.lineJoin = 'round';
      ctx.beginPath();
      ctx.moveTo(8.5, 8.5); ctx.lineTo(16, 16); ctx.lineTo(23.5, 8.5);
      ctx.moveTo(16, 16); ctx.lineTo(16, 25);
      ctx.stroke();
      link.href = cv.toDataURL();
    }
    draw();
    setInterval(draw, 120);
  })();

  /* ========== 幸运今日（按日期固定） ========== */
  (function () {
    var el = document.getElementById('luckyToday');
    if (!el) return;
    var d = new Date();
    var key = d.getFullYear() * 10000 + (d.getMonth() + 1) * 100 + d.getDate();
    var h = 0, s = String(key);
    for (var i = 0; i < s.length; i++) { h = (h * 31 + s.charCodeAt(i)) >>> 0; }
    var lucky = (h % 100) + 1;
    var colors = [
      ['#0284c7', '晴蓝'], ['#0ea5e9', '天青'], ['#38bdf8', '云青'],
      ['#22d3ee', '湖青'], ['#06b6d4', '碧波'], ['#0891b2', '松青']
    ];
    var c = colors[h % colors.length];
    var tips = ['宜写代码', '宜喝咖啡', '宜听歌', '宜发呆', '宜早睡', '宜整理', '宜散步', '宜收藏', '宜分享', '宜读书'];
    var tip = tips[(h >> 4) % tips.length];
    el.innerHTML = '今日幸运 <b style="color:' + c[0] + '">' + lucky + '</b> · ' + c[1] + ' ' + tip;
  })();
</script>"""
if tail in html:
    html = html.replace(tail, add_js, 1); changed.append("js add")
else:
    print("FAIL js tail")

open(path, "w", encoding="utf-8").write(html)
print("CHANGED:", changed)
