# -*- coding: utf-8 -*-
import re, glob

def extract_scripts(path):
    s = open(path, encoding="utf-8").read()
    return re.findall(r"<script>(.*?)</script>", s, re.S)

# 主页检查
html = open("index.html", encoding="utf-8").read()
checks = {
    "主页有 pageLoader": 'id="pageLoader"' in html,
    "主页简笔画 CSS": ".page-loader {\n    position: fixed;\n    inset: 0;\n    z-index: 9999;\n    background: var(--bg);" in html,
    "主页 playSplash 简笔画": "loader.classList.add('done');" in html and "splashTimer" in html,
    "主页无 startLoading('') 开屏": "startLoading('', '', false)" not in html,
    "卡片无 data-loading": html.count("data-loading=\"正在加载作品\"") == 0,
    "卡片点击统一进详情": "if (dd) { window.location.href = dd; }" in html and "classList.toggle('expanded')" not in html,
    "overlay 保留进度条一体": "loading-overlay .loader-svg" in html and "loading-bar" in html,
    "主页 data-loading 跳转保留": "a[data-loading]" in html,
}
bad = 0
for k, v in checks.items():
    print(("OK  " if v else "BAD "), k)
    if not v: bad += 1

# 详情页检查
for f in sorted(glob.glob("works/*.html")):
    s = open(f, encoding="utf-8").read()
    ok = ("立即体验" in s and 'id="pageLoader"' in s
          and "document.querySelector('.btn-primary')" in s
          and "window.location.href = target" in s
          and "长按加速" in s)
    print(("OK  " if ok else "BAD "), f)
    if not ok: bad += 1
print("FAILURES:", bad)
