# -*- coding: utf-8 -*-
import re
html = open("index.html", encoding="utf-8").read()
s = re.search(r"<script>(.*?)</script>", html, re.S)
open("_tmp_chk.js", "w", encoding="utf-8").write(s.group(1))

checks = {
    "playIntro 定义": "function playIntro()" in html,
    "开屏调用": "playIntro();" in html,
    "开屏标题": "欢迎你的到来" in html and "startLoading('', '欢迎你的到来', false)" in html,
    "completeLoading 开屏分支": "} else if (pendingUrl) {" in html and "开屏模式" in html,
    "bfcache 补播": "if (e.persisted) { playIntro(); return; }" in html,
    "hash 锚点恢复": "location.hash.slice(1)" in html,
}
bad = 0
for k, v in checks.items():
    print(("OK  " if v else "BAD "), k)
    if not v: bad += 1
print("FAILURES:", bad)
