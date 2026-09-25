# -*- coding: utf-8 -*-
"""v15: 新增 4 个板块——开源仓库墙(GitHub API) + 技能雷达图(SVG) + 版本更新日志(时间轴) + 人生清单(点亮交互)"""
path = "index.html"
html = open(path, encoding="utf-8").read()
changed = []

# ============ 1. CSS ============
anchor = """  /* ===== 页脚新增项 ===== */
  .footer-bottom .visit b { color: var(--accent-2); font-weight: 600; }
  .footer-bottom .lucky b { font-weight: 600; }
  .footer-bottom .lucky { white-space: nowrap; }
"""
add_css = """  /* ===== 页脚新增项 ===== */
  .footer-bottom .visit b { color: var(--accent-2); font-weight: 600; }
  .footer-bottom .lucky b { font-weight: 600; }
  .footer-bottom .lucky { white-space: nowrap; }

  /* ===== 开源仓库墙 ===== */
  .repo-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
  .repo-card {
    display: flex;
    flex-direction: column;
    gap: 8px;
    border: 1px solid var(--line);
    border-radius: 14px;
    background: var(--card-bg);
    padding: 20px 22px;
    transition: border-color 0.15s, transform 0.15s, box-shadow 0.15s;
  }
  .repo-card:hover { border-color: var(--accent); transform: translateY(-3px); box-shadow: 0 10px 28px rgba(0,0,0,0.07); }
  .repo-card .repo-name { display: flex; align-items: center; gap: 8px; font-size: 15.5px; font-weight: 600; color: var(--accent); }
  .repo-card .repo-name svg { width: 15px; height: 15px; flex: none; }
  .repo-card .repo-desc { font-size: 13.5px; color: var(--ink-2); line-height: 1.65; flex: 1; }
  .repo-card .repo-meta { display: flex; align-items: center; gap: 14px; font-size: 12.5px; color: var(--ink-2); }
  .repo-card .repo-meta span { display: inline-flex; align-items: center; gap: 5px; }
  .repo-card .repo-meta svg { width: 13px; height: 13px; }
  .lang-dot { width: 10px; height: 10px; border-radius: 50%; display: inline-block; }
  .repo-meta .repo-updated { margin-left: auto; }
  @media (max-width: 640px) { .repo-grid { grid-template-columns: 1fr; } }

  /* ===== 技能雷达图 ===== */
  .skill-wrap { display: grid; grid-template-columns: 1.1fr 1fr; gap: 36px; align-items: center; }
  .radar-box { max-width: 380px; margin: 0 auto; }
  .radar-box svg { width: 100%; height: auto; display: block; }
  .radar-grid-line { fill: none; stroke: var(--line); stroke-width: 1; }
  .radar-axis { stroke: var(--line); stroke-width: 1; }
  .radar-area { fill: rgba(2, 132, 199, 0.22); stroke: var(--accent); stroke-width: 2; transition: all 0.6s ease; }
  .radar-dot { fill: var(--accent); }
  .radar-label { font-size: 11.5px; fill: var(--ink-2); text-anchor: middle; }
  .radar-label strong { font-size: 13px; fill: var(--ink); font-weight: 600; }
  .skill-text h3 { font-size: 18px; font-weight: 600; margin-bottom: 12px; }
  .skill-text p { font-size: 14.5px; color: var(--ink-2); line-height: 1.85; }
  .skill-bars { margin-top: 18px; display: flex; flex-direction: column; gap: 10px; }
  .skill-bar-row { display: flex; align-items: center; gap: 12px; font-size: 13px; }
  .skill-bar-row .sb-name { width: 74px; flex: none; color: var(--ink-2); }
  .skill-bar-row .sb-track { flex: 1; height: 6px; background: var(--line); border-radius: 999px; overflow: hidden; }
  .skill-bar-row .sb-fill { height: 100%; background: linear-gradient(90deg, var(--accent), var(--accent-2)); border-radius: 999px; width: 0; transition: width 0.9s ease; }
  .skill-bar-row .sb-num { width: 30px; text-align: right; color: var(--accent); font-weight: 600; }
  @media (max-width: 640px) { .skill-wrap { grid-template-columns: 1fr; gap: 24px; } }

  /* ===== 版本更新日志（时间轴） ===== */
  .timeline { display: grid; grid-template-columns: 84px 26px 1fr; gap: 0; }
  .tl-time { text-align: right; font-size: 12.5px; color: var(--ink-2); padding-top: 2px; font-variant-numeric: tabular-nums; }
  .tl-axis { position: relative; }
  .tl-axis::before {
    content: "";
    position: absolute;
    left: 50%;
    top: 4px;
    bottom: 4px;
    width: 2px;
    transform: translateX(-50%);
    background: linear-gradient(180deg, var(--accent), rgba(2,132,199,0.15));
    border-radius: 2px;
  }
  .tl-dot {
    position: absolute;
    left: 50%;
    top: 6px;
    width: 10px;
    height: 10px;
    transform: translateX(-50%);
    border-radius: 50%;
    background: var(--accent);
    border: 2px solid var(--bg);
    box-shadow: 0 0 0 2px rgba(2,132,199,0.25);
  }
  .tl-dot.now { background: var(--accent-2); animation: tlPulse 2s ease infinite; }
  @keyframes tlPulse { 0%,100% { box-shadow: 0 0 0 2px rgba(56,189,248,0.25); } 50% { box-shadow: 0 0 0 6px rgba(56,189,248,0.08); } }
  .tl-item { padding: 0 0 26px 14px; }
  .tl-item:last-child { padding-bottom: 4px; }
  .tl-title { font-size: 14.5px; font-weight: 600; color: var(--ink); line-height: 1.5; }
  .tl-desc { font-size: 13px; color: var(--ink-2); margin-top: 4px; line-height: 1.7; }
  .tl-tag { display: inline-block; font-size: 11px; color: var(--accent); border: 1px solid rgba(2,132,199,0.3); background: rgba(2,132,199,0.05); border-radius: 999px; padding: 1px 9px; margin-left: 8px; vertical-align: 2px; }

  /* ===== 人生清单 ===== */
  .bucket-head { display: flex; align-items: baseline; gap: 14px; margin-bottom: 18px; flex-wrap: wrap; }
  .bucket-progress { font-size: 13.5px; color: var(--ink-2); }
  .bucket-progress b { color: var(--accent); font-size: 16px; }
  .bucket-track { flex: 1; min-width: 140px; height: 6px; background: var(--line); border-radius: 999px; overflow: hidden; }
  .bucket-fill { height: 100%; background: linear-gradient(90deg, var(--accent), var(--accent-2)); border-radius: 999px; width: 0; transition: width 0.4s ease; }
  .bucket-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; }
  .bucket-item {
    display: flex;
    align-items: center;
    gap: 8px;
    border: 1px solid var(--line);
    border-radius: 12px;
    background: var(--card-bg);
    padding: 11px 13px;
    font-size: 13px;
    color: var(--ink-2);
    cursor: pointer;
    transition: all 0.18s ease;
    user-select: none;
  }
  .bucket-item:hover { border-color: var(--accent); transform: translateY(-2px); }
  .bucket-item .bk-check {
    width: 18px; height: 18px; flex: none;
    border: 1.5px solid var(--line);
    border-radius: 6px;
    display: flex; align-items: center; justify-content: center;
    color: transparent;
    transition: all 0.18s ease;
  }
  .bucket-item .bk-check svg { width: 11px; height: 11px; }
  .bucket-item.done { color: var(--ink); border-color: rgba(2,132,199,0.45); background: rgba(2,132,199,0.05); }
  .bucket-item.done .bk-check { background: var(--accent); border-color: var(--accent); color: #fff; }
  .bucket-item.done .bk-text { text-decoration: line-through; text-decoration-color: rgba(2,132,199,0.5); }
  @media (max-width: 900px) { .bucket-grid { grid-template-columns: repeat(2, 1fr); } }
  @media (max-width: 480px) { .bucket-grid { grid-template-columns: 1fr; } }
"""
if anchor in html:
    html = html.replace(anchor, add_css, 1); changed.append("css")
