# -*- coding: utf-8 -*-
"""i18n 补全 B：动态文本双语（一言/天气/日期/纪念日/生活数据/下载/仓库/技能/清单/toast/标语）+ 进度条平滑与数字"""
p = "index.html"
s = open(p, encoding="utf-8").read()
n0 = len(s)
log = []
OPS = []

def rep(old, new, tag):
    OPS.append((old, new, tag))

# ===== 0. 静态：loading 遮罩 hint / skip =====
rep("""<p class="loading-hint">稍等片刻，马上就好…</p>""",
    """<p class="loading-hint" data-i18n="loading.hint">稍等片刻，马上就好…</p>""", "loading.hint")
rep("""<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
    长按加速 <small>按住不放，加载更快</small>""",
    """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
    <span data-i18n="loading.skip1">长按加速</span> <small data-i18n="loading.skip2">按住不放，加载更快</small>""", "loading.skip")

# ===== 1. I18N 字典：zh 追加 =====
rep("""      'footer.contact': '联系', 'footer.email': '邮箱', 'footer.rss': 'RSS 订阅'
    },""",
    """      'footer.contact': '联系', 'footer.email': '邮箱', 'footer.rss': 'RSS 订阅',
      'hero.quoteTitle': '换一句',
      'life.c1': '瑞幸咖啡', 'life.tag1': '续命中', 'life.un2': '杯',
      'life.d1': '从第一杯咖啡开始，悄悄记录每一次续命时刻',
      'life.d2': '美式、拿铁、生椰……每一杯都是生活的续命剂。',
      'life.c2': '网易云音乐', 'life.tag2': '循环播放中', 'life.un1': '首',
      'life.h1': '累计收听', 'life.h2': '+ 小时，旋律里藏着无数个夜晚',
      'life.d3': '深夜的旋律，陪我度过每一个失眠夜。',
      'life.song': '今日推荐：', 'life.songload': '正在挑选…',
      'mc.sub1': '布吉岛', 'mc.sub2': '花雨亭',
      'mc.l1': '游戏对局', 'mc.l2': '在线时长', 'mc.l3': '胜场', 'mc.l4': '放置方块',
      'mc.l5': '挖掘方块', 'mc.l6': '成就解锁', 'mc.l7': '游玩天数', 'mc.l8': '累计上线',
      'mc.u1': '局', 'mc.u2': 'h', 'mc.u3': '胜', 'mc.u4': '个', 'mc.u5': '天',
      'mc.n1': '生存、建筑与联机日常，记录仍在继续。',
      'mc.n2': '花雨亭已停服，数据定格在停服前一天（2025-06-14）。',
      'works.t1': '兴华中学广播站系统', 'works.t1d': '广播排班管理、播放日程控制、站点信息维护，独立设计开发并投入校园实际使用。', 'works.t1p': '广播排班、播放日程、站点信息一站式维护，从零开发并投入校园日常使用。', 'works.tag1a': '广播', 'works.tag1b': '管理',
      'works.t2': '自助记账系统', 'works.t2d': '收支记录、分类统计、数据可视化，轻量化单文件本地工具，开箱即用。', 'works.t2p': '收支流水、分类统计、报表导出，让每一笔账都清清楚楚。', 'works.tag2a': '记账', 'works.tag2b': '工具',
      'works.t3': '代码编写系统', 'works.t3d': '可视化拖拽生成 C++ 代码，降低编程入门门槛，助力机器人编程学习。', 'works.t3p': '代码编写辅助工作台，模板化快速生成，让日常编码更顺手。', 'works.tag3a': '编码', 'works.tag3b': '效率',
      'works.t4': '表情转图片转换器', 'works.t4d': '文字、表情符号一键转图片，支持自定义背景与文字颜色，导出高清 PNG。', 'works.t4p': '把文字图案一键转成 Emoji 图片，分享出来更有趣。', 'works.tag4a': '趣味', 'works.tag4b': '图像',
      'works.t5': 'CS 灵敏度校准', 'works.t5d': '输入 DPI 与灵敏度参数，智能评估输出最佳游戏鼠标灵敏度。', 'works.t5p': 'FPS 游戏鼠标灵敏度科学校准，找到真正属于自己的手感。', 'works.tag5a': '游戏', 'works.tag5b': '外设',
      'works.t6': '棋类合集', 'works.t6d': '五子棋与中国象棋，本地运行，无需联网。', 'works.t6p': '象棋与五子棋同页双开，约上好友面对面来一局。', 'works.tag6a': '游戏', 'works.tag6b': '对战',
      'anniv.a1': '与这个世界相遇', 'anniv.a2': '与这座小站相遇',
      'anniv.l1': '活着的第', 'anniv.l2': '天', 'anniv.l3': '本站上线第', 'anniv.l4': '天',
      'anniv.meta1': '人生进度计算中…', 'anniv.meta2': '下一个里程碑计算中…',
      'anniv.d1': '自 2012 年 1 月 17 日起', 'anniv.d2': '自 2026 年 9 月 18 日起',
      'repos.loading': '正在读取仓库…', 'repos.connecting': '连接 GitHub API 中，稍等片刻。',
      'skills.h3': '从校园工具到小游戏，什么都想试一试。',
      'skills.p': '广播站系统、记账工具、代码生成器、棋类游戏……都是一个人从零写完的。爱折腾前端交互，也愿意沉下去做工具；会调音视频，也会为一个小游戏磨上几个晚上。',
      'bucket.progress': '已点亮', 'bucket.progress2': '件',
      'loading.hint': '稍等片刻，马上就好…', 'loading.skip1': '长按加速', 'loading.skip2': '按住不放，加载更快'
    },""", "I18N zh 追加")

