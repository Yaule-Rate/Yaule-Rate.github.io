# -*- coding: utf-8 -*-
"""i18n 补全 A：静态 data-i18n 标记（life/MC/works/anniv/repos/skills/bucket）+ 进度条数字元素"""
import re

p = "index.html"
s = open(p, encoding="utf-8").read()
n0 = len(s)
log = []

def rep(old, new, tag):
    global s
    assert s.count(old) >= 1, "未找到: " + tag
    s = s.replace(old, new)
    log.append(tag)

# ===== lang-loader 增加百分比数字 =====
rep('<div class="lang-bar"><div class="lang-bar-fill" id="langBarFill"></div></div>',
    '<div class="lang-bar"><div class="lang-bar-fill" id="langBarFill"></div></div>\n  <p class="lang-pct" id="langBarPct">0%</p>', "langBarPct 元素")

# ===== CSS：lang-pct =====
rep("  .lang-bar-fill { height: 100%; width: 0%; border-radius: 999px; background: linear-gradient(90deg, var(--accent), var(--accent-2)); }",
    "  .lang-bar-fill { height: 100%; width: 0%; border-radius: 999px; background: linear-gradient(90deg, var(--accent), var(--accent-2)); }\n  .lang-pct { font-size: 13px; color: var(--ink-2); font-variant-numeric: tabular-nums; letter-spacing: .06em; margin-top: -6px; }",
    "lang-pct CSS")

# ===== life 卡 =====
rep('<h3>瑞幸咖啡 <span class="tag">续命中</span></h3>',
    '<h3><span data-i18n="life.c1">瑞幸咖啡</span> <span class="tag" data-i18n="life.tag1">续命中</span></h3>', "life.c1")
rep('<p class="data-desc">从第一杯咖啡开始，悄悄记录每一次续命时刻</p>',
    '<p class="data-desc" data-i18n="life.d1">从第一杯咖啡开始，悄悄记录每一次续命时刻</p>', "life.d1")
rep('<p class="data-desc" style="margin-top:8px">美式、拿铁、生椰……每一杯都是生活的续命剂。</p>',
    '<p class="data-desc" style="margin-top:8px" data-i18n="life.d2">美式、拿铁、生椰……每一杯都是生活的续命剂。</p>', "life.d2")
rep('<div class="data-number" id="cups">176<small>杯</small></div>',
    '<div class="data-number" id="cups">176<small data-i18n="life.un2">杯</small></div>', "life.un2")
rep('<h3>网易云音乐 <span class="tag">循环播放中</span></h3>',
    '<h3><span data-i18n="life.c2">网易云音乐</span> <span class="tag" data-i18n="life.tag2">循环播放中</span></h3>', "life.c2")
rep('<div class="data-number"><span id="songs">305</span><small>首</small></div>',
    '<div class="data-number"><span id="songs">305</span><small data-i18n="life.un1">首</small></div>', "life.un1")
rep('<p class="data-desc">累计收听 <span id="hours">2000</span>+ 小时，旋律里藏着无数个夜晚</p>',
    '<p class="data-desc"><span data-i18n="life.h1">累计收听</span> <span id="hours">2000</span><span data-i18n="life.h2">+ 小时，旋律里藏着无数个夜晚</span></p>', "life.h")
rep('<p class="data-desc" style="margin-top:8px">深夜的旋律，陪我度过每一个失眠夜。</p>',
    '<p class="data-desc" style="margin-top:8px" data-i18n="life.d3">深夜的旋律，陪我度过每一个失眠夜。</p>', "life.d3")
rep('<p class="data-desc daily-song" style="margin-top:8px">今日推荐：<a id="dailySong" href="#" target="_blank" rel="noopener">正在挑选…</a></p>',
    '<p class="data-desc daily-song" style="margin-top:8px"><span data-i18n="life.song">今日推荐：</span><a id="dailySong" href="#" target="_blank" rel="noopener" data-i18n="life.songload">正在挑选…</a></p>', "life.song")

# ===== MC 卡 =====
rep('<button class="mc-subtab active" data-server="bjd" role="tab">布吉岛</button>',
    '<button class="mc-subtab active" data-server="bjd" role="tab" data-i18n="mc.sub1">布吉岛</button>', "mc.sub1")
rep('<button class="mc-subtab" data-server="hyt" role="tab">花雨亭</button>',
    '<button class="mc-subtab" data-server="hyt" role="tab" data-i18n="mc.sub2">花雨亭</button>', "mc.sub2")