else:
    print("FAIL css")

# ============ 2. HTML：4 个 section（footer 前） ============
old_footer = """</section>


<footer>"""
if old_footer not in html:
    print("FAIL footer anchor")
    old_footer = None

new_sections = """</section>

<!-- 板块 6：开源仓库墙 -->
<section class="section" id="repos">
  <div class="wrap">
    <div class="section-head">
      <p class="kicker">OPEN SOURCE</p>
      <h2>开源仓库</h2>
      <p class="desc">最近活跃的仓库，数据实时来自 GitHub。</p>
    </div>
    <div class="repo-grid" id="repoGrid">
      <div class="repo-card">
        <div class="repo-name"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 .5C5.65.5.5 5.65.5 12c0 5.08 3.29 9.39 7.86 10.91.58.11.79-.25.79-.56 0-.27-.01-1.02-.02-2-3.2.7-3.88-1.54-3.88-1.54-.52-1.33-1.28-1.68-1.28-1.68-1.04-.71.08-.7.08-.7 1.15.08 1.76 1.18 1.76 1.18 1.02 1.75 2.69 1.25 3.35.95.1-.74.4-1.25.72-1.54-2.55-.29-5.23-1.28-5.23-5.68 0-1.26.45-2.28 1.18-3.09-.12-.29-.51-1.46.11-3.05 0 0 .96-.31 3.15 1.18a10.9 10.9 0 0 1 5.74 0c2.19-1.49 3.15-1.18 3.15-1.18.62 1.59.23 2.76.11 3.05.74.81 1.18 1.83 1.18 3.09 0 4.41-2.69 5.39-5.25 5.67.41.36.78 1.06.78 2.14 0 1.55-.01 2.79-.01 3.17 0 .31.21.68.8.56A10.52 10.52 0 0 0 23.5 12C23.5 5.65 18.35.5 12 .5Z"/></svg>正在读取仓库…</div>
        <div class="repo-desc">连接 GitHub API 中，稍等片刻。</div>
        <div class="repo-meta"><span><i class="lang-dot"></i>--</span><span>0 ★</span><span>0 ⑂</span></div>
      </div>
    </div>
  </div>
</section>

<!-- 板块 7：技能雷达图 -->
<section class="section alt" id="skills">
  <div class="wrap">
    <div class="section-head">
      <p class="kicker">SKILLS</p>
      <h2>擅长的事</h2>
      <p class="desc">六个方向的自我评估，图是画出来的，路是一点点走的。</p>
    </div>
    <div class="skill-wrap">
      <div class="radar-box">
        <svg id="radarSvg" viewBox="0 0 100 100" role="img" aria-label="技能雷达图"></svg>
      </div>
      <div class="skill-text">
        <h3>从校园工具到小游戏，什么都想试一试。</h3>
        <p>广播站系统、记账工具、代码生成器、棋类游戏……都是一个人从零写完的。爱折腾前端交互，也愿意沉下去做工具；会调音视频，也会为一个小游戏磨上几个晚上。</p>
        <div class="skill-bars" id="skillBars"></div>
      </div>
    </div>
  </div>
</section>

<!-- 板块 8：版本更新日志 -->
<section class="section" id="changelog">
  <div class="wrap">
    <div class="section-head">
      <p class="kicker">CHANGELOG</p>
      <h2>更新日志</h2>
      <p class="desc">这个页面是怎么一点点长成现在这样的。</p>
    </div>
    <div class="timeline">
      <div class="tl-time">2026-09-25</div>
      <div class="tl-axis"><span class="tl-dot now"></span></div>
      <div class="tl-item"><span class="tl-title">站点增强 v14</span><span class="tl-tag">当前</span><div class="tl-desc">RSS 订阅、访问计数、SEO 标签、作品展开预览、图标呼吸、今年进度环。</div></div>
      <div class="tl-time">2026-09-25</div>
      <div class="tl-axis"><span class="tl-dot"></span></div>
      <div class="tl-item"><span class="tl-title">此刻板块 v12</span><div class="tl-desc">时钟与天气独立成板块，新增翻牌时钟、节日飘浮与专属欢迎语。</div></div>
      <div class="tl-time">2026-09-24</div>
      <div class="tl-axis"><span class="tl-dot"></span></div>
      <div class="tl-item"><span class="tl-title">天气与纪念日 v9</span><div class="tl-desc">接入实时天气（Open-Meteo），纪念日倒计时上线。</div></div>
      <div class="tl-time">2026-09-22</div>
      <div class="tl-axis"><span class="tl-dot"></span></div>
      <div class="tl-item"><span class="tl-title">作品卡片 v3</span><div class="tl-desc">精选作品上架，支持下载与伪进度条进入。</div></div>
      <div class="tl-time">2026-09-19</div>
      <div class="tl-axis"><span class="tl-dot"></span></div>
      <div class="tl-item"><span class="tl-title">生活瞬间 v2</span><div class="tl-desc">瑞幸咖啡、网易云音乐、我的世界三块生活数据。</div></div>
      <div class="tl-time">2026-09-18</div>
      <div class="tl-axis"><span class="tl-dot"></span></div>
      <div class="tl-item"><span class="tl-title">站点上线 v1</span><div class="tl-desc">全世界语言的「欢迎你的到来」打字机欢迎页，部署到 GitHub Pages。</div></div>
    </div>
  </div>
</section>

<!-- 板块 9：人生清单 -->
<section class="section alt" id="bucket">
  <div class="wrap">
    <div class="section-head">
      <p class="kicker">BUCKET LIST</p>
      <h2>人生清单</h2>
      <p class="desc">想做的 100 件小事，完成一件，点亮一件。</p>
    </div>
    <div class="bucket-head">
      <span class="bucket-progress">已点亮 <b id="bkDone">0</b> / <b id="bkTotal">24</b> 件</span>
      <div class="bucket-track"><div class="bucket-fill" id="bkFill"></div></div>
    </div>
    <div class="bucket-grid" id="bucketGrid"></div>
  </div>
</section>


<footer>"""

