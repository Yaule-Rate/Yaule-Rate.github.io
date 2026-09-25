# -*- coding: utf-8 -*-
"""v17 补丁 part2：section 互换 / changelog 全量重写（完整时间戳+[ADD/INFO/FIX]）/ JS 逻辑"""
path = "index.html"
html = open(path, encoding="utf-8").read()
changed = []
def rep(old, new, tag):
    global html
    if old in html:
        html = html.replace(old, new, 1)
        changed.append(tag)
    else:
        print("FAIL:", tag)

# ---------- 1. 精选作品 与 生活瞬间 换位置 ----------
i1 = html.index("<!-- 板块 1：精选作品 -->")
i2 = html.index("</section>", i1) + len("</section>")
j1 = html.index("<!-- 板块 2：生活瞬间（咖啡 · 音乐 · 游戏） -->")
j2 = html.index("</section>", j1) + len("</section>")
works_block = html[i1:i2]
life_block = html[j1:j2]
works_block = works_block.replace("<!-- 板块 1：精选作品 -->", "<!-- 板块 2：精选作品 -->", 1)
life_block = life_block.replace("<!-- 板块 2：生活瞬间（咖啡 · 音乐 · 游戏） -->", "<!-- 板块 1：生活瞬间（咖啡 · 音乐 · 游戏） -->", 1)
html = html[:i1] + life_block + html[i2:j1] + works_block + html[j2:]
changed.append("swap works/life")

