# -*- coding: utf-8 -*-
"""取消统一顶部青色渐变细线（v18 青色血脉），保留卡片 position:relative（分享浮层定位依赖）"""
path = "index.html"
html = open(path, encoding="utf-8").read()

old = """  /* ===== v18 视觉统一：下方板块注入青色血脉（顶部渐变分线） ===== */
  .card, .repo-card, .mc-ver, .now-card, .bucket-item { position: relative; }
  .card::before, .repo-card::before, .mc-ver::before, .now-card::before, .bucket-item::before {
    content: "";
    position: absolute; top: 0; left: 0; right: 0; height: 3px;
    border-radius: 999px 999px 0 0;
    background: linear-gradient(90deg, var(--accent), var(--accent-2));
    opacity: 0.9;
    pointer-events: none;
    z-index: 1;
  }
  .bucket-item { transition: border-color 0.15s; }

"""
new = """  .card, .repo-card, .mc-ver, .now-card, .bucket-item { position: relative; }

"""
if old not in html:
    print("FAIL 未找到目标代码块")
else:
    html = html.replace(old, new, 1)
    open(path, "w", encoding="utf-8").write(html)
    print("OK   顶部渐变线已取消")
    print("残留 ::before 计数:", html.count("height: 3px"))
