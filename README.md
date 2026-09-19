# 🌙 失眠夜 · 个人空间

> 在代码里构建逻辑，在方块里搭建世界，在赛场里验证热爱。

一个基于纯前端 HTML/CSS/JavaScript 构建的个人主页，融合了编程开发、机器人工程、游戏竞技等多元兴趣展示，配有丰富的交互动画和深夜主题彩蛋。

![GitHub](https://img.shields.io/badge/HTML-5-E34F26?logo=html5&logoColor=white)
![CSS](https://img.shields.io/badge/CSS-3-1572B6?logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-F7DF1E?logo=javascript&logoColor=black)
![GitHub Pages](https://img.shields.io/badge/Deploy-GitHub%20Pages-222222?logo=github)

---

## ✨ 功能特性

### 📄 页面板块

| 板块 | 说明 |
|------|------|
| 🏠 首页 | 全屏入场警告弹窗 + Hero 大标题 + 打字机标语 + 入场动画 |
| 👤 关于我 | 个人简介 + 能力雷达图 + 12 个悬浮技能泡泡 |
| ❤️ 个人爱好 | 5 列卡片展示（音乐 / 旅行 / 自行车 / 游戏 / 体育） |
| 🌳 技能树 | SVG 辐射状技能图谱，6 大主技能 + 8 个子技能，连线依次绘制 |
| 📷 生活瞬间 | 3 列响应式照片墙，图片存储于仓库 `Moments of Life/` 目录 |
| 📈 成长轨迹 | 左侧竖线时间线，技术成长历程记录 |
| 🎮 游戏档案 | CS 系列 + 我的世界双列展示，总游戏时长 2025.7 小时 + 扇形统计图 |
| 🖥️ 设备配置 | ROG 全家桶外设展示（夜魔 X / 冰刃 S / 夜神 Pro 550Hz / 棱镜 2 / 卓威） |
| 🤖 机器人竞赛 | 机甲大师 RoboMaster 等竞赛经历 |
| 💻 开发作品 | 4 个项目卡片，点击跳转仓库内实际运行的 HTML 项目 |
| 🏆 荣誉奖项 | 2×3 网格布局，获奖经历展示 |
| ✍️ 留下名字 | 访客留言板，提交后自动写入仓库 `visitors.txt`，超 5 人电影片尾式滚动 |
| 📬 联系我 | 4 卡片联系方式（邮箱 / GitHub / QQ / 个人网站） |

### 🎨 交互与动画

- **滚动进度条**：顶部实时显示页面滚动进度
- **右侧侧边导航**：圆点导航，悬停显示板块名称，点击平滑跳转
- **双向滚动动画**：IntersectionObserver 实现，向上/向下滚动均触发卡片依次展开
- **入场动画**：确认进入后，导航栏下滑 + Hero 元素逐级上浮
- **鼠标点击粒子**：每次点击产生紫色粒子扩散特效
- **流星背景**：Canvas 绘制的缓慢流星，全屏均匀分布，带拖尾效果
- **卡片悬停**：顶部紫色渐变横条 + 发光边框 + 上浮效果
- **大标题发光**：Hero 标题、板块标题均带紫色光晕

### 🌙 主题与彩蛋

| 功能 | 触发方式 |
|------|----------|
| ☀️ 亮色模式 | 默认主题 |
| 🌙 暗色模式 | 导航栏月亮/太阳图标切换，favicon 同步变化 |
| 🌌 深夜彩蛋模式 | 双击导航栏「失眠夜」logo，触发深夜主题 + 提示弹窗 |
| ⌨️ Konami 代码雨 | 键盘输入 `↑↑↓↓←→←→BA`，触发黑客帝国风格代码雨 |
| 🎵 音乐播放器 | 左下角悬浮播放器，播放仓库内 `Summer Wind - Fire Sheep is Sleeping.mp3` |

### 📊 统计功能

- 页脚显示网站平稳运行天数
- 实时显示本次停留时间（分:秒）
- 接入不蒜子统计，展示独立访客数与访问量

---

## 🛠️ 技术栈

- **HTML5** — 语义化标签，单文件结构
- **CSS3** — 自定义属性（CSS Variables）三套主题、Grid/Flex 布局、动画关键帧、响应式媒体查询
- **原生 JavaScript (ES6+)** — 无任何框架依赖，IntersectionObserver、Canvas API、Fetch API、GitHub REST API
- **SVG** — 内联矢量图标、技能树图谱、雷达图、扇形统计图
- **GitHub Pages** — 静态托管部署

---

## 🚀 部署说明

### 方式一：直接部署（推荐）

1. Fork 本仓库到你的 GitHub 账号
2. 进入仓库 Settings → Pages
3. Source 选择 `Deploy from a branch`，Branch 选择 `main` / `root`
4. 等待部署完成，访问 `https://你的用户名.github.io/`

### 方式二：本地预览

```bash
# 克隆仓库
git clone https://github.com/你的用户名/你的仓库名.git
cd 你的仓库名

# 用浏览器直接打开 index.html 即可
# 或使用本地服务器（推荐，避免部分浏览器跨域限制）
python3 -m http.server 8080
# 访问 http://localhost:8080
```

---

## 📁 项目结构

```
N1ghtGlow520.github.io/
├── index.html                              # 主页面（单文件包含所有 CSS/JS）
├── visitors.txt                            # 访客留言板存储文件
├── Summer Wind - Fire Sheep is Sleeping.mp3  # 背景音乐
├── Moments of Life/                        # 生活瞬间照片目录
│   ├── Robot competition venue.jpg
│   ├── road cycling.jpg
│   ├── Late-night coding.png
│   ├── MC Redstone Creations.png
│   ├── Music Time.jpg
│   ├── Equipment upgrade.jpg
│   ├── team collaboration.jpg
│   ├── Award Moment.jpg
│   └── Travel Time.jpg
├── Xinghua Middle School Broadcasting Station System.html   # 开发作品1
├── Self-service accounting system Pro Enhanced V6.html      # 开发作品2
├── Nayingte M4e Code Writing System V2.9Pro.html           # 开发作品3
└── README.md
```

---

## ⚙️ 自定义说明

### 替换个人信息

打开 `index.html`，搜索以下关键词进行替换：

| 内容 | 搜索关键词 |
|------|-----------|
| 个人名称 | `失眠夜` |
| 个人简介 | `你好，我是失眠夜` |
| 导航链接 | `navbar-links` |
| 开发作品 | `id="projects"` |
| 联系方式 | `id="contact"` |

### 替换生活瞬间照片

1. 将照片放入 `Moments of Life/` 目录
2. 在 `index.html` 中搜索 `photo-wall`，修改对应 `<img src="...">` 的文件名
3. 支持 JPG / PNG / WebP 格式，建议宽度 ≥ 800px

### 配置访客留言板写入功能

访客留言板默认从 `visitors.txt` 读取名单。要实现提交后写入仓库，需配置 GitHub Token：

1. 前往 [GitHub Token 设置页](https://github.com/settings/tokens) 生成 Classic Token，勾选 `repo` 权限
2. 在 `index.html` 中搜索 `YOUR_GITHUB_TOKEN_HERE`，替换为你的 Token
3. 确保仓库根目录存在 `visitors.txt` 文件

> ⚠️ **安全提示**：Token 暴露在前端代码中存在被他人滥用的风险。个人项目可接受，建议定期轮换 Token。如需更高安全性，可考虑使用 GitHub OAuth App 或第三方 Serverless 函数代理写入操作。

### 修改主题配色

在 `index.html` 的 `<style>` 顶部搜索 `:root`，修改 CSS 变量：

```css
:root {
  --primary: #7c3aed;        /* 主色 */
  --primary-light: #a78bfa;  /* 浅色 */
  --bg-card: #f8f7ff;        /* 卡片背景 */
  /* ... 更多变量 */
}
```

暗色模式和深夜彩蛋模式的变量分别在 `body.dark-theme` 和 `body.night-mode` 中定义。

---

## 🎮 开发作品链接

网站内「开发作品」板块直接跳转至仓库内的独立 HTML 项目：

1. **兴华中学广播站系统** — 校园广播管理系统
2. **自助记账系统 Pro Enhanced V6** — 个人财务管理工具
3. **纳英特 M4e 代码编写系统 V2.9Pro** — 机器人编程 IDE

---

## 📝 许可证

本项目仅供个人学习与展示使用。如需转载或使用，请注明出处。

---

## 🙏 致谢

- 不蒜子 — 网页访问量统计
- GitHub Pages — 静态网站托管
- 所有访问过这个空间的朋友 ✨

---

<p align="center">
  <i>夜色温柔，代码不眠，星光与你都在。</i>
</p>
