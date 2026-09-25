# -*- coding: utf-8 -*-
"""v22.2 脚本 A：head(og/twitter 大图 + hreflang + JSON-LD) + 深夜元素 + 热力图/留言板板块 + CSS"""
p = "index.html"
s = open(p, encoding="utf-8").read()
OPS = []
def rep(o, n, t):
    OPS.append((o, n, t))

# ---- 1. head：og:image / twitter 大图 + hreflang + JSON-LD ----
rep("""<link rel="canonical" href="https://Yaule-Rate.github.io/">
<link rel="alternate" type="application/atom+xml" title="Yaule 的个人空间" href="https://Yaule-Rate.github.io/atom.xml">""",
    """<link rel="canonical" href="https://Yaule-Rate.github.io/">
<link rel="alternate" type="application/atom+xml" title="Yaule 的个人空间" href="https://Yaule-Rate.github.io/atom.xml">
<link rel="alternate" hreflang="zh-CN" href="https://Yaule-Rate.github.io/">
<link rel="alternate" hreflang="en" href="https://Yaule-Rate.github.io/?lang=en">
<link rel="alternate" hreflang="x-default" href="https://Yaule-Rate.github.io/">""", "hreflang")
rep("""<meta property="og:locale" content="zh_CN">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="Yaule · 欢迎你的到来">
<meta name="twitter:description" content="欢迎来到 Yaule 的个人主页。这里记录着咖啡、音乐、游戏与作品。">""",
    """<meta property="og:locale" content="zh_CN">
<meta property="og:image" content="https://Yaule-Rate.github.io/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Yaule · 失眠夜空间 · 个人主页">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Yaule · 欢迎你的到来">
<meta name="twitter:description" content="欢迎来到 Yaule 的个人主页。这里记录着咖啡、音乐、游戏与作品。">
<meta name="twitter:image" content="https://Yaule-Rate.github.io/og-image.png">""", "og/twitter 大图")
rep("""<link rel="stylesheet" href="https://miaoda.feishu.cn/fonts/css2?family=Noto+Serif+SC:wght@600;700&family=Noto+Sans+SC:wght@400;500;600;700&family=Ma+Shan+Zheng&display=swap">""",
    """<link rel="stylesheet" href="https://miaoda.feishu.cn/fonts/css2?family=Noto+Serif+SC:wght@600;700&family=Noto+Sans+SC:wght@400;500;600;700&family=Ma+Shan+Zheng&display=swap">
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"WebSite","name":"Yaule 失眠夜空间","alternateName":"Yaule-Rate.github.io","url":"https://Yaule-Rate.github.io/","inLanguage":["zh-CN","en"],"publisher":{"@type":"Person","name":"Yaule","url":"https://github.com/Yaule-Rate","email":"1957784559@qq.com"},"potentialAction":{"@type":"SearchAction","target":"https://Yaule-Rate.github.io/?q={search_term_string}","query-input":"required name=search_term_string"}}
</script>""", "JSON-LD")

# ---- 2. body 深夜元素（月亮 + 星空） ----
rep("""<body>
<!-- 开屏简笔画：青色 Y 一笔画 + Yaule -->""",
    """<body>
<!-- 深夜特调：月亮 + 星空（22:00-06:00 显示） -->
<div class="night-sky" id="nightSky" aria-hidden="true"></div>
<div class="night-moon" id="nightMoon" aria-hidden="true"><svg viewBox="0 0 64 64" fill="currentColor"><path d="M40.6 4a30 30 0 1 0 19.4 28.2A26.5 26.5 0 0 1 40.6 4z"/></svg></div>
<!-- 开屏简笔画：青色 Y 一笔画 + Yaule -->""", "深夜元素")

# ---- 3. 贡献热力图板块（repos 后） ----
rep("""    </div>
  </div>
</section>

<!-- 板块 7：技能雷达图 -->""",
    """    </div>
  </div>
</section>

<!-- 板块 6.5：开源足迹 · GitHub 贡献热力图 -->
<section class="section alt" id="heatmap">
  <div class="wrap">
    <div class="section-head">
      <p class="kicker">CONTRIBUTIONS</p>
      <h2 data-i18n="heatmap.h2">开源足迹</h2>
      <p class="desc" data-i18n="heatmap.desc">过去一年在 GitHub 上的每一天，青色越深代表越活跃。</p>
    </div>
    <div class="hm-wrap">
      <div class="hm-grid" id="hmGrid"></div>
      <p class="hm-total" id="hmTotal"></p>
    </div>
  </div>
</section>

<!-- 板块 7：技能雷达图 -->""", "热力图板块")

