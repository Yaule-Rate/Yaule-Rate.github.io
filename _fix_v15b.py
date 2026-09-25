# -*- coding: utf-8 -*-
"""v15b 修复：雷达标签重叠 + 仓库栅格自适应列数"""
path = "index.html"
html = open(path, encoding="utf-8").read()
changed = []

# ---- 1. repo-grid 自适应列（避免 2+1 尾巴） ----
old = ".repo-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }"
new = ".repo-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; }"
if old in html:
    html = html.replace(old, new, 1); changed.append("repo-grid")
else:
    print("FAIL repo-grid")

# ---- 2. 雷达标签：小字号 + 方向锚点 ----
old_css = ".radar-label { font-size: 11.5px; fill: var(--ink-2); text-anchor: middle; }"
new_css = ".radar-label { font-size: 2.9px; fill: var(--ink-2); }"
if old_css in html:
    html = html.replace(old_css, new_css, 1); changed.append("radar css")
else:
    print("FAIL radar css")

old_js = """    var labels = '';
    for (var i5 = 0; i5 < 6; i5++) {
      var a5 = (i5 * 60 - 90) * Math.PI / 180;
      var lx = C + (R + 9) * Math.cos(a5);
      var ly = C + (R + 9) * Math.sin(a5);
      labels += '<text class="radar-label" x="' + lx.toFixed(1) + '" y="' + ly.toFixed(1) + '" dominant-baseline="middle">' + skills[i5].name + '</text>';
    }"""
new_js = """    var labels = '';
    var anchors = ['middle', 'start', 'end', 'middle', 'end', 'start'];
    for (var i5 = 0; i5 < 6; i5++) {
      var a5 = (i5 * 60 - 90) * Math.PI / 180;
      var lx = C + (R + 10) * Math.cos(a5);
      var ly = C + (R + 10) * Math.sin(a5);
      var dx = 0, dy = 0;
      if (i5 === 0) dy = -1.2;
      if (i5 === 3) dy = 1.6;
      if (i5 === 1 || i5 === 5) dx = 1.5;
      if (i5 === 2 || i5 === 4) dx = -1.5;
      labels += '<text class="radar-label" x="' + (lx + dx).toFixed(1) + '" y="' + (ly + dy).toFixed(1) + '" text-anchor="' + anchors[i5] + '" dominant-baseline="middle">' + skills[i5].name + '</text>';
    }"""
if old_js in html:
    html = html.replace(old_js, new_js, 1); changed.append("radar js")
else:
    print("FAIL radar js")

open(path, "w", encoding="utf-8").write(html)
print("CHANGED:", changed)
