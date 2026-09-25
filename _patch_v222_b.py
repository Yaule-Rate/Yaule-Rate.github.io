# -*- coding: utf-8 -*-
"""v22.2 脚本 B：JS —— 深夜一言池/星星、留言板(防注入+违禁词)、热力图、i18n 键、applyLang 增强"""
p = "index.html"
s = open(p, encoding="utf-8").read()
OPS = []
def rep(o, n, t):
    OPS.append((o, n, t))

# ---- 1. I18N 键 zh/en ----
rep("""      'footer.contact': '联系', 'footer.email': '邮箱', 'footer.rss': 'RSS 订阅', 'footer.visit1': '本站访问', 'footer.visit2': ' 次',""",
    """      'footer.contact': '联系', 'footer.email': '邮箱', 'footer.rss': 'RSS 订阅', 'footer.visit1': '本站访问', 'footer.visit2': ' 次',
      'heatmap.h2': '开源足迹', 'heatmap.desc': '过去一年在 GitHub 上的每一天，青色越深代表越活跃。',
      'guestbook.h2': '访客留言板', 'guestbook.desc': '来过的人都可以留下一句话。提交后跳转 GitHub 确认，内容同步显示在这里。',
      'guestbook.name': '昵称', 'guestbook.text': '想说的话（300 字以内）', 'guestbook.submit': '写下留言',
      'guestbook.load': '正在读取留言…', 'guestbook.empty': '还没有留言，来做第一个吧。', 'guestbook.loadfail': '暂时读不到留言（网络或接口限制），稍后再来看看。',""", "i18n zh")
rep("""      'footer.contact': 'Contact', 'footer.email': 'Email', 'footer.rss': 'RSS Feed', 'footer.visit1': 'Visits', 'footer.visit2': '',""",
    """      'footer.contact': 'Contact', 'footer.email': 'Email', 'footer.rss': 'RSS Feed', 'footer.visit1': 'Visits', 'footer.visit2': '',
      'heatmap.h2': 'Open-Source Footprint', 'heatmap.desc': 'Every day on GitHub over the past year — the deeper the cyan, the more active.',
      'guestbook.h2': 'Guestbook', 'guestbook.desc': 'Leave a word if you have been here. Submitting opens GitHub to confirm, then it shows up here.',
      'guestbook.name': 'Nickname', 'guestbook.text': 'Your message (up to 300 chars)', 'guestbook.submit': 'Leave a message',
      'guestbook.load': 'Loading messages…', 'guestbook.empty': 'No messages yet. Be the first!', 'guestbook.loadfail': 'Could not load messages right now (network or rate limit). Check back later.',""", "i18n en")

# ---- 2. applyLang：placeholder + 热力图合计 ----
rep("""    document.querySelectorAll('[data-i18n]').forEach(function (el) {
      var k = el.getAttribute('data-i18n');
      if (I18N[L] && k in I18N[L]) el.textContent = I18N[L][k];
    });""",
    """    document.querySelectorAll('[data-i18n]').forEach(function (el) {
      var k = el.getAttribute('data-i18n');
      if (I18N[L] && k in I18N[L]) el.textContent = I18N[L][k];
    });
    document.querySelectorAll('[data-i18n-ph]').forEach(function (el) {
      var kp = el.getAttribute('data-i18n-ph');
      if (I18N[L] && kp in I18N[L]) el.setAttribute('placeholder', I18N[L][kp]);
    });""", "applyLang placeholder")
rep("""    document.querySelectorAll('.card-dl').forEach(function (a) { a.title = L === 'en' ? 'Download work' : '下载作品'; });
    window.dispatchEvent(new CustomEvent('yaule-langchange'));""",
    """    document.querySelectorAll('.card-dl').forEach(function (a) { a.title = L === 'en' ? 'Download work' : '下载作品'; });
    if (window.__renderHmTotal) window.__renderHmTotal();
    window.dispatchEvent(new CustomEvent('yaule-langchange'));""", "applyLang 热力图合计")

