# -*- coding: utf-8 -*-
import re
html = open("index.html", encoding="utf-8").read()
s = re.search(r"<script>(.*?)</script>", html, re.S)
open("_tmp_chk.js", "w", encoding="utf-8").write(s.group(1))

checks = {
    "playSplash 定义": "function playSplash(restart)" in html,
    "初始调用 false": "playSplash(false);" in html,
    "bfcache 重播 true": "if (e.persisted) { playSplash(true); return; }" in html,
    "loader 重建": "document.createElement('div')" in html and "loader.className = 'page-loader'" in html,
    "重播克隆路径": "cloneNode(true)" in html,
    "playIntro 已移除": "function playIntro" not in html,
    "8 秒进度条开屏已移除": "startLoading('', '欢迎你的到来', false)" not in html,
    "completeLoading 分支保留": "} else if (pendingUrl) {" in html,
}
bad = 0
for k, v in checks.items():
    print(("OK  " if v else "BAD "), k)
    if not v: bad += 1
print("FAILURES:", bad)
