# -*- coding: utf-8 -*-
"""v17 补丁：生活切换防闪 / 翻牌残影 / 纪念日美化 / 此刻优化 / 日志完整时间戳+[ADD/INFO/FIX] / 详细日志按钮 / 进度条8秒+长按加速+第3秒弹出 / works与life换位 / 日志补记v15v16"""
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

# ---------- 1. 生活瞬间容器固定高度（防下方闪动） ----------
rep(".life-panels { position: relative; }",
    ".life-panels { position: relative; min-height: 440px; }",
    "life panels min-height")
rep("    .life-panel { flex-direction: column; gap: 26px; padding: 32px 22px; text-align: center; align-items: center; }",
    "    .life-panel { flex-direction: column; gap: 26px; padding: 32px 22px; text-align: center; align-items: center; }\n    .life-panels { min-height: 730px; }",
    "life panels min-height mobile")

# ---------- 2. 翻牌时钟残影（fill-mode forwards） ----------
rep(".fl-old { position: absolute; inset: 0; animation: flipOut .4s ease; }",
    ".fl-old { position: absolute; inset: 0; animation: flipOut .4s ease forwards; }",
    "flip old forwards")
rep(".fl-new { display: inline-block; animation: flipIn .4s ease; }",
    ".fl-new { display: inline-block; animation: flipIn .4s ease forwards; }",
    "flip new forwards")

# ---------- 3. 纪念日美化 CSS ----------
rep(".anniv-grid {\n    display: grid;\n    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));\n    gap: 20px;\n  }\n  .anniv-card {\n    background: var(--card-bg);\n    border: 1px solid var(--line);\n    border-radius: 20px;\n    padding: 34px 32px;\n  }\n  .anniv-num {\n    font-family: \"Noto Serif SC\", Georgia, serif;\n    font-size: clamp(42px, 6vw, 64px);\n    font-weight: 700;\n    color: var(--accent);\n    line-height: 1.1;\n  }\n  .anniv-label { font-size: 14px; color: var(--ink-2); margin-top: 8px; }\n  .anniv-date { font-size: 13px; color: var(--ink-2); opacity: 0.8; margin-top: 14px; }",
    ".anniv-grid {\n    display: grid;\n    grid-template-columns: repeat(auto-fit, minmax(270px, 1fr));\n    gap: 20px;\n  }\n  .anniv-card {\n    position: relative;\n    overflow: hidden;\n    background: var(--card-bg);\n    border: 1px solid var(--line);\n    border-radius: 20px;\n    padding: 30px 32px 26px;\n    transition: border-color 0.18s ease, transform 0.18s ease, box-shadow 0.18s ease;\n  }\n  .anniv-card:hover { border-color: rgba(2,132,199,0.45); transform: translateY(-3px); box-shadow: 0 14px 32px rgba(0,0,0,0.08); }\n  .anniv-card::before {\n    content: \"\"; position: absolute; top: 0; left: 0; right: 0; height: 4px;\n    background: linear-gradient(90deg, var(--accent), var(--accent-2));\n  }\n  .anniv-top {\n    display: flex; align-items: center; gap: 8px;\n    font-size: 12.5px; color: var(--ink-2); letter-spacing: 0.08em;\n  }\n  .anniv-top svg { width: 15px; height: 15px; color: var(--accent); flex: none; }\n  .anniv-num {\n    font-family: \"Noto Serif SC\", Georgia, serif;\n    font-size: clamp(44px, 6vw, 62px);\n    font-weight: 700;\n    color: var(--accent);\n    line-height: 1.1;\n    margin-top: 14px;\n    font-variant-numeric: tabular-nums;\n  }\n  .anniv-label { font-size: 14px; color: var(--ink-2); margin-top: 8px; }\n  .anniv-track {\n    margin-top: 18px; height: 6px; background: var(--line);\n    border-radius: 999px; overflow: hidden;\n  }\n  .anniv-fill {\n    height: 100%; width: 0;\n    background: linear-gradient(90deg, var(--accent), var(--accent-2));\n    border-radius: 999px;\n    transition: width 1.2s ease;\n  }\n  .anniv-meta { margin-top: 12px; font-size: 12.5px; color: var(--ink-2); opacity: 0.85; }\n  .anniv-date { font-size: 13px; color: var(--ink-2); opacity: 0.8; margin-top: 8px; }",
    "anniv css")

