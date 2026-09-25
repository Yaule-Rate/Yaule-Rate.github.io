# -*- coding: utf-8 -*-
"""index.html：整站 i18n（中英切换 + 3 秒伪进度条）+ 此刻区每日推荐"""
import io

p = "index.html"
s = io.open(p, encoding="utf-8").read()
n0 = len(s)
log = []

def rep(old, new, tag, must=True):
    global s
    if old not in s:
        if must:
            raise SystemExit("未找到锚点: " + tag)
        print("WARN 跳过(未找到):", tag); return
    s = s.replace(old, new, 1)
    log.append(tag)

# ============ A. CSS 注入 ============
CSS = """
  /* ===== 语言切换按钮（右上角） ===== */
  .lang-toggle {
    position: fixed; top: 18px; right: 72px; z-index: 10001;
    height: 44px; padding: 0 14px; border-radius: 999px;
    border: 1px solid var(--line); background: var(--card-bg); color: var(--ink);
    display: flex; align-items: center; gap: 7px;
    cursor: pointer; font-size: 13px; font-weight: 700; font-family: inherit;
    box-shadow: 0 2px 10px rgba(0,0,0,0.06);
    transition: background .25s, color .25s, transform .2s, box-shadow .25s;
  }
  .lang-toggle:hover { transform: scale(1.06); }
  .lang-toggle svg { width: 17px; height: 17px; color: var(--accent); }
  .lang-toggle #langLabel { min-width: 22px; text-align: center; }

  /* ===== 语言切换 3 秒伪进度条 ===== */
  .lang-loader {
    position: fixed; inset: 0; z-index: 10050;
    background: var(--bg);
    display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 20px;
    opacity: 0; pointer-events: none; transition: opacity .3s;
  }
  .lang-loader.active { opacity: 1; pointer-events: auto; }
  .lang-loader .splash-y { width: 76px; height: 76px; }
  .lang-loader .y-path { stroke-dasharray: 340; stroke-dashoffset: 340; animation: ydraw 1s ease forwards; }
  @keyframes ydraw { to { stroke-dashoffset: 0; } }
  .lang-loader-tip { font-size: 14px; color: var(--ink-2); letter-spacing: .12em; }
  .lang-bar { width: 240px; height: 4px; border-radius: 999px; background: var(--soft); overflow: hidden; }
  .lang-bar-fill { height: 100%; width: 0%; border-radius: 999px; background: linear-gradient(90deg, var(--accent), var(--accent-2)); }

  /* ===== 此刻 · 每日推荐卡 ===== */
  .now-reco { grid-column: 1 / -1; min-height: 130px; }
  .now-reco .reco-head { display: flex; align-items: center; gap: 8px; font-size: 12px; letter-spacing: .14em; color: var(--ink-2); text-transform: uppercase; }
  .now-reco .reco-head svg { width: 15px; height: 15px; color: var(--accent); }
  .now-reco .reco-text { margin-top: 16px; font-size: clamp(16px, 2.6vw, 21px); line-height: 1.75; font-weight: 600; color: var(--ink); }
  .now-reco .reco-tag { margin-top: 12px; font-size: 12px; color: var(--accent); letter-spacing: .08em; }
"""
idx = s.rfind("</style>")
assert idx != -1, "无 </style>"
s = s[:idx] + CSS + s[idx:]

# ============ B. HTML 注入 ============
# B1. 语言切换按钮（theme-toggle 前）
LANG_BTN = """<button class="lang-toggle" id="langToggle" title="切换语言" aria-label="切换语言">
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>
  <span id="langLabel">中</span>
</button>
"""
rep('<button class="theme-toggle" id="themeToggle"', LANG_BTN + '<button class="theme-toggle" id="themeToggle"', "langToggle 按钮")