# ===== 2. I18N 字典：en 追加 =====
rep("""      'footer.contact': 'Contact', 'footer.email': 'Email', 'footer.rss': 'RSS Feed'
    }""",
    """      'footer.contact': 'Contact', 'footer.email': 'Email', 'footer.rss': 'RSS Feed',
      'hero.quoteTitle': 'Another quote',
      'life.c1': 'Luckin Coffee', 'life.tag1': 'LIVE', 'life.un2': 'cups',
      'life.d1': 'From the first cup, quietly counting every refuel',
      'life.d2': 'Americano, latte, coconut milk… every cup keeps life going.',
      'life.c2': 'NetEase Cloud Music', 'life.tag2': 'ON LOOP', 'life.un1': 'songs',
      'life.h1': 'Total listened', 'life.h2': '+ hours of melodies that kept the nights company',
      'life.d3': 'Late-night melodies, through every sleepless night.',
      'life.song': "Today's pick: ", 'life.songload': 'Picking…',
      'mc.sub1': 'Bujidao', 'mc.sub2': 'Huayuting',
      'mc.l1': 'Matches', 'mc.l2': 'Online time', 'mc.l3': 'Wins', 'mc.l4': 'Blocks placed',
      'mc.l5': 'Blocks mined', 'mc.l6': 'Achievements', 'mc.l7': 'Play days', 'mc.l8': 'Days online',
      'mc.u1': 'games', 'mc.u2': 'h', 'mc.u3': 'wins', 'mc.u4': '', 'mc.u5': 'days',
      'mc.n1': 'Survival, building and multiplayer — still recording.',
      'mc.n2': 'Huayuting is offline; data frozen the day before shutdown (2025-06-14).',
      'works.t1': 'Xinghua Broadcasting System', 'works.t1d': 'Broadcast scheduling, playlist control and station maintenance — built for real campus use.', 'works.t1p': 'One-stop broadcasting ops: scheduling, playlists, station info — built from scratch for daily campus use.', 'works.tag1a': 'Broadcast', 'works.tag1b': 'Manage',
      'works.t2': 'Self-Service Accounting', 'works.t2d': 'Income & expense tracking, category stats and charts — a lightweight single-file tool.', 'works.t2p': 'Ledger, categories, export — every cent stays crystal clear.', 'works.tag2a': 'Finance', 'works.tag2b': 'Tool',
      'works.t3': 'Code Writing System', 'works.t3d': 'Drag-and-drop C++ generation that lowers the barrier for robotics learners.', 'works.t3p': 'A coding workbench with template-based generation for smoother daily work.', 'works.tag3a': 'Code', 'works.tag3b': 'Efficiency',
      'works.t4': 'Emoji to Image Converter', 'works.t4d': 'Turn text & emoji into images with custom colors and HD PNG export.', 'works.t4p': 'Convert text patterns into fun emoji images for sharing.', 'works.tag4a': 'Fun', 'works.tag4b': 'Image',
      'works.t5': 'CS Sensitivity Calibrator', 'works.t5d': 'Input DPI & sens, get an AI-evaluated optimal mouse sensitivity.', 'works.t5p': 'Science-based mouse sensitivity calibration for your own feel.', 'works.tag5a': 'Game', 'works.tag5b': 'Gear',
      'works.t6': 'Chess & Gomoku Collection', 'works.t6d': 'Gomoku and Chinese chess, fully offline.', 'works.t6p': 'Chess and gomoku on one page — challenge a friend face to face.', 'works.tag6a': 'Game', 'works.tag6b': 'Versus',
      'anniv.a1': 'Met this world', 'anniv.a2': 'Met this little site',
      'anniv.l1': 'Day', 'anniv.l2': 'of being alive', 'anniv.l3': 'Day', 'anniv.l4': 'of this site',
      'anniv.meta1': 'Calculating…', 'anniv.meta2': 'Calculating…',
      'anniv.d1': 'Since Jan 17, 2012', 'anniv.d2': 'Since Sep 18, 2026',
      'repos.loading': 'Loading repos…', 'repos.connecting': 'Connecting to GitHub API…',
      'skills.h3': 'From campus tools to mini games — I try a bit of everything.',
      'skills.p': 'Broadcasting systems, accounting tools, code generators, board games… all written from scratch alone. I love tinkering with front-end interaction and going deep on tools — audio & video too, and grinding nights on a mini game.',
      'bucket.progress': 'Done', 'bucket.progress2': 'of',
      'loading.hint': 'Just a moment…', 'loading.skip1': 'Hold to speed up', 'loading.skip2': 'Press and hold to load faster'
    }""", "I18N en 追加")

