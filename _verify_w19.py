# -*- coding: utf-8 -*-
import re
html = open("index.html", encoding="utf-8").read()

checks = {
  "title 加长": "| 个人主页 · 失眠夜空间 · 作品与日常" in html,
  "description 加长": "校园工具到游戏辅助的自研项目" in html,
  "分享按钮 CSS": ".card-share" in html and ".share-pop" in html,
  "分享 JS 注入": "card-foot" in html and "service.weibo.com" in html and "shareqq" in html,
  "标语轮换": "正在泡咖啡" in html and "loadHint" in html,
  "自动深色": "h >= 22 || h < 6" in html,
  "防重注入": html.count("card-foot')") <= 2 and html.count("share-pop =") <= 2,
}
bad = 0
for k, v in checks.items():
    print(("OK  " if v else "BAD "), k)
    if not v: bad += 1

chg = open("changelog.html", encoding="utf-8").read()
print("OK   changelog title:", "完整版本记录与详细时间戳" in chg)
print("OK   changelog 标语:", "正在整理日志" in chg and 'id="loadHint"' in chg)
print("OK   changelog 自动深色:", "h >= 22 || h < 6" in chg)

sp = open("space.html", encoding="utf-8").read()
print("OK   space description:", "失眠夜个人空间" in sp and "og:title" in sp)

w = open("works/xinghua.html", encoding="utf-8").read()
print("OK   works desc 加长:", "投入校园实际使用" in w and len(re.search(r'<meta name="description" content="(.*?)">', w).group(1)) > 60)

# 提取所有 script 检查语法
for f in ("index.html", "changelog.html"):
    s = open(f, encoding="utf-8").read()
    m = re.search(r"<script>(.*?)</script>", s, re.S)
    open("_tmp_chk_%s.js" % f.split(".")[0], "w", encoding="utf-8").write(m.group(1))
print("FAILURES:", bad)