# B2. 语言切换 3 秒伪进度条遮罩（toast 前）
LANG_LOADER = """<div class="lang-loader" id="langLoader" aria-hidden="true">
  <svg class="splash-y" viewBox="0 0 100 100" fill="none" stroke-linecap="round" stroke-linejoin="round">
    <path class="y-path" pathLength="100" d="M22 30 L50 52 L78 30 L50 52 L50 78" stroke="var(--accent)" stroke-width="6"/>
  </svg>
  <p class="lang-loader-tip" id="langLoaderTip">正在切换语言…</p>
  <div class="lang-bar"><div class="lang-bar-fill" id="langBarFill"></div></div>
</div>
"""
rep('<div class="toast" id="toast"></div>', LANG_LOADER + '<div class="toast" id="toast"></div>', "langLoader 遮罩")

# B3. 此刻 · 每日推荐卡（now-weather 前）
RECO_CARD = """      <div class="now-card now-reco">
        <p class="reco-head">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.83z"/><line x1="7" y1="7" x2="7.01" y2="7"/></svg>
          <span data-i18n="now.reco">今日推荐</span>
        </p>
        <p class="reco-text" id="recoText">正在挑选今日推荐…</p>
        <p class="reco-tag" id="recoTag"></p>
      </div>

"""
rep('      <div class="now-card now-weather">', RECO_CARD + '      <div class="now-card now-weather">', "每日推荐卡")

# ============ C. data-i18n 标记 ============
rep('<p class="intro" id="intro">这里是我的个人小角落，记录着咖啡、音乐、游戏与作品。不紧不慢，慢慢翻就好。</p>',
    '<p class="intro" id="intro" data-i18n="hero.intro">这里是我的个人小角落，记录着咖啡、音乐、游戏与作品。不紧不慢，慢慢翻就好。</p>', "hero.intro")
rep('<p class="scroll-hint" id="scrollHint">向下滑动 <span class="arrow">↓</span></p>',
    '<p class="scroll-hint" id="scrollHint"><span data-i18n="hero.scroll">向下滑动</span> <span class="arrow">↓</span></p>', "hero.scroll")

rep('<p class="kicker">PERSONAL SPACE</p>', '<p class="kicker" data-i18n="enter.kicker">PERSONAL SPACE</p>', "enter.kicker")
rep('<h2>失眠夜 · 个人空间</h2>', '<h2 data-i18n="enter.h2">失眠夜 · 个人空间</h2>', "enter.h2")
rep('<p class="desc">这里收纳着关于我的一切——爱好的碎片、写过的项目、走过的路，还有一些零零散散的日常。</p>',
    '<p class="desc" data-i18n="enter.desc">这里收纳着关于我的一切——爱好的碎片、写过的项目、走过的路，还有一些零零散散的日常。</p>', "enter.desc")
rep('<a class="btn-enter" href="space.html" data-loading="正在进入个人空间">\n      进入个人空间\n      <span>→</span>',
    '<a class="btn-enter" href="space.html" data-loading="正在进入个人空间">\n      <span data-i18n="enter.btn">进入个人空间</span>\n      <span>→</span>', "enter.btn")

rep('<h2>生活瞬间</h2>', '<h2 data-i18n="life.h2">生活瞬间</h2>', "life.h2")
rep('<p class="desc">一些悄悄累积的数字，随时间慢慢长大。点击上方切换。</p>',
    '<p class="desc" data-i18n="life.desc">一些悄悄累积的数字，随时间慢慢长大。点击上方切换。</p>', "life.desc")
rep('<button class="life-tab active" data-life="coffee" role="tab">咖啡</button>',
    '<button class="life-tab active" data-life="coffee" role="tab" data-i18n="life.tab1">咖啡</button>', "life.tab1")
rep('<button class="life-tab" data-life="music" role="tab">音乐</button>',
    '<button class="life-tab" data-life="music" role="tab" data-i18n="life.tab2">音乐</button>', "life.tab2")
rep('<button class="life-tab" data-life="game" role="tab">游戏</button>',
    '<button class="life-tab" data-life="game" role="tab" data-i18n="life.tab3">游戏</button>', "life.tab3")

rep('<h2>精选作品</h2>', '<h2 data-i18n="works.h2">精选作品</h2>', "works.h2")
rep('<p class="desc">从校园工具到游戏辅助，都是一点点写出来的小玩意。点卡片打开，点右上角下载。</p>',
    '<p class="desc" data-i18n="works.desc">从校园工具到游戏辅助，都是一点点写出来的小玩意。点卡片打开，点右上角下载。</p>', "works.desc")
