# -*- coding: utf-8 -*-
"""v19.2 根目录 6 个旧版作品页 SEO 补齐：title 加长 + meta description（与 works/ 详情页同口径）+ og"""
import re

PLAN = {
    "Xinghua Middle School Broadcasting Station System.html": {
        "title": "兴华中学广播站系统 · 校园广播管理工具 | Yaule 作品",
        "desc": "兴华中学广播站系统是 Yaule 独立设计开发并投入校园实际使用的广播管理工具：广播排班管理、播放日程控制、站点信息维护一站式完成，从需求梳理到上线运营全部独立完成。",
    },
    "Self-service accounting system Pro Enhanced V6.html": {
        "title": "自助记账系统 Pro Enhanced V6 · 收支统计工具 | Yaule 作品",
        "desc": "自助记账系统 Pro 是轻量化单文件本地记账工具：收支记录、分类统计、数据可视化报表开箱即用，无需联网不泄露隐私，适合日常记账与月度复盘。",
    },
    "Nayingte M4e Code Writing System V2.9Pro.html": {
        "title": "纳英特 M4e 代码编写系统 V2.9Pro · 可视化编程工具 | Yaule 作品",
        "desc": "代码编写系统是一款可视化拖拽生成 C++ 代码的辅助工作台：通过图形化积木式操作降低编程入门门槛，内置模板库与代码生成引擎，助力机器人编程学习。",
    },
    "Fancy-Pattern-Emoji-to-Image-Converter.html": {
        "title": "花式图案表情转图片转换器 · 表情一键转图 | Yaule 作品",
        "desc": "表情转图片转换器可以把文字与表情符号一键转成高清 PNG 图片：支持自定义背景色、文字颜色与排版，适合聊天表情包、社交分享与创意海报制作。",
    },
    "CS-Sens-Calibrator.html": {
        "title": "AIM MATRIX 量子瞄准校准矩阵 · CS 灵敏度校准 | Yaule 作品",
        "desc": "CS 灵敏度校准器是一款 FPS 游戏鼠标灵敏度校准工具：通过科学换算与多游戏灵敏度映射，帮助你找到真正适合自己的手感，告别凭感觉调灵敏度。",
    },
    "Chess-Gomoku-Collection.html": {
        "title": "对弈 · 五子棋与中国象棋合集 | Yaule 作品",
        "desc": "棋类合集将五子棋与中国象棋合二为一，本地运行无需联网：支持同屏双人对战、悔棋与难度选择，约上好友面对面来一局，随时随地开棋。",
    },
}

for f, meta in PLAN.items():
    s = open(f, encoding="utf-8").read()
    log = []
    # title
    m = re.search(r"<title>(.*?)</title>", s, re.S)
    if m:
        s = s.replace(m.group(0), "<title>%s</title>" % meta["title"], 1)
        log.append("title")
    else:
        s = s.replace("</head>", "<title>%s</title>\n</head>" % meta["title"], 1)
        log.append("title(插入)")
    # description + og（去重）
    if '<meta name="description"' not in s:
        inject = ('<meta name="description" content="%s">\n'
                  '<meta property="og:title" content="%s">\n'
                  '<meta property="og:description" content="%s">\n'
                  '<meta name="twitter:card" content="summary">\n'
                  ) % (meta["desc"], meta["title"], meta["desc"])
        s = s.replace("</head>", inject + "</head>", 1)
        log.append("desc+og")
    open(f, "w", encoding="utf-8").write(s)
    print("OK  ", f, "->", " / ".join(log))

# 验证
print("-" * 50)
for f in PLAN:
    s = open(f, encoding="utf-8").read()
    t = re.search(r"<title>(.*?)</title>", s).group(1)
    d = re.search(r'<meta name="description" content="(.*?)">', s).group(1)
    print("OK  %s | title %d 字 | desc %d 字" % (f, len(t), len(d)))
print("DONE")
