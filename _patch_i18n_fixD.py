# -*- coding: utf-8 -*-
"""i18n 修复 D：访问计数 / 今日幸运（色名+tips 英文+可重渲染）/ 下载按钮 title"""
p = "index.html"
s = open(p, encoding="utf-8").read()
OPS = []
def rep(o, n, t):
    OPS.append((o, n, t))

# 1. 访问计数拆分 data-i18n（保留 busuanzi b 标签不动）
rep("""      <span class="visit">本站访问 <b id="pvCount" class="busuanzi_value_site_pv">--</b> 次</span>""",
    """      <span class="visit"><span data-i18n="footer.visit1">本站访问</span> <b id="pvCount" class="busuanzi_value_site_pv">--</b><span data-i18n="footer.visit2"> 次</span></span>""", "visit 拆分")

# 2. 字典 zh/en 加 visit1/visit2
rep("""      'footer.contact': '联系', 'footer.email': '邮箱', 'footer.rss': 'RSS 订阅',""",
    """      'footer.contact': '联系', 'footer.email': '邮箱', 'footer.rss': 'RSS 订阅', 'footer.visit1': '本站访问', 'footer.visit2': ' 次',""", "visit zh")
rep("""      'footer.contact': 'Contact', 'footer.email': 'Email', 'footer.rss': 'RSS Feed',""",
    """      'footer.contact': 'Contact', 'footer.email': 'Email', 'footer.rss': 'RSS Feed', 'footer.visit1': 'Visits', 'footer.visit2': '',""", "visit en")

# 3. 今日幸运：英文色名 + tips 双语 + 抽 renderLucky 可重渲染
rep("""    var colors = [
      ['#0284c7', '晴蓝'], ['#0ea5e9', '天青'], ['#38bdf8', '云青'],
      ['#22d3ee', '湖青'], ['#06b6d4', '碧波'], ['#0891b2', '松青']
    ];
    var c = colors[h % colors.length];
    var tips = ['宜写代码', '宜喝咖啡', '宜听歌', '宜发呆', '宜早睡', '宜整理', '宜散步', '宜收藏', '宜分享', '宜读书'];
    var tip = tips[(h >> 4) % tips.length];
    el.innerHTML = (window.YAULE_LANG === 'en'
      ? 'Today\\'s luck <b style="color:' + c[0] + '">' + lucky + '</b> · ' + c[1] + ' ' + tip
      : '今日幸运 <b style="color:' + c[0] + '">' + lucky + '</b> · ' + c[1] + ' ' + tip);""",
    """    var colors = [
      ['#0284c7', '晴蓝', 'sky blue'], ['#0ea5e9', '天青', 'azure'], ['#38bdf8', '云青', 'cloud cyan'],
      ['#22d3ee', '湖青', 'lake cyan'], ['#06b6d4', '碧波', 'wave blue'], ['#0891b2', '松青', 'pine cyan']
    ];
    var tipsZh = ['宜写代码', '宜喝咖啡', '宜听歌', '宜发呆', '宜早睡', '宜整理', '宜散步', '宜收藏', '宜分享', '宜读书'];
    var tipsEn = ['code today', 'have a coffee', 'listen to music', 'daydream', 'sleep early', 'tidy up', 'take a walk', 'collect something', 'share with a friend', 'read a book'];
    function renderLucky() {
      var d2 = new Date();
      var key2 = d2.getFullYear() * 10000 + (d2.getMonth() + 1) * 100 + d2.getDate();
      var h2 = 0, ss = String(key2);
      for (var j = 0; j < ss.length; j++) { h2 = (h2 * 31 + ss.charCodeAt(j)) >>> 0; }
      var lk = (h2 % 100) + 1;
      var cc = colors[h2 % colors.length];
      var tk = (window.YAULE_LANG === 'en') ? tipsEn[(h2 >> 4) % tipsEn.length] : tipsZh[(h2 >> 4) % tipsZh.length];
      el.innerHTML = (window.YAULE_LANG === 'en'
        ? 'Today\\'s luck <b style="color:' + cc[0] + '">' + lk + '</b> · ' + cc[2] + ' ' + tk
        : '今日幸运 <b style="color:' + cc[0] + '">' + lk + '</b> · ' + cc[1] + ' ' + tk);
    }
    window.__renderLucky = renderLucky;
    renderLucky();""", "lucky 双语可重渲染")

# 4. applyLang 加：下载按钮 title + 今日幸运重渲染
rep("""    if (window.__renderShares) window.__renderShares();
    if (window.__renderChangelog) window.__renderChangelog();""",
    """    if (window.__renderShares) window.__renderShares();
    if (window.__renderChangelog) window.__renderChangelog();
    if (window.__renderLucky) window.__renderLucky();
    document.querySelectorAll('.card-dl').forEach(function (a) { a.title = L === 'en' ? 'Download work' : '下载作品'; });""", "applyLang 下载title+lucky")

bad = [(t, s.count(o)) for (o, _, t) in OPS if s.count(o) != 1]
if bad:
    for t, c in bad:
        print("锚点失败(%d): %s" % (c, t))
    raise SystemExit(1)
for (o, n, t) in OPS:
    s = s.replace(o, n, 1)
open(p, "w", encoding="utf-8").write(s)
print("ok:", len(OPS))