# ===== 3. switchLang：rAF 平滑 + 百分比数字 =====
rep("""    var p = 0;
    var t = setInterval(function () {
      p += Math.random() * 6.5;
      if (p > 90) p = 90;
      fill.style.width = p + '%';
    }, 90);
    setTimeout(function () {
      clearInterval(t);
      fill.style.width = '100%';""",
    """    var pctEl = document.getElementById('langBarPct');
    var t0 = Date.now();
    var raf = null;
    function step() {
      var el = (Date.now() - t0) / 3000;
      var p = Math.min(90, el * 100);
      fill.style.width = p + '%';
      if (pctEl) pctEl.textContent = Math.floor(p) + '%';
      if (Date.now() - t0 < 3000) raf = requestAnimationFrame(step);
    }
    raf = requestAnimationFrame(step);
    setTimeout(function () {
      if (raf) cancelAnimationFrame(raf);
      fill.style.width = '100%';
      if (pctEl) pctEl.textContent = '100%';""", "switchLang rAF")

# ===== 4. applyLang：aria / title + 触发各渲染 =====
rep("""    var st = document.getElementById('stayTime');
    if (st) st.innerHTML = L === 'en' ? 'Stayed 0 min 0 sec' : '已停留 0 分 0 秒';
    window.dispatchEvent(new CustomEvent('yaule-langchange'));""",
    """    var st = document.getElementById('stayTime');
    if (st) st.innerHTML = L === 'en' ? 'Stayed 0 min 0 sec' : '已停留 0 分 0 秒';
    var qn = document.getElementById('quoteNext');
    if (qn) { var qt = L === 'en' ? 'Another quote' : '换一句'; qn.setAttribute('aria-label', qt); qn.title = qt; }
    var rs = document.getElementById('radarSvg');
    if (rs) rs.setAttribute('aria-label', L === 'en' ? 'Skills radar chart' : '技能雷达图');
    var tt = document.getElementById('themeToggle');
    if (tt) tt.title = L === 'en' ? 'Toggle dark / light theme' : '切换深色 / 浅色主题';
    var ltb = document.getElementById('langToggle');
    if (ltb) ltb.title = L === 'en' ? 'Switch language' : '切换语言';
    if (window.__renderLife) window.__renderLife();
    if (window.__renderAnniv) window.__renderAnniv();
    if (window.__renderWeather) window.__renderWeather();
    if (window.__renderDl) window.__renderDl();
    if (window.__renderRepos) window.__renderRepos();
    if (window.__renderSkills) window.__renderSkills();
    if (window.__renderBucket) window.__renderBucket();
    if (window.__reQuote) window.__reQuote();
    if (window.__setFest) window.__setFest();
    window.dispatchEvent(new CustomEvent('yaule-langchange'));""", "applyLang 增强")

# ===== 5. life 数据 render =====
rep("""    var cups = 176 + Math.floor(d / 3);
    var songs = 305 + Math.floor(d / 2);
    var hours = 2000 + Math.floor(d / 2) * 25.7;
    document.getElementById('cups').innerHTML = cups + '<small>杯</small>';
    document.getElementById('songs').textContent = songs;
    document.getElementById('hours').textContent = Math.floor(hours);
  })();""",
    """    var cups = 176 + Math.floor(d / 3);
    var songs = 305 + Math.floor(d / 2);
    var hours = 2000 + Math.floor(d / 2) * 25.7;
    function render() {
      var en = window.YAULE_LANG === 'en';
      var ce = document.getElementById('cups');
      if (ce) ce.innerHTML = cups + '<small>' + (en ? 'cups' : '杯') + '</small>';
      var se = document.getElementById('songs');
      if (se) se.textContent = songs;
      var he = document.getElementById('hours');
      if (he) he.textContent = Math.floor(hours);
    }
    window.__renderLife = render;
    render();
  })();""", "life render")

