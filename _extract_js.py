# -*- coding: utf-8 -*-
"""提取 index.html 内联 <script>（无 src）到临时文件，供 node --check 校验"""
import re, os

p = "index.html"
s = open(p, encoding="utf-8").read()
blocks = re.findall(r'<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>', s, re.S)
print("内联 script 块数:", len(blocks))
out = "\n;\n".join(b for b in blocks)
tmp = "_inline_check.js"
open(tmp, "w", encoding="utf-8").write(out)
print("写出:", tmp, len(out), "chars")
