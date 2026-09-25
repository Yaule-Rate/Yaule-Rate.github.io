# -*- coding: utf-8 -*-
"""主页更新日志改版：
- VSCode 风格：深色面板 + 彩色圆点（绿/蓝/橙/红/黄）+ 完整时间戳 + 标签 + 内容
- 主页只显示最新版本（简短），完整历史进详细日志 changelog.html
- 全量日志数据写入 localStorage 供 changelog.html 读取
"""
path = "index.html"
html = open(path, encoding="utf-8").read()
log = []

def rep(old, new, tag):
    global html
    if old not in html:
        log.append("FAIL " + tag)
        return
    html = html.replace(old, new, 1)
    log.append("OK   " + tag)

# ===== CSS：MC 风格 -> VSCode 风格 =====
rep("""  /* ===== 更新日志（我的世界启动器风格） ===== */
  .mc-log { display: flex; flex-direction: column; gap: 14px; max-width: 860px; margin: 0 auto; }
  .mc-ver {
    background: var(--card-bg);
    border: 1px solid var(--line);
    border-radius: 16px;
    padding: 20px 26px 14px;
    position: relative;
    transition: border-color 0.18s ease;
  }
  .mc-ver:hover { border-color: rgba(2,132,199,0.45); }
  .mc-ver.current { border-color: rgba(2,132,199,0.55); box-shadow: 0 0 0 3px rgba(2,132,199,0.08); }
  .mc-ver-head { display: flex; align-items: center; gap: 12px; margin-bottom: 12px; flex-wrap: wrap; }
  .mc-ver-badge {
    font-family: "Noto Serif SC", Georgia, serif;
    font-weight: 700;
    font-size: 16px;
    color: #fff;
    background: linear-gradient(135deg, var(--accent), var(--accent-2));
    padding: 4px 14px;
    border-radius: 9px;
    letter-spacing: 0.5px;
    box-shadow: 0 4px 12px rgba(2,132,199,0.28);
  }
  .mc-ver.current .mc-ver-badge { animation: badgeGlow 2.4s ease infinite; }
  @keyframes badgeGlow { 0%,100% { box-shadow: 0 4px 12px rgba(2,132,199,0.28); } 50% { box-shadow: 0 4px 20px rgba(56,189,248,0.55); } }
  .mc-ver-date {
    font-family: ui-monospace, "Cascadia Code", Consolas, monospace;
    font-size: 12px; color: var(--ink-2); letter-spacing: 0.3px;
  }
  .mc-ver-list { list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 7px; }
  .mc-ver-list li {
    position: relative;
    padding-left: 17px;
    font-size: 13.5px;
    color: var(--ink-2);
    line-height: 1.75;
  }
  .mc-ver-list li::before {
    content: "";
    position: absolute;
    left: 0;
    top: 0.72em;
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--line-strong);
  }
  .mc-ver-list li b {
    font-family: ui-monospace, "Cascadia Code", Consolas, monospace;
    font-weight: 700;
    font-size: 11px;
    letter-spacing: 0.05em;
    border-radius: 5px;
    padding: 1px 7px;
    margin-right: 7px;
    background: var(--bg);
  }
  .mc-ver-list li .li-time {
    font-family: ui-monospace, "Cascadia Code", Consolas, monospace;
    font-size: 11px;
    color: var(--ink-2); opacity: 0.7;
    margin-right: 8px;
    letter-spacing: 0.03em;
  }
  .mc-ver-list li.cat-new b { color: #15803d; border-color: rgba(34,197,94,0.4); background: rgba(34,197,94,0.07); }
  .mc-ver-list li.cat-new::before { background: #22c55e; }
  .mc-ver-list li.cat-chg b { color: var(--accent); border-color: rgba(2,132,199,0.4); background: rgba(2,132,199,0.07); }
  .mc-ver-list li.cat-chg::before { background: var(--accent); }
  .mc-ver-list li.cat-fix b { color: #c2410c; border-color: rgba(249,115,22,0.4); background: rgba(249,115,22,0.07); }
  .mc-ver-list li.cat-fix::before { background: #f97316; }""",
"""  /* ===== 更新日志（VSCode 风格：深色面板 + 彩色圆点 + 完整时间戳） ===== */
  .vs-log { display: flex; flex-direction: column; gap: 16px; max-width: 860px; margin: 0 auto; }
  .vs-ver {
    background: #0d1117;
    border: 1px solid #30363d;
    border-radius: 10px;
    overflow: hidden;
    font-family: ui-monospace, "Cascadia Code", Consolas, "SF Mono", monospace;
  }
  .vs-ver-head {
    display: flex; align-items: center; gap: 12px;
    padding: 10px 16px;
    background: #161b22;
    border-bottom: 1px solid #30363d;
    flex-wrap: wrap;
  }
  .vs-ver-tab {
    display: inline-flex; align-items: center; gap: 8px;
    font-size: 12.5px; font-weight: 700; color: #e6edf3;
    letter-spacing: 0.04em;
  }
  .vs-ver-tab::before {
    content: ""; width: 3px; height: 14px; border-radius: 2px;
    background: linear-gradient(180deg, var(--accent), var(--accent-2));
  }
  .vs-ver-date {
    font-size: 11px; color: #8b949e; letter-spacing: 0.02em;
  }
  .vs-ver-badge {
    margin-left: auto; font-size: 10.5px; color: #3fb950;
    border: 1px solid rgba(63,185,80,0.35); background: rgba(63,185,80,0.08);
    border-radius: 999px; padding: 2px 9px; letter-spacing: 0.05em;
  }
  .vs-rows { padding: 8px 0 10px; }
  .vs-row {
    display: flex; align-items: baseline; gap: 10px;
    padding: 4.5px 16px;
    font-size: 12.5px; line-height: 1.6;
  }
  .vs-row:hover { background: rgba(56,139,253,0.06); }
  .vs-dot {
    flex: none; width: 7px; height: 7px; border-radius: 50%;
    transform: translateY(-1px);
    background: #8b949e;
  }
  .vs-time {
    flex: none; font-size: 11px; color: #8b949e; letter-spacing: 0.02em;
  }
  .vs-tag {
    flex: none; font-size: 10.5px; font-weight: 700; letter-spacing: 0.04em;
  }
  .vs-text { color: #c9d1d9; }
  .vs-row.cat-add .vs-dot { background: #3fb950; }
  .vs-row.cat-add .vs-tag { color: #3fb950; }
  .vs-row.cat-info .vs-dot { background: #58a6ff; }
  .vs-row.cat-info .vs-tag { color: #58a6ff; }
  .vs-row.cat-fix .vs-dot { background: #f97316; }
  .vs-row.cat-fix .vs-tag { color: #f97316; }
  .vs-row.cat-del .vs-dot { background: #f85149; }
  .vs-row.cat-del .vs-tag { color: #f85149; }
  .vs-row.cat-warn .vs-dot { background: #e3b341; }
  .vs-row.cat-warn .vs-tag { color: #e3b341; }""",
"CSS VSCode 风格")