# ===== 6. 时钟日期 en =====
rep("""      dateEl.textContent = d.getFullYear() + ' 年 ' + (d.getMonth() + 1) + ' 月 ' + d.getDate() + ' 日 · 星期' + week[d.getDay()];""",
    """      var en = window.YAULE_LANG === 'en';
      dateEl.textContent = en
        ? ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'][d.getDay()] + ', ' + ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][d.getMonth()] + ' ' + d.getDate() + ', ' + d.getFullYear()
        : d.getFullYear() + ' 年 ' + (d.getMonth() + 1) + ' 月 ' + d.getDate() + ' 日 · 星期' + week[d.getDay()];""", "clock date en")

# ===== 7. 一言：ENQ + pickLocal/nextQuote + __reQuote =====
rep("""    var text = document.getElementById('quoteText');
    var next = document.getElementById('quoteNext');
    var cur = 0;""",
    """    var text = document.getElementById('quoteText');
    var next = document.getElementById('quoteNext');
    var cur = 0;
    var ENQ = [
      ['Stay hungry, stay foolish.', 'Steve Jobs'],
      ['The only way to do great work is to love what you do.', 'Steve Jobs'],
      ['Simplicity is the ultimate sophistication.', 'Leonardo da Vinci'],
      ['It always seems impossible until it\\'s done.', 'Nelson Mandela'],
      ['Code is poetry.', 'WordPress'],
      ['Sleep is the best meditation.', 'Dalai Lama'],
      ['Make it work, make it right, make it fast.', 'Kent Beck'],
      ['Talk is cheap. Show me the code.', 'Linus Torvalds'],
      ['Good artists copy; great artists steal.', 'Steve Jobs'],
      ['Do not go gentle into that good night.', 'Dylan Thomas'],
      ['The night is darkest just before the dawn.', 'English proverb'],
      ['Dreams are the answers to questions we haven\\'t asked yet.', 'Unknown'],
      ['Coffee first. Schemes later.', 'Unknown'],
      ['Keep it simple, make it beautiful.', 'Unknown'],
      ['One day or day one. You decide.', 'Unknown'],
      ['Every night is a new version of you.', 'Yaule']
    ];""", "ENQ 池")
rep("""    function pickLocal(random) {
      if (random) {
        var i;
        do { i = Math.floor(Math.random() * quotes.length); } while (i === cur);
        cur = i;
      } else {
        var d = new Date();
        var key = d.getFullYear() * 10000 + (d.getMonth() + 1) * 100 + d.getDate();
        cur = key % quotes.length;
      }
      render(quotes[cur]);
    }""",
    """    function pickLocal(random) {
      var pool = (window.YAULE_LANG === 'en') ? ENQ : quotes;
      if (random) {
        var i;
        do { i = Math.floor(Math.random() * pool.length); } while (i === cur);
        cur = i;
      } else {
        var d = new Date();
        var key = d.getFullYear() * 10000 + (d.getMonth() + 1) * 100 + d.getDate();
        cur = key % pool.length;
      }
      render(pool[cur]);
    }
    window.__reQuote = function () { pickLocal(false); };""", "pickLocal 双语")
rep("""    function nextQuote() {
      fetchNet(function (q) {
        if (q) { fadeSwap(function () { render(q); }); }
        else { fadeSwap(function () { pickLocal(true); }); }
      });
    }""",
    """    function nextQuote() {
      if (window.YAULE_LANG === 'en') { fadeSwap(function () { pickLocal(true); }); return; }
      fetchNet(function (q) {
        if (q) { fadeSwap(function () { render(q); }); }
        else { fadeSwap(function () { pickLocal(true); }); }
      });
    }""", "nextQuote 双语")