# ---------- 4. 此刻优化：天气详情小卡 + 年份环剩余天数 ----------
rep(".weather-detail {\n    display: flex;\n    flex-wrap: wrap;\n    gap: 10px 22px;\n    margin-top: 18px;\n    padding-top: 16px;\n    border-top: 1px dashed var(--line);\n    font-size: 13.5px;\n    color: var(--ink-2);\n  }\n  .weather-detail span { display: inline-flex; align-items: baseline; gap: 4px; }\n  .weather-detail b { color: var(--accent); font-weight: 600; font-variant-numeric: tabular-nums; }",
    ".weather-detail {\n    display: grid;\n    grid-template-columns: repeat(4, 1fr);\n    gap: 12px;\n    margin-top: 20px;\n    padding-top: 18px;\n    border-top: 1px dashed var(--line);\n  }\n  .wd-item {\n    background: var(--soft);\n    border-radius: 12px;\n    padding: 12px 10px;\n    text-align: center;\n  }\n  .wd-label { font-size: 11px; color: var(--ink-2); letter-spacing: 0.06em; }\n  .wd-val { font-size: 21px; font-weight: 700; color: var(--ink); font-variant-numeric: tabular-nums; margin-top: 2px; line-height: 1.2; }\n  .wd-unit { font-size: 12px; color: var(--ink-2); }",
    "weather detail grid")
rep(".ring-pct { font-size: 30px; font-weight: 800; color: var(--ink); font-family: \"Noto Serif SC\", Georgia, serif; line-height: 1; }",
    ".ring-pct { font-size: 34px; font-weight: 800; color: var(--ink); font-family: \"Noto Serif SC\", Georgia, serif; line-height: 1; font-variant-numeric: tabular-nums; }",
    "ring pct bigger")
rep(".ring-foot { margin-top: 14px; font-size: 13px; color: var(--ink-2); }",
    ".ring-foot { margin-top: 14px; font-size: 13px; color: var(--ink-2); }\n  .ring-foot b { color: var(--accent); font-weight: 600; }",
    "ring foot b")

# ---------- 5. 进度条 8 秒 + 加速按钮样式 ----------
rep(".loading-hint {\n    margin-top: 24px;\n    font-size: 13px;\n    color: var(--ink-2);\n    opacity: 0.6;\n  }",
    ".loading-hint {\n    margin-top: 24px;\n    font-size: 13px;\n    color: var(--ink-2);\n    opacity: 0.6;\n  }\n  .load-skip {\n    margin-top: 20px;\n    display: inline-flex; align-items: center; gap: 7px;\n    font-size: 12.5px; color: var(--accent);\n    border: 1px solid rgba(2,132,199,0.35); background: rgba(2,132,199,0.06);\n    border-radius: 999px; padding: 9px 20px; cursor: pointer;\n    opacity: 0; transform: translateY(8px);\n    transition: opacity 0.35s ease, transform 0.35s ease;\n    font-family: inherit; user-select: none; -webkit-user-select: none;\n  }\n  .load-skip.show { opacity: 1; transform: translateY(0); }\n  .load-skip svg { width: 14px; height: 14px; }\n  .load-skip:active { background: rgba(2,132,199,0.16); }\n  .load-skip small { font-size: 11px; opacity: 0.75; }",
    "load skip css")

