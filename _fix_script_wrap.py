# -*- coding: utf-8 -*-
"""把注入的裸 JS 包进 <script> 标签（修复未执行问题）"""
s = open("index.html", encoding="utf-8").read()
mark = "  /* ========== 整站 i18n：中英切换（3 秒伪进度条） ========== */"
idx = s.find(mark)
assert idx != -1, "未找到 i18n JS 起点"
# 检查起点前是否已是 <script>（防止重复包裹）
before = s[max(0, idx - 40):idx]
if "<script>" in before:
    print("已是 script 块内，无需处理")
else:
    # 找到注入块结尾：紧随其后的 "</body>"
    end_mark = "\n</body>"
    eidx = s.find(end_mark, idx)
    assert eidx != -1, "未找到 </body>"
    s = s[:idx] + "<script>\n" + s[idx:eidx] + "\n</script>" + s[eidx:]
    open("index.html", "w", encoding="utf-8").write(s)
    print("OK 已包裹 <script> 标签")
