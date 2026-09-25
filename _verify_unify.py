# -*- coding: utf-8 -*-
import re
html = open("index.html", encoding="utf-8").read()
s = re.search(r"<script>(.*?)</script>", html, re.S)
open("_tmp_chk.js", "w", encoding="utf-8").write(s.group(1))

checks = {
    "overlay 含 Y SVG": 'class="loader-svg"' in html and "loader-path" in html,
    "overlay 含名字": '<p class="loader-name">Yaule</p>' in html,
    "overlay 实底背景": ".loading-overlay {\n    position: fixed;\n    inset: 0;\n    background: var(--bg);" in html,
    "无独立 pageLoader HTML": 'id="pageLoader"' not in html,
    "无 loadTitle": "loadTitle" not in html,
    "startLoading 重播 Y": "lp.parentNode.replaceChild(lc, lp)" in html,
    "playSplash 统一": "function playSplash() {\n    window.scrollTo(0, 0);\n    startLoading('', '', false);" in html,
    "pageshow 补播": "if (e.persisted) { playSplash(); return; }" in html,
    "keyframes 存在": "@keyframes loaderDraw" in html and "@keyframes loaderName" in html,
    "进度条 300px": ".loading-bar {\n    width: 300px;" in html,
}
bad = 0
for k, v in checks.items():
    print(("OK  " if v else "BAD "), k)
    if not v: bad += 1
print("FAILURES:", bad)
