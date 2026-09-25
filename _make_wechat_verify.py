# -*- coding: utf-8 -*-
"""创建微信部署验证文件（精确内容，无 BOM、无换行）"""
fn = "9309d4ee83c41c1b5e8e5557224562b4.txt"
content = "4ca21659c058853a3a3f7f9068738ba1af5c407a"
with open(fn, "w", encoding="ascii", newline="") as f:
    f.write(content)
# 验证：无 BOM、无换行、内容精确
raw = open(fn, "rb").read()
print("字节:", raw)
print("长度:", len(raw))
print("BOM 检查:", raw[:3] == b"\xef\xbb\xbf")
print("换行检查:", b"\n" in raw or b"\r" in raw)
