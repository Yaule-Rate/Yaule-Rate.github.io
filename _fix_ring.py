# -*- coding: utf-8 -*-
s = open("index.html", encoding="utf-8").read()
old = "if (pctText) pctText.textContent = '今年已过 ' + pct + '%';"
new = "if (pctText) pctText.textContent = pct + '%';"
assert s.count(old) == 1, "锚点数量异常: %d" % s.count(old)
s = s.replace(old, new)
open("index.html", "w", encoding="utf-8").write(s)
print("OK 年环百分比修复")
