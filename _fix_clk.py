# -*- coding: utf-8 -*-
"""修复：此刻板块时钟卡排版——日期换行独占一行"""
path = "index.html"
html = open(path, encoding="utf-8").read()

old = """  .now-card .clock-row {
    font-size: 18px;
    margin-top: 6px;
  }
  .now-card #clockTime {
    font-size: clamp(34px, 6vw, 52px);
    line-height: 1.15;
  }
  .now-card #clockDate { font-size: 15px; }"""
new = """  .now-card .clock-row {
    font-size: 18px;
    margin-top: 0;
    flex-wrap: wrap;
    row-gap: 6px;
    column-gap: 10px;
  }
  .now-card .clock-row svg { margin-top: 3px; }
  .now-card #clockTime {
    font-size: clamp(34px, 5vw, 48px);
    line-height: 1.15;
  }
  .now-card #clockDate { width: 100%; font-size: 15px; margin-top: 2px; }"""

if old in html:
    html = html.replace(old, new, 1)
    open(path, "w", encoding="utf-8").write(html)
    print("clock layout fixed")
else:
    print("FAIL")
