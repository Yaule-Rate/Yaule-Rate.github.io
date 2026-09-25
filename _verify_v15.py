# -*- coding: utf-8 -*-
import re
html = open("index.html", encoding="utf-8").read()
m = re.search(r"<script>(.*?)</script>", html, re.S)
open("_tmp_check.js", "w", encoding="utf-8").write(m.group(1))
void = {"meta","link","img","br","hr","input","path","circle","rect","polyline","line","polygon","stop","use","ellipse","radialGradient"}
stack, errs = [], []
for mm in re.finditer(r"<(/?)([a-zA-Z][a-zA-Z0-9]*)((?:\s[^<>]*?)?)(/?)>", html):
    closing, tag, attrs, selfclose = mm.group(1), mm.group(2), mm.group(3), mm.group(4)
    if tag in void or selfclose:
        continue
    if closing:
        if stack and stack[-1] == tag:
            stack.pop()
        else:
            errs.append("</%s>" % tag)
    else:
        stack.append(tag)
print("tags:", "OK" if not errs and not stack else (errs[:5], stack[-5:]))
for c in ["repoGrid", "radarSvg", "skillBars", "bucketGrid", "bkDone", "bkFill", "changelog", "radar-area", "tl-dot"]:
    print(c, "->", c in html)
print("sections:", html.count("<section"), html.count("</section>"))
