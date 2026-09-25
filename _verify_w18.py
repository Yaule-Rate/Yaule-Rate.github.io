# -*- coding: utf-8 -*-
import re
html = open("index.html", encoding="utf-8").read()
m = re.search(r"<script>(.*?)</script>", html, re.S)
open("_tmp_check.js", "w", encoding="utf-8").write(m.group(1))

checks = {
  "递增公式 hold*12": "var inc = 4 + hold * 12;" in html,
  "95% 冲满": "completeLoading();" in html and "progress >= 95" in html,
  "按钮热区": "loadSkip.addEventListener('mousedown', startBoost)" in html,
  "提示文字热区": "loadHint.addEventListener('mousedown', startBoost)" in html,
  "无 translateY": "transform: translateY(8px)" not in html,
  "顶部分线 5 卡": html.count("::before {") >= 5 and "卡片顶部青色分线" in html,
  "mc-metric 青": "rgba(2,132,199,0.38)" in html,
  "btn-more 青": "rgba(2,132,199,0.05)" in html,
  "card-image 加深": "#9fd9f3" in html,
}
bad = 0
for k, v in checks.items():
    print(("OK  " if v else "BAD "), k)
    if not v: bad += 1

chg = open("changelog.html", encoding="utf-8").read()
print("OK   changelog 递增:", "hold * 12" in chg and "finishLoad" in chg)
print("OK   changelog 无位移:", "transform: translateY(8px)" not in chg)
print("FAILURES:", bad)
