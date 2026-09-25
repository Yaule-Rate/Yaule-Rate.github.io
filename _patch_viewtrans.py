# -*- coding: utf-8 -*-
"""页面转场（View Transitions MPA）：index/space/changelog/works×6 注入转场 CSS"""
import os, glob

CSS = """
  /* ===== 页面转场（View Transitions）===== */
  @view-transition { navigation: auto; }
  ::view-transition-old(root) { animation: yt-out .22s ease both; }
  ::view-transition-new(root) { animation: yt-in .34s ease both; }
  @keyframes yt-out { to { opacity: 0; transform: scale(.98); } }
  @keyframes yt-in { from { opacity: 0; transform: translateY(12px); } }
"""

files = ["index.html", "space.html", "changelog.html"] + sorted(glob.glob("works/*.html"))
for f in files:
    if not os.path.exists(f):
        print("SKIP (不存在)", f); continue
    s = open(f, encoding="utf-8").read()
    if "@view-transition" in s:
        print("SKIP (已有)", f); continue
    idx = s.rfind("</style>")
    if idx == -1:
        print("FAIL (无 </style>)", f); continue
    s = s[:idx] + CSS + s[idx:]
    open(f, "w", encoding="utf-8").write(s)
    print("OK  ", f)
print("DONE")