rep('<button class="btn-more" id="btnMore">查看更多 ↓</button>',
    '<button class="btn-more" id="btnMore" data-i18n="works.more">查看更多 ↓</button>', "works.more")

rep('<h2>纪念日</h2>', '<h2 data-i18n="anniv.h2">纪念日</h2>', "anniv.h2")
rep('<p class="desc">有些日子值得被记住，有些时间悄悄在走。</p>',
    '<p class="desc" data-i18n="anniv.desc">有些日子值得被记住，有些时间悄悄在走。</p>', "anniv.desc")

rep('<h2>此刻</h2>', '<h2 data-i18n="now.h2">此刻</h2>', "now.h2")
rep('<p class="desc">时间与天气，都在悄悄走。</p>',
    '<p class="desc" data-i18n="now.desc">时间与天气，都在悄悄走。</p>', "now.desc")
rep('<span class="ring-label">天 · 2026 还剩</span>',
    '<span class="ring-label" data-i18n="now.ring">天 · 2026 还剩</span>', "now.ring")
rep('<p class="ring-foot"><b id="yearPctText">今年已过 --%</b></p>',
    '<p class="ring-foot"><b><span data-i18n="now.ringfoot">今年已过</span> <span id="yearPctText">--%</span></b></p>', "now.ringfoot")
rep('<div class="wd-label">体感</div>', '<div class="wd-label" data-i18n="now.w1">体感</div>', "now.w1")
rep('<div class="wd-label">湿度</div>', '<div class="wd-label" data-i18n="now.w2">湿度</div>', "now.w2")
rep('<div class="wd-label">风速</div>', '<div class="wd-label" data-i18n="now.w3">风速</div>', "now.w3")
rep('<div class="wd-label">紫外线</div>', '<div class="wd-label" data-i18n="now.w4">紫外线</div>', "now.w4")

rep('<h2>开源仓库</h2>', '<h2 data-i18n="repos.h2">开源仓库</h2>', "repos.h2")
rep('<p class="desc">最近活跃的仓库，数据实时来自 GitHub。</p>',
    '<p class="desc" data-i18n="repos.desc">最近活跃的仓库，数据实时来自 GitHub。</p>', "repos.desc")

rep('<h2>擅长的事</h2>', '<h2 data-i18n="skills.h2">擅长的事</h2>', "skills.h2")
rep('<p class="desc">六个方向的自我评估，图是画出来的，路是一点点走的。</p>',
    '<p class="desc" data-i18n="skills.desc">六个方向的自我评估，图是画出来的，路是一点点走的。</p>', "skills.desc")

rep('<h2>更新日志</h2>', '<h2 data-i18n="changelog.h2">更新日志</h2>', "changelog.h2")
rep('<p class="desc">这个页面是怎么一点点长成现在这样的。</p>',
    '<p class="desc" data-i18n="changelog.desc">这个页面是怎么一点点长成现在这样的。</p>', "changelog.desc")
rep('        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>\n        详细日志\n      </a>',
    '        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>\n        <span data-i18n="changelog.more">详细日志</span>\n      </a>', "changelog.more")

rep('<h2>人生清单</h2>', '<h2 data-i18n="bucket.h2">人生清单</h2>', "bucket.h2")
rep('<p class="desc">想做的 100 件小事，完成一件，点亮一件。</p>',
    '<p class="desc" data-i18n="bucket.desc">想做的 100 件小事，完成一件，点亮一件。</p>', "bucket.desc")

rep('<p>个人空间入口：这里收录我的作品与项目，全部开源托管在 GitHub 上。</p>',
    '<p data-i18n="footer.brand">个人空间入口：这里收录我的作品与项目，全部开源托管在 GitHub 上。</p>', "footer.brand")