# ---- 4. 留言板板块（changelog 后 bucket 前） ----
rep("""    <div class="vs-log" id="mcLog"></div>
  </div>
</section>

<section class="section alt" id="bucket">""",
    """    <div class="vs-log" id="mcLog"></div>
  </div>
</section>

<!-- 板块 8.5：访客留言板（GitHub Issues 驱动，防注入 + 违禁词过滤） -->
<section class="section alt" id="guestbook">
  <div class="wrap">
    <div class="section-head">
      <p class="kicker">GUESTBOOK</p>
      <h2 data-i18n="guestbook.h2">访客留言板</h2>
      <p class="desc" data-i18n="guestbook.desc">来过的人都可以留下一句话。提交后跳转 GitHub 确认，内容同步显示在这里。</p>
    </div>
    <div class="gb-wrap">
      <form class="gb-form" id="gbForm">
        <input type="text" id="gbName" maxlength="20" autocomplete="nickname" data-i18n="guestbook.name" data-i18n-ph="guestbook.name">
        <textarea id="gbText" maxlength="300" rows="3" data-i18n="guestbook.text" data-i18n-ph="guestbook.text"></textarea>
        <button type="submit" id="gbSubmit" data-i18n="guestbook.submit">写下留言</button>
      </form>
      <p class="gb-hint" id="gbHint"></p>
      <div class="gb-list" id="gbList">
        <p class="gb-load" data-i18n="guestbook.load">正在读取留言…</p>
      </div>
    </div>
  </div>
</section>

<section class="section alt" id="bucket">""", "留言板板块")

# ---- 5. CSS（</style> 前） ----
rep("""  .now-reco .reco-tag { margin-top: 12px; font-size: 12px; color: var(--accent); letter-spacing: .08em; }
</style>""",
    """  .now-reco .reco-tag { margin-top: 12px; font-size: 12px; color: var(--accent); letter-spacing: .08em; }

  /* ===== 贡献热力图 ===== */
  .hm-wrap { display: flex; flex-direction: column; gap: 14px; }
  .hm-grid { display: grid; grid-template-columns: repeat(53, 1fr); gap: 3px; }
  .hm-cell { aspect-ratio: 1; border-radius: 3px; background: var(--soft); }
  .hm-cell.l0 { background: var(--soft); }
  .hm-cell.l1 { background: #bae6fd; }
  .hm-cell.l2 { background: #7dd3fc; }
  .hm-cell.l3 { background: #38bdf8; }
  .hm-cell.l4 { background: #0284c7; }
  :root[data-theme="dark"] .hm-cell.l0 { background: #23262b; }
  .hm-total { font-size: 13px; color: var(--ink-2); }

  /* ===== 访客留言板 ===== */
  .gb-wrap { max-width: 720px; }
  .gb-form { display: flex; flex-direction: column; gap: 10px; margin-bottom: 10px; }
  .gb-form input, .gb-form textarea {
    width: 100%; padding: 11px 14px; border-radius: 10px; border: 1px solid var(--line);
    background: var(--card-bg); color: var(--ink); font: inherit; box-sizing: border-box;
  }
  .gb-form input:focus, .gb-form textarea:focus { outline: none; border-color: var(--accent); box-shadow: 0 0 0 3px rgba(2,132,199,.12); }
  .gb-form button {
    align-self: flex-start; padding: 9px 22px; border: 0; border-radius: 10px; cursor: pointer;
    background: var(--accent); color: #fff; font: inherit; font-weight: 600; transition: transform .15s ease, opacity .15s ease;
  }
  .gb-form button:hover { transform: translateY(-1px); }
  .gb-form button:disabled { opacity: .5; cursor: not-allowed; transform: none; }
  .gb-hint { min-height: 18px; font-size: 12px; color: var(--accent); margin-bottom: 4px; }
  .gb-hint.err { color: #dc2626; }
  .gb-list { display: flex; flex-direction: column; gap: 10px; }
  .gb-item { padding: 12px 16px; border: 1px solid var(--line); border-radius: 12px; background: var(--card-bg); }
  .gb-item .gb-head { display: flex; align-items: center; gap: 8px; font-size: 12px; color: var(--ink-2); margin-bottom: 6px; }
  .gb-item .gb-head b { color: var(--accent); }
  .gb-item .gb-body { font-size: 14px; line-height: 1.7; color: var(--ink); word-break: break-word; white-space: pre-wrap; }
  .gb-load, .gb-empty { font-size: 13px; color: var(--ink-2); }

  /* ===== 深夜特调 ===== */
  .night-sky { position: fixed; inset: 0; z-index: 1; pointer-events: none; overflow: hidden; }
  .night-star {
    position: absolute; width: 3px; height: 3px; border-radius: 50%;
    background: #7dd3fc; opacity: 0;
    animation: nightTwinkle 3.2s ease-in-out infinite;
  }
  @keyframes nightTwinkle { 0%, 100% { opacity: 0; } 50% { opacity: .9; } }
  .night-moon {
    position: fixed; top: 76px; right: 34px; z-index: 1; pointer-events: none;
    color: #f8fafc; width: 44px; height: 44px; opacity: 0; transition: opacity .8s ease;
    filter: drop-shadow(0 0 14px rgba(56,189,248,.55));
  }
  body.night .night-moon { opacity: 1; }
  .section, footer { position: relative; z-index: 2; }
</style>""", "CSS 新板块 + 深夜")

bad = [(t, s.count(o)) for (o, _, t) in OPS if s.count(o) != 1]
if bad:
    for t, c in bad:
        print("锚点失败(%d): %s" % (c, t))
    raise SystemExit(1)
for (o, n, t) in OPS:
    s = s.replace(o, n, 1)
open(p, "w", encoding="utf-8").write(s)
print("A ok:", len(OPS))
