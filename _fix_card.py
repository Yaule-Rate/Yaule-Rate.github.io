# -*- coding: utf-8 -*-
"""v14-fix: 卡片交互修复——点任意处展开简介；查看详情同页打开（去掉 target=_blank 防拦截）"""
import re
path = "index.html"
html = open(path, encoding="utf-8").read()
changed = []

# ---------- 1. card-image 去掉 target="_blank"（6 处） ----------
old_pat = re.compile(r'(<a class="card-image" href="[^"]+" )target="_blank" rel="noopener"( data-loading="[^"]*")>')
def repl(m):
    changed.append("no-blank: " + m.group(1)[:50])
    return m.group(1) + 'rel="noopener"' + m.group(2) + '>'
html, n = old_pat.subn(repl, html)
if n == 0:
    print("FAIL no-blank")
print("no-blank count:", n)

# ---------- 2. 卡片点击 handler ----------
old_click = """    card.addEventListener('click', function (e) {
      if (e.target.closest('.card-dl')) return;
      var link = this.querySelector('a.card-image');
      if (e.target.closest('a.card-image')) return;
      if (e.target.closest('.meta')) {
        if (link) link.click();
        return;
      }
      this.classList.toggle('expanded');
    });"""
new_click = """    card.addEventListener('click', function (e) {
      if (e.target.closest('.card-dl')) return;
      if (e.target.closest('a.card-image')) {
        e.preventDefault();
        this.classList.toggle('expanded');
        return;
      }
      if (e.target.closest('.meta')) {
        var link = this.querySelector('a.card-image');
        if (link) link.click();
        return;
      }
      this.classList.toggle('expanded');
    });"""
if old_click in html:
    html = html.replace(old_click, new_click, 1); changed.append("click handler")
else:
    print("FAIL click handler")

# ---------- 3. 展开态小提示：meta 文字在展开时变化 ----------
old_meta_css = """  .card { cursor: pointer; }
  .card .meta { transition: color 0.2s ease; }
  .card.expanded .meta { color: var(--accent); }"""
new_meta_css = """  .card { cursor: pointer; }
  .card .meta { transition: color 0.2s ease; }
  .card.expanded .meta { color: var(--accent); }
  .card .meta::after { content: "查看详情 →"; }
  .card.expanded .meta::after { content: "打开作品 →"; }"""
if old_meta_css in html:
    html = html.replace(old_meta_css, new_meta_css, 1); changed.append("meta css")
else:
    print("FAIL meta css")

# ---------- 4. 去掉 meta 里的旧文字（由 ::after 提供） ----------
old_meta_html = '<span class="meta">查看详情 →</span>'
if old_meta_html in html:
    html = html.replace(old_meta_html, '<span class="meta"></span>')
    changed.append("meta html")
else:
    print("FAIL meta html")

open(path, "w", encoding="utf-8").write(html)
print("CHANGED:", changed)
