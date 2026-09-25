# -*- coding: utf-8 -*-
"""修正 playSplash：初始播放不克隆（避免 Y 画两遍），仅 bfcache 重播时重建/克隆"""
path = "index.html"
html = open(path, encoding="utf-8").read()

old = """  /* ========== 开屏动画：青色 Y 一笔画（每次进入本站均播放，含作品页返回 / 浏览器后退） ========== */
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
  playSplash();"""
new = """  /* ========== 开屏动画：青色 Y 一笔画（每次进入本站均播放，含作品页返回 / 浏览器后退） ========== */
  var splashTimer = null;
  function playSplash(restart) {
    if (splashTimer) { clearTimeout(splashTimer); splashTimer = null; }
    var loader = document.getElementById('pageLoader');
    if (!loader) {
      // bfcache 返回时原 loader 已从 DOM 移除：重建并播放
      loader = document.createElement('div');
      loader.className = 'page-loader';
      loader.id = 'pageLoader';
      loader.innerHTML = '<svg class="loader-svg" viewBox="0 0 120 120" fill="none" stroke="currentColor" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"><path class="loader-path" pathLength="100" d="M22 18 L60 54 L98 18 M60 54 L60 102"/></svg><p class="loader-name">Yaule</p>';
      document.body.insertBefore(loader, document.body.firstChild);
    } else if (restart) {
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
  playSplash(false);"""

if old not in html:
    print("FAIL 未找到 playSplash 块")
else:
    html = html.replace(old, new, 1)
    # pageshow 调用带 true
    html = html.replace("if (e.persisted) { playSplash(); return; }",
                        "if (e.persisted) { playSplash(true); return; }", 1)
    open(path, "w", encoding="utf-8").write(html)
    print("OK   playSplash 参数化完成")
