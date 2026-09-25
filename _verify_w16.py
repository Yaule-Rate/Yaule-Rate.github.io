# -*- coding: utf-8 -*-
import re
html = open("index.html", encoding="utf-8").read()
m = re.search(r"<script>(.*?)</script>", html, re.S)
open("_tmp_check.js", "w", encoding="utf-8").write(m.group(1))
print("js extracted")
# 图标检查
print("luckin:", "8.59 7.185" in html)
print("netease:", "13.046 9.388" in html)
print("mc:", "23.7397 10.0058" in html)
print("bucket preset:", "[1, 2, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15, 17, 18, 19]" in html)
print("mc-log:", html.count('class="mc-ver'))
print("weather detail:", "wFeels" in html and "wHum" in html)
print("card detail count:", html.count('data-detail="works/'))
print("sb inline:", 'style="width:\' + (s.val * 10) + \'%' in html)