# MC 单位映射
unit_map = {'局': 'mc.u1', 'h': 'mc.u2', '胜': 'mc.u3', '个': 'mc.u4', '天': 'mc.u5'}
def unit_sub(m):
    u = m.group(2)
    return m.group(1) + '<small data-i18n="' + unit_map[u] + '">' + u + '</small>'
s2 = re.sub(r'(<div class="m-val"[^>]*>[0-9]+)<small>(局|h|胜|个|天)</small>', unit_sub, s)
if s2 != s:
    s = s2; log.append("mc units ×16")
else:
    raise SystemExit("未找到 mc units")

# MC 标签
label_map = {'游戏对局': 'mc.l1', '在线时长': 'mc.l2', '胜场': 'mc.l3', '放置方块': 'mc.l4',
             '挖掘方块': 'mc.l5', '成就解锁': 'mc.l6', '游玩天数': 'mc.l7', '累计上线': 'mc.l8'}
def label_sub(m):
    return '<div class="m-label" data-i18n="' + label_map[m.group(1)] + '">' + m.group(1) + '</div>'
s2 = re.sub(r'<div class="m-label">(游戏对局|在线时长|胜场|放置方块|挖掘方块|成就解锁|游玩天数|累计上线)</div>', label_sub, s)
if s2 != s:
    s = s2; log.append("mc labels ×16")
else:
    raise SystemExit("未找到 mc labels")

rep('<p class="mc-note">生存、建筑与联机日常，记录仍在继续。</p>',
    '<p class="mc-note" data-i18n="mc.n1">生存、建筑与联机日常，记录仍在继续。</p>', "mc.n1")
rep('<p class="mc-note">花雨亭已停服，数据定格在停服前一天（2025-06-14）。</p>',
    '<p class="mc-note" data-i18n="mc.n2">花雨亭已停服，数据定格在停服前一天（2025-06-14）。</p>', "mc.n2")

# ===== works 卡（6 张）=====
rep('<h3>兴华中学广播站系统</h3>', '<h3 data-i18n="works.t1">兴华中学广播站系统</h3>', "works.t1")
rep('<p>广播排班管理、播放日程控制、站点信息维护，独立设计开发并投入校园实际使用。</p>',
    '<p data-i18n="works.t1d">广播排班管理、播放日程控制、站点信息维护，独立设计开发并投入校园实际使用。</p>', "works.t1d")
rep('<p>广播排班、播放日程、站点信息一站式维护，从零开发并投入校园日常使用。</p>',
    '<p data-i18n="works.t1p">广播排班、播放日程、站点信息一站式维护，从零开发并投入校园日常使用。</p>', "works.t1p")
rep('<span class="card-tags"><span>广播</span><span>管理</span></span>',
    '<span class="card-tags"><span data-i18n="works.tag1a">广播</span><span data-i18n="works.tag1b">管理</span></span>', "works.t1 tags")
rep('<h3>自助记账系统</h3>', '<h3 data-i18n="works.t2">自助记账系统</h3>', "works.t2")
rep('<p>收支记录、分类统计、数据可视化，轻量化单文件本地工具，开箱即用。</p>',
    '<p data-i18n="works.t2d">收支记录、分类统计、数据可视化，轻量化单文件本地工具，开箱即用。</p>', "works.t2d")
rep('<p>收支流水、分类统计、报表导出，让每一笔账都清清楚楚。</p>',
    '<p data-i18n="works.t2p">收支流水、分类统计、报表导出，让每一笔账都清清楚楚。</p>', "works.t2p")
rep('<span class="card-tags"><span>记账</span><span>工具</span></span>',
    '<span class="card-tags"><span data-i18n="works.tag2a">记账</span><span data-i18n="works.tag2b">工具</span></span>', "works.t2 tags")
rep('<h3>代码编写系统</h3>', '<h3 data-i18n="works.t3">代码编写系统</h3>', "works.t3")
rep('<p>可视化拖拽生成 C++ 代码，降低编程入门门槛，助力机器人编程学习。</p>',
    '<p data-i18n="works.t3d">可视化拖拽生成 C++ 代码，降低编程入门门槛，助力机器人编程学习。</p>', "works.t3d")
rep('<p>代码编写辅助工作台，模板化快速生成，让日常编码更顺手。</p>',
    '<p data-i18n="works.t3p">代码编写辅助工作台，模板化快速生成，让日常编码更顺手。</p>', "works.t3p")