# ===== 8. 天气 renderWeather =====
rep("""    function textFor(code) {
      if (code === 0) return '晴';
      if (code === 1) return '大部晴朗';
      if (code === 2) return '多云';
      if (code === 3) return '阴';
      if (code <= 48) return '雾';
      if (code <= 56) return '毛毛雨';
      if (code <= 67) return '雨';
      if (code <= 77) return '雪';
      if (code <= 82) return '阵雨';
      if (code <= 86) return '阵雪';
      return '雷阵雨';
    }""",
    """    function textFor(code) {
      if (code === 0) return '晴';
      if (code === 1) return '大部晴朗';
      if (code === 2) return '多云';
      if (code === 3) return '阴';
      if (code <= 48) return '雾';
      if (code <= 56) return '毛毛雨';
      if (code <= 67) return '雨';
      if (code <= 77) return '雪';
      if (code <= 82) return '阵雨';
      if (code <= 86) return '阵雪';
      return '雷阵雨';
    }
    function textForEn(code) {
      if (code === 0) return 'Clear';
      if (code === 1) return 'Mostly clear';
      if (code === 2) return 'Partly cloudy';
      if (code === 3) return 'Overcast';
      if (code <= 48) return 'Fog';
      if (code <= 56) return 'Drizzle';
      if (code <= 67) return 'Rain';
      if (code <= 77) return 'Snow';
      if (code <= 82) return 'Showers';
      if (code <= 86) return 'Snow showers';
      return 'Thunderstorm';
    }
    var wData = null;
    function renderWeather() {
      if (!wData) return;
      var c = wData;
      var en = window.YAULE_LANG === 'en';
      icon.innerHTML = svgFor(c.weather_code);
      txt.innerHTML = '<span>' + (en ? 'Quzhou' : '衢州') + '</span><span class="weather-temp">' + Math.round(c.temperature_2m) + '°C</span><span>' + (en ? textForEn(c.weather_code) : textFor(c.weather_code)) + '</span>';
    }
    window.__renderWeather = renderWeather;""", "weather 双语")
rep("""        var c = d.current;
        window.__wCode = c.weather_code;
        icon.innerHTML = svgFor(c.weather_code);
        txt.innerHTML = '<span>衢州</span><span class="weather-temp">' + Math.round(c.temperature_2m) + '°C</span><span>' + textFor(c.weather_code) + '</span>';""",
    """        var c = d.current;
        window.__wCode = c.weather_code;
        wData = c;
        renderWeather();""", "weather fetch")
rep("""      .catch(function () { txt.textContent = '衢州 · 天气暂时不可用'; });""",
    """      .catch(function () { txt.textContent = (window.YAULE_LANG === 'en') ? 'Quzhou · weather unavailable right now' : '衢州 · 天气暂时不可用'; });""", "weather catch")

# ===== 9. anniv renderAnniv =====
rep("""    // 生命进度条：以 80 岁（29200 天）为参考
    var lifeFill = document.getElementById('lifeFill');
    var lifeMeta = document.getElementById('lifeMeta');
    if (lifeFill && lifeMeta) {
      var span = 29200;
      var pct = Math.min(100, Math.round((a / span) * 1000) / 10);
      setTimeout(function () { lifeFill.style.width = pct + '%'; }, 120);
      lifeMeta.textContent = '人生进度约 ' + pct + '%（参考 80 岁）';
    }
    // 站点里程碑：下一个 30 / 100 / 365 / 1000 天
    var siteFill = document.getElementById('siteFill');
    var siteMeta = document.getElementById('siteMeta');
    if (siteFill && siteMeta) {
      var goals = [30, 100, 365, 1000, 3650];
      var next = 3650;
      for (var i = 0; i < goals.length; i++) {
        if (s < goals[i]) { next = goals[i]; break; }
      }
      setTimeout(function () { siteFill.style.width = Math.min(100, (s / next) * 100) + '%'; }, 120);
      siteMeta.textContent = '距离 ' + next + ' 天里程碑还有 ' + (next - s) + ' 天';
    }
  })();""",
    """    // 生命进度条：以 80 岁（29200 天）为参考；站点里程碑：下一个 30 / 100 / 365 / 1000 天
    var lifeFill = document.getElementById('lifeFill');
    var lifeMeta = document.getElementById('lifeMeta');
    var siteFill = document.getElementById('siteFill');
    var siteMeta = document.getElementById('siteMeta');
    var span = 29200;
    var pct = Math.min(100, Math.round((a / span) * 1000) / 10);
    var goals = [30, 100, 365, 1000, 3650];
    var next = 3650;
    for (var i = 0; i < goals.length; i++) {
      if (s < goals[i]) { next = goals[i]; break; }
    }
    function renderAnniv() {
      var en = window.YAULE_LANG === 'en';
      if (lifeFill) setTimeout(function () { lifeFill.style.width = pct + '%'; }, 120);
      if (lifeMeta) lifeMeta.textContent = en ? 'About ' + pct + '% of a life lived (based on 80 years)' : '人生进度约 ' + pct + '%（参考 80 岁）';
      if (siteFill) setTimeout(function () { siteFill.style.width = Math.min(100, (s / next) * 100) + '%'; }, 120);
      if (siteMeta) siteMeta.textContent = en ? (next - s) + ' days to the ' + next + '-day milestone' : '距离 ' + next + ' 天里程碑还有 ' + (next - s) + ' 天';
    }
    window.__renderAnniv = renderAnniv;
    renderAnniv();
  })();""", "anniv render")

