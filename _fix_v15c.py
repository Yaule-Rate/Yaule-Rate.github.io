# -*- coding: utf-8 -*-
path = "index.html"
html = open(path, encoding="utf-8").read()
old = "@media (max-width: 640px) { .skill-wrap { grid-template-columns: 1fr; gap: 24px; } }"
new = "@media (max-width: 640px) { .skill-wrap { grid-template-columns: 1fr; gap: 24px; } .radar-box { max-width: 100%; } }"
if old in html:
    html = html.replace(old, new, 1)
    open(path, "w", encoding="utf-8").write(html)
    print("OK")
else:
    print("FAIL")
