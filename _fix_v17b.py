# -*- coding: utf-8 -*-
path = "index.html"
html = open(path, encoding="utf-8").read()
old = "<p class=\"ring-foot\">今年已过 <b id=\"yearPctText\">--%</b></p>"
if old in html:
    html = html.replace(old, "<p class=\"ring-foot\"><b id=\"yearPctText\">今年已过 --%</b></p>", 1)
    old_js = "if (pctText) pctText.textContent = y + ' 年已过 ' + pct + '%';"
    new_js = "if (pctText) pctText.textContent = '今年已过 ' + pct + '%';"
    if old_js in html:
        html = html.replace(old_js, new_js, 1)
        open(path, "w", encoding="utf-8").write(html)
        print("OK")
    else:
        print("FAIL js")
else:
    print("FAIL html")