# ===== 10. 节日欢迎语双语 =====
rep("""    var GREETING = {
      '春节': '新年快乐，万事顺遂。',
      '除夕': '辞旧迎新，灯火可亲。',
      '元宵节': '元宵喜乐，阖家团圆。',
      '清明节': '气清景明，万物皆显。',
      '劳动节': '辛苦了，今天属于你。',
      '端午节': '端午安康，粽叶飘香。',
      '中秋节': '今晚的月亮，借你一半。',
      '国庆节': '山河远阔，人间烟火。'
    };""",
    """    var GREETING = {
      '春节': '新年快乐，万事顺遂。',
      '除夕': '辞旧迎新，灯火可亲。',
      '元宵节': '元宵喜乐，阖家团圆。',
      '清明节': '气清景明，万物皆显。',
      '劳动节': '辛苦了，今天属于你。',
      '端午节': '端午安康，粽叶飘香。',
      '中秋节': '今晚的月亮，借你一半。',
      '国庆节': '山河远阔，人间烟火。'
    };
    var GREETING_EN = {
      '春节': 'Happy Spring Festival — share your first wish of the year.',
      '除夕': "New Year's Eve — enjoy a proper family dinner.",
      '元宵节': 'Happy Lantern Festival — grab a bowl of tangyuan.',
      '清明节': 'Clear and bright — take a spring walk.',
      '劳动节': 'Happy Labor Day — you deserve today.',
      '端午节': 'Dragon Boat Festival — have a zongzi.',
      '中秋节': 'Mid-Autumn — half the moon is yours tonight.',
      '国庆节': 'National Day — go see the land.'
    };
    window.__setFest = function () {
      var gEl = document.getElementById('festGreeting');
      if (!gEl || !window.__festName) return;
      var v = (window.YAULE_LANG === 'en') ? GREETING_EN : GREETING;
      if (v[window.__festName]) { gEl.textContent = v[window.__festName]; gEl.classList.add('show'); }
    };""", "GREETING_EN")
rep("""        if (gEl && GREETING[matched.name]) {
          gEl.textContent = GREETING[matched.name];
          gEl.classList.add('show');
        }""",
    """        window.__festName = matched.name;
        if (gEl) window.__setFest();""", "fest 设置")

# ===== 11. 下载次数双语 =====
rep("""    document.querySelectorAll('.card').forEach(function (card) {
      var body = card.querySelector('.card-body');
      if (!body) return;
      var badge = document.createElement('span');
      badge.className = 'card-dl-count';
      badge.textContent = '下载 ' + (store[nameOf(card)] || 0) + ' 次';
      body.appendChild(badge);
    });""",
    """    function badgeText(n) { return (window.YAULE_LANG === 'en') ? n + ' downloads' : '下载 ' + n + ' 次'; }
    function renderAllBadges() {
      document.querySelectorAll('.card-dl-count').forEach(function (b) {
        var card = b.closest('.card');
        if (card) b.textContent = badgeText(store[nameOf(card)] || 0);
      });
    }
    window.__renderDl = renderAllBadges;
    document.querySelectorAll('.card').forEach(function (card) {
      var body = card.querySelector('.card-body');
      if (!body) return;
      var badge = document.createElement('span');
      badge.className = 'card-dl-count';
      badge.textContent = badgeText(store[nameOf(card)] || 0);
      body.appendChild(badge);
    });""", "dl badge")
rep("""        var badge = card ? card.querySelector('.card-dl-count') : null;
        if (badge) badge.textContent = '下载 ' + store[name] + ' 次';""",
    """        var badge = card ? card.querySelector('.card-dl-count') : null;
        if (badge) badge.textContent = badgeText(store[name]);""", "dl badge 更新")

# ===== 12. repos 双语 =====
rep("""    var fallback = [
      { name: 'Yaule-Rate.github.io', desc: '本站源码：全世界语言的欢迎页与个人标签页。', lang: 'HTML', stars: 0, forks: 0, updated: '2026-09-25', color: '#e34c26' }
    ];""",
    """    var fallback = [
      { name: 'Yaule-Rate.github.io', desc: '本站源码：全世界语言的欢迎页与个人标签页。', lang: 'HTML', stars: 0, forks: 0, updated: '2026-09-25', color: '#e34c26' }
    ];
    var fallbackEn = [
      { name: 'Yaule-Rate.github.io', desc: 'Source of this site: multilingual welcome page & personal hub.', lang: 'HTML', stars: 0, forks: 0, updated: '2026-09-25', color: '#e34c26' }
    ];""", "repos fallbackEn")