rep('<span class="card-tags"><span>编码</span><span>效率</span></span>',
    '<span class="card-tags"><span data-i18n="works.tag3a">编码</span><span data-i18n="works.tag3b">效率</span></span>', "works.t3 tags")
rep('<h3>表情转图片转换器</h3>', '<h3 data-i18n="works.t4">表情转图片转换器</h3>', "works.t4")
rep('<p>文字、表情符号一键转图片，支持自定义背景与文字颜色，导出高清 PNG。</p>',
    '<p data-i18n="works.t4d">文字、表情符号一键转图片，支持自定义背景与文字颜色，导出高清 PNG。</p>', "works.t4d")
rep('<p>把文字图案一键转成 Emoji 图片，分享出来更有趣。</p>',
    '<p data-i18n="works.t4p">把文字图案一键转成 Emoji 图片，分享出来更有趣。</p>', "works.t4p")
rep('<span class="card-tags"><span>趣味</span><span>图像</span></span>',
    '<span class="card-tags"><span data-i18n="works.tag4a">趣味</span><span data-i18n="works.tag4b">图像</span></span>', "works.t4 tags")
rep('<h3>CS 灵敏度校准</h3>', '<h3 data-i18n="works.t5">CS 灵敏度校准</h3>', "works.t5")
rep('<p>输入 DPI 与灵敏度参数，智能评估输出最佳游戏鼠标灵敏度。</p>',
    '<p data-i18n="works.t5d">输入 DPI 与灵敏度参数，智能评估输出最佳游戏鼠标灵敏度。</p>', "works.t5d")
rep('<p>FPS 游戏鼠标灵敏度科学校准，找到真正属于自己的手感。</p>',
    '<p data-i18n="works.t5p">FPS 游戏鼠标灵敏度科学校准，找到真正属于自己的手感。</p>', "works.t5p")
rep('<span class="card-tags"><span>游戏</span><span>外设</span></span>',
    '<span class="card-tags"><span data-i18n="works.tag5a">游戏</span><span data-i18n="works.tag5b">外设</span></span>', "works.t5 tags")
rep('<h3>棋类合集</h3>', '<h3 data-i18n="works.t6">棋类合集</h3>', "works.t6")
rep('<p>五子棋与中国象棋，本地运行，无需联网。</p>',
    '<p data-i18n="works.t6d">五子棋与中国象棋，本地运行，无需联网。</p>', "works.t6d")
rep('<p>象棋与五子棋同页双开，约上好友面对面来一局。</p>',
    '<p data-i18n="works.t6p">象棋与五子棋同页双开，约上好友面对面来一局。</p>', "works.t6p")
rep('<span class="card-tags"><span>游戏</span><span>对战</span></span>',
    '<span class="card-tags"><span data-i18n="works.tag6a">游戏</span><span data-i18n="works.tag6b">对战</span></span>', "works.t6 tags")

# ===== anniv 卡 =====
rep('<span>与这个世界相遇</span>', '<span data-i18n="anniv.a1">与这个世界相遇</span>', "anniv.a1")
rep('<span>与这座小站相遇</span>', '<span data-i18n="anniv.a2">与这座小站相遇</span>', "anniv.a2")
rep('<div class="anniv-label">活着的第 <span id="annivDaysN">--</span> 天</div>',
    '<div class="anniv-label"><span data-i18n="anniv.l1">活着的第</span> <span id="annivDaysN">--</span> <span data-i18n="anniv.l2">天</span></div>', "anniv.l1")
rep('<div class="anniv-label">本站上线第 <span id="siteDaysN">--</span> 天</div>',
    '<div class="anniv-label"><span data-i18n="anniv.l3">本站上线第</span> <span id="siteDaysN">--</span> <span data-i18n="anniv.l4">天</span></div>', "anniv.l3")
rep('<div class="anniv-meta" id="lifeMeta">人生进度计算中…</div>',
    '<div class="anniv-meta" id="lifeMeta" data-i18n="anniv.meta1">人生进度计算中…</div>', "anniv.meta1")
rep('<div class="anniv-meta" id="siteMeta">下一个里程碑计算中…</div>',
    '<div class="anniv-meta" id="siteMeta" data-i18n="anniv.meta2">下一个里程碑计算中…</div>', "anniv.meta2")
rep('<div class="anniv-date">自 2012 年 1 月 17 日起</div>',
    '<div class="anniv-date" data-i18n="anniv.d1">自 2012 年 1 月 17 日起</div>', "anniv.d1")