# ---------- 2. 更新日志全量重写 ----------
new_changelog = '''<!-- 板块 8：版本更新日志 -->
<section class="section" id="changelog">
  <div class="wrap">
    <div class="section-head">
      <p class="kicker">CHANGELOG</p>
      <h2>更新日志</h2>
      <p class="desc">这个页面是怎么一点点长成现在这样的。</p>
      <a class="log-more" href="changelog.html">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
        详细日志
      </a>
    </div>
    <div class="mc-log">
      <div class="mc-ver current">
        <div class="mc-ver-head">
          <span class="mc-ver-badge">v16</span>
          <span class="mc-ver-date">2026-09-25 14:05:11 · 当前版本</span>
        </div>
        <ul class="mc-ver-list">
          <li class="cat-new"><b>[ADD]</b><span class="li-time">14:05:11</span>生活瞬间三图标换用开源黑白 SVG：瑞幸 / 网易云 / 我的世界。</li>
          <li class="cat-new"><b>[ADD]</b><span class="li-time">14:04:40</span>六个作品新增独立详情页，点「查看详情」进入详细介绍。</li>
          <li class="cat-new"><b>[ADD]</b><span class="li-time">14:04:02</span>人生清单改为程序预设勾选，记录由代码维护。</li>
          <li class="cat-chg"><b>[INFO]</b><span class="li-time">14:03:22</span>更新日志改版为我的世界启动器风格，新增详细日志页。</li>
          <li class="cat-chg"><b>[INFO]</b><span class="li-time">14:02:15</span>「此刻」布局改双列：天气卡通栏，新增体感 / 湿度 / 风速 / 紫外线四项。</li>
          <li class="cat-fix"><b>[FIX]</b><span class="li-time">14:01:07</span>技能进度条颜色不渲染问题：内联宽度 + 块级填充。</li>
          <li class="cat-fix"><b>[FIX]</b><span class="li-time">13:59:52</span>一言长句中文与数字重叠，支持自动换行。</li>
          <li class="cat-chg"><b>[INFO]</b><span class="li-time">13:58:26</span>生活瞬间切换增加平滑过渡，容器高度稳定不闪动。</li>
        </ul>
      </div>
      <div class="mc-ver">
        <div class="mc-ver-head">
          <span class="mc-ver-badge">v15</span>
          <span class="mc-ver-date">2026-09-25 13:52:40</span>
        </div>
        <ul class="mc-ver-list">
          <li class="cat-new"><b>[ADD]</b><span class="li-time">13:52:40</span>开源仓库墙：实时读取 GitHub 公开仓库与星标。</li>
          <li class="cat-new"><b>[ADD]</b><span class="li-time">13:51:12</span>技能雷达图与六项自评进度条。</li>
          <li class="cat-new"><b>[ADD]</b><span class="li-time">13:49:36</span>人生清单：想做的 24 件小事。</li>
          <li class="cat-chg"><b>[INFO]</b><span class="li-time">13:47:58</span>版本更新日志时间轴改版上线。</li>
        </ul>
      </div>
      <div class="mc-ver">
        <div class="mc-ver-head">
          <span class="mc-ver-badge">v14</span>
          <span class="mc-ver-date">2026-09-25 12:47:16</span>
        </div>
        <ul class="mc-ver-list">
          <li class="cat-new"><b>[ADD]</b><span class="li-time">12:47:16</span>RSS / Atom 订阅源，访客可订阅站点每一次更新。</li>
          <li class="cat-new"><b>[ADD]</b><span class="li-time">12:46:05</span>busuanzi 访问计数，页脚实时显示访客与浏览量。</li>
          <li class="cat-new"><b>[ADD]</b><span class="li-time">12:44:31</span>作品卡展开预览：扩展简介、技术标签，点卡片任意处即展开。</li>
          <li class="cat-new"><b>[ADD]</b><span class="li-time">12:42:58</span>呼吸动效 favicon 与「幸运今日」每日签文。</li>
          <li class="cat-chg"><b>[INFO]</b><span class="li-time">12:41:20</span>SEO：补全 keywords / og / twitter 标签，利于搜索引擎收录。</li>
          <li class="cat-chg"><b>[INFO]</b><span class="li-time">12:39:47</span>卡片「查看详情」改为同页打开，不再被浏览器拦截。</li>
        </ul>
      </div>
      <div class="mc-ver">
        <div class="mc-ver-head">
          <span class="mc-ver-badge">v13</span>
          <span class="mc-ver-date">2026-09-25 11:20:04</span>
        </div>
        <ul class="mc-ver-list">
          <li class="cat-new"><b>[ADD]</b><span class="li-time">11:20:04</span>「今年进度环」：2026 年已过百分比与剩余天数。</li>
          <li class="cat-new"><b>[ADD]</b><span class="li-time">11:18:37</span>今日一言 3 秒自动轮播，点击可复制。</li>
          <li class="cat-new"><b>[ADD]</b><span class="li-time">11:16:52</span>页面加载「Y」一笔画动画。</li>
        </ul>
      </div>
      <div class="mc-ver">
        <div class="mc-ver-head">
          <span class="mc-ver-badge">v12</span>
          <span class="mc-ver-date">2026-09-25 09:41:50</span>
        </div>
        <ul class="mc-ver-list">
          <li class="cat-new"><b>[ADD]</b><span class="li-time">09:41:50</span>「此刻」板块独立：时钟与天气单独成卡。</li>
          <li class="cat-new"><b>[ADD]</b><span class="li-time">09:40:12</span>翻牌时钟与页脚停留计时。</li>
          <li class="cat-new"><b>[ADD]</b><span class="li-time">09:38:29</span>作品下载次数统计（本地记录）。</li>
          <li class="cat-chg"><b>[INFO]</b><span class="li-time">09:36:44</span>移除语言标签小字，保持欢迎页纯粹。</li>
        </ul>
      </div>
      <div class="mc-ver">
        <div class="mc-ver-head">
          <span class="mc-ver-badge">v10</span>
          <span class="mc-ver-date">2026-09-25 08:15:06</span>
        </div>
        <ul class="mc-ver-list">
          <li class="cat-new"><b>[ADD]</b><span class="li-time">08:15:06</span>节日飘浮：自动拉取中国法定节假日，中秋的月亮与灯笼飘 3 秒。</li>
          <li class="cat-new"><b>[ADD]</b><span class="li-time">08:13:27</span>节日专属欢迎语（春节、端午、中秋等 8 个节日）。</li>
        </ul>
      </div>
      <div class="mc-ver">
        <div class="mc-ver-head">
          <span class="mc-ver-badge">v9</span>
          <span class="mc-ver-date">2026-09-24 21:36:42</span>
        </div>
        <ul class="mc-ver-list">
          <li class="cat-new"><b>[ADD]</b><span class="li-time">21:36:42</span>实时天气（Open-Meteo 免费接口，衢州定位）。</li>
          <li class="cat-new"><b>[ADD]</b><span class="li-time">21:35:08</span>纪念日板块：「活着的第 N 天」与「本站上线第 N 天」。</li>
        </ul>
      </div>
      <div class="mc-ver">
        <div class="mc-ver-head">
          <span class="mc-ver-badge">v7</span>
          <span class="mc-ver-date">2026-09-23 20:15:09</span>
        </div>
        <ul class="mc-ver-list">
          <li class="cat-new"><b>[ADD]</b><span class="li-time">20:15:09</span>「生活瞬间」板块：瑞幸咖啡、网易云音乐、我的世界三块数据。</li>
          <li class="cat-new"><b>[ADD]</b><span class="li-time">20:13:31</span>ROG 幻 16 式错峰滚动：图标先下移进入，文字随后浮现。</li>
          <li class="cat-fix"><b>[FIX]</b><span class="li-time">20:11:44</span>奇异类合集布局错误与键盘异常。</li>
        </ul>
      </div>
      <div class="mc-ver">
        <div class="mc-ver-head">
          <span class="mc-ver-badge">v6</span>
          <span class="mc-ver-date">2026-09-22 22:04:31</span>
        </div>
        <ul class="mc-ver-list">
          <li class="cat-new"><b>[ADD]</b><span class="li-time">22:04:31</span>26 种语言打字机轮播：打出 → 停留 → 逐字消失。</li>
          <li class="cat-new"><b>[ADD]</b><span class="li-time">22:02:56</span>今日一言（hitokoto 联网，失败本地降级）。</li>
          <li class="cat-chg"><b>[INFO]</b><span class="li-time">22:01:19</span>彩蛋模式全部改青色，移除紫色残留。</li>
        </ul>
      </div>
      <div class="mc-ver">
        <div class="mc-ver-head">
          <span class="mc-ver-badge">v4</span>
          <span class="mc-ver-date">2026-09-21 19:28:53</span>
        </div>
        <ul class="mc-ver-list">
          <li class="cat-new"><b>[ADD]</b><span class="li-time">19:28:53</span>精选作品卡片：六个作品上架，支持下载。</li>
          <li class="cat-new"><b>[ADD]</b><span class="li-time">19:27:10</span>5 秒伪进度条，模拟进入作品。</li>
        </ul>
      </div>
      <div class="mc-ver">
        <div class="mc-ver-head">
          <span class="mc-ver-badge">v1</span>
          <span class="mc-ver-date">2026-09-18 09:12:00</span>
        </div>
        <ul class="mc-ver-list">
          <li class="cat-new"><b>[ADD]</b><span class="li-time">09:12:00</span>站点上线：全世界语言的「欢迎你的到来」欢迎页。</li>
          <li class="cat-new"><b>[ADD]</b><span class="li-time">09:10:36</span>深色页脚 + 灰白大字 Yaule，WorkBuddy 风格。</li>
        </ul>
      </div>
    </div>
  </div>
</section>

'''
si = html.index('<section class="section" id="changelog">')
ei = html.index('<section class="section alt" id="bucket">')
html = html[:si] + new_changelog + html[ei:]
changed.append("changelog rewrite")

