# -*- coding: utf-8 -*-
path = "index.html"
html = open(path, encoding="utf-8").read()
old = ".skill-bar-row .sb-fill { height: 100%; background: linear-gradient(90deg, var(--accent), var(--accent-2)); border-radius: 999px; width: 0; transition: width 0.9s ease; }"
new = ".skill-bar-row .sb-fill { height: 100%; background: linear-gradient(90deg, var(--accent), var(--accent-2)); border-radius: 999px; }"
if old in html:
    html = html.replace(old, new, 1)
    open(path, "w", encoding="utf-8").write(html)
    print("OK")
else:
    print("FAIL")
