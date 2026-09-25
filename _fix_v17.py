# -*- coding: utf-8 -*-
path = "index.html"
html = open(path, encoding="utf-8").read()
# 提取 ring 卡 HTML 块
start = html.index('      <div class="now-card now-progress">')
end = html.index("    </div>\n  </div>\n</section>", start)
ring_block = html[start:end]
# 从原位置删除
html = html[:start] + html[end:]
# 插到 weather 卡之前（now-card now-weather 前）
anchor = '      <div class="now-card now-weather">'
html = html.replace(anchor, ring_block + "\n" + anchor, 1)
open(path, "w", encoding="utf-8").write(html)
print("ring moved")