# ===== HTML：mc-log 卡片区 -> vs-log 动态容器 =====
import re
start = html.index('    <div class="mc-log">')
end = html.index('    </div>\n  </div>\n</section>\n\n<section class="section alt" id="bucket">')
html = html[:start] + '    <div class="vs-log" id="mcLog"></div>\n' + html[end + len('    </div>\n'):]
log.append("OK   替换 mc-log -> vs-log")

# ===== JS：DOM 序列化 -> 全量数据 + 简短渲染 + localStorage =====
rep("""  /* ========== 更新日志同步：写入 localStorage（供 changelog.html 读取） ========== */
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
  })();""",
"""  /* ========== 更新日志（VSCode 风格）全量数据 + 主页简短渲染 + localStorage 同步 ========== */
  var YAULE_CHANGELOG = [
    { ver: "v19.6", date: "2026-09-25 16:20:11", current: true, list: [
      { lv: "[ADD]", time: "2026-09-25 16:20:11", text: "六件作品详情页加入评分系统（兴华 4.9 / 记账 5.0 / 代码 4.8 / 表情 5.0 / CS 5.0 / 棋类 4.9）。" },
      { lv: "[ADD]", time: "2026-09-25 16:12:30", text: "四件作品内全部 emoji 替换为内联 SVG 图标。" },
      { lv: "[INFO]", time: "2026-09-25 16:05:02", text: "更新日志改版为 VSCode 风格：彩色圆点 + 完整时间戳，主页只展示最新版本，完整历史移入详细日志。" },
      { lv: "[FIX]", time: "2026-09-25 15:58:40", text: "修复从个人空间/作品返回标签页时进度条遮罩残留。" }
    ]},
    { ver: "v19.5", date: "2026-09-25 15:40:12", current: false, list: [
      { lv: "[INFO]", time: "2026-09-25 15:40:12", text: "作品卡点击统一进入详情页；详情页「立即体验」加载与更新日志一致的 8 秒进度条后进入作品。" },
      { lv: "[INFO]", time: "2026-09-25 15:22:45", text: "主页开屏恢复为青色 Y 简笔画（首次进入 / 返回均播放）。" }
    ]},
    { ver: "v19.4", date: "2026-09-25 14:40:55", current: false, list: [
      { lv: "[INFO]", time: "2026-09-25 14:40:55", text: "加载遮罩统一为「进入日志」样式：Y 一笔画 + 名字 + 8 秒进度条 + 长按加速。" }
    ]},
    { ver: "v19", date: "2026-09-25 13:10:00", current: false, list: [
      { lv: "[ADD]", time: "2026-09-25 13:10:00", text: "作品卡分享按钮（微博 / QQ），加载遮罩内随机标语轮换。" },
      { lv: "[ADD]", time: "2026-09-25 12:58:32", text: "22:00–06:00 自动切换深色模式（手动选择优先）。" },
      { lv: "[INFO]", time: "2026-09-25 12:47:03", text: "SEO 增强：标题 / 描述加长，sitemap.xml 与 atom.xml 自动维护。" },
      { lv: "[FIX]", time: "2026-09-25 12:30:18", text: "取消卡片顶部青色渐变细线；根目录六件旧作品页补全 SEO 信息。" }
    ]},
    { ver: "v16", date: "2026-09-25 14:05:11", current: false, list: [
      { lv: "[ADD]", time: "2026-09-25 14:05:11", text: "生活瞬间三图标换用开源黑白 SVG：瑞幸 / 网易云 / 我的世界。" },
      { lv: "[ADD]", time: "2026-09-25 14:04:40", text: "六个作品新增独立详情页，点「查看详情」进入详细介绍。" },
      { lv: "[ADD]", time: "2026-09-25 14:04:02", text: "人生清单改为程序预设勾选，记录由代码维护。" },
      { lv: "[INFO]", time: "2026-09-25 14:03:22", text: "更新日志改版为我的世界启动器风格，新增详细日志页。" },
      { lv: "[INFO]", time: "2026-09-25 14:02:15", text: "「此刻」布局改双列：天气卡通栏，新增体感 / 湿度 / 风速 / 紫外线四项。" },
      { lv: "[FIX]", time: "2026-09-25 14:01:07", text: "技能进度条颜色不渲染问题：内联宽度 + 块级填充。" },
      { lv: "[FIX]", time: "2026-09-25 13:59:52", text: "一言长句中文与数字重叠，支持自动换行。" },
      { lv: "[INFO]", time: "2026-09-25 13:58:26", text: "生活瞬间切换增加平滑过渡，容器高度稳定不闪动。" }
    ]},
    { ver: "v15", date: "2026-09-25 13:52:40", current: false, list: [
      { lv: "[ADD]", time: "2026-09-25 13:52:40", text: "开源仓库墙：实时读取 GitHub 公开仓库与星标。" },
      { lv: "[ADD]", time: "2026-09-25 13:51:12", text: "技能雷达图与六项自评进度条。" },
      { lv: "[ADD]", time: "2026-09-25 13:49:36", text: "人生清单：想做的 24 件小事。" },
      { lv: "[INFO]", time: "2026-09-25 13:47:58", text: "版本更新日志时间轴改版上线。" }
    ]},
    { ver: "v14", date: "2026-09-25 12:47:16", current: false, list: [
      { lv: "[ADD]", time: "2026-09-25 12:47:16", text: "RSS / Atom 订阅源，访客可订阅站点每一次更新。" },
      { lv: "[ADD]", time: "2026-09-25 12:46:05", text: "busuanzi 访问计数，页脚实时显示访客与浏览量。" },
      { lv: "[ADD]", time: "2026-09-25 12:44:31", text: "作品卡展开预览：扩展简介、技术标签，点卡片任意处即展开。" },
      { lv: "[ADD]", time: "2026-09-25 12:42:58", text: "呼吸动效 favicon 与「幸运今日」每日签文。" },
      { lv: "[INFO]", time: "2026-09-25 12:41:20", text: "SEO：补全 keywords / og / twitter 标签，利于搜索引擎收录。" },
      { lv: "[FIX]", time: "2026-09-25 12:39:47", text: "卡片「查看详情」改为同页打开，不再被浏览器拦截。" }
    ]},
    { ver: "v13", date: "2026-09-25 11:20:04", current: false, list: [
      { lv: "[ADD]", time: "2026-09-25 11:20:04", text: "「今年进度环」：2026 年已过百分比与剩余天数。" },
      { lv: "[ADD]", time: "2026-09-25 11:18:37", text: "今日一言 3 秒自动轮播，点击可复制。" },
      { lv: "[ADD]", time: "2026-09-25 11:16:52", text: "页面加载「Y」一笔画动画。" }
    ]},
    { ver: "v12", date: "2026-09-25 09:41:50", current: false, list: [
      { lv: "[ADD]", time: "2026-09-25 09:41:50", text: "「此刻」板块独立：时钟与天气单独成卡。" },
      { lv: "[ADD]", time: "2026-09-25 09:40:12", text: "翻牌时钟与页脚停留计时。" },
      { lv: "[ADD]", time: "2026-09-25 09:38:29", text: "作品下载次数统计（本地记录）。" },
      { lv: "[INFO]", time: "2026-09-25 09:36:44", text: "移除语言标签小字，保持欢迎页纯粹。" }
    ]},
    { ver: "v10", date: "2026-09-25 08:15:06", current: false, list: [
      { lv: "[ADD]", time: "2026-09-25 08:15:06", text: "节日飘浮：自动拉取中国法定节假日，中秋的月亮与灯笼飘 3 秒。" },
      { lv: "[ADD]", time: "2026-09-25 08:13:27", text: "节日专属欢迎语（春节、端午、中秋等 8 个节日）。" }
    ]},
    { ver: "v9", date: "2026-09-24 21:36:42", current: false, list: [
      { lv: "[ADD]", time: "2026-09-24 21:36:42", text: "实时天气（Open-Meteo 免费接口，衢州定位）。" },
      { lv: "[ADD]", time: "2026-09-24 21:35:08", text: "纪念日板块：「活着的第 N 天」与「本站上线第 N 天」。" }
    ]},
    { ver: "v7", date: "2026-09-23 20:15:09", current: false, list: [
      { lv: "[ADD]", time: "2026-09-23 20:15:09", text: "「生活瞬间」板块：瑞幸咖啡、网易云音乐、我的世界三块数据。" },
      { lv: "[ADD]", time: "2026-09-23 20:13:31", text: "ROG 幻 16 式错峰滚动：图标先下移进入，文字随后浮现。" },
      { lv: "[FIX]", time: "2026-09-23 20:11:44", text: "奇异类合集布局错误与键盘异常。" }
    ]},
    { ver: "v6", date: "2026-09-22 22:04:31", current: false, list: [
      { lv: "[ADD]", time: "2026-09-22 22:04:31", text: "26 种语言打字机轮播：打出 → 停留 → 逐字消失。" },
      { lv: "[ADD]", time: "2026-09-22 22:02:56", text: "今日一言（hitokoto 联网，失败本地降级）。" },
      { lv: "[INFO]", time: "2026-09-22 22:01:19", text: "彩蛋模式全部改青色，移除紫色残留。" }
    ]},
    { ver: "v4", date: "2026-09-21 19:28:53", current: false, list: [
      { lv: "[ADD]", time: "2026-09-21 19:28:53", text: "精选作品卡片：六个作品上架，支持下载。" },
      { lv: "[ADD]", time: "2026-09-21 19:27:10", text: "5 秒伪进度条，模拟进入作品。" }
    ]},
    { ver: "v1", date: "2026-09-18 09:12:00", current: false, list: [
      { lv: "[ADD]", time: "2026-09-18 09:12:00", text: "站点上线：全世界语言的「欢迎你的到来」欢迎页。" },
      { lv: "[ADD]", time: "2026-09-18 09:10:36", text: "深色页脚 + 灰白大字 Yaule，WorkBuddy 风格。" }
    ]}
  ];
  (function () {
    var lvClass = { "[ADD]": "cat-add", "[INFO]": "cat-info", "[FIX]": "cat-fix", "[DEL]": "cat-del", "[WARN]": "cat-warn" };
    function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
    function rowHtml(item) {
      var cls = lvClass[item.lv] || 'cat-info';
      return '<div class="vs-row ' + cls + '"><span class="vs-dot"></span><span class="vs-time">' + esc(item.time || '') + '</span><span class="vs-tag">' + esc(item.lv || '') + '</span><span class="vs-text">' + esc(item.text || '') + '</span></div>';
    }
    function verHtml(v) {
      var rows = (v.list || []).map(rowHtml).join('');
      return '<div class="vs-ver' + (v.current ? ' current' : '') + '"><div class="vs-ver-head"><span class="vs-ver-tab">' + esc(v.ver) + '</span><span class="vs-ver-date">' + esc(v.date) + '</span>' + (v.current ? '<span class="vs-ver-badge">当前版本</span>' : '') + '</div><div class="vs-rows">' + rows + '</div></div>';
    }
    var box = document.getElementById('mcLog');
    if (box) {
      // 主页只展示最新版本（简短），完整历史见详细日志 changelog.html
      var top = YAULE_CHANGELOG[0];
      if (top) box.innerHTML = verHtml(top);
    }
    try { localStorage.setItem('yaule_changelog', JSON.stringify(YAULE_CHANGELOG)); } catch (e) {}
  })();""",
"JS 全量数据 + 简短渲染")

# 1086 行去掉 .mc-ver
rep(".card, .repo-card, .mc-ver, .now-card, .bucket-item { position: relative; }",
    ".card, .repo-card, .now-card, .bucket-item { position: relative; }",
    "移除 .mc-ver 引用")

open(path, "w", encoding="utf-8").write(html)
for l in log:
    print(l)
print("DONE")
