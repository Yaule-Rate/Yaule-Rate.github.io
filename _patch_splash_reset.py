# -*- coding: utf-8 -*-
"""修复：bfcache 返回标签页时进度条遮罩残留（playSplash 前先复位 loadingOverlay）"""
path = "index.html"
html = open(path, encoding="utf-8").read()

old = """  function playSplash() {
    if (splashTimer) { clearTimeout(splashTimer); splashTimer = null; }
    window.scrollTo(0, 0);
    var loader = document.getElementById('pageLoader');"""

new = """  function playSplash() {
    if (splashTimer) { clearTimeout(splashTimer); splashTimer = null; }
    window.scrollTo(0, 0);
    // 修复：bfcache 返回时若此前经「进入个人空间」等跳转离开，进度条遮罩可能残留激活态——先复位隐藏
    var ov = document.getElementById('loadingOverlay');
    if (ov) {
      ov.classList.remove('active');
      var lb = document.getElementById('loadBar');
      if (lb) lb.style.width = '0%';
      var lp = document.getElementById('loadPercent');
      if (lp) lp.textContent = '0%';
      var ls = document.getElementById('loadSkip');
      if (ls) ls.classList.remove('show');
    }
    var loader = document.getElementById('pageLoader');"""

if old not in html:
    print("FAIL: playSplash 片段未找到")
else:
    html = html.replace(old, new, 1)
    open(path, "w", encoding="utf-8").write(html)
    print("OK: playSplash 已加入遮罩复位")
