# -*- coding: utf-8 -*-
"""详情页 ×6 加入评分系统：SVG 五角星（按分数填充）+ 分数 + 标签"""
import re, glob

STAR_PATH = "M12 2l2.9 6.2 6.8.8-5 4.6 1.3 6.7L12 17.8 5.9 20.3l1.3-6.7-5-4.6 6.8-.8z"

def star_svg(fill_expr):
    return '<svg viewBox="0 0 24 24" fill="%s" style="width:18px;height:18px"><path d="%s"/></svg>' % (fill_expr, STAR_PATH)

def stars_html(score):
    """按分数生成 5 颗星：整数颗全亮 + 第 5 颗按百分比渐变"""
    full = int(score)
    frac = score - full
    parts = []
    for i in range(full):
        parts.append(star_svg("currentColor"))
    if frac > 0:
        pct = int(round(frac * 100))
        gid = "rg%d" % pct
        parts.append(
            '<svg viewBox="0 0 24 24" style="width:18px;height:18px"><defs><linearGradient id="%s" x1="0" y1="0" x2="1" y2="0">'
            '<stop offset="%d%%" stop-color="currentColor"/><stop offset="%d%%" stop-color="#d5dbe3"/></linearGradient></defs>'
            '<path fill="url(#%s)" d="%s"/></svg>' % (gid, pct, pct, gid, STAR_PATH)
        )
    while len(parts) < 5:
        parts.append(star_svg("#d5dbe3"))
    return '<span class="rating-stars">' + "".join(parts) + '</span>'

CSS = """
  .rating { display: flex; align-items: center; gap: 10px; margin: 14px 0 2px; flex-wrap: wrap; }
  .rating-stars { display: inline-flex; gap: 3px; color: var(--accent); }
  .rating-score { font-size: 17px; font-weight: 700; color: var(--ink); font-variant-numeric: tabular-nums; }
  .rating-note { font-size: 12px; color: var(--ink-2); }
"""

JOBS = [
    ("works/xinghua.html", 4.9),
    ("works/accounting.html", 5.0),
    ("works/code-system.html", 4.8),
    ("works/emoji-converter.html", 5.0),
    ("works/cs-sens.html", 5.0),
    ("works/chess.html", 4.9),
]
for f, score in JOBS:
    s = open(f, encoding="utf-8").read()
    log = []
    if "rating-stars" not in s:
        # 注入 CSS
        s = s.replace("</style>", CSS + "</style>", 1)
        log.append("CSS")
        # 注入 HTML：在 .actions 前
        star = stars_html(score)
        rating = ('\n    <div class="rating">\n      ' + star +
                  '\n      <span class="rating-score">%.1f</span>\n      <span class="rating-note">用户评分 · 满分 5.0</span>\n    </div>' % score)
        m = re.search(r'(<div class="actions">)', s)
        if m:
            s = s[:m.start()] + rating + "\n" + s[m.start():]
            log.append("HTML @actions")
    open(f, "w", encoding="utf-8").write(s)
    print("OK  ", f, "-> %.1f | " % score, " / ".join(log))
print("DONE")