# ---- 3. 深夜一言池（ENQ 后） ----
rep("""      ['Every night is a new version of you.', 'Yaule']
    ];
    function render(q) {""",
    """      ['Every night is a new version of you.', 'Yaule']
    ];
    var NIGHTQ = [
      ['深夜适合想念，也适合慢慢把事情做完。', 'Yaule'],
      ['失眠夜不孤单，还有代码陪你。', 'Yaule'],
      ['月亮不睡我不睡，我是人间小宝贝。', '网络'],
      ['晚安，世界；早安，自己。', 'Yaule'],
      ['夜晚是白天的另一个版本，安静而有光。', 'Yaule'],
      ['把今天熬成明天，把咖啡换成月亮。', 'Yaule'],
      ['夜再深，星星也会替你点灯。', 'Yaule'],
      ['凌晨的风很轻，适合想一些重要的小事。', 'Yaule']
    ];
    function isNight() { var hh = new Date().getHours(); return hh >= 22 || hh < 6; }
    function render(q) {""", "深夜一言池")
rep("""      var pool = (window.YAULE_LANG === 'en') ? ENQ : quotes;""",
    """      var pool = (window.YAULE_LANG === 'en') ? ENQ : (isNight() ? NIGHTQ : quotes);""", "pickLocal 深夜分支")

