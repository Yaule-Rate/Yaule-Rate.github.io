# -*- coding: utf-8 -*-
"""日志 v21：index.html YAULE_CHANGELOG + changelog.html FALLBACK_LOGS 同步插入"""

V21 = """    { ver: "v21", date: "2026-09-25 20:18:00", current: true, list: [
      { lv: "[ADD]", time: "2026-09-25 20:18:00", text: "整站 i18n：右上角中英一键切换，独立 3 秒伪进度条。" },
      { lv: "[ADD]", time: "2026-09-25 20:09:47", text: "此刻 · 每日推荐：结合节日 / 天气 / 星期，每天一条。" },
      { lv: "[ADD]", time: "2026-09-25 19:58:32", text: "页面转场：返回标签页时 View Transitions 衔接。" },
      { lv: "[ADD]", time: "2026-09-25 19:50:10", text: "独立 404 页：Y 一笔画 + 「失眠夜迷路了」+ 返回按钮。" }
    ]},
"""

old_v19 = '    { ver: "v19.6", date: "2026-09-25 16:20:11", current: true, list: ['
new_v19 = '    { ver: "v19.6", date: "2026-09-25 16:20:11", current: false, list: ['

for f, anchor in [("index.html", "  var YAULE_CHANGELOG = [\n"), ("changelog.html", "var FALLBACK_LOGS = [\n")]:
    s = open(f, encoding="utf-8").read()
    assert anchor in s, f
    assert s.count(old_v19) == 1, (f, s.count(old_v19))
    s = s.replace(anchor, anchor + V21, 1)
    s = s.replace(old_v19, new_v19, 1)
    open(f, "w", encoding="utf-8").write(s)
    print("OK", f)
print("DONE")
