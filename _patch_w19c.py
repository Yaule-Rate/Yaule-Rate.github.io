# -*- coding: utf-8 -*-
"""v19 space.html：补全 SEO——title 加长 + description/og 元信息（必应提示标题与描述过短）"""
path = "space.html"
html = open(path, encoding="utf-8").read()
log = []

def rep(old, new, tag):
    global html
    if old not in html:
        log.append("FAIL " + tag)
        return
    html = html.replace(old, new, 1)
    log.append("OK   " + tag)

rep("<title>失眠夜の个人空间</title>",
    "<title>失眠夜 · 个人空间 | Yaule 的作品、荣誉与日常</title>",
    "title 加长")

rep('<meta name="creative-medium" content="interactive-prototype">',
    '''<meta name="creative-medium" content="interactive-prototype">
<meta name="description" content="Yaule 的失眠夜个人空间：收录自研作品与项目（广播站系统、记账工具、代码编写系统等）、荣誉奖项与联系方式的完整个人主页。">
<meta name="keywords" content="Yaule,个人空间,作品集,广播站系统,记账工具,代码编写,GitHub Pages,失眠夜">
<meta property="og:type" content="website">
<meta property="og:title" content="失眠夜 · 个人空间 | Yaule">
<meta property="og:description" content="Yaule 的失眠夜个人空间：收录自研作品与项目、荣誉奖项与联系方式。">
<meta property="og:url" content="https://Yaule-Rate.github.io/space.html">
<meta property="og:site_name" content="Yaule 的个人空间">
<meta property="og:locale" content="zh_CN">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="失眠夜 · 个人空间 | Yaule">
<meta name="twitter:description" content="Yaule 的失眠夜个人空间：收录自研作品与项目、荣誉奖项与联系方式。">''',
    "补全 description/og")

open(path, "w", encoding="utf-8").write(html)
for l in log:
    print(l)
print("DONE")