# ---- 4. 深夜星星 + 留言板 + 热力图（幸运今日前） ----
rep("""  /* ========== 幸运今日（按日期固定） ========== */""",
    """  /* ========== 深夜特调：22:00-06:00 星空 + 月亮 ========== */
  (function () {
    var hh = new Date().getHours();
    if (hh >= 22 || hh < 6) {
      document.body.classList.add('night');
      var sky = document.getElementById('nightSky');
      if (sky) {
        var frag = document.createDocumentFragment();
        for (var i = 0; i < 46; i++) {
          var st = document.createElement('span');
          st.className = 'night-star';
          st.style.left = (Math.random() * 100) + '%';
          st.style.top = (Math.random() * 100) + '%';
          st.style.animationDelay = (Math.random() * 3.2) + 's';
          st.style.animationDuration = (2.5 + Math.random() * 3) + 's';
          frag.appendChild(st);
        }
        sky.appendChild(frag);
      }
    }
  })();

  /* ========== 访客留言板（GitHub Issues 驱动，防注入 + 违禁词） ========== */
  (function () {
    var REPO = 'Yaule-Rate/Yaule-Rate.github.io';
    var list = document.getElementById('gbList');
    var form = document.getElementById('gbForm');
    var hint = document.getElementById('gbHint');
    var nameEl = document.getElementById('gbName');
    var textEl = document.getElementById('gbText');
    var badWords = ['色情', '赌博', '博彩', '诈骗', '传销', '刷单', '毒品', '冰毒', '海洛因', '大麻', '违禁品', '假币', '枪支', '裸聊', '约炮', '援交', '代购'];
    function hasBad(t) {
      var low = String(t || '').toLowerCase();
      for (var i = 0; i < badWords.length; i++) { if (low.indexOf(badWords[i]) !== -1) return true; }
      if (/<script|javascript:|onerror=|onclick=|<iframe|<svg/i.test(low)) return true;
      return false;
    }
    function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
    function fmtTime(t) {
      var d = new Date(t);
      if (isNaN(d.getTime())) return '';
      return d.toLocaleDateString() + ' ' + d.toTimeString().slice(0, 5);
    }
    function syncNewI18n() {
      var L = window.YAULE_LANG;
      if (!L || !window.I18N) return;
      document.querySelectorAll('#gbList [data-i18n]').forEach(function (el) {
        var k2 = el.getAttribute('data-i18n');
        if (k2 in window.I18N[L]) el.textContent = window.I18N[L][k2];
      });
    }
    function load() {
      fetch('https://api.github.com/repos/' + REPO + '/issues?state=all&sort=created&direction=desc&per_page=20')
        .then(function (r) { if (!r.ok) throw new Error('http'); return r.json(); })
        .then(function (arr) {
          var msgs = (arr || []).filter(function (it) { return it && it.title && it.title.indexOf('[留言]') === 0; });
          if (!msgs.length) {
            list.innerHTML = '<p class="gb-empty" data-i18n="guestbook.empty">还没有留言，来做第一个吧。</p>';
            syncNewI18n();
            return;
          }
          var html = '';
          msgs.forEach(function (m) {
            html += '<div class="gb-item"><div class="gb-head"><b>' + esc(m.user ? m.user.login : 'guest') + '</b><span>' + esc(fmtTime(m.created_at)) + '</span></div><div class="gb-body">' + esc(m.body || '') + '</div></div>';
          });
          list.innerHTML = html;
        })
        .catch(function () {
          list.innerHTML = '<p class="gb-empty" data-i18n="guestbook.loadfail">暂时读不到留言（网络或接口限制），稍后再来看看。</p>';
          syncNewI18n();
        });
    }
    var CD_KEY = 'yaule_gb_cd';
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var en = window.YAULE_LANG === 'en';
      var name = String(nameEl.value || '').trim().slice(0, 20);
      var body = String(textEl.value || '').trim().slice(0, 300);
      if (!name) { hint.textContent = en ? 'Please enter a nickname.' : '请先填写昵称。'; hint.className = 'gb-hint err'; return; }
      if (!body) { hint.textContent = en ? 'Please write something.' : '请写下想说的话。'; hint.className = 'gb-hint err'; return; }
      if (hasBad(name) || hasBad(body)) { hint.textContent = en ? 'Contains banned words, please rewrite.' : '内容包含违禁词，请修改后重试。'; hint.className = 'gb-hint err'; return; }
      var cd = 0;
      try { cd = parseInt(localStorage.getItem(CD_KEY) || '0', 10) || 0; } catch (err) {}
      if (Date.now() < cd) {
        var left = Math.ceil((cd - Date.now()) / 1000);
        hint.textContent = en ? 'Please wait ' + left + 's before the next message.' : '请 ' + left + ' 秒后再留言。';
        hint.className = 'gb-hint err';
        return;
      }
      try { localStorage.setItem(CD_KEY, String(Date.now() + 30000)); } catch (err) {}
      var title = '[留言] ' + name;
      var issueBody = body + '\\n\\n---\\nvia guestbook on ' + new Date().toLocaleString();
      var url = 'https://github.com/' + REPO + '/issues/new?title=' + encodeURIComponent(title) + '&body=' + encodeURIComponent(issueBody);
      var w = window.open(url, '_blank');
      if (w) w.opener = null;
      hint.textContent = en ? 'Opened GitHub. Sign in and click \\"Submit new issue\\" to publish.' : '已跳转 GitHub，登录后点击「Submit new issue」即可发布。';
      hint.className = 'gb-hint';
      textEl.value = '';
    });
    load();
  })();

  /* ========== 开源足迹 · GitHub 贡献热力图 ========== */
  (function () {
    var grid = document.getElementById('hmGrid');
    var totalEl = document.getElementById('hmTotal');
    if (!grid || !totalEl) return;
    var lastSum = 0;
    function paint(contribs) {
      var html = '';
      var sum = 0;
      contribs.forEach(function (c) {
        var lvl = c.level || 0;
        if (lvl > 4) lvl = 4;
        sum += (c.count || 0);
        html += '<span class="hm-cell l' + lvl + '" title="' + esc(c.date) + ': ' + (c.count || 0) + '"></span>';
      });
      lastSum = sum;
      grid.innerHTML = html;
      window.__renderHmTotal();
    }
    function fallback() {
      var arr = [];
      var d = new Date();
      for (var i = 0; i < 365; i++) {
        d.setDate(d.getDate() - 1);
        var w = d.getDay();
        var n = 0;
        if (i % 13 === 0) n = 3 + (i % 5);
        else if (i % 29 === 0) n = 1;
        if (w === 0 || w === 6) n = 0;
        arr.push({ date: d.toISOString().slice(0, 10), count: n, level: n >= 4 ? 4 : n });
      }
      arr.reverse();
      paint(arr);
      window.__hmFallback = true;
      window.__renderHmTotal();
    }
    window.__renderHmTotal = function () {
      var en = window.YAULE_LANG === 'en';
      totalEl.textContent = window.__hmFallback
        ? (en ? 'Preview data (API unavailable)' : '预览数据（接口暂不可用）')
        : (en ? 'Contributions in the last year: ' + lastSum : '过去一年累计贡献：' + lastSum);
    };
    fetch('https://github-contributions-api.jogruber.de/v4/user/Yaule-Rate?y=last')
      .then(function (r) { if (!r.ok) throw new Error('http'); return r.json(); })
      .then(function (d) {
        var contribs = d && d.contributions;
        if (!contribs || !contribs.length) throw new Error('empty');
        paint(contribs);
      })
      .catch(function () { fallback(); });
  })();

  /* ========== 幸运今日（按日期固定） ========== */""", "深夜星星+留言板+热力图")

bad = [(t, s.count(o)) for (o, _, t) in OPS if s.count(o) != 1]
if bad:
    for t, c in bad:
        print("锚点失败(%d): %s" % (c, t))
    raise SystemExit(1)
for (o, n, t) in OPS:
    s = s.replace(o, n, 1)
open(p, "w", encoding="utf-8").write(s)
print("B ok:", len(OPS))
