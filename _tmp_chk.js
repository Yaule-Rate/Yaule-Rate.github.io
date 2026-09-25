
  document.getElementById('year').textContent = new Date().getFullYear();

  /* ========== Toast ========== */
  var toastEl = document.getElementById('toast');
  var toastTimer = null;
  function showToast(msg) {
    toastEl.textContent = msg;
    toastEl.classList.add('show');
    if (toastTimer) clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { toastEl.classList.remove('show'); }, 2600);
  }

  /* ========== 查看更多按钮 ========== */
  var btn = document.getElementById('btnMore');
  var hiddenCards = document.querySelectorAll('.card.hidden');
  var expanded = false;
  btn.addEventListener('click', function () {
    expanded = !expanded;
    hiddenCards.forEach(function (c) { c.classList.toggle('hidden', !expanded); });
    btn.textContent = expanded ? '收起 ↑' : '查看更多 ↓';
  });

  /* ========== 伪进度条加载（修复：新标签页打开后自动隐藏 + bfcache 返回残留） ========== */
  var overlay = document.getElementById('loadingOverlay');
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
      } else if (pendingUrl) {
        window.location.href = pendingUrl;
      } else {
        // 开屏模式：无跳转，淡出遮罩停留本页；带锚点（如 #changelog）则滚回该处
        hideLoading();
        if (location.hash) {
          var el = document.getElementById(location.hash.slice(1));
          if (el && el.scrollIntoView) el.scrollIntoView({ behavior: 'auto' });
        }
      }
    }, 250);
  }

  function startLoading(targetUrl, title, openInNew) {
    loadTitle.textContent = title || '正在进入';
    overlay.classList.add('active');
    var LOAD_LINES = [
      '正在泡咖啡…', '正在数星星…', '正在整理作品…', '正在点亮灯笼…',
      '正在问候全世界…', '正在翻今天的日记…', '正在检查进度条…', '正在等你…'
    ];
    if (loadHint) loadHint.textContent = LOAD_LINES[Math.floor(Math.random() * LOAD_LINES.length)];
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
      var inc = 2 + hold * 4;
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

  document.querySelectorAll('a[data-loading]').forEach(function (link) {
    link.addEventListener('click', function (e) {
      e.preventDefault();
      var title = this.getAttribute('data-loading');
      var url = this.getAttribute('href');
      var openInNew = this.getAttribute('target') === '_blank';
      startLoading(url, title, openInNew);
    });
  });

  // 修复：浏览器后退（bfcache 恢复）时进度条残留 —— 同时重播 Y 一笔画开屏
  window.addEventListener('pageshow', function (e) {
    if (e.persisted) { playSplash(true); return; }
    if (overlay.classList.contains('active')) hideLoading();
  });

  /* ========== 作品卡分享按钮（微博 / QQ 带文案） ========== */
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
        ? base.replace(/\/[^/]*$/, '/') + detail
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

  /* ========== 下载按钮（不触发进度条，直接下载） ========== */
  document.querySelectorAll('.card-dl').forEach(function (dl) {
    dl.addEventListener('click', function (e) {
      e.stopPropagation();
      e.preventDefault();
      var url = this.getAttribute('href');
      var name = this.getAttribute('download') || 'download.html';
      var a = document.createElement('a');
      a.href = url;
      a.download = name;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      showToast('开始下载 ' + name);
    });
  });

  // 作品卡片：点卡片展开预览；点「查看详情」打开作品；下载按钮除外
  document.querySelectorAll('.card').forEach(function (card) {
    card.addEventListener('click', function (e) {
      if (e.target.closest('.card-dl')) return;
      if (e.target.closest('a.card-image')) {
        e.preventDefault();
        this.classList.toggle('expanded');
        return;
      }
      if (e.target.closest('.meta')) {
        var dd = this.getAttribute('data-detail');
        if (dd) { window.location.href = dd; return; }
        var link = this.querySelector('a.card-image');
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
  });

  /* ========== 首屏：全世界语言的欢迎轮播（循环）+ 小字逐字打字机 ========== */
  (function () {
    var langs = [
      ['Welcome to You', '英语'],
      ['Bienvenue à toi', '法语'],
      ['Bienvenido a ti', '西班牙语'],
      ['Willkommen bei dir', '德语'],
      ['Benvenuto da te', '意大利语'],
      ['Vítejte u vás', '捷克语'],
      ['Witamy u Ciebie', '波兰语'],
      ['Tervetuloa luoksesi', '芬兰语'],
      ['Välkommen till dig', '瑞典语'],
      ['Üdvözöljük nálad', '匈牙利语'],
      ['Добре дошли при теб', '保加利亚语'],
      ['Bine ai venit la tine', '罗马尼亚语'],
      ['Καλώς ήρθες', '希腊语'],
      ['ברוך הבא אליך', '希伯来语'],
      ['أهلاً بك', '阿拉伯语'],
      ['Merhaba, hoş geldin', '土耳其语'],
      ['स्वागत है आपका', '印地语'],
      ['ยินดีต้อนรับ', '泰语'],
      ['Xin chào bạn', '越南语'],
      ['Selamat datang kepada anda', '印尼语'],
      ['ようこそ', '日语'],
      ['어서 오세요', '韩语'],
      ['Bem-vindo a você', '葡萄牙语'],
      ['Welkom bij jou', '荷兰语'],
      ['歡迎你的到來', '繁体中文'],
      ['欢迎你的到来', '中文']
    ];
    var roamer = document.getElementById('langRoamer');
    var enTitle = document.getElementById('enTitle');
    var intro = document.getElementById('intro');
    var scrollHint = document.getElementById('scrollHint');

    // 小字与向下滚动：一进来就一直存在
    var quoteRow = document.getElementById('quoteRow');
    enTitle.classList.add('show');
    scrollHint.classList.add('show');
    intro.classList.add('show');
    quoteRow.classList.add('show');

    // 大标题：全世界语言轮播 · 打字机（缓慢打出 → 停留 → 逐字消失 → 切换）
    var li = 0;
    function roamNext() {
      li = (li + 1) % langs.length;
      roamType();
    }
    function roamType() {
      var text = langs[li][0];
      var len = text.length;
      var c = 0;
      roamer.textContent = '';
      roamer.classList.add('show');
      // 缓慢打出
      (function type() {
        c++;
        roamer.textContent = text.slice(0, c);
        if (c < len) {
          setTimeout(type, 55);
        } else {
          setTimeout(erase, 1300);
        }
      })();
      // 逐字消失（打印机倒放）
      function erase() {
        c--;
        if (c > 0) {
          roamer.textContent = text.slice(0, c);
          setTimeout(erase, 55);
        } else {
          roamer.textContent = '';
          setTimeout(roamNext, 320);
        }
      }
    }
    setTimeout(roamType, 300);
  })();



  (function () {
    // 锚点：2026-09-24，与上线日对齐；之后随时间自动增长
    var ANCHOR = new Date(2026, 8, 24);
    var d = Math.max(0, Math.floor((Date.now() - ANCHOR.getTime()) / 86400000));
    var cups = 176 + Math.floor(d / 3);
    var songs = 305 + Math.floor(d / 2);
    var hours = 2000 + Math.floor(d / 2) * 25.7;
    document.getElementById('cups').innerHTML = cups + '<small>杯</small>';
    document.getElementById('songs').textContent = songs;
    document.getElementById('hours').textContent = Math.floor(hours);
  })();

  /* ========== ROG 幻16 式错峰滚动（图标先下移进入，文字随后浮现） ========== */
  (function () {
    var panels = document.querySelectorAll('.life-panel');
    if (!('IntersectionObserver' in window)) return;
    panels.forEach(function (c) { c.classList.add('pending'); });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('in-view');
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -8% 0px' });
    panels.forEach(function (c) { io.observe(c); });
    setTimeout(function () {
      panels.forEach(function (c) {
        if (!c.classList.contains('in-view')) {
          var rr = c.getBoundingClientRect();
          if (rr.top < window.innerHeight) c.classList.add('in-view');
        }
      });
    }, 2500);
  })();


  (function () {
    var tabs = document.querySelectorAll('.life-tab');
    var panels = {
      coffee: document.getElementById('lifeCoffee'),
      music: document.getElementById('lifeMusic'),
      game: document.getElementById('lifeGame')
    };
    tabs.forEach(function (tab) {
      tab.addEventListener('click', function () {
        if (this.classList.contains('active')) return;
        tabs.forEach(function (t) { t.classList.remove('active'); });
        this.classList.add('active');
        var key = this.getAttribute('data-life');
        Object.keys(panels).forEach(function (k2) { panels[k2].classList.remove('active'); });
        setTimeout(function () { panels[key].classList.add('active'); }, 70);
      });
    });
  })();

  /* ========== 我的世界：布吉岛 / 花雨亭 切换 ========== */
  (function () {
    var tabs = document.querySelectorAll('.mc-subtab');
    var bjd = document.getElementById('mcPanelBJD');
    var hyt = document.getElementById('mcPanelHYT');
    tabs.forEach(function (tab) {
      tab.addEventListener('click', function () {
        tabs.forEach(function (t) { t.classList.remove('active'); });
        this.classList.add('active');
        var key = this.getAttribute('data-server');
        if (key === 'bjd') { bjd.classList.remove('hidden'); hyt.classList.add('hidden'); }
        else { hyt.classList.remove('hidden'); bjd.classList.add('hidden'); }
      });
    });
  })();

  /* ========== 实时时钟 ========== */
  (function () {
    var timeEl = document.getElementById('clockTime');
    var dateEl = document.getElementById('clockDate');
    var week = ['日', '一', '二', '三', '四', '五', '六'];
    var prev = '';
    function tick() {
      var d = new Date();
      var hh = String(d.getHours()).padStart(2, '0');
      var mm = String(d.getMinutes()).padStart(2, '0');
      var ss = String(d.getSeconds()).padStart(2, '0');
      var s = hh + ':' + mm + ':' + ss;
      var html = '';
      for (var i = 0; i < s.length; i++) {
        var ch = s[i];
        if (ch === ':') {
          html += '<span class="fl-colon">:</span>';
          continue;
        }
        var pch = i < prev.length ? prev[i] : '';
        if (pch && pch !== ch) {
          html += '<span class="flip-digit"><span class="fl-old">' + pch + '</span><span class="fl-new">' + ch + '</span></span>';
        } else {
          html += '<span class="flip-digit">' + ch + '</span>';
        }
      }
      timeEl.innerHTML = html;
      prev = s;
      dateEl.textContent = d.getFullYear() + ' 年 ' + (d.getMonth() + 1) + ' 月 ' + d.getDate() + ' 日 · 星期' + week[d.getDay()];
    }
    tick();
    setInterval(tick, 1000);
  })();

  /* ========== 今日一言（每日一句，点击换一句） ========== */
  (function () {
    var quotes = [
      ['保持好奇，缓慢生长。', 'Yaule'],
      ['每一行代码，都是对世界的一次回应。', 'Yaule'],
      ['夜里睡不着，就写点东西吧。', 'Yaule'],
      ['生活不止眼前的 Bug，还有诗和远方。', '佚名'],
      ['把每一天，当作一次新的版本迭代。', 'Yaule'],
      ['咖啡续命，代码养魂。', 'Yaule'],
      ['慢慢来，比较快。', '佚名'],
      ['热爱可抵岁月漫长。', '佚名'],
      ['写下的，终会有人看见。', 'Yaule'],
      ['不赶路，去感受路。', '佚名'],
      ['做自己喜欢的事，顺便养活自己。', '佚名'],
      ['种一棵树最好的时间是十年前，其次是现在。', '谚语'],
      ['黑夜给了我黑色的眼睛，我却用它寻找光明。', '顾城'],
      ['路漫漫其修远兮，吾将上下而求索。', '屈原'],
      ['千磨万击还坚劲，任尔东西南北风。', '郑燮'],
      ['长风破浪会有时，直挂云帆济沧海。', '李白'],
      ['会当凌绝顶，一览众山小。', '杜甫'],
      ['山重水复疑无路，柳暗花明又一村。', '陆游'],
      ['沉舟侧畔千帆过，病树前头万木春。', '刘禹锡'],
      ['欲穷千里目，更上一层楼。', '王之涣'],
      ['千里之行，始于足下。', '老子'],
      ['知人者智，自知者明。', '老子'],
      ['天行健，君子以自强不息。', '《周易》'],
      ['业精于勤，荒于嬉；行成于思，毁于随。', '韩愈'],
      ['纸上得来终觉浅，绝知此事要躬行。', '陆游'],
      ['问渠那得清如许？为有源头活水来。', '朱熹'],
      ['世上无难事，只怕有心人。', '谚语'],
      ['宝剑锋从磨砺出，梅花香自苦寒来。', '《警世贤文》'],
      ['Stay hungry, stay foolish.', 'Steve Jobs'],
      ['The only way to do great work is to love what you do.', 'Steve Jobs']
    ];
    var text = document.getElementById('quoteText');
    var next = document.getElementById('quoteNext');
    var cur = 0;
    function render(q) {
      text.textContent = '“' + q[0] + '”' + (q[1] ? ' —— ' + q[1] : '');
    }
    function fetchNet(ok) {
      var ctrl = ('AbortController' in window) ? new AbortController() : null;
      var timer = setTimeout(function () { if (ctrl) ctrl.abort(); }, 4500);
      fetch('https://v1.hitokoto.cn/?encode=json&charset=utf-8', ctrl ? { signal: ctrl.signal } : {})
        .then(function (r) { return r.json(); })
        .then(function (d) {
          clearTimeout(timer);
          ok(d && d.hitokoto ? [d.hitokoto, d.from || ''] : null);
        })
        .catch(function () { clearTimeout(timer); ok(null); });
    }
    function pickLocal(random) {
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
    }
    // 一言：每 3 秒自动换（联网优先，失败本地随机）；点击复制
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
  })();

  /* ========== 主题切换（深色 / 浅色；22:00–06:00 自动深色，手动选择优先） ========== */
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
  })();

  /* ========== 每日推荐：按日期从歌单取一首，跳网易云搜索 ========== */
  (function () {
    var DAILY_SONGS = [
      ['起风了', '买辣椒也用券'],
      ['平凡之路', '朴树'],
      ['夜空中最亮的星', '逃跑计划'],
      ['晴天', '周杰伦'],
      ['光年之外', 'G.E.M. 邓紫棋'],
      ['海阔天空', 'Beyond'],
      ['稻香', '周杰伦'],
      ['Shape of You', 'Ed Sheeran'],
      ['人间', '王菲'],
      ['成都', '赵雷'],
      ['Viva La Vida', 'Coldplay'],
      ['千千阙歌', '陈慧娴']
    ];
    var link = document.getElementById('dailySong');
    if (link) {
      var d = new Date();
      var key = d.getFullYear() * 10000 + (d.getMonth() + 1) * 100 + d.getDate();
      var song = DAILY_SONGS[key % DAILY_SONGS.length];
      link.textContent = song[0] + ' — ' + song[1];
      link.href = 'https://music.163.com/#/search/m/?s=' + encodeURIComponent(song[0] + ' ' + song[1]);
    }
  })();

  /* ========== 天气：Open-Meteo 免费接口（衢州 28.94, 118.87） ========== */
  (function () {
    var icon = document.getElementById('weatherIcon');
    var txt = document.getElementById('weatherText');
    if (!icon || !txt) return;
    function svgFor(code) {
      var cloud = '<path d="M17.5 19H9a7 7 0 1 1 6.71-9h1.79a4.5 4.5 0 1 1 0 9Z"/>';
      if (code === 0) {
        return '<circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/>';
      }
      if (code <= 3) return cloud;
      if (code <= 48) return cloud + '<line x1="7" y1="15" x2="7" y2="18"/><line x1="12" y1="15" x2="12" y2="18"/><line x1="17" y1="15" x2="17" y2="18"/>';
      if (code <= 67) return cloud + '<line x1="7" y1="17" x2="7" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/><line x1="17" y1="17" x2="17" y2="21"/>';
      if (code <= 77) return cloud + '<line x1="8" y1="17" x2="8" y2="21"/><line x1="16" y1="17" x2="16" y2="21"/>';
      if (code <= 82) return cloud + '<line x1="7" y1="17" x2="7" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/><line x1="17" y1="17" x2="17" y2="21"/>';
      if (code <= 86) return cloud + '<line x1="8" y1="17" x2="8" y2="21"/><line x1="16" y1="17" x2="16" y2="21"/>';
      return cloud + '<polyline points="13 12 11 16 14 16 12 20"/>';
    }
    function textFor(code) {
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
    fetch('https://api.open-meteo.com/v1/forecast?latitude=28.94&longitude=118.87&current=temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m,uv_index&timezone=Asia%2FShanghai&forecast_days=1')
      .then(function (r) { if (!r.ok) throw new Error('weather'); return r.json(); })
      .then(function (d) {
        var c = d.current;
        icon.innerHTML = svgFor(c.weather_code);
        txt.innerHTML = '<span>衢州</span><span class="weather-temp">' + Math.round(c.temperature_2m) + '°C</span><span>' + textFor(c.weather_code) + '</span>';
        var fe = document.getElementById('wFeels');
        var hu = document.getElementById('wHum');
        var wi = document.getElementById('wWind');
        var uv = document.getElementById('wUvi');
        if (fe) fe.textContent = Math.round(c.apparent_temperature);
        if (hu) hu.textContent = Math.round(c.relative_humidity_2m);
        if (wi) wi.textContent = Math.round(c.wind_speed_10m);
        if (uv) uv.textContent = Math.round(c.uv_index);
      })
      .catch(function () { txt.textContent = '衢州 · 天气暂时不可用'; });
  })();

  /* ========== 纪念日：活着第几天 / 网站上线天数 ========== */
  (function () {
    function daysSince(y, m, d) {
      var start = new Date(y, m - 1, d);
      var now = new Date();
      now.setHours(0, 0, 0, 0);
      return Math.floor((now - start) / 86400000) + 1;
    }
    var a = daysSince(2012, 1, 17);
    var s = daysSince(2026, 9, 18);
    var e1 = document.getElementById('annivDays');
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
  })();

  /* ========== 节日飘浮：自动拉取中国法定节假日，节日当天飘 3 秒 ========== */
  (function () {
    var layer = document.getElementById('festLayer');
    if (!layer) return;
    var GREETING = {
      '春节': '新年快乐，万事顺遂。',
      '除夕': '辞旧迎新，灯火可亲。',
      '元宵节': '元宵喜乐，阖家团圆。',
      '清明节': '气清景明，万物皆显。',
      '劳动节': '辛苦了，今天属于你。',
      '端午节': '端午安康，粽叶飘香。',
      '中秋节': '今晚的月亮，借你一半。',
      '国庆节': '山河远阔，人间烟火。'
    };
    var FEST = {
      '春节': ['lantern', 'firework', 'lantern', 'couplet'],
      '除夕': ['lantern', 'firework'],
      '元宵节': ['lantern', 'tangyuan'],
      '清明节': ['willow', 'rain'],
      '劳动节': ['star', 'firework'],
      '端午节': ['zongzi', 'zongzi', 'dragonboat'],
      '中秋节': ['mooncake', 'lantern', 'rabbit', 'mooncake'],
      '国庆节': ['flag', 'firework', 'flag', 'star']
    };
    var ICONS = {
      mooncake: '🥮', lantern: '🏮', rabbit: '🐇', zongzi: '🫔',
      dragonboat: '🛶', firework: '🎆', willow: '🌿', rain: '🌧️',
      flag: '🎇', star: '⭐', tangyuan: '🍡', couplet: '🧧'
    };
    var year = new Date().getFullYear();
    var url = 'https://raw.githubusercontent.com/NateScarlet/holiday-cn/master/' + year + '.json';
    fetch(url)
      .then(function (r) { if (!r.ok) throw new Error('holiday'); return r.json(); })
      .then(function (data) {
        var now = new Date();
        var ymd = now.getFullYear() + '-' + String(now.getMonth() + 1).padStart(2, '0') + '-' + String(now.getDate()).padStart(2, '0');
        var matched = null;
        (data.days || []).forEach(function (day) {
          if (day.date === ymd && day.isOffDay) matched = day;
        });
        if (!matched) return;
        var gEl = document.getElementById('festGreeting');
        if (gEl && GREETING[matched.name]) {
          gEl.textContent = GREETING[matched.name];
          gEl.classList.add('show');
        }
        var icons = FEST[matched.name] || ['star', 'firework'];
        for (var i = 0; i < 7; i++) {
          (function (i) {
            var el = document.createElement('span');
            el.className = 'fest-item';
            el.style.left = (6 + Math.random() * 86) + '%';
            el.style.fontSize = (34 + Math.random() * 34) + 'px';
            el.style.animationDelay = (Math.random() * 0.9) + 's';
            el.style.animationDuration = (2.6 + Math.random() * 1.1) + 's';
            el.textContent = ICONS[icons[i % icons.length]];
            layer.appendChild(el);
            setTimeout(function () { el.remove(); }, 4200);
          })(i);
        }
      })
      .catch(function () {});
  })();

  /* ========== 页面停留计时 ========== */
  (function () {
    var el = document.getElementById('stayTime');
    if (!el) return;
    var start = Date.now();
    function update() {
      var sec = Math.floor((Date.now() - start) / 1000);
      var m = Math.floor(sec / 60);
      var s = sec % 60;
      el.innerHTML = '已停留 <b>' + m + '</b> 分 <b>' + s + '</b> 秒';
    }
    update();
    setInterval(update, 1000);
  })();

  /* ========== 作品下载计数（localStorage） ========== */
  (function () {
    var KEY = 'yaule_dl_count';
    var store = {};
    try { store = JSON.parse(localStorage.getItem(KEY) || '{}') || {}; } catch (e) {}
    function nameOf(card) {
      var dl = card.querySelector('.card-dl');
      return dl ? (dl.getAttribute('download') || 'unknown') : 'unknown';
    }
    document.querySelectorAll('.card').forEach(function (card) {
      var body = card.querySelector('.card-body');
      if (!body) return;
      var badge = document.createElement('span');
      badge.className = 'card-dl-count';
      badge.textContent = '下载 ' + (store[nameOf(card)] || 0) + ' 次';
      body.appendChild(badge);
    });
    document.querySelectorAll('.card-dl').forEach(function (dl) {
      dl.addEventListener('click', function () {
        var card = this.closest('.card');
        var name = nameOf(card);
        store[name] = (store[name] || 0) + 1;
        try { localStorage.setItem(KEY, JSON.stringify(store)); } catch (e) {}
        var badge = card ? card.querySelector('.card-dl-count') : null;
        if (badge) badge.textContent = '下载 ' + store[name] + ' 次';
      }, true);
    });
  })();

  /* ========== 今年进度环 ========== */
  (function () {
    var ring = document.getElementById('yearRing');
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
      if (pctText) pctText.textContent = '今年已过 ' + pct + '%';
    }
    update();
    setInterval(update, 60000);
  })();

  /* ========== 更新日志同步：写入 localStorage（供 changelog.html 读取） ========== */
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

  /* ========== 开屏动画：青色 Y 一笔画（每次进入本站均播放，含作品页返回 / 浏览器后退） ========== */
  var splashTimer = null;
  function playSplash(restart) {
    if (splashTimer) { clearTimeout(splashTimer); splashTimer = null; }
    var loader = document.getElementById('pageLoader');
    if (!loader) {
      // bfcache 返回时原 loader 已从 DOM 移除：重建并播放
      loader = document.createElement('div');
      loader.className = 'page-loader';
      loader.id = 'pageLoader';
      loader.innerHTML = '<svg class="loader-svg" viewBox="0 0 120 120" fill="none" stroke="currentColor" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"><path class="loader-path" pathLength="100" d="M22 18 L60 54 L98 18 M60 54 L60 102"/></svg><p class="loader-name">Yaule</p>';
      document.body.insertBefore(loader, document.body.firstChild);
    } else if (restart) {
      // 重播：克隆路径与名字节点以重新触发 CSS 动画
      var path = loader.querySelector('.loader-path');
      if (path) { var c1 = path.cloneNode(true); path.parentNode.replaceChild(c1, path); }
      var name = loader.querySelector('.loader-name');
      if (name) { var c2 = name.cloneNode(true); name.parentNode.replaceChild(c2, name); }
      loader.classList.remove('done');
    }
    splashTimer = setTimeout(function () {
      loader.classList.add('done');
    }, 1700);
  }
  playSplash(false);

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
    var anchors = ['middle', 'start', 'end', 'middle', 'end', 'start'];
    for (var i5 = 0; i5 < 6; i5++) {
      var a5 = (i5 * 60 - 90) * Math.PI / 180;
      var lx = C + (R + 10) * Math.cos(a5);
      var ly = C + (R + 10) * Math.sin(a5);
      var dx = 0, dy = 0;
      if (i5 === 0) dy = -1.2;
      if (i5 === 3) dy = 1.6;
      if (i5 === 1 || i5 === 5) dx = 1.5;
      if (i5 === 2 || i5 === 4) dx = -1.5;
      labels += '<text class="radar-label" x="' + (lx + dx).toFixed(1) + '" y="' + (ly + dy).toFixed(1) + '" text-anchor="' + anchors[i5] + '" dominant-baseline="middle">' + skills[i5].name + '</text>';
    }
    svg.innerHTML = defs + grid + axes + area + dots + labels;
    if (bars) {
      bars.innerHTML = skills.map(function (s) {
        return '<div class="skill-bar-row"><span class="sb-name">' + s.name + '</span><span class="sb-track"><span class="sb-fill" style="width:' + (s.val * 10) + '%"></span></span><span class="sb-num">' + s.val + '</span></div>';
      }).join('');
    }
  })();

  /* ========== 人生清单 ========== */
  (function () {
    var grid = document.getElementById('bucketGrid');
    if (!grid) return;
    // 预设完成状态：默认写死在程序里（第1行2、3；第2行1、2、3；第3行1、2、3、4；第4行1、2、3、4；第5行2、3、4）
    var items = ['去看一次现场演唱会', '看一场完整的日出', '学会弹一首完整的曲子', '写一本属于自己的小说', '跑一次五公里', '去一次西藏', '给爸妈买一份大礼物', '养一盆活过一年的绿植', '亲手做一顿年夜饭', '学会一门新的外语', '看一次极光', '独自去一座陌生城市旅行', '学会做咖啡拉花', '给十年后的自己写一封信', '种一棵属于自己的树', '养一只猫', '跳一次伞', '读完《三国演义》', '做一次公益志愿者', '发一张自己的专辑', '开一家小店', '通宵看一次流星雨', '把房间布置成喜欢的样子', '拍一支 Vlog 记录一天'];
    var doneMap = {};
    [1, 2, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15, 17, 18, 19].forEach(function (i) { doneMap[i] = 1; });
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
      var on = doneMap[idx];
      return '<div class="bucket-item' + (on ? ' done' : '') + '"><span class="bk-check"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg></span><span class="bk-text">' + t + '</span></div>';
    }).join('');
    refresh();
  })();
