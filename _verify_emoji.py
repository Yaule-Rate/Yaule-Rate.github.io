# -*- coding: utf-8 -*-
import re, glob
files = [
    "Xinghua Middle School Broadcasting Station System.html",
    "Self-service accounting system Pro Enhanced V6.html",
    "Nayingte M4e Code Writing System V2.9Pro.html",
    "Fancy-Pattern-Emoji-to-Image-Converter.html",
]
bad = 0
for f in files:
    s = open(f, encoding="utf-8").read()
    # 残留 emoji
    em = re.findall(r"[\U0001F000-\U0001FAFF\u2600-\u27BF\u2705\u274C]", s)
    # textContent 里含 <svg（会显示源码）
    tc = re.findall(r"\.textContent = ['\"][^'\"]*<svg", s)
    # 未被替换的 emoji 上下文
    ctx = []
    seen = set()
    for m in re.finditer(r"[\U0001F000-\U0001FAFF\u2600-\u27BF\u2705\u274C]", s):
        ch = m.group(0)
        if ch in seen: continue
        seen.add(ch)
        pos = m.start()
        ctx.append((ch, s[max(0,pos-25):pos+10].replace("\n", " ")))
    print("====", f, "| 残留 emoji:", len(em), "| textContent 含 svg:", len(tc))
    for ch, c in ctx[:10]:
        print("   %s  ...%s..." % (ch, c))
    if em or tc:
        bad += 1
print("ISSUES:", bad)