if old_footer:
    html = html.replace(old_footer, new_sections, 1); changed.append("sections html")
else:
    print("FAIL sections")

# ============ 3. JS ============
tail = "  })();\n</script>"
add_js = """  })();

  /* ========== 开源仓库墙（GitHub API） ========== */
  (function () {
    var grid = document.getElementById('repoGrid');
    if (!grid) return;
    var fallback = [
      { name: 'Yaule-Rate.github.io', desc: '本站源码：全世界语言的欢迎页与个人标签页。', lang: 'HTML', stars: 0, forks: 0, updated: '2026-09-25', color: '#e34c26' }
    ];
    var langColor = { 'HTML': '#e34c26', 'CSS': '#563d7c', 'JavaScript': '#f1e05a', 'TypeScript': '#3178c6', 'Python': '#3572A5', 'Java': '#b07219', 'C++': '#f34b7d', 'C#': '#178600', 'PHP': '#4F5D95', 'Shell': '#89e051', 'Vue': '#41b883', 'Jupyter Notebook': '#DA5B0B', 'MDX': '#fcb32c' };
    function esc(s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
    function render(list) {
      if (!list || !list.length) list = fallback;
      var htmls = list.slice(0, 6).map(function (r) {
        var c = langColor[r.lang] || '#8b949e';
        var date = (r.updated || '').slice(0, 10);
        return '<div class="repo-card"><div class="repo-name"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 .5C5.65.5.5 5.65.5 12c0 5.08 3.29 9.39 7.86 10.91.58.11.79-.25.79-.56 0-.27-.01-1.02-.02-2-3.2.7-3.88-1.54-3.88-1.54-.52-1.33-1.28-1.68-1.28-1.68-1.04-.71.08-.7.08-.7 1.15.08 1.76 1.18 1.76 1.18 1.02 1.75 2.69 1.25 3.35.95.1-.74.4-1.25.72-1.54-2.55-.29-5.23-1.28-5.23-5.68 0-1.26.45-2.28 1.18-3.09-.12-.29-.51-1.46.11-3.05 0 0 .96-.31 3.15 1.18a10.9 10.9 0 0 1 5.74 0c2.19-1.49 3.15-1.18 3.15-1.18.62 1.59.23 2.76.11 3.05.74.81 1.18 1.83 1.18 3.09 0 4.41-2.69 5.39-5.25 5.67.41.36.78 1.06.78 2.14 0 1.55-.01 2.79-.01 3.17 0 .31.21.68.8.56A10.52 10.52 0 0 0 23.5 12C23.5 5.65 18.35.5 12 .5Z"/></svg>' + esc(r.name) + '</div><div class="repo-desc">' + esc(r.desc || '暂无简介') + '</div><div class="repo-meta"><span><i class="lang-dot" style="background:' + c + '"></i>' + esc(r.lang || '—') + '</span><span><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 17.27 18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/></svg>' + (r.stars || 0) + '</span><span><svg viewBox="0 0 24 24" fill="currentColor"><path d="M7 7h10v2H7zm0 4h10v2H7zm0 4h6v2H7zM4 21V3h16v18h-2V5H6v16H4z"/></svg>' + (r.forks || 0) + '</span><span class="repo-updated">' + date + '</span></div></div>';
      }).join('');
      grid.innerHTML = htmls;
    }
    var ctrl = ('AbortController' in window) ? new AbortController() : null;
    var timer = setTimeout(function () { if (ctrl) ctrl.abort(); }, 6000);
    fetch('https://api.github.com/users/Yaule-Rate/repos?sort=updated&per_page=6', ctrl ? { signal: ctrl.signal } : {})
      .then(function (r) { return r.json(); })
      .then(function (list) {
        clearTimeout(timer);
        if (!Array.isArray(list)) { render(fallback); return; }
        render(list.map(function (r) {
          return { name: r.name, desc: r.description, lang: r.language, stars: r.stargazers_count, forks: r.forks_count, updated: r.updated_at };
        }));
      })
      .catch(function () { clearTimeout(timer); render(fallback); });
  })();

  /* ========== 技能雷达图 ========== */
  (function () {
    var svg = document.getElementById('radarSvg');
    var bars = document.getElementById('skillBars');
    if (!svg) return;
    var skills = [
      { name: '前端开发', val: 8 },
      { name: '效率工具', val: 9 },
      { name: '音视频', val: 7 },
      { name: '游戏开发', val: 8 },
      { name: '界面设计', val: 6 },
      { name: '后端开发', val: 6 }
    ];
    var C = 50, R = 36;
    function pt(i, r) {
      var a = (i * 60 - 90) * Math.PI / 180;
      return (C + r * Math.cos(a)).toFixed(1) + ',' + (C + r * Math.sin(a)).toFixed(1);
    }
    var defs = '<defs><radialGradient id="radarGrad" cx="50%" cy="50%" r="70%"><stop offset="0%" stop-color="rgba(56,189,248,0.35)"/><stop offset="100%" stop-color="rgba(2,132,199,0.12)"/></radialGradient></defs>';
    var grid = '';
    for (var k = 1; k <= 4; k++) {
      var pts = [];
      for (var i = 0; i < 6; i++) pts.push(pt(i, R * k / 4));
      grid += '<polygon class="radar-grid-line" points="' + pts.join(' ') + '"/>';
    }
    var axes = '';
    for (var i2 = 0; i2 < 6; i2++) {
      axes += '<line class="radar-axis" x1="' + C + '" y1="' + C + '" x2="' + pt(i2, R).split(',')[0] + '" y2="' + pt(i2, R).split(',')[1] + '"/>';
    }
    var areaPts = [];
    for (var i3 = 0; i3 < 6; i3++) areaPts.push(pt(i3, R * skills[i3].val / 10));
    var area = '<polygon class="radar-area" points="' + areaPts.join(' ') + '" fill="url(#radarGrad)"/>';
    var dots = '';
    for (var i4 = 0; i4 < 6; i4++) {
      var dp = pt(i4, R * skills[i4].val / 10).split(',');
      dots += '<circle class="radar-dot" cx="' + dp[0] + '" cy="' + dp[1] + '" r="1.6"/>';
    }
    var labels = '';
    for (var i5 = 0; i5 < 6; i5++) {
      var a5 = (i5 * 60 - 90) * Math.PI / 180;
      var lx = C + (R + 9) * Math.cos(a5);
      var ly = C + (R + 9) * Math.sin(a5);
      labels += '<text class="radar-label" x="' + lx.toFixed(1) + '" y="' + ly.toFixed(1) + '" dominant-baseline="middle">' + skills[i5].name + '</text>';
    }
    svg.innerHTML = defs + grid + axes + area + dots + labels;
    if (bars) {
      bars.innerHTML = skills.map(function (s) {
        return '<div class="skill-bar-row"><span class="sb-name">' + s.name + '</span><span class="sb-track"><span class="sb-fill" data-w="' + (s.val * 10) + '"></span></span><span class="sb-num">' + s.val + '</span></div>';
      }).join('');
      setTimeout(function () {
        bars.querySelectorAll('.sb-fill').forEach(function (f) { f.style.width = f.getAttribute('data-w') + '%'; });
      }, 300);
    }
  })();

  /* ========== 人生清单 ========== */
  (function () {
    var grid = document.getElementById('bucketGrid');
    if (!grid) return;
    var items = ['去看一次现场演唱会', '看一场完整的日出', '学会弹一首完整的曲子', '写一本属于自己的小说', '跑一次五公里', '去一次西藏', '给爸妈买一份大礼物', '养一盆活过一年的绿植', '亲手做一顿年夜饭', '学会一门新的外语', '看一次极光', '独自去一座陌生城市旅行', '学会做咖啡拉花', '给十年后的自己写一封信', '种一棵属于自己的树', '养一只猫', '跳一次伞', '读完《三国演义》', '做一次公益志愿者', '发一张自己的专辑', '开一家小店', '通宵看一次流星雨', '把房间布置成喜欢的样子', '拍一支 Vlog 记录一天'];
    var KEY = 'yaule_bucket';
    var done = {};
    try { done = JSON.parse(localStorage.getItem(KEY) || '{}') || {}; } catch (e) {}
    var doneN = document.getElementById('bkDone');
    var totalN = document.getElementById('bkTotal');
    var fill = document.getElementById('bkFill');
    function refresh() {
      var n = 0;
      grid.querySelectorAll('.bucket-item').forEach(function (el) {
        if (el.classList.contains('done')) n++;
      });
      if (doneN) doneN.textContent = n;
      if (totalN) totalN.textContent = items.length;
      if (fill) fill.style.width = (n / items.length * 100) + '%';
    }
    grid.innerHTML = items.map(function (t, idx) {
      var on = done[idx];
      return '<div class="bucket-item' + (on ? ' done' : '') + '" data-i="' + idx + '" role="button" tabindex="0"><span class="bk-check"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg></span><span class="bk-text">' + t + '</span></div>';
    }).join('');
    grid.addEventListener('click', function (e) {
      var item = e.target.closest('.bucket-item');
      if (!item) return;
      var i = item.getAttribute('data-i');
      item.classList.toggle('done');
      done[i] = item.classList.contains('done') ? 1 : 0;
      try { localStorage.setItem(KEY, JSON.stringify(done)); } catch (err) {}
      refresh();
    });
    grid.addEventListener('keydown', function (e) {
      if ((e.key === 'Enter' || e.key === ' ') && e.target.classList.contains('bucket-item')) {
        e.preventDefault();
        e.target.click();
      }
    });
    refresh();
  })();
</script>"""
if tail in html:
    html = html.replace(tail, add_js, 1); changed.append("js")
else:
    print("FAIL js")

open(path, "w", encoding="utf-8").write(html)
print("CHANGED:", changed)