rep("""    function render(list) {
      if (!list || !list.length) list = fallback;
      var htmls = list.slice(0, 6).map(function (r) {
        var c = langColor[r.lang] || '#8b949e';
        var date = (r.updated || '').slice(0, 10);""",
    """    function render(list) {
      if (!list || !list.length) list = (window.YAULE_LANG === 'en') ? fallbackEn : fallback;
      window.__reposList = list;
      var htmls = list.slice(0, 6).map(function (r) {
        var c = langColor[r.lang] || '#8b949e';
        var date = (r.updated || '').slice(0, 10);
        var desc = r.desc;
        if (!desc) desc = (window.YAULE_LANG === 'en') ? 'No description' : '暂无简介';""", "repos render 双语")
rep("""      }).join('');
      grid.innerHTML = htmls;
    }""",
    """      }).join('');
      grid.innerHTML = htmls;
    }
    window.__renderRepos = function () { if (window.__reposList) render(window.__reposList); };""", "repos __renderRepos")
rep("""</div><div class="repo-desc">' + esc(r.desc || '暂无简介') + '</div>""",
    """</div><div class="repo-desc">' + esc(desc) + '</div>""", "repos desc 变量")

# ===== 13. skills 双语 =====
rep("""  (function () {
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
    ];""",
    """  (function () {
    function renderSkills() {
    var svg = document.getElementById('radarSvg');
    var bars = document.getElementById('skillBars');
    if (!svg) return;
    var skills = [
      { name: '前端开发', en: 'Front-end', val: 8 },
      { name: '效率工具', en: 'Tools', val: 9 },
      { name: '音视频', en: 'AV Media', val: 7 },
      { name: '游戏开发', en: 'Game Dev', val: 8 },
      { name: '界面设计', en: 'UI Design', val: 6 },
      { name: '后端开发', en: 'Back-end', val: 6 }
    ];
    function sname(i) { return (window.YAULE_LANG === 'en') ? skills[i].en : skills[i].name; }""", "skills 函数化")
rep("""      labels += '<text class="radar-label" x="' + (lx + dx).toFixed(1) + '" y="' + (ly + dy).toFixed(1) + '" text-anchor="' + anchors[i5] + '" dominant-baseline="middle">' + skills[i5].name + '</text>';""",
    """      labels += '<text class="radar-label" x="' + (lx + dx).toFixed(1) + '" y="' + (ly + dy).toFixed(1) + '" text-anchor="' + anchors[i5] + '" dominant-baseline="middle">' + sname(i5) + '</text>';""", "radar labels")
rep("""      bars.innerHTML = skills.map(function (s) {
        return '<div class="skill-bar-row"><span class="sb-name">' + s.name + '</span><span class="sb-track"><span class="sb-fill" style="width:' + (s.val * 10) + '%"></span></span><span class="sb-num">' + s.val + '</span></div>';
      }).join('');
    }
  })();""",
    """      bars.innerHTML = skills.map(function (s, si) {
        return '<div class="skill-bar-row"><span class="sb-name">' + sname(si) + '</span><span class="sb-track"><span class="sb-fill" style="width:' + (s.val * 10) + '%"></span></span><span class="sb-num">' + s.val + '</span></div>';
      }).join('');
    }
    }
    window.__renderSkills = renderSkills;
    renderSkills();
  })();""", "skills bars + 挂载")

# ===== 14. bucket 双语 =====
rep("""    var items = ['去看一次现场演唱会', '看一场完整的日出', '学会弹一首完整的曲子', '写一本属于自己的小说', '跑一次五公里', '去一次西藏', '给爸妈买一份大礼物', '养一盆活过一年的绿植', '亲手做一顿年夜饭', '学会一门新的外语', '看一次极光', '独自去一座陌生城市旅行', '学会做咖啡拉花', '给十年后的自己写一封信', '种一棵属于自己的树', '养一只猫', '跳一次伞', '读完《三国演义》', '做一次公益志愿者', '发一张自己的专辑', '开一家小店', '通宵看一次流星雨', '把房间布置成喜欢的样子', '拍一支 Vlog 记录一天'];""",
    """    var itemsZh = ['去看一次现场演唱会', '看一场完整的日出', '学会弹一首完整的曲子', '写一本属于自己的小说', '跑一次五公里', '去一次西藏', '给爸妈买一份大礼物', '养一盆活过一年的绿植', '亲手做一顿年夜饭', '学会一门新的外语', '看一次极光', '独自去一座陌生城市旅行', '学会做咖啡拉花', '给十年后的自己写一封信', '种一棵属于自己的树', '养一只猫', '跳一次伞', '读完《三国演义》', '做一次公益志愿者', '发一张自己的专辑', '开一家小店', '通宵看一次流星雨', '把房间布置成喜欢的样子', '拍一支 Vlog 记录一天'];
    var itemsEn = ['Watch a live concert', 'See a full sunrise', 'Learn to play a song on an instrument', 'Write a novel of my own', 'Run 5 kilometers', 'Travel to Tibet', 'Buy a big gift for my parents', 'Keep a plant alive for a year', 'Cook the New Year dinner myself', 'Learn a new language', 'See the aurora', 'Travel alone to a strange city', 'Learn latte art', 'Write a letter to my future self in 10 years', 'Plant a tree of my own', 'Adopt a cat', 'Go skydiving', 'Finish reading Romance of the Three Kingdoms', 'Volunteer for charity once', 'Release my own album', 'Open a little shop', 'Stay up all night for a meteor shower', 'Decorate my room the way I like', 'Make a day-in-my-life Vlog'];""", "bucket items 双语")
