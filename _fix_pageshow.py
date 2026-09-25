# -*- coding: utf-8 -*-
"""修复 pageshow bug：初始加载时 pageshow 触发（非 persisted）误把已激活的开屏遮罩关闭。
仅 bfcache 恢复（e.persisted）时重播；正常进入不做任何干预。
"""
path = "index.html"
html = open(path, encoding="utf-8").read()

old = """  window.addEventListener('pageshow', function (e) {
    if (e.persisted) { playSplash(); return; }
    if (overlay.classList.contains('active')) hideLoading();
  });"""
new = """  window.addEventListener('pageshow', function (e) {
    // 仅 bfcache 恢复（浏览器后退）时重播开屏；正常进入由 playSplash 启动，不做干预
    if (e.persisted) playSplash();
  });"""
if old not in html:
    print("FAIL 未找到 pageshow 块")
else:
    html = html.replace(old, new, 1)
    open(path, "w", encoding="utf-8").write(html)
    print("OK   pageshow 已修复")
