# -*- coding: utf-8 -*-
path = "index.html"
html = open(path, encoding="utf-8").read()
old = ".radar-box { max-width: 380px; margin: 0 auto; }"
new = ".radar-box { width: min(380px, 100%); margin: 0 auto; }"
if old in html:
    html = html.replace(old, new, 1)
    open(path, "w", encoding="utf-8").write(html)
    print("OK")
else:
    print("FAIL")
