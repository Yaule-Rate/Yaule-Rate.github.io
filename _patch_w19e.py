# -*- coding: utf-8 -*-
"""v19 微修：清单项去掉 cursor/hover（不可交互展示）；分享按钮移动端加大命中区"""
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

# 1. bucket-item：去掉 cursor:pointer 与 hover 动效（清单为预设展示，不可点击）
rep("""    font-size: 13px;
    color: var(--ink-2);
    cursor: pointer;
    transition: all 0.18s ease;
    user-select: none;
  }
  .bucket-item:hover { border-color: var(--accent); transform: translateY(-2px); }""",
"""    font-size: 13px;
    color: var(--ink-2);
    transition: border-color 0.18s ease;
    user-select: none;
  }""",
"bucket-item 去 cursor/hover")

# 2. v18 追加的 hover 也去掉（防止误触提示）
rep("""  .bucket-item { transition: border-color 0.15s, transform 0.15s; }
  .bucket-item:hover { border-color: rgba(2,132,199,0.45); transform: translateY(-2px); }""",
"""  .bucket-item { transition: border-color 0.15s; }""",
"v18 hover 清除")

# 3. 分享按钮移动端 min-height 44px
rep("""    html { scroll-behavior: auto; }
    .card, .btn-enter, .btn-more, .card-dl, .mc-tab { transition: none; }""",
"""    html { scroll-behavior: auto; }
    .card, .btn-enter, .btn-more, .card-dl, .mc-tab { transition: none; }
    .card-share { min-height: 44px; }""",
"分享按钮移动端命中区")

open(path, "w", encoding="utf-8").write(html)
for l in log:
    print(l)
print("DONE")