rep("""    grid.innerHTML = items.map(function (t, idx) {
      var on = doneMap[idx];
      return '<div class="bucket-item' + (on ? ' done' : '') + '"><span class="bk-check"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg></span><span class="bk-text">' + t + '</span></div>';
    }).join('');
    refresh();""",
    """    function render() {
      var arr = (window.YAULE_LANG === 'en') ? itemsEn : itemsZh;
      grid.innerHTML = arr.map(function (t, idx) {
        var on = doneMap[idx];
        return '<div class="bucket-item' + (on ? ' done' : '') + '"><span class="bk-check"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg></span><span class="bk-text">' + t + '</span></div>';
      }).join('');
      var n = 0;
      grid.querySelectorAll('.bucket-item').forEach(function (el) {
        if (el.classList.contains('done')) n++;
      });
      if (doneN) doneN.textContent = n;
      if (totalN) totalN.textContent = arr.length;
      if (fill) fill.style.width = (n / arr.length * 100) + '%';
    }
    window.__renderBucket = render;
    render();""", "bucket render")

# ===== 15. toast 双语 =====
rep("""        showToast('已在新标签页打开');""",
    """        showToast(window.YAULE_LANG === 'en' ? 'Opened in a new tab' : '已在新标签页打开');""", "toast new tab")
rep("""      showToast('开始下载 ' + name);""",
    """      showToast((window.YAULE_LANG === 'en' ? 'Downloading ' : '开始下载 ') + name);""", "toast download")
rep("""      function done() { showToast('一言已复制'); }""",
    """      function done() { showToast(window.YAULE_LANG === 'en' ? 'Quote copied' : '一言已复制'); }""", "toast quote")

# ===== 16. LOAD_LINES 双语 =====
rep("""    var LOAD_LINES = [
      '正在泡咖啡…', '正在数星星…', '正在整理作品…', '正在点亮灯笼…',
      '正在问候全世界…', '正在翻今天的日记…', '正在检查进度条…', '正在等你…'
    ];
    if (loadHint) loadHint.textContent = LOAD_LINES[Math.floor(Math.random() * LOAD_LINES.length)];""",
    """    var LOAD_LINES = [
      '正在泡咖啡…', '正在数星星…', '正在整理作品…', '正在点亮灯笼…',
      '正在问候全世界…', '正在翻今天的日记…', '正在检查进度条…', '正在等你…'
    ];
    var LOAD_LINES_EN = [
      'Brewing coffee…', 'Counting stars…', 'Polishing works…', 'Lighting lanterns…',
      'Greeting the world…', "Flipping today's diary…", 'Checking the progress bar…', 'Waiting for you…'
    ];
    if (loadHint) {
      var LPOOL = (window.YAULE_LANG === 'en') ? LOAD_LINES_EN : LOAD_LINES;
      loadHint.textContent = LPOOL[Math.floor(Math.random() * LPOOL.length)];
    }""", "LOAD_LINES 双语")

# ===== 17. btnMore 展开态双语（移除 data-i18n 冲突）=====
rep("""<button class="btn-more" id="btnMore" data-i18n="works.more">查看更多 ↓</button>""",
    """<button class="btn-more" id="btnMore">查看更多 ↓</button>""", "btnMore 去 data-i18n")
rep("""    btn.textContent = expanded ? '收起 ↑' : '查看更多 ↓';""",
    """    btn.textContent = (window.YAULE_LANG === 'en')
      ? (expanded ? 'Collapse ↑' : 'View More ↓')
      : (expanded ? '收起 ↑' : '查看更多 ↓');""", "btnMore 双语")

# ===== 执行 =====
bad = [(t, s.count(o)) for (o, _, t) in OPS if s.count(o) != 1]
if bad:
    for t, c in bad:
        print("锚点失败(%d): %s" % (c, t))
    raise SystemExit(1)
for (o, n, t) in OPS:
    s = s.replace(o, n, 1)
    log.append(t)

open(p, "w", encoding="utf-8").write(s)
print("完成。替换:", len(log), "处 | 增长:", len(s) - n0)
for t in log:
    print(" -", t)
