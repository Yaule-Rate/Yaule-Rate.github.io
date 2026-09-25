# -*- coding: utf-8 -*-
"""每次进入 index 自动开屏动画：
1. completeLoading 支持无跳转模式（pendingUrl 为空 → 淡出遮罩停留本页，hash 锚点恢复）
2. 新增 playIntro()：滚回顶部 + startLoading('', '欢迎你的到来', false)，播完停留
3. 页面加载即调用；bfcache 后退也补播开屏（作品页返回、刷新、直接访问均触发）
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

# 1. completeLoading 无跳转分支
rep("""    setTimeout(function () {
      if (pendingNew) {
        window.open(pendingUrl, '_blank');
        hideLoading();
        showToast('已在新标签页打开');
      } else {
        window.location.href = pendingUrl;
      }
    }, 250);""",
"""    setTimeout(function () {
      if (pendingNew) {
        window.open(pendingUrl, '_blank');
        hideLoading();
        showToast('已在新标签页打开');
      } else if (pendingUrl) {
        window.location.href = pendingUrl;
      } else {
        // 开屏模式：无跳转，淡出遮罩停留本页；带锚点（如 #changelog）则滚回该处
        hideLoading();
        if (location.hash) {
          var el = document.getElementById(location.hash.slice(1));
          if (el && el.scrollIntoView) el.scrollIntoView({ behavior: 'auto' });
        }
      }
    }, 250);""",
"completeLoading 开屏分支")

# 2. playIntro 定义 + 调用（放在 data-loading 绑定之后）
rep("""  document.querySelectorAll('a[data-loading]').forEach(function (link) {
    link.addEventListener('click', function (e) {
      e.preventDefault();
      var title = this.getAttribute('data-loading');
      var url = this.getAttribute('href');
      var openInNew = this.getAttribute('target') === '_blank';
      startLoading(url, title, openInNew);
    });
  });

  // 修复：浏览器后退（bfcache 恢复）时进度条残留
  window.addEventListener('pageshow', function (e) {
    if (e.persisted || overlay.classList.contains('active')) hideLoading();
  });""",
"""  document.querySelectorAll('a[data-loading]').forEach(function (link) {
    link.addEventListener('click', function (e) {
      e.preventDefault();
      var title = this.getAttribute('data-loading');
      var url = this.getAttribute('href');
      var openInNew = this.getAttribute('target') === '_blank';
      startLoading(url, title, openInNew);
    });
  });

  /* ========== 每次进入本站自动开屏动画（访问 / 刷新 / 作品页返回 / 浏览器后退均触发） ========== */
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
"playIntro 定义与调用")

open(path, "w", encoding="utf-8").write(html)
for l in log:
    print(l)
print("DONE")
