# -*- coding: utf-8 -*-
"""v19 works×6：加长 meta description（必应提示描述过短）"""
import glob

DESC = {
    "works/xinghua.html": "兴华中学广播站系统是 Yaule 独立设计开发并投入校园实际使用的广播管理工具：广播排班管理、播放日程控制、站点信息维护一站式完成，从需求梳理到上线运营全部独立完成。",
    "works/accounting.html": "自助记账系统 Pro 是轻量化单文件本地记账工具：收支记录、分类统计、数据可视化报表开箱即用，无需联网不泄露隐私，适合日常记账与月度复盘。",
    "works/code-system.html": "代码编写系统是一款可视化拖拽生成 C++ 代码的辅助工作台：通过图形化积木式操作降低编程入门门槛，内置模板库与代码生成引擎，助力机器人编程学习。",
    "works/emoji-converter.html": "表情转图片转换器可以把文字与表情符号一键转成高清 PNG 图片：支持自定义背景色、文字颜色与排版，适合聊天表情包、社交分享与创意海报制作。",
    "works/cs-sens.html": "CS 灵敏度校准器是一款 FPS 游戏鼠标灵敏度校准工具：通过科学换算与多游戏灵敏度映射，帮助你找到真正适合自己的手感，告别凭感觉调灵敏度。",
    "works/chess.html": "棋类合集将五子棋与中国象棋合二为一，本地运行无需联网：支持同屏双人对战、悔棋与难度选择，约上好友面对面来一局，随时随地开棋。",
}

for f in sorted(glob.glob("works/*.html")):
    html = open(f, encoding="utf-8").read()
    key = f.replace("\\", "/")
    if key not in DESC:
        print("SKIP", f)
        continue
    old = html
    import re
    m = re.search(r'<meta name="description" content="(.*?)">', html)
    if not m:
        print("FAIL no desc", f)
        continue
    html = html.replace(m.group(0), '<meta name="description" content="' + DESC[key] + '">', 1)
    if html != old:
        open(f, "w", encoding="utf-8").write(html)
        print("OK  ", f)
    else:
        print("NOCH", f)
print("DONE")
