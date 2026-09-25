# -*- coding: utf-8 -*-
"""i18n 修复 C：applyLang 空译文短路 / tip 写反 / btnMore 初始 / reco tag / wd-unit / changelog 双语 / 分享弹窗双语"""
p = "index.html"
s = open(p, encoding="utf-8").read()
log = []
OPS = []

def rep(old, new, tag):
    OPS.append((old, new, tag))

# 1. applyLang 空译文短路（mc.u4='' 等生效）
rep("""      if (I18N[L] && I18N[L][k]) el.textContent = I18N[L][k];""",
    """      if (I18N[L] && k in I18N[L]) el.textContent = I18N[L][k];""", "applyLang 短路修复")

# 2. langLoaderTip 写反
rep("""    if (tip) tip.textContent = next === 'en' ? '正在切换语言…' : 'Switching language…';""",
    """    if (tip) tip.textContent = next === 'en' ? 'Switching language…' : '正在切换语言…';""", "tip 写反修复")

# 3. applyLang 尾部：btnMore 初始 + 分享 + 日志
rep("""    if (window.__setFest) window.__setFest();
    window.dispatchEvent(new CustomEvent('yaule-langchange'));""",
    """    if (window.__setFest) window.__setFest();
    var bm = document.getElementById('btnMore');
    if (bm) {
      var hiddenN = document.querySelectorAll('.works-grid .card.hidden').length;
      var isOpen = hiddenN === 0;
      bm.textContent = L === 'en' ? (isOpen ? 'Collapse ↑' : 'View More ↓') : (isOpen ? '收起 ↑' : '查看更多 ↓');
    }
    if (window.__renderShares) window.__renderShares();
    if (window.__renderChangelog) window.__renderChangelog();
    window.dispatchEvent(new CustomEvent('yaule-langchange'));""", "applyLang 尾部增强")

# 4. reco 每日推荐 tag 双语
rep("""      if (fest && FEST.zh[fest]) return { zh: FEST.zh[fest], en: FEST.en[fest], tag: fest };""",
    """      if (fest && FEST.zh[fest]) {
        var tagEn = { '春节': 'Spring Festival', '除夕': "New Year's Eve", '元宵节': 'Lantern Festival', '清明节': 'Qingming', '劳动节': 'Labor Day', '端午节': 'Dragon Boat Festival', '中秋节': 'Mid-Autumn', '国庆节': 'National Day' }[fest] || fest;
        return { zh: FEST.zh[fest], en: FEST.en[fest], tag: (window.YAULE_LANG === 'en') ? tagEn : fest };
      }""", "reco tag 双语")

# 5. wd-unit 紫外线单位
rep("""<div class="wd-item"><div class="wd-label" data-i18n="now.w4">紫外线</div><div class="wd-val"><b id="wUvi">--</b><span class="wd-unit">级</span></div></div>""",
    """<div class="wd-item"><div class="wd-label" data-i18n="now.w4">紫外线</div><div class="wd-val"><b id="wUvi">--</b><span class="wd-unit" data-i18n="now.uvi">级</span></div></div>""", "wd-unit uvi")
rep("""      'now.w1': '体感', 'now.w2': '湿度', 'now.w3': '风速', 'now.w4': '紫外线',""",
    """      'now.w1': '体感', 'now.w2': '湿度', 'now.w3': '风速', 'now.w4': '紫外线', 'now.uvi': '级',""", "now.uvi zh")
rep("""      'now.w1': 'Feels', 'now.w2': 'Humidity', 'now.w3': 'Wind', 'now.w4': 'UV',""",
    """      'now.w1': 'Feels', 'now.w2': 'Humidity', 'now.w3': 'Wind', 'now.w4': 'UV', 'now.uvi': '',""", "now.uvi en")

# 6. changelog：v21 条目 en + 渲染双语
rep("""    { ver: "v21", date: "2026-09-25 20:18:00", current: true, list: [
      { lv: "[ADD]", time: "2026-09-25 20:18:00", text: "整站 i18n：右上角中英一键切换，独立 3 秒伪进度条。" },
      { lv: "[ADD]", time: "2026-09-25 20:09:47", text: "此刻 · 每日推荐：结合节日 / 天气 / 星期，每天一条。" },
      { lv: "[ADD]", time: "2026-09-25 19:58:32", text: "页面转场：返回标签页时 View Transitions 衔接。" },
      { lv: "[ADD]", time: "2026-09-25 19:50:10", text: "独立 404 页：Y 一笔画 + 「失眠夜迷路了」+ 返回按钮。" }
    ]},""",
    """    { ver: "v22", date: "2026-09-25 21:30:00", current: true, list: [
      { lv: "[ADD]", time: "2026-09-25 21:30:00", text: "i18n 补全：英文模式下全部可见文字英译（生活瞬间 / 作品 / 纪念日 / 此刻 / 技能 / 清单 / 页脚），切换进度条平滑并显示百分比。", en: "i18n complete: every visible string now translates to English (life moments / works / anniversaries / now / skills / bucket / footer); the switch progress bar is now smooth with a live percentage." },
      { lv: "[FIX]", time: "2026-09-25 21:28:00", text: "修复英文模式下载数、分享弹窗、推荐标签与紫外线单位未翻译的问题。", en: "Fixed download counts, share popup, daily-pick tag and UV unit staying untranslated in English mode." },
      { lv: "[ADD]", time: "2026-09-25 20:18:00", text: "整站 i18n：右上角中英一键切换，独立 3 秒伪进度条。", en: "Site-wide i18n: one-click EN/CN switch top-right, with a dedicated 3-second pseudo progress bar." },
      { lv: "[ADD]", time: "2026-09-25 20:09:47", text: "此刻 · 每日推荐：结合节日 / 天气 / 星期，每天一条。", en: "Right Now · Daily pick: holidays / weather / weekday, one per day." },
      { lv: "[ADD]", time: "2026-09-25 19:58:32", text: "页面转场：返回标签页时 View Transitions 衔接。", en: "Page transitions: View Transitions when navigating back to the tab page." },
      { lv: "[ADD]", time: "2026-09-25 19:50:10", text: "独立 404 页：Y 一笔画 + 「失眠夜迷路了」+ 返回按钮。", en: "Dedicated 404 page: Y stroke animation + 'Lost in the Insomnia Night' + back buttons." }
    ]},""", "changelog v22")