# ---------- 6. 详细日志按钮样式 ----------
rep(".section-head .desc {",
    ".log-more {\n    display: inline-flex; align-items: center; gap: 6px;\n    font-size: 12.5px; color: var(--accent);\n    border: 1px solid rgba(2,132,199,0.35); background: rgba(2,132,199,0.06);\n    border-radius: 999px; padding: 6px 15px;\n    text-decoration: none; transition: all 0.18s ease;\n  }\n  .log-more:hover { background: rgba(2,132,199,0.14); color: var(--accent); transform: translateY(-1px); }\n  .log-more svg { width: 13px; height: 13px; }\n  .section-head .desc {",
    "log-more css")

# ---------- 7. 日志终端标签样式（[ADD]/[INFO]/[FIX] + 行内时间） ----------
rep(".mc-ver-list li b {\n    font-weight: 600;\n    font-size: 12px;\n    color: var(--ink);\n    border: 1px solid var(--line);\n    border-radius: 6px;\n    padding: 0 7px;\n    margin-right: 8px;\n    background: var(--bg);\n  }",
    ".mc-ver-list li b {\n    font-family: ui-monospace, \"Cascadia Code\", Consolas, monospace;\n    font-weight: 700;\n    font-size: 11px;\n    letter-spacing: 0.05em;\n    border-radius: 5px;\n    padding: 1px 7px;\n    margin-right: 7px;\n    background: var(--bg);\n  }\n  .mc-ver-list li .li-time {\n    font-family: ui-monospace, \"Cascadia Code\", Consolas, monospace;\n    font-size: 11px;\n    color: var(--ink-2); opacity: 0.7;\n    margin-right: 8px;\n    letter-spacing: 0.03em;\n  }",
    "log li b mono")
rep(".mc-ver-date { font-size: 12.5px; color: var(--ink-2); letter-spacing: 0.4px; }",
    ".mc-ver-date {\n    font-family: ui-monospace, \"Cascadia Code\", Consolas, monospace;\n    font-size: 12px; color: var(--ink-2); letter-spacing: 0.3px;\n  }",
    "mc-ver-date mono")
rep(".mc-ver-list li.cat-new b { color: #15803d; border-color: rgba(34,197,94,0.35); background: rgba(34,197,94,0.06); }",
    ".mc-ver-list li.cat-new b { color: #15803d; border-color: rgba(34,197,94,0.4); background: rgba(34,197,94,0.07); }",
    "cat-new b")
rep(".mc-ver-list li.cat-chg b { color: var(--accent); border-color: rgba(2,132,199,0.35); background: rgba(2,132,199,0.06); }",
    ".mc-ver-list li.cat-chg b { color: var(--accent); border-color: rgba(2,132,199,0.4); background: rgba(2,132,199,0.07); }",
    "cat-chg b")
rep(".mc-ver-list li.cat-fix b { color: #c2410c; border-color: rgba(249,115,22,0.35); background: rgba(249,115,22,0.06); }",
    ".mc-ver-list li.cat-fix b { color: #c2410c; border-color: rgba(249,115,22,0.4); background: rgba(249,115,22,0.07); }",
    "cat-fix b")

# ---------- 8. 加载遮罩 HTML 加加速按钮 ----------
rep('<p class="loading-hint">稍等片刻，马上就好…</p>',
    '<p class="loading-hint">稍等片刻，马上就好…</p>\n  <button class="load-skip" id="loadSkip" type="button">\n    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>\n    长按加速 <small>按住不放，加载更快</small>\n  </button>',
    "load skip html")