rep('<h4>导航</h4>', '<h4 data-i18n="footer.nav">导航</h4>', "footer.nav")
rep('<h4>作品</h4>', '<h4 data-i18n="footer.works">作品</h4>', "footer.works")
rep('<h4>联系</h4>', '<h4 data-i18n="footer.contact">联系</h4>', "footer.contact")
rep('<li><a href="#hero">首页</a></li>', '<li><a href="#hero" data-i18n="footer.home">首页</a></li>', "footer.home")
rep('<li><a href="space.html">个人空间</a></li>', '<li><a href="space.html" data-i18n="footer.space">个人空间</a></li>', "footer.space")
rep('<li><a href="#works">项目</a></li>', '<li><a href="#works" data-i18n="footer.projects">项目</a></li>', "footer.projects")
rep('<li><a href="#life">生活数据</a></li>', '<li><a href="#life" data-i18n="footer.lifedata">生活数据</a></li>', "footer.lifedata")
rep('<li><a href="space.html">失眠夜个人空间</a></li>', '<li><a href="space.html" data-i18n="footer.space2">失眠夜个人空间</a></li>', "footer.space2")
rep('<li><a href="space.html#awards">荣誉奖项</a></li>', '<li><a href="space.html#awards" data-i18n="footer.awards">荣誉奖项</a></li>', "footer.awards")
rep('<li><a href="space.html#contact">联系我</a></li>', '<li><a href="space.html#contact" data-i18n="footer.contactme">联系我</a></li>', "footer.contactme")
rep('<li><a href="mailto:1957784559@qq.com">邮箱</a></li>', '<li><a href="mailto:1957784559@qq.com" data-i18n="footer.email">邮箱</a></li>', "footer.email")
rep('<li><a href="atom.xml">RSS 订阅</a></li>', '<li><a href="atom.xml" data-i18n="footer.rss">RSS 订阅</a></li>', "footer.rss")

# ============ D. 数据透出：节日 / 天气 ============
rep("        if (!matched) return;",
    "        window.__festNow = matched ? matched.name : null;\n        if (!matched) return;", "节日透出")
rep("        var c = d.current;\n        icon.innerHTML = svgFor(c.weather_code);",
    "        var c = d.current;\n        window.__wCode = c.weather_code;\n        icon.innerHTML = svgFor(c.weather_code);", "天气透出")

# ============ E. 动态文本双语 ============
rep("      el.innerHTML = '已停留 <b>' + m + '</b> 分 <b>' + s + '</b> 秒';",
    "      el.innerHTML = (window.YAULE_LANG === 'en')\n        ? 'Stayed <b>' + m + '</b> min <b>' + s + '</b> sec'\n        : '已停留 <b>' + m + '</b> 分 <b>' + s + '</b> 秒';", "stayTime 双语")
rep("    el.innerHTML = '今日幸运 <b style=\"color:' + c[0] + '\">' + lucky + '</b> · ' + c[1] + ' ' + tip;",
    "    el.innerHTML = (window.YAULE_LANG === 'en'\n      ? 'Today\\'s luck <b style=\"color:' + c[0] + '\">' + lucky + '</b> · ' + c[1] + ' ' + tip\n      : '今日幸运 <b style=\"color:' + c[0] + '\">' + lucky + '</b> · ' + c[1] + ' ' + tip);", "lucky 双语")

