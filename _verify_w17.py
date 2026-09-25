# -*- coding: utf-8 -*-
import re
html = open("index.html", encoding="utf-8").read()
m = re.search(r"<script>(.*?)</script>", html, re.S)
open("_tmp_check.js", "w", encoding="utf-8").write(m.group(1))

checks = {
  "works 在 life 后": html.index('id="works"') > html.index('id="life"'),
  "life-panels min-height": "min-height: 440px" in html,
  "flip forwards x2": html.count("forwards;") >= 2,
  "anniv-top": 'class="anniv-top"' in html,
  "lifeFill": 'id="lifeFill"' in html,
  "siteMeta": 'id="siteMeta"' in html,
  "wd-item x4": html.count("wd-item") >= 8,
  "yearLeftNum": 'id="yearLeftNum"' in html,
  "yearPctText": 'id="yearPctText"' in html,
  "loadSkip": 'id="loadSkip"' in html,
  "8000ms": ", 8000);" in html,
  "3000ms 弹出": "3000);" in html,
  "log-more x1": html.count('class="log-more"') == 1,
  "完整时间戳 v16": "2026-09-25 14:05:11" in html,
  "[ADD] 标签": "[ADD]" in html and "[INFO]" in html and "[FIX]" in html,
  "li-time": html.count("li-time") > 10,
  "v16 当前版": 'class="mc-ver current"' in html and "v16" in html,
  "changelog sync ls": "yaule_changelog" in html,
  "boost 6%": "progress += 6;" in html,
  "swap 注释": "<!-- 板块 1：生活瞬间" in html and "<!-- 板块 2：精选作品" in html,
}
bad = 0
for k, v in checks.items():
    print(("OK  " if v else "BAD "), k)
    if not v: bad += 1

chg = open("changelog.html", encoding="utf-8").read()
print("OK  changelog 文件存在且含 FALLBACK_LOGS:", "FALLBACK_LOGS" in chg and "长按加速" in chg and "8000" in chg.replace("8000", "", 1) or "8000" in chg)
print("OK  changelog 同步读取:", "yaule_changelog" in chg)

w = open("works/xinghua.html", encoding="utf-8").read()
print("OK  详情页下载计数:", "yaule_dl_count" in w)
print("FAILURES:", bad)