# ---------- 9. 纪念日 HTML 新结构 ----------
rep('''    <div class="anniv-grid">
      <div class="anniv-card">
        <div class="anniv-num" id="annivDays">--</div>
        <div class="anniv-label">活着的第 <span id="annivDaysN">--</span> 天</div>
        <div class="anniv-date">自 2012 年 1 月 17 日起</div>
      </div>
      <div class="anniv-card">
        <div class="anniv-num" id="siteDays">--</div>
        <div class="anniv-label">本站上线第 <span id="siteDaysN">--</span> 天</div>
        <div class="anniv-date">自 2026 年 9 月 18 日起</div>
      </div>
    </div>''',
    '''    <div class="anniv-grid">
      <div class="anniv-card">
        <div class="anniv-top">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
          <span>与这个世界相遇</span>
        </div>
        <div class="anniv-num" id="annivDays">--</div>
        <div class="anniv-label">活着的第 <span id="annivDaysN">--</span> 天</div>
        <div class="anniv-track"><div class="anniv-fill" id="lifeFill"></div></div>
        <div class="anniv-meta" id="lifeMeta">人生进度计算中…</div>
        <div class="anniv-date">自 2012 年 1 月 17 日起</div>
      </div>
      <div class="anniv-card">
        <div class="anniv-top">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M12 19l7-7 3 3-7 7-3-3z"/><path d="M18 13l-1.5-7.5L2 2l3.5 14.5L13 18l5-5z"/><path d="M2 2l7.586 7.586"/><circle cx="11" cy="11" r="2"/></svg>
          <span>与这座小站相遇</span>
        </div>
        <div class="anniv-num" id="siteDays">--</div>
        <div class="anniv-label">本站上线第 <span id="siteDaysN">--</span> 天</div>
        <div class="anniv-track"><div class="anniv-fill" id="siteFill"></div></div>
        <div class="anniv-meta" id="siteMeta">下一个里程碑计算中…</div>
        <div class="anniv-date">自 2026 年 9 月 18 日起</div>
      </div>
    </div>''',
    "anniv html")

# ---------- 10. 此刻 HTML：天气详情小卡 + 年份环剩余天数 ----------
rep('''        <div class="weather-detail" id="weatherDetail">
          <span>体感 <b id="wFeels">--</b>°C</span>
          <span>湿度 <b id="wHum">--</b>%</span>
          <span>风速 <b id="wWind">--</b> km/h</span>
          <span>紫外线 <b id="wUvi">--</b></span>
        </div>''',
    '''        <div class="weather-detail" id="weatherDetail">
          <div class="wd-item"><div class="wd-label">体感</div><div class="wd-val"><b id="wFeels">--</b><span class="wd-unit">°C</span></div></div>
          <div class="wd-item"><div class="wd-label">湿度</div><div class="wd-val"><b id="wHum">--</b><span class="wd-unit">%</span></div></div>
          <div class="wd-item"><div class="wd-label">风速</div><div class="wd-val"><b id="wWind">--</b><span class="wd-unit">km/h</span></div></div>
          <div class="wd-item"><div class="wd-label">紫外线</div><div class="wd-val"><b id="wUvi">--</b><span class="wd-unit">级</span></div></div>
        </div>''',
    "weather detail html")
rep('''          <div class="ring-center">
            <span class="ring-pct" id="yearPct">--%</span>
            <span class="ring-label">今年已过</span>
          </div>
        </div>
        <p class="ring-foot" id="yearLeft">2026 年还剩 -- 天</p>''',
    '''          <div class="ring-center">
            <span class="ring-pct" id="yearLeftNum">--</span>
            <span class="ring-label">天 · 2026 还剩</span>
          </div>
        </div>
        <p class="ring-foot">今年已过 <b id="yearPctText">--%</b></p>''',
    "year ring html")

# ---------- 11. 详细日志按钮 HTML ----------
rep('''    <div class="section-head">
      <p class="kicker">CHANGELOG</p>
      <h2>更新日志</h2>
      <p class="desc">这个页面是怎么一点点长成现在这样的。</p>
    </div>''',
    '''    <div class="section-head">
      <p class="kicker">CHANGELOG</p>
      <h2>更新日志</h2>
      <p class="desc">这个页面是怎么一点点长成现在这样的。</p>
      <a class="log-more" href="changelog.html">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
        详细日志
      </a>
    </div>''',
    "log-more html")

open(path, "w", encoding="utf-8").write(html)
print("CHANGED:", ", ".join(changed))
print("DONE part1")
