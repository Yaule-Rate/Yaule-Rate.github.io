# -*- coding: utf-8 -*-
"""残留修复：.textContent = '<svg...>' -> .innerHTML = '<svg...>'"""
import re
for f in [
    "Self-service accounting system Pro Enhanced V6.html",
    "Nayingte M4e Code Writing System V2.9Pro.html",
]:
    s = open(f, encoding="utf-8").read()
    s2 = re.sub(r"\.textContent = (['\"])<svg", r".innerHTML = \1<svg", s)
    open(f, "w", encoding="utf-8").write(s2)
    print("OK  ", f, "| 修改:", s.count(".textContent = '<svg"))
