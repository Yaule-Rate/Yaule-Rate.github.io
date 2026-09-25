# -*- coding: utf-8 -*-
"""把 4 个作品文件中 svg.em 块的双引号属性统一改为单引号（避免嵌入 JS 双引号字符串冲突）"""
import re
files = [
    "Xinghua Middle School Broadcasting Station System.html",
    "Self-service accounting system Pro Enhanced V6.html",
    "Nayingte M4e Code Writing System V2.9Pro.html",
    "Fancy-Pattern-Emoji-to-Image-Converter.html",
]
for f in files:
    s = open(f, encoding="utf-8").read()
    def fix_block(m):
        return m.group(0).replace('"', "'")
    s2 = re.sub(r"<svg class=\"em\".*?</svg>", fix_block, s, flags=re.S)
    open(f, "w", encoding="utf-8").write(s2)
    print("OK  ", f)
# 复验 JS 语法
import subprocess, glob
for f in files:
    s = open(f, encoding="utf-8").read()
    for i, js in enumerate(re.findall(r"<script>(.*?)</script>", s, re.S)):
        open("_t3.js", "w", encoding="utf-8").write(js)
        r = subprocess.run(["node", "--check", "_t3.js"], capture_output=True, text=True)
        print(("OK  " if r.returncode == 0 else "FAIL"), f, i)
        if r.returncode != 0:
            print(r.stderr[:300])
import os
if os.path.exists("_t3.js"): os.remove("_t3.js")
print("DONE")
