# -*- coding: utf-8 -*-
"""v16c: 生成 6 个作品详情页（works/ 子目录，每页 100+ 行）"""
import os, json

TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{name} · Yaule 作品详情</title>
<meta name="description" content="{desc}">
<style>
:root {{
  --bg: #f6fafc; --card: #ffffff; --ink: #0f172a; --ink-2: #5b6b7e;
  --line: #e2e8f0; --accent: #0284c7; --accent-2: #38bdf8; --soft: #e0f2fe;
}}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
  background: var(--bg); color: var(--ink);
  font-family: "Noto Sans SC", "PingFang SC", "Microsoft YaHei", sans-serif;
  line-height: 1.75; -webkit-font-smoothing: antialiased;
}}
.wrap {{ max-width: 860px; margin: 0 auto; padding: 40px 24px 90px; }}
.topbar {{ display: flex; align-items: center; gap: 14px; margin-bottom: 34px; }}
.back-btn {{
  display: inline-flex; align-items: center; gap: 6px;
  font-size: 13.5px; color: var(--ink-2); text-decoration: none;
  border: 1px solid var(--line); background: var(--card);
  padding: 7px 15px; border-radius: 999px; transition: all 0.18s ease;
}}
.back-btn:hover {{ color: var(--accent); border-color: var(--accent); transform: translateX(-2px); }}
.back-btn svg {{ width: 14px; height: 14px; }}
.breadcrumb {{ font-size: 12.5px; color: var(--ink-2); }}
.breadcrumb a {{ color: var(--accent); text-decoration: none; }}
.hero {{ margin-bottom: 30px; }}
.kicker {{ font-size: 12px; letter-spacing: 2.5px; color: var(--accent); font-weight: 600; margin-bottom: 8px; }}
h1 {{ font-size: 34px; font-weight: 700; line-height: 1.35; margin-bottom: 10px; }}
.sub {{ font-size: 15px; color: var(--ink-2); max-width: 640px; }}
.panel {{
  background: var(--card); border: 1px solid var(--line); border-radius: 18px;
  padding: 26px 30px; margin-bottom: 22px;
}}
.panel h2 {{
  font-size: 16px; font-weight: 600; margin-bottom: 14px;
  display: flex; align-items: center; gap: 9px;
}}
.panel h2::before {{
  content: ""; width: 4px; height: 16px; border-radius: 3px;
  background: linear-gradient(180deg, var(--accent), var(--accent-2));
}}
.panel p, .panel li {{ font-size: 14.5px; color: var(--ink-2); }}
.panel ul {{ padding-left: 20px; }}
.panel ul li {{ margin-bottom: 6px; }}
.tags {{ display: flex; flex-wrap: wrap; gap: 8px; margin-top: 14px; }}
.tag {{
  font-size: 12px; color: var(--accent); border: 1px solid rgba(2,132,199,0.3);
  background: rgba(2,132,199,0.05); border-radius: 999px; padding: 2px 12px;
}}
.actions {{ display: flex; gap: 12px; margin-top: 18px; flex-wrap: wrap; }}
.btn {{
  display: inline-flex; align-items: center; gap: 8px;
  font-size: 14px; font-weight: 500; text-decoration: none;
  border-radius: 12px; padding: 10px 22px; transition: all 0.18s ease;
}}
.btn-primary {{ background: var(--accent); color: #fff; box-shadow: 0 6px 16px rgba(2,132,199,0.3); }}
.btn-primary:hover {{ background: #0369a1; transform: translateY(-2px); }}
.btn-ghost {{ border: 1px solid var(--line); color: var(--ink-2); background: var(--card); }}
.btn-ghost:hover {{ border-color: var(--accent); color: var(--accent); }}
.btn svg {{ width: 15px; height: 15px; }}
.spec-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 12px; }}
.spec {{
  background: var(--bg); border: 1px solid var(--line); border-radius: 12px;
  padding: 13px 15px;
}}
.spec .k {{ font-size: 11.5px; color: var(--ink-2); letter-spacing: 1px; margin-bottom: 3px; }}
.spec .v {{ font-size: 14px; font-weight: 600; }}
.vlog {{
  border-left: 2px solid var(--line); padding-left: 18px; margin-top: 4px;
  display: flex; flex-direction: column; gap: 12px;
}}
.vlog .v-item {{ position: relative; }}
.vlog .v-item::before {{
  content: ""; position: absolute; left: -23.5px; top: 7px;
  width: 7px; height: 7px; border-radius: 50%; background: var(--accent);
}}
.vlog .v-ver {{ font-weight: 600; font-size: 14px; }}
.vlog .v-desc {{ font-size: 13.5px; color: var(--ink-2); margin-top: 2px; }}
footer {{ margin-top: 44px; padding-top: 22px; border-top: 1px solid var(--line); }}
footer p {{ font-size: 12.5px; color: var(--ink-2); text-align: center; }}
footer a {{ color: var(--accent); text-decoration: none; }}
@media (max-width: 640px) {{
  .wrap {{ padding: 26px 16px 60px; }}
  h1 {{ font-size: 27px; }}
  .panel {{ padding: 20px 18px; }}
}}
</style>
</head>
<body>
<div class="wrap">
  <div class="topbar">
    <a class="back-btn" href="../index.html">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/></svg>
      返回标签页
    </a>
    <span class="breadcrumb"><a href="../index.html">首页</a> / <a href="../index.html#works">精选作品</a> / {name}</span>
  </div>

  <div class="hero">
    <p class="kicker">SELECTED WORK</p>
    <h1>{name}</h1>
    <p class="sub">{sub}</p>
    <div class="tags">{tags_html}</div>
    <div class="actions">
      <a class="btn btn-primary" href="{src_file}" data-nodl>
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="22" y1="12" x2="2" y2="12"/><polyline points="5 9 12 16 19 9" transform="rotate(90 12 12)"/></svg>
        开始使用
      </a>
      <a class="btn btn-ghost" href="{src_file}" download="{src_file}">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
        下载文件
      </a>
    </div>
  </div>

  <div class="panel">
    <h2>项目简介</h2>
    <p>{overview}</p>
    <div class="spec-grid">{spec_html}</div>
  </div>

  <div class="panel">
    <h2>核心功能</h2>
    <ul>{features_html}</ul>
  </div>

  <div class="panel">
    <h2>技术细节</h2>
    <ul>{tech_html}</ul>
  </div>

  <div class="panel">
    <h2>使用指南</h2>
    <ul>{guide_html}</ul>
  </div>

  <div class="panel">
    <h2>版本记录</h2>
    <div class="vlog">{versions_html}</div>
  </div>

  <footer>
    <p>© 2026 <a href="../index.html">Yaule</a> · 一个藏在失眠夜里的小作品</p>
  </footer>
</div>
</body>
</html>
"""

WORKS = [
    {
        "file": "xinghua.html", "src_file": "../Xinghua%20Middle%20School%20Broadcasting%20Station%20System.html",
        "name": "兴华中学广播站系统", "sub": "为校园广播站量身定制的排班与播放管理系统，已在兴华中学投入日常使用。",
        "desc": "广播排班管理、播放日程控制、站点信息维护，独立设计开发并投入校园实际使用。",
        "tags": ["校园工具", "排班管理", "广播系统", "实际部署"],
        "overview": "这是为兴华中学广播站独立设计开发的综合管理系统。从广播员的排班表、每日播放日程的编排，到站点设备与栏目信息的维护，全部集中在一个轻量化的网页里完成。系统已在校园实际运行，替代了原先手写排班表与纸质日程的方式，让每天的广播工作有章可循。",
        "spec": [("开发形式", "单文件 HTML"), ("适用场景", "校园广播站"), ("部署状态", "已实际使用"), ("数据存储", "本地结构")],
        "features": [
            "广播员排班管理：按周生成值班表，支持多人轮值、调班与请假标记。",
            "播放日程控制：为每个时段编排曲目与栏目，到点提醒，不漏播不空播。",
            "站点信息维护：维护栏目介绍、设备清单与广播文案等站点资料。",
            "一目了然的周视图：本周谁值班、今天播什么，打开页面就能看到。",
            "轻量单文件：无需安装任何依赖，浏览器打开即可使用，方便部署到校园公共电脑。",
        ],
        "tech": [
            "纯 HTML + CSS + JavaScript 实现，零第三方依赖，离线可用。",
            "数据以结构化方式保存在本地，刷新页面不丢失，随开随用。",
            "排班逻辑采用周期计算，跨周自动滚动，节假日可手动跳过。",
            "界面遵循校园使用习惯，字号偏大、操作路径短，值班同学上手即会。",
        ],
        "guide": [
            "打开页面后，默认进入本周排班视图，可直接查看当日值班人与播放内容。",
            "点击「编辑排班」可调整任意时段的栏目与人员，修改即时保存。",
            "设备与栏目资料在「站点信息」中维护，供全站复用。",
            "建议在广播站电脑上固定一个浏览器窗口常驻使用。",
        ],
        "versions": [
            ("v1.0", "首个可用版本：排班表 + 播放日程 + 站点信息三大模块上线。"),
            ("v1.1", "增加周视图自动滚动到当日，优化移动端浏览。"),
            ("v1.2", "修复排班跨周滚动边界问题，补充节假日跳过功能。"),
        ],
    },
    {
        "file": "accounting.html", "src_file": "../Self-service%20accounting%20system%20Pro%20Enhanced%20V6.html",
        "name": "自助记账系统", "sub": "轻量化的单文件本地记账工具，收支分类、统计与可视化开箱即用。",
        "desc": "收支记录、分类统计、数据可视化，轻量化单文件本地工具，开箱即用。",
        "tags": ["效率工具", "记账", "数据可视化", "本地运行"],
        "overview": "一个把「记账」这件事做简单的单文件工具：记录每一笔收入和支出，按分类自动汇总，并用图表直观呈现钱都去了哪里。所有数据都保存在本地，不依赖任何云端服务，隐私安全，导出方便。适合个人日常消费管理与月度复盘。",
        "spec": [("开发形式", "单文件 HTML"), ("数据存储", "本地持久化"), ("统计维度", "分类 / 月度 / 趋势"), ("适用人群", "个人与家庭")],
        "features": [
            "收支记录：一键记一笔，支持收入 / 支出双类型与任意分类。",
            "分类统计：餐饮、交通、购物、娱乐等分类自动汇总，占比一目了然。",
            "数据可视化：月度收支柱状图、分类占比图，趋势看得见。",
            "本地保存：所有数据仅存于本机，不联网、不上传，隐私安全。",
            "导出与重置：支持数据导出备份，随时清空重来。",
        ],
        "tech": [
            "单文件 HTML 实现，无需安装与联网，任何设备打开即用。",
            "记账数据采用本地存储结构，关闭页面不丢失，跨会话持续累积。",
            "图表由原生绘制，无第三方库依赖，加载快、体积小。",
            "内置月度结算逻辑：自动计算结余、环比与分类占比。",
        ],
        "guide": [
            "首次打开即进入记账页，输入金额、选择分类、点击保存即可完成一笔记录。",
            "首页默认展示本月概览：总收入、总支出、结余与分类占比。",
            "右上角可切换历史月份，回看往月明细与图表。",
            "数据备份建议定期导出保存到本地，防止误清。",
        ],
        "versions": [
            ("Pro Enhanced V6", "当前版本：优化分类体系与月度对比视图，图表交互升级。"),
            ("V5", "新增月度切换与数据导出功能。"),
            ("V1", "初版：仅支持收支记录与简单汇总。"),
        ],
    },
    {
        "file": "code-system.html", "src_file": "../Nayingte%20M4e%20Code%20Writing%20System%20V2.9Pro.html",
        "name": "代码编写系统", "sub": "可视化拖拽生成 C++ 代码，降低编程入门门槛，助力机器人编程学习。",
        "desc": "可视化拖拽生成 C++ 代码，降低编程入门门槛，助力机器人编程学习。",
        "tags": ["教育工具", "C++", "拖拽编程", "机器人"],
        "overview": "面向机器人编程学习场景的可视化编程系统：把繁琐的 C++ 语法封装成可视化的积木块，通过拖拽、连线与参数配置，即可自动生成可直接编译运行的 C++ 代码。让初学者把注意力放在逻辑本身，而不是被语法细节绊住。",
        "spec": [("开发形式", "单文件 HTML"), ("目标语言", "C++"), ("交互方式", "可视化拖拽"), ("适用场景", "机器人编程教学")],
        "features": [
            "拖拽式搭建：将逻辑块拖入画布，按顺序与条件组织程序结构。",
            "参数可视化配置：数值、条件、循环次数等参数以表单方式设置。",
            "一键生成 C++ 代码：搭建完成后自动输出完整可编译的源码。",
            "内置常用积木：涵盖传感器读取、电机控制、循环判断等机器人常用模块。",
            "即时预览：右侧实时同步代码，边拖边看。",
        ],
        "tech": [
            "前端交互采用原生事件驱动，拖拽与连线逻辑完全本地执行。",
            "代码生成引擎将积木节点映射为 C++ 语法片段，支持嵌套与顺序组合。",
            "内置语法模板库：包含头文件、主函数、传感器与控制语句模板。",
            "错误兜底：未连接的积木自动忽略并给出提示，不生成残缺代码。",
        ],
        "guide": [
            "从左侧积木库拖出所需模块到画布，按逻辑顺序排列。",
            "点击积木可展开参数面板，填写具体数值或选择项。",
            "点击「生成代码」右侧即输出 C++ 源码，可直接复制到 IDE 编译。",
            "建议配合机器人套件教学使用，先搭积木、再读生成的代码。",
        ],
        "versions": [
            ("V2.9 Pro", "当前版本：新增循环嵌套与条件分支积木，代码生成稳定性优化。"),
            ("V2.0", "支持传感器模块与多积木组合。"),
            ("V1.0", "初版：基础顺序结构拖拽生成。"),
        ],
    },
    {
        "file": "emoji-converter.html", "src_file": "../Fancy-Pattern-Emoji-to-Image-Converter.html",
        "name": "表情转图片转换器", "sub": "文字、表情符号一键转图片，支持自定义背景与文字颜色，导出高清 PNG。",
        "desc": "文字、表情符号一键转图片，支持自定义背景与文字颜色，导出高清PNG。",
        "tags": ["创意工具", "表情包", "PNG 导出", "自定义配色"],
        "overview": "一个有趣的小工具：把一串文字或表情符号，排版成一张好看的图片。可以自定义背景色、文字颜色、排列方式与画布尺寸，一键导出高清 PNG。做表情包、做文案配图、做社交分享卡片，几秒钟就能搞定。",
        "spec": [("开发形式", "单文件 HTML"), ("导出格式", "PNG"), ("画布尺寸", "多档可选"), ("应用场景", "表情包 / 配图")],
        "features": [
            "文字 / 表情自由混排：中英文、Emoji、特殊符号任意组合。",
            "自定义配色：背景色、文字色、强调色全部可调。",
            "多档画布：支持方形、竖版、横版与高清大图多种尺寸。",
            "图案背景：内置简约几何纹理可选，让图片更有设计感。",
            "一键导出：渲染为高清 PNG 直接下载，可用于社交平台。",
        ],
        "tech": [
            "基于 Canvas 渲染，文字排版与表情绘制完全本地完成。",
            "Emoji 采用系统字体渲染，保证跨平台显示效果一致。",
            "导出前自动按目标尺寸重采样，保证 PNG 清晰度。",
            "配色方案使用 HSL 调色，颜色选择器即时预览。",
        ],
        "guide": [
            "在上方输入框输入想转换的文字或表情。",
            "选择背景色、文字颜色与画布比例。",
            "点击「生成预览」查看排版效果，不满意可继续调整。",
            "点击「下载 PNG」保存高清图片到本地。",
        ],
        "versions": [
            ("v1.3", "当前版本：新增几何纹理背景与竖版画布。"),
            ("v1.0", "初版：文字表情转图片核心功能。"),
        ],
    },
    {
        "file": "cs-sens.html", "src_file": "../CS-Sens-Calibrator.html",
        "name": "CS 灵敏度校准器", "sub": "输入 DPI 与灵敏度参数，智能评估输出最佳游戏鼠标灵敏度。",
        "desc": "FPS 游戏鼠标灵敏度科学校准，找到真正属于自己的手感。",
        "tags": ["游戏工具", "FPS", "灵敏度校准", "外设"],
        "overview": "FPS 玩家都知道，一套适合自己的鼠标灵敏度有多重要。这个校准器通过输入你的鼠标 DPI、游戏内灵敏度与常用瞄准习惯，结合常用的 eDPI 换算与手感区间模型，给出一个科学的参考区间，帮你快速找到「打起来顺手」的灵敏度，减少反复试错的成本。",
        "spec": [("开发形式", "单文件 HTML"), ("适用游戏", "CS 系列等 FPS"), ("核心计算", "eDPI 换算"), ("输出形式", "建议区间")],
        "features": [
            "DPI 与灵敏度换算：自动计算 eDPI，跨游戏对照参考。",
            "手感区间评估：根据常用模型输出低 / 中 / 高三档建议值。",
            "按瞄准习惯细分：步枪点射、压枪、狙击等不同场景分别建议。",
            "历史记录：保存多组配置，方便对比切换。",
            "纯本地运行：不联网，数据只留在你的浏览器里。",
        ],
        "tech": [
            "灵敏度模型基于主流 FPS 社区公认的 eDPI 换算公式实现。",
            "区间建议采用分段函数计算，随 DPI 与习惯自动适配。",
            "所有输入即时重算，无提交等待，交互流畅。",
            "本地存储记录历史配置，支持一键清除。",
        ],
        "guide": [
            "输入你的鼠标 DPI（一般在鼠标驱动中可查）。",
            "填入当前游戏内灵敏度，选择瞄准习惯。",
            "查看建议区间与换算结果，直接套用到游戏内。",
            "多组配置可保存对比，找到最顺手的那一档。",
        ],
        "versions": [
            ("v1.2", "当前版本：新增瞄准习惯分档与历史记录。"),
            ("v1.0", "初版：基础 eDPI 换算与建议区间。"),
        ],
    },
    {
        "file": "chess.html", "src_file": "../Chess-Gomoku-Collection.html",
        "name": "棋类合集", "sub": "五子棋与中国象棋同页双开，本地运行，无需联网。",
        "desc": "五子棋与中国象棋，本地运行，无需联网。约上好友面对面来一局。",
        "tags": ["游戏", "象棋", "五子棋", "本地对战"],
        "overview": "一个把五子棋与中国象棋放在同一个页面里的棋类合集。无需联网、无需登录，打开就能和身边的朋友来一局。棋子、棋盘、规则判断全部本地实现，界面清爽，手感流畅，是聚会与课间的解闷利器。",
        "spec": [("开发形式", "单文件 HTML"), ("游戏数量", "2 款"), ("对战方式", "本地双人"), ("运行要求", "浏览器即可")],
        "features": [
            "五子棋：标准 15×15 棋盘，禁手之外的规则完整实现，支持悔棋。",
            "中国象棋：完整棋规——马走日、象走田、蹩马腿、塞象眼、将帅对脸判定。",
            "同页切换：两款游戏一键互切，无需刷新页面。",
            "胜负判定自动完成：五子连珠、将军、绝杀即时提示。",
            "悔棋与复盘：下错可悔，结束后可回放整局。",
        ],
        "tech": [
            "棋盘以 Canvas 渲染，落子动画流畅，移动端同样顺滑。",
            "象棋走法合法性校验完整覆盖，包含吃子与将军状态检测。",
            "规则引擎独立实现，不依赖任何第三方库。",
            "本地会话内保留对局状态，误刷新前可恢复。",
        ],
        "guide": [
            "打开页面后在顶部切换「五子棋 / 中国象棋」。",
            "执黑 / 执红一方先手，点击棋盘落子。",
            "对局结束自动弹出胜负提示，可点击复盘或重新开始。",
            "「悔棋」按钮可回退上一步，适合友谊局。",
        ],
        "versions": [
            ("v2.1", "当前版本：修复象棋异常判断，新增悔棋与复盘。"),
            ("v1.0", "初版：五子棋上线。"),
            ("v1.5", "新增中国象棋，双棋合璧。"),
        ],
    },
]

os.makedirs("works", exist_ok=True)
for w in WORKS:
    tags_html = "".join('<span class="tag">' + t + "</span>" for t in w["tags"])
    spec_html = "".join('<div class="spec"><div class="k">' + k + '</div><div class="v">' + v + "</div></div>" for k, v in w["spec"])
    features_html = "".join("<li>" + f + "</li>" for f in w["features"])
    tech_html = "".join("<li>" + t + "</li>" for t in w["tech"])
    guide_html = "".join("<li>" + g + "</li>" for g in w["guide"])
    versions_html = "".join('<div class="v-item"><div class="v-ver">' + v[0] + '</div><div class="v-desc">' + v[1] + "</div></div>" for v in w["versions"])
    page = TEMPLATE.format(
        name=w["name"], sub=w["sub"], desc=w["desc"], src_file=w["src_file"],
        overview=w["overview"],
        tags_html=tags_html, spec_html=spec_html, features_html=features_html,
        tech_html=tech_html, guide_html=guide_html, versions_html=versions_html,
    )
    path = os.path.join("works", w["file"])
    with open(path, "w", encoding="utf-8") as f:
        f.write(page)
    lines = page.count("\n") + 1
    print(w["file"], "lines:", lines)
print("DONE")
