# -*- coding: utf-8 -*-
"""svg.em 块内所有属性引号统一为 &quot; 实体（HTML / JS 单双引号字符串均无冲突）"""
import re, subprocess, os
files = [
    "Xinghua Middle School Broadcasting Station System.html",
    "Self-service accounting system Pro Enhanced V6.html",
    "Nayingte M4e Code Writing System V2.9Pro.html",
    "Fancy-Pattern-Emoji-to-Image-Converter.html",
]
for f in files:
    s = open(f, encoding="utf-8").read()
    def fix_block(m):
        return re.sub(r'["\']', "&quot;", m.group(0))
    s2 = re.sub(r"<svg class=&quot;em&quot;.*?</svg>", fix_block, s, flags=re.S)
    if s2 == s:
        # 可能是单引号 class
        s2 = re.sub(r"<svg class=['\"]em['\"].*?</svg>", fix_block, s, flags=re.S)
    open(f, "w", encoding="utf-8").write(s2)
    # JS 语法复验
    for i, js in enumerate(re.findall(r"<script>(.*?)</script>", s2, re.S)):
        open("_t4.js", "w", encoding="utf-8").write(js)
        r = subprocess.run(["node", "--check", "_t4.js"], capture_output=True, text=True)
        print(("OK  " if r.returncode == 0 else "FAIL"), f, i)
        if r.returncode != 0:
            print(r.stderr[:200])
if os.path.exists("_t4.js"): os.remove("_t4.js")
print("DONE")
