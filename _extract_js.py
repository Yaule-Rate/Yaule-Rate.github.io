# -*- coding: utf-8 -*-
"""提取 index.html 内联 <script>（无 src、非 JSON-LD）到临时文件，供 node --check 校验"""
import re

p = "index.html"
s = open(p, encoding="utf-8").read()
blocks = []
for m in re.finditer(r'<script(?P<attrs>[^>]*)>(?P<body>.*?)</script>', s, re.S):
    attrs = m.group('attrs')
    if re.search(r'\bsrc=', attrs):
        continue
    if 'ld+json' in attrs:
        continue
    blocks.append(m.group('body'))
print("内联 script 块数:", len(blocks))
out = "\n;\n".join(blocks)
tmp = "_inline_check.js"
open(tmp, "w", encoding="utf-8").write(out)
print("写出:", tmp, len(out), "chars")