# ============ F. JS 注入（i18n 引擎 + 每日推荐） ============
JS = r"""
  /* ========== 整站 i18n：中英切换（3 秒伪进度条） ========== */
  var I18N = {
    zh: {
      'hero.intro': '这里是我的个人小角落，记录着咖啡、音乐、游戏与作品。不紧不慢，慢慢翻就好。',
      'hero.scroll': '向下滑动',
      'enter.kicker': 'PERSONAL SPACE',
      'enter.h2': '失眠夜 · 个人空间',
      'enter.desc': '这里收纳着关于我的一切——爱好的碎片、写过的项目、走过的路，还有一些零零散散的日常。',
      'enter.btn': '进入个人空间',
      'life.h2': '生活瞬间', 'life.desc': '一些悄悄累积的数字，随时间慢慢长大。点击上方切换。',
      'life.tab1': '咖啡', 'life.tab2': '音乐', 'life.tab3': '游戏',
      'works.h2': '精选作品', 'works.desc': '从校园工具到游戏辅助，都是一点点写出来的小玩意。点卡片打开，点右上角下载。', 'works.more': '查看更多 ↓',
      'anniv.h2': '纪念日', 'anniv.desc': '有些日子值得被记住，有些时间悄悄在走。',
      'now.h2': '此刻', 'now.desc': '时间与天气，都在悄悄走。', 'now.reco': '今日推荐',
      'now.ring': '天 · 2026 还剩', 'now.ringfoot': '今年已过',
      'now.w1': '体感', 'now.w2': '湿度', 'now.w3': '风速', 'now.w4': '紫外线',
      'repos.h2': '开源仓库', 'repos.desc': '最近活跃的仓库，数据实时来自 GitHub。',
      'skills.h2': '擅长的事', 'skills.desc': '六个方向的自我评估，图是画出来的，路是一点点走的。',
      'changelog.h2': '更新日志', 'changelog.desc': '这个页面是怎么一点点长成现在这样的。', 'changelog.more': '详细日志',
      'bucket.h2': '人生清单', 'bucket.desc': '想做的 100 件小事，完成一件，点亮一件。',
      'footer.brand': '个人空间入口：这里收录我的作品与项目，全部开源托管在 GitHub 上。',
      'footer.nav': '导航', 'footer.home': '首页', 'footer.space': '个人空间', 'footer.projects': '项目', 'footer.lifedata': '生活数据',
      'footer.works': '作品', 'footer.space2': '失眠夜个人空间', 'footer.awards': '荣誉奖项', 'footer.contactme': '联系我',
      'footer.contact': '联系', 'footer.email': '邮箱', 'footer.rss': 'RSS 订阅'
    },
    en: {
      'hero.intro': 'This is my little corner — coffee, music, games and works. Take it slow.',
      'hero.scroll': 'Scroll down',
      'enter.kicker': 'PERSONAL SPACE',
      'enter.h2': 'Insomnia Night · My Space',
      'enter.desc': "Everything about me — hobby fragments, projects I've written, roads I've walked, and bits of everyday life.",
      'enter.btn': 'Enter My Space',
      'life.h2': 'Life Moments', 'life.desc': 'Numbers that quietly grow with time. Click to switch.',
      'life.tab1': 'Coffee', 'life.tab2': 'Music', 'life.tab3': 'Games',
      'works.h2': 'Featured Works', 'works.desc': 'From campus tools to game aids — little things written one by one. Click a card to open, click download top-right.', 'works.more': 'View More ↓',
      'anniv.h2': 'Anniversaries', 'anniv.desc': 'Some days are worth remembering; some time quietly passes.',
      'now.h2': 'Right Now', 'now.desc': 'Time and weather, quietly passing.', 'now.reco': "Today's Pick",
      'now.ring': 'days left in 2026', 'now.ringfoot': 'of 2026 used',
      'now.w1': 'Feels', 'now.w2': 'Humidity', 'now.w3': 'Wind', 'now.w4': 'UV',
      'repos.h2': 'Open Source', 'repos.desc': 'Recently active repos, live from GitHub.',
      'skills.h2': "What I'm Good At", 'skills.desc': 'Self-assessment in six directions — drawn as a chart, built step by step.',
      'changelog.h2': 'Changelog', 'changelog.desc': 'How this page grew into what it is today.', 'changelog.more': 'Full Log',
      'bucket.h2': 'Bucket List', 'bucket.desc': '100 little things I want to do — done one, lit one.',
      'footer.brand': 'Entry to my space: my works and projects, all open-sourced on GitHub.',
      'footer.nav': 'Navigate', 'footer.home': 'Home', 'footer.space': 'My Space', 'footer.projects': 'Projects', 'footer.lifedata': 'Life Data',
      'footer.works': 'Works', 'footer.space2': 'Insomnia Night Space', 'footer.awards': 'Awards', 'footer.contactme': 'Contact',
      'footer.contact': 'Contact', 'footer.email': 'Email', 'footer.rss': 'RSS Feed'
    }
  };
  function getLang() {
    try { return localStorage.getItem('yaule_lang') === 'en' ? 'en' : 'zh'; } catch (e) { return 'zh'; }
  }
  function setLang(l) {
    try { localStorage.setItem('yaule_lang', l); } catch (e) {}
  }
  function applyLang() {
    var L = getLang();
    window.YAULE_LANG = L;
    document.documentElement.lang = L === 'en' ? 'en' : 'zh-CN';
    document.querySelectorAll('[data-i18n]').forEach(function (el) {
      var k = el.getAttribute('data-i18n');
      if (I18N[L] && I18N[L][k]) el.textContent = I18N[L][k];
    });
    var lb = document.getElementById('langLabel');
    if (lb) lb.textContent = L === 'en' ? 'EN' : '中';
    var st = document.getElementById('stayTime');
    if (st) st.innerHTML = L === 'en' ? 'Stayed 0 min 0 sec' : '已停留 0 分 0 秒';
    window.dispatchEvent(new CustomEvent('yaule-langchange'));
  }
  var langBusy = false;
  function switchLang() {
    if (langBusy) return;
    langBusy = true;
    var next = getLang() === 'en' ? 'zh' : 'en';
    var loader = document.getElementById('langLoader');
    var fill = document.getElementById('langBarFill');
    var tip = document.getElementById('langLoaderTip');
    if (!loader || !fill) { langBusy = false; return; }
    loader.classList.add('active');
    fill.style.width = '0%';
    if (tip) tip.textContent = next === 'en' ? '正在切换语言…' : 'Switching language…';
    var p = 0;
    var t = setInterval(function () {
      p += Math.random() * 6.5;
      if (p > 90) p = 90;
      fill.style.width = p + '%';
    }, 90);
    setTimeout(function () {
      clearInterval(t);
      fill.style.width = '100%';
      setTimeout(function () {
        setLang(next);
        applyLang();
        loader.classList.remove('active');
        langBusy = false;
      }, 420);
    }, 3000);
  }
  document.addEventListener('DOMContentLoaded', function () {
    var btn = document.getElementById('langToggle');
    if (btn) btn.addEventListener('click', switchLang);
    applyLang();
  });

  /* ========== 每日推荐（此刻区）：节日 > 天气 > 星期 > 随机，每天固定 ========== */
  (function () {
    var el = document.getElementById('recoText');
    if (!el) return;
    var tagEl = document.getElementById('recoTag');
    var RECO = {
      zh: [
        '喝杯咖啡，看看窗外。', '写几行代码，或删掉几行。', '整理一下桌面和房间。',
        '读几页书，慢一点。', '听一首老歌，单曲循环。', '给老朋友发条消息。',
        '早一点睡，明天会更好。', '出门走一走，吹吹风。', '学一个没用的冷知识。',
        '把相册翻到去年今天。', '给自己泡杯热茶。', '在清单上点亮一件事。'
      ],
      en: [
        'Have a coffee, watch the window.', 'Write some code — or delete some.', 'Tidy up your desk and room.',
        'Read a few pages, slowly.', 'Put on an old song on repeat.', 'Message an old friend.',
        'Sleep early — tomorrow is better.', 'Step out and feel the breeze.', 'Learn a useless fun fact.',
        'Flip your photos to this day last year.', 'Brew yourself a warm tea.', 'Tick one thing off your list.'
      ]
    };
    var FEST = {
      zh: {
        '春节': '今天春节，把新年的第一句祝福送给身边的人。', '除夕': '除夕夜，好好吃顿年夜饭。',
        '元宵节': '元宵节，记得吃碗汤圆。', '清明节': '清明时节，出去踏踏青。',
        '劳动节': '劳动节快乐，今天你最大。', '端午节': '端午安康，吃个粽子吧。',
        '中秋节': '中秋快乐，今晚的月亮借你一半。', '国庆节': '国庆快乐，出门看看山河。'
      },
      en: {
        '春节': "It's Spring Festival — share your first wish of the year.",
        '除夕': "New Year's Eve — enjoy a proper family dinner.",
        '元宵节': 'Lantern Festival — grab a bowl of tangyuan.',
        '清明节': 'Qingming — take a spring walk.',
        '劳动节': 'Happy Labor Day — you deserve today.',
        '端午节': 'Dragon Boat Festival — have a zongzi.',
        '中秋节': 'Mid-Autumn — half the moon is yours tonight.',
        '国庆节': 'National Day — go see the land.'
      }
    };
    var WX = {
      0: { zh: '晴空万里，适合出门晒晒太阳。', en: 'Clear sky — go soak up some sun.', tag: 'Sunny' },
      1: { zh: '天气不错，去散个步吧。', en: 'Not bad out — take a walk.', tag: 'Clear' },
      2: { zh: '多云天气，适合做点安静的事。', en: 'Partly cloudy — a quiet day for calm things.', tag: 'Cloudy' },
      3: { zh: '阴天，泡杯咖啡写写代码正好。', en: 'Overcast — perfect for coffee and code.', tag: 'Overcast' },
      48: { zh: '有雾，路上小心，慢慢走。', en: 'Foggy — take it easy out there.', tag: 'Foggy' },
      67: { zh: '下雨天，适合窝在家里写代码、喝咖啡。', en: 'Rainy — great day to code indoors with a coffee.', tag: 'Rainy' },
      77: { zh: '下雪了，记得保暖，喝杯热的。', en: 'Snowy — stay warm, grab something hot.', tag: 'Snowy' },
      95: { zh: '雷雨天少出门，戴上耳机听会儿歌。', en: 'Stormy — stay in and put on some music.', tag: 'Stormy' },
      '-1': { zh: '天气刚好，去试试没做过的事吧。', en: "Weather's fine — try something new.", tag: '' }
    };
    function wKey(code) {
      if (code === 0) return 0;
      if (code >= 1 && code <= 3) return code;
      if (code <= 48) return 48;
      if (code <= 67) return 67;
      if (code <= 77) return 77;
      if (code <= 86) return 77;
      if (code >= 95) return 95;
      return -1;
    }
    var WEEK = {
      1: { zh: '新的一周，从一杯咖啡开始。', en: 'New week — start with a coffee.', tag: 'Monday' },
      2: { zh: '工作日也要好好生活。', en: 'Keep the week steady.', tag: 'Tuesday' },
      3: { zh: '周三，已经过了一半。', en: 'Wednesday — halfway there.', tag: 'Wednesday' },
      4: { zh: '再坚持一下，周末快到了。', en: 'Almost the weekend — hold on.', tag: 'Thursday' },
      5: { zh: '周五啦，今晚给自己放个假。', en: 'Friday — give yourself the night off.', tag: 'Friday' },
      6: { zh: '周末愉快，去做点喜欢的事。', en: 'Happy weekend — do something you love.', tag: 'Weekend' },
      0: { zh: '周末愉快，去做点喜欢的事。', en: 'Happy weekend — do something you love.', tag: 'Weekend' }
    };
    function pick() {
      var fest = window.__festNow;
      if (fest && FEST.zh[fest]) return { zh: FEST.zh[fest], en: FEST.en[fest], tag: fest };
      var w = window.__wCode;
      if (typeof w === 'number') {
        var wx = WX[wKey(w)];
        if (wx) return { zh: wx.zh, en: wx.en, tag: wx.tag };
      }
      var wk = WEEK[new Date().getDay()];
      if (wk) return { zh: wk.zh, en: wk.en, tag: wk.tag };
      var i = Math.floor(Math.random() * RECO.zh.length);
      return { zh: RECO.zh[i], en: RECO.en[i], tag: '' };
    }
    function render() {
      if (!el) return;
      var L = getLang();
      var r = pick();
      el.textContent = r[L] || r.zh;
      if (tagEl) tagEl.textContent = r.tag ? ('· ' + r.tag) : '';
    }
    render();
    window.addEventListener('yaule-langchange', render);
    setTimeout(render, 2500);
    setTimeout(render, 6000);
  })();
"""
idx = s.rfind("</body>")
assert idx != -1, "无 </body>"
s = s[:idx] + JS + "\n" + s[idx:]

io.open(p, "w", encoding="utf-8").write(s)
print("完成。改动:", len(log), "处 | 文件增长:", len(s) - n0, "字符")
for t in log:
    print(" -", t)