rep("""      return '<div class="vs-row ' + cls + '"><span class="vs-dot"></span><span class="vs-time">' + esc(item.time || '') + '</span><span class="vs-tag">' + esc(item.lv || '') + '</span><span class="vs-text">' + esc(item.text || '') + '</span></div>';""",
    """      var t = (window.YAULE_LANG === 'en' && item.en) ? item.en : (item.text || '');
      return '<div class="vs-row ' + cls + '"><span class="vs-dot"></span><span class="vs-time">' + esc(item.time || '') + '</span><span class="vs-tag">' + esc(item.lv || '') + '</span><span class="vs-text">' + esc(t) + '</span></div>';""", "rowHtml 双语")
rep("""      return '<div class="vs-ver' + (v.current ? ' current' : '') + '"><div class="vs-ver-head"><span class="vs-ver-tab">' + esc(v.ver) + '</span><span class="vs-ver-date">' + esc(v.date) + '</span>' + (v.current ? '<span class="vs-ver-badge">当前版本</span>' : '') + '</div><div class="vs-rows">' + rows + '</div></div>';""",
    """      var badge = (window.YAULE_LANG === 'en') ? 'Current' : '当前版本';
      return '<div class="vs-ver' + (v.current ? ' current' : '') + '"><div class="vs-ver-head"><span class="vs-ver-tab">' + esc(v.ver) + '</span><span class="vs-ver-date">' + esc(v.date) + '</span>' + (v.current ? '<span class="vs-ver-badge">' + badge + '</span>' : '') + '</div><div class="vs-rows">' + rows + '</div></div>';""", "verHtml badge 双语")
rep("""    var box = document.getElementById('mcLog');
    if (box) {
      // 主页只展示最新版本（简短），完整历史见详细日志 changelog.html
      var top = YAULE_CHANGELOG[0];
      if (top) box.innerHTML = verHtml(top);
    }""",
    """    function renderTop() {
      var box2 = document.getElementById('mcLog');
      if (box2) {
        // 主页只展示最新版本（简短），完整历史见详细日志 changelog.html
        var top2 = YAULE_CHANGELOG[0];
        if (top2) box2.innerHTML = verHtml(top2);
      }
    }
    window.__renderChangelog = renderTop;
    renderTop();""", "changelog renderTop")

# 7. 分享弹窗双语（renderShareTexts 按语言更新）
rep("""  /* ========== 作品卡分享按钮（微博 / QQ 带文案） ========== */
  (function () {
    var base = location.origin + location.pathname;
    function closeShares() {
      document.querySelectorAll('.share-pop.show').forEach(function (p) { p.classList.remove('show'); });
    }""",
    """  /* ========== 作品卡分享按钮（微博 / QQ 带文案） ========== */
  (function () {
    var base = location.origin + location.pathname;
    function closeShares() {
      document.querySelectorAll('.share-pop.show').forEach(function (p) { p.classList.remove('show'); });
    }
    function renderShareTexts() {
      var en = window.YAULE_LANG === 'en';
      document.querySelectorAll('.card').forEach(function (card) {
        var h3 = card.querySelector('h3');
        var btn = card.querySelector('.card-share');
        var pop = card.querySelector('.share-pop');
        if (!h3 || !btn || !pop) return;
        var name = h3.textContent.trim() || (en ? 'work' : '作品');
        var detail = card.getAttribute('data-detail') || '';
        var shareUrl = detail ? base.replace(/\\/[^/]*$/, '/') + detail : base;
        var text = en ? 'Yaule\\'s work "' + name + '" — Insomnia Night Space' : '来自 Yaule 的作品「' + name + '」——失眠夜个人空间';
        var wb = pop.querySelector('.sp-wb');
        var qq = pop.querySelector('.sp-qq');
        if (wb) { wb.href = 'https://service.weibo.com/share/share.php?url=' + encodeURIComponent(shareUrl) + '&title=' + encodeURIComponent(text); wb.lastChild.textContent = en ? ' Weibo' : '微博'; }
        if (qq) { qq.href = 'https://connect.qq.com/widget/shareqq/index.html?url=' + encodeURIComponent(shareUrl) + '&title=' + encodeURIComponent(text) + '&summary=' + encodeURIComponent(en ? 'Take a look at this work' : '点开看看这个作品'); qq.lastChild.textContent = 'QQ'; }
        btn.title = en ? 'Share work' : '分享作品';
        btn.setAttribute('aria-label', en ? 'Share work' : '分享作品');
        btn.lastChild.textContent = en ? ' Share' : '分享';
      });
    }
    window.__renderShares = renderShareTexts;""", "renderShareTexts")

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
print("完成。替换:", len(log), "处")
for t in log:
    print(" -", t)
