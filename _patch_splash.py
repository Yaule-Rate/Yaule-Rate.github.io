# -*- coding: utf-8 -*-
"""开屏动画修正：用户要的是「青色 Y 一笔画 + Yaule」品牌开屏，不是 8 秒进度条。
1. 回滚上一轮的 playIntro（8 秒进度条遮罩开屏）
2. 新增 playSplash()：每次进入本站重播 Y 一笔画（含 bfcache 返回时重建 loader）
3. pageshow persisted -> playSplash()
"""
path = "index.html"
html = open(path, encoding="utf-8").read()
log = []

def rep(old, new, tag):
    global html
    if old not in html:
        log.append("FAIL " + tag)
        return
    html = html.replace(old, new, 1)
    log.append("OK   " + tag)

# 1. 回滚 playIntro 块 -> pageshow 改调 playSplash
rep("""  /* ========== 每次进入本站自动开屏动画（访问 / 刷新 / 作品页返回 / 浏览器后退均触发） ========== */
  function playIntro() {
    window.scrollTo(0, 0);
    startLoading('', '欢迎你的到来', false);
  }
  playIntro();

  // 修复：浏览器后退（bfcache 恢复）时进度条残留 —— 同时补播开屏动画
  window.addEventListener('pageshow', function (e) {
    if (e.persisted) { playIntro(); return; }
    if (overlay.classList.contains('active')) hideLoading();
  });""",
"""  // 修复：浏览器后退（bfcache 恢复）时进度条残留 —— 同时重播 Y 一笔画开屏
  window.addEventListener('pageshow', function (e) {
    if (e.persisted) { playSplash(); return; }
    if (overlay.classList.contains('active')) hideLoading();
  });""",
"回滚 playIntro -> pageshow 调 playSplash")

# 2. 页面加载动画移除块 -> playSplash 管理（初始调用 + bfcache 重建）
rep("""  /* ========== 页面加载动画移除 ========== */
  (function () {
    var loader = document.getElementById('pageLoader');
    if (!loader) return;
    setTimeout(function () {
      loader.classList.add('done');
      setTimeout(function () {
        if (loader.parentNode) loader.parentNode.removeChild(loader);
      }, 600);
    }, 1700);
  })();""",
"""  /* ========== 开屏动画：青色 Y 一笔画（每次进入本站均播放，含作品页返回 / 浏览器后退） ========== */
  var splashTimer = null;
  function playSplash() {
    if (splashTimer) { clearTimeout(splashTimer); splashTimer = null; }
    var loader = document.getElementById('pageLoader');
    if (!loader) {
      // bfcache 返回时原 loader 已从 DOM 移除：重建并播放
      loader = document.createElement('div');
      loader.className = 'page-loader';
      loader.id = 'pageLoader';
      loader.innerHTML = '<svg class="loader-svg" viewBox="0 0 120 120" fill="none" stroke="currentColor" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"><path class="loader-path" pathLength="100" d="M22 18 L60 54 L98 18 M60 54 L60 102"/></svg><p class="loader-name">Yaule</p>';
      document.body.insertBefore(loader, document.body.firstChild);
    } else {
      // 重播：克隆路径与名字节点以重新触发 CSS 动画
      var path = loader.querySelector('.loader-path');
      if (path) { var c1 = path.cloneNode(true); path.parentNode.replaceChild(c1, path); }
      var name = loader.querySelector('.loader-name');
      if (name) { var c2 = name.cloneNode(true); name.parentNode.replaceChild(c2, name); }
      loader.classList.remove('done');
    }
    splashTimer = setTimeout(function () {
      loader.classList.add('done');
    }, 1700);
  }
  playSplash();""",
"页面加载动画块 -> playSplash")

open(path, "w", encoding="utf-8").write(html)
for l in log:
    print(l)
print("DONE")