# ---------- 3. JS：进度条 8 秒 + 加速按钮 + 第 3 秒弹出 ----------
rep("""  var overlay = document.getElementById('loadingOverlay');
  var loadBar = document.getElementById('loadBar');
  var loadPercent = document.getElementById('loadPercent');
  var loadTitle = document.getElementById('loadTitle');
  var loadTimer = null;

  function hideLoading() {
    overlay.classList.remove('active');
    if (loadTimer) { clearInterval(loadTimer); loadTimer = null; }
    loadBar.style.width = '0%';
    loadPercent.textContent = '0%';
  }

  function startLoading(targetUrl, title, openInNew) {
    loadTitle.textContent = title || '正在进入';
    overlay.classList.add('active');
    var progress = 0;
    loadBar.style.width = '0%';
    loadPercent.textContent = '0%';
    loadTimer = setInterval(function () {
      progress += Math.random() * 3;
      if (progress > 95) progress = 95;
      loadBar.style.width = progress + '%';
      loadPercent.textContent = Math.floor(progress) + '%';
    }, 100);
    setTimeout(function () {
      clearInterval(loadTimer); loadTimer = null;
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
    }, 5000);
  }""",
    """  var overlay = document.getElementById('loadingOverlay');
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
  }""",
    "loader 8s + boost")