rep('<div class="anniv-date">自 2026 年 9 月 18 日起</div>',
    '<div class="anniv-date" data-i18n="anniv.d2">自 2026 年 9 月 18 日起</div>', "anniv.d2")

# ===== repos 占位 =====
rep('<div class="repo-name"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 .5C5.65.5.5 5.65.5 12c0 5.08 3.29 9.39 7.86 10.91.58.11.79-.25.79-.56 0-.27-.01-1.02-.02-2-3.2.7-3.88-1.54-3.88-1.54-.52-1.33-1.28-1.68-1.28-1.68-1.04-.71.08-.7.08-.7 1.15.08 1.76 1.18 1.76 1.18 1.02 1.75 2.69 1.25 3.35.95.1-.74.4-1.25.72-1.54-2.55-.29-5.23-1.28-5.23-5.68 0-1.26.45-2.28 1.18-3.09-.12-.29-.51-1.46.11-3.05 0 0 .96-.31 3.15 1.18a10.9 10.9 0 0 1 5.74 0c2.19-1.49 3.15-1.18 3.15-1.18.62 1.59.23 2.76.11 3.05.74.81 1.18 1.83 1.18 3.09 0 4.41-2.69 5.39-5.25 5.67.41.36.78 1.06.78 2.14 0 1.55-.01 2.79-.01 3.17 0 .31.21.68.8.56A10.52 10.52 0 0 0 23.5 12C23.5 5.65 18.35.5 12 .5Z"/></svg>正在读取仓库…</div>',
    '<div class="repo-name"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 .5C5.65.5.5 5.65.5 12c0 5.08 3.29 9.39 7.86 10.91.58.11.79-.25.79-.56 0-.27-.01-1.02-.02-2-3.2.7-3.88-1.54-3.88-1.54-.52-1.33-1.28-1.68-1.28-1.68-1.04-.71.08-.7.08-.7 1.15.08 1.76 1.18 1.76 1.18 1.02 1.75 2.69 1.25 3.35.95.1-.74.4-1.25.72-1.54-2.55-.29-5.23-1.28-5.23-5.68 0-1.26.45-2.28 1.18-3.09-.12-.29-.51-1.46.11-3.05 0 0 .96-.31 3.15 1.18a10.9 10.9 0 0 1 5.74 0c2.19-1.49 3.15-1.18 3.15-1.18.62 1.59.23 2.76.11 3.05.74.81 1.18 1.83 1.18 3.09 0 4.41-2.69 5.39-5.25 5.67.41.36.78 1.06.78 2.14 0 1.55-.01 2.79-.01 3.17 0 .31.21.68.8.56A10.52 10.52 0 0 0 23.5 12C23.5 5.65 18.35.5 12 .5Z"/></svg><span data-i18n="repos.loading">正在读取仓库…</span></div>',
    "repos.loading")
rep('<div class="repo-desc">连接 GitHub API 中，稍等片刻。</div>',
    '<div class="repo-desc" data-i18n="repos.connecting">连接 GitHub API 中，稍等片刻。</div>', "repos.connecting")

# ===== skills =====
rep('<h3>从校园工具到小游戏，什么都想试一试。</h3>',
    '<h3 data-i18n="skills.h3">从校园工具到小游戏，什么都想试一试。</h3>', "skills.h3")
rep('<p>广播站系统、记账工具、代码生成器、棋类游戏……都是一个人从零写完的。爱折腾前端交互，也愿意沉下去做工具；会调音视频，也会为一个小游戏磨上几个晚上。</p>',
    '<p data-i18n="skills.p">广播站系统、记账工具、代码生成器、棋类游戏……都是一个人从零写完的。爱折腾前端交互，也愿意沉下去做工具；会调音视频，也会为一个小游戏磨上几个晚上。</p>', "skills.p")

# ===== bucket 进度 =====
rep('<span class="bucket-progress">已点亮 <b id="bkDone">0</b> / <b id="bkTotal">24</b> 件</span>',
    '<span class="bucket-progress"><span data-i18n="bucket.progress">已点亮</span> <b id="bkDone">0</b> / <b id="bkTotal">24</b> <span data-i18n="bucket.progress2">件</span></span>', "bucket.progress")

open(p, "w", encoding="utf-8").write(s)
print("完成。替换:", len(log), "处 | 增长:", len(s) - n0)
for t in log:
    print(" -", t)
