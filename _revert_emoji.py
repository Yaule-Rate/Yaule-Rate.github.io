# -*- coding: utf-8 -*-
"""验证作品 emoji 恢复 + 日志同步修正（删除 v19.6 中「emoji 替换为 SVG」一条）"""
import re

# 1. 验证作品 emoji 恢复
files = [
    "Xinghua Middle School Broadcasting Station System.html",
    "Self-service accounting system Pro Enhanced V6.html",
    "Nayingte M4e Code Writing System V2.9Pro.html",
    "Fancy-Pattern-Emoji-to-Image-Converter.html",
]
for f in files:
    s = open(f, encoding="utf-8").read()
    em = set(re.findall(r"[\U0001F000-\U0001FAFF\u2600-\u27BF\u2705\u274C]", s))
    svg_em = s.count('class=&quot;em&quot;') + s.count('class="em"') + s.count("class='em'")
    print("====", f, "| emoji 种类:", len(em), "| svg.em 残留:", svg_em)

# 2. 日志同步修正：删除 v19.6 中 emoji 替换一条（index + changelog）
old_line = '      { lv: "[ADD]", time: "2026-09-25 16:12:30", text: "四件作品内全部 emoji 替换为内联 SVG 图标。" },\n'
for f in ["index.html", "changelog.html"]:
    s = open(f, encoding="utf-8").read()
    n = s.count(old_line)
    s = s.replace(old_line, "")
    open(f, "w", encoding="utf-8").write(s)
    print("OK  ", f, "| 删除 emoji 日志行:", n)
print("DONE")