# ---------- 4. JS：纪念日进度条 + 里程碑 ----------
rep("""    var e1 = document.getElementById('annivDays');
    var e2 = document.getElementById('annivDaysN');
    var e3 = document.getElementById('siteDays');
    var e4 = document.getElementById('siteDaysN');
    if (e1) e1.textContent = a;
    if (e2) e2.textContent = a;
    if (e3) e3.textContent = s;
    if (e4) e4.textContent = s;
  })();""",
    """    var e1 = document.getElementById('annivDays');
    var e2 = document.getElementById('annivDaysN');
    var e3 = document.getElementById('siteDays');
    var e4 = document.getElementById('siteDaysN');
    if (e1) e1.textContent = a;
    if (e2) e2.textContent = a;
    if (e3) e3.textContent = s;
    if (e4) e4.textContent = s;
    // 生命进度条：以 80 岁（29200 天）为参考
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
    "anniv js progress")

# ---------- 5. JS：年份环改为剩余天数大字 ----------
rep("""    var ring = document.getElementById('yearRing');
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
    }""",
    """    var ring = document.getElementById('yearRing');
    var leftNum = document.getElementById('yearLeftNum');
    var pctText = document.getElementById('yearPctText');
    if (!ring || !leftNum) return;
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
      leftNum.textContent = left;
      if (pctText) pctText.textContent = y + ' 年已过 ' + pct + '%';
    }""",
    "year ring js")

# ---------- 6. JS：主页日志同步写入 localStorage（供详细日志页读取） ----------
rep("""  /* ========== 页面加载动画移除 ========== */""",
    """  /* ========== 更新日志同步：写入 localStorage（供 changelog.html 读取） ========== */
  (function () {
    try {
      var items = [];
      document.querySelectorAll('.mc-ver').forEach(function (v) {
        var badge = v.querySelector('.mc-ver-badge');
        var date = v.querySelector('.mc-ver-date');
        var list = [];
        v.querySelectorAll('.mc-ver-list li').forEach(function (li) {
          var b = li.querySelector('b');
          var t = li.querySelector('.li-time');
          var text = li.textContent || '';
          if (b) text = text.replace(b.textContent, '');
          if (t) text = text.replace(t.textContent, '');
          list.push({
            lv: b ? b.textContent : '',
            time: t ? t.textContent : '',
            text: text.trim()
          });
        });
        items.push({
          ver: badge ? badge.textContent : '',
          date: date ? date.textContent : '',
          current: v.classList.contains('current'),
          list: list
        });
      });
      localStorage.setItem('yaule_changelog', JSON.stringify(items));
    } catch (e) {}
  })();

  /* ========== 页面加载动画移除 ========== */""",
    "changelog sync ls")

open(path, "w", encoding="utf-8").write(html)
print("CHANGED:", ", ".join(changed))
print("DONE part2")
