# -*- coding: utf-8 -*-
"""v16 主补丁：人生清单预设 / MC启动器式更新日志 / 进度条颜色 / quote防重叠 / 此刻布局+天气详情 / 生活瞬间平滑切换 / 开源图标 / 卡片详情页入口 / 整体美化"""
path = "index.html"
html = open(path, encoding="utf-8").read()
changed = []

def rep(old, new, tag):
    global html
    if old in html:
        html = html.replace(old, new, 1); changed.append(tag); return True
    print("FAIL:", tag); return False

# ============ 1. 开源图标（瑞幸 / 网易云 / MC，黑白） ============
import re
# 瑞幸（Arcticons GPL）
luckin_svg = '<svg viewBox="0 0 48 48" fill="none" stroke="#17181C" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M8.59 7.185C16.616 26.679 36.858 17.289 37.163 5.5"/><path d="M5.36 11.748c14.195 11.548 29.842 6.712 37.28-3.931M26.07 27.054c-4.152.607-8.14 7.827-.56 11.304c4.427 2.03 11.45-.182 13.69 4.142M16.874 22.28c-4.253 4.097-6.784 9.884-6.178 18.745"/><path d="M23.45 18.408c.43 2.522 4.259 2.63 8.168 2.679a6.18 6.18 0 0 1-.983 3.861a6.54 6.54 0 0 1-4.564 2.107m-9.197-4.775a8.5 8.5 0 0 1-9.303-2.036c2.148-.837 4.314-1.66 9.478-.21c1.378-.36 1.532-1.208 2.139-1.875m11.979 5.809l-2.814.48"/></svg>'
# 网易云（simple-icons CC0）
netease_svg = '<svg viewBox="0 0 24 24" fill="#17181C" xmlns="http://www.w3.org/2000/svg"><path d="M13.046 9.388a3.919 3.919 0 0 0-.66.19c-.809.312-1.447.991-1.666 1.775a2.269 2.269 0 0 0-.074.81c.048.546.333 1.05.764 1.35a1.483 1.483 0 0 0 2.01-.286c.406-.531.355-1.183.24-1.636-.098-.387-.22-.816-.345-1.249a64.76 64.76 0 0 1-.269-.954zm-.82 10.07c-3.984 0-7.224-3.24-7.224-7.223 0-.98.226-3.02 1.884-4.822A7.188 7.188 0 0 1 9.502 5.6a.792.792 0 1 1 .587 1.472 5.619 5.619 0 0 0-2.795 2.462 5.538 5.538 0 0 0-.707 2.7 5.645 5.645 0 0 0 5.638 5.638c1.844 0 3.627-.953 4.542-2.428 1.042-1.68.772-3.931-.627-5.238a3.299 3.299 0 0 0-1.437-.777c.172.589.334 1.18.494 1.772.284 1.12.1 2.181-.519 2.989-.39.51-.956.888-1.592 1.064a3.038 3.038 0 0 1-2.58-.44 3.45 3.45 0 0 1-1.44-2.514c-.04-.467.002-.93.128-1.376.35-1.256 1.356-2.339 2.622-2.826a5.5 5.5 0 0 1 .823-.246l-.134-.505c-.37-1.371.25-2.579 1.547-3.007.329-.109.68-.145 1.025-.105.792.09 1.476.592 1.709 1.023.258.507-.096 1.153-.706 1.153a.788.788 0 0 1-.54-.213c-.088-.08-.163-.174-.259-.247a.825.825 0 0 0-.632-.166.807.807 0 0 0-.634.551c-.056.191-.031.406.02.595.07.256.159.597.217.82 1.11.098 2.162.54 2.97 1.296 1.974 1.844 2.35 4.886.892 7.233-1.197 1.93-3.509 3.177-5.889 3.177zM0 12c0 6.627 5.373 12 12 12s12-5.373 12-12S18.627 0 12 0 0 5.373 0 12Z"/></svg>'
# Minecraft（simple-icons v9 CC0）
mc_svg = '<svg viewBox="0 0 24 24" fill="#17181C" xmlns="http://www.w3.org/2000/svg"><path d="M23.7397 10.0058l-2.4424.0023-.076.1198-.03-.1175h-2.4586l-.0599.136-.023-.136-2.4793.0023-.0438.1613-.0161-.1613-2.5023.0023-.023.265-.007-.265-2.5184.0046-.0092.242-.0254-.242-2.4954.0023-.016.1567-.0439-.1567H7.2673l-.0968.6705-.0553-.1382-.0254-.0024-.2096-.53-1.189.0024-.023.129-.0622-.129H4.431l-.03.1198-.0691-.1198-1.1659.0023-.136.523h-.3156l-.06.2282-.5506-.7512-1.1337.0023L0 13.0403l1.03.954h1.1244l.1774-.6706.0876.0968h.2995l.5.5737h1.1544l.023-.1082.0807.1082h1.1636l.0207-.1175.0737.1175h1.1751l.09-.629.3018.629h1.1889l.0138-.1451.0507.1451H11.03l.0093-.228.0276.228h2.4954l.023-.2511.0093.2511h1.2235l.0392-.175.0115.175h1.2097l.0506-.152.0139.152h1.1958l.0622-.1336.0185.1336h1.1843l.0714-.122.0208.122h1.175l.6798-.9677-.0323-.1544h.3756l.5346-.7396.4562 1.8594h1.152L24 13.0334l-.0184-.0737-.0738-.2535-.069-.2327s-.219-.712-.2466-.8065c-.0346-.1152-.0714-.2327-.1037-.3456l-.0046-.0184.4838-.583zm-2.325.1682h2.2005l.1567.493h-.6383l.0046.0162c.0254.1083.0554.2189.0853.3295.03.1129.0645.2258.0968.3433.0345.1152.069.235.106.3525.0368.1199.0737.2374.1083.3572.023.0737.0438.1451.0668.2189.023.0737.046.1497.0691.2235l.0692.228c.023.0761.0437.1522.0667.2282h-.9976l-.6268-2.2973h-.6405zm-.3548.0023l.1222.493h-1.295l.1175.56h1.3134l.136.553h-1.3342l.2466 1.182-.9954.0023-.5093-2.788zm-2.553.0023l.4816 2.788h-.9954l-.129-.8986h-.3733l.1221.8986h-.9954l-.3064-2.7857zm-2.5484.0023l.1037 1.0322h-.3272l.03.3111h.3272l.1451 1.4424h-.993l-.09-1.1751-.3686-.0092.076 1.1843h-.993l-.1037-2.7834zm-2.546.0023l.0138.493h-1.272l-.0299 1.719h1.3503l.016.5737h-2.364l.0945-2.7834zm-2.5438.0023l-.0208.493H9.56l-.0415.5692 1.3042.0023-.023.5369-1.3296.0023-.0437.6014 1.3456.0045-.0253.5738H8.387l.2926-2.7811zm-2.5392.0023l-.3226 2.781h-.9908l.1245-.8847-.3273-.0092.083-.5737-.3594-.007-.235 1.477H5.311l.5184-2.7811h.917l-.0806.5138.3157.0092-.076.5369.3548.0046L7.41 10.19zm-5.0346.0046h.9171l-.6475 2.7788h-.9884l.2972-1.1797H2.516l-.1543.5737h-.6406l.159-.5737h-.3595l-.3502 1.1797h-.97l.8917-2.7765h.8986l-.1475.5046.3134.0115L2 11.257h.6959l.1451-.5391h.318zm2.182.0046l-.546 2.7811h-.9885l.6175-2.7788zm12.1683.4217l.0391.3248-.341-.0023-.0437-.3202h-.4217l.0438.3525h.387l.0185.129h-.1936l.0715.5461h.2327l-.0184-.1843.3456-.0023.03.1866h.2373l-.083-.5414h-.1935l-.0162-.1314.3963-.0023-.0553-.3548zm-2.9286.0553l.0369.5737h.364l-.0438-.5737zm-1.1958 1.0046l.0184.5484-1.2166-.0023.0115-.4102h1.1774Z"/></svg>'

def replace_visual(idx_anchor, new_svg, tag):
    """替换 life-visual 内第一个 svg 块"""
    global html
    pos = html.find(idx_anchor)
    if pos < 0: print("FAIL:", tag, "anchor"); return
    s = html.find('<svg', pos)
    e = html.find('</svg>', s) + 6
    html = html[:s] + new_svg + html[e:]
    changed.append(tag)

replace_visual('id="lifeCoffee"', luckin_svg, 'icon luckin')
replace_visual('id="lifeMusic"', netease_svg, 'icon netease')
replace_visual('id="lifeGame"', mc_svg, 'icon minecraft')

# ============ 2. 生活瞬间：切换时先淡出再淡入 ============
rep("""    tabs.forEach(function (tab) {
      tab.addEventListener('click', function () {
        tabs.forEach(function (t) { t.classList.remove('active'); });
        this.classList.add('active');
        var key = this.getAttribute('data-life');
        Object.keys(panels).forEach(function (k2) {
          panels[k2].classList.toggle('active', k2 === key);
        });
      });
    });""",
"""    tabs.forEach(function (tab) {
      tab.addEventListener('click', function () {
        if (this.classList.contains('active')) return;
        tabs.forEach(function (t) { t.classList.remove('active'); });
        this.classList.add('active');
        var key = this.getAttribute('data-life');
        Object.keys(panels).forEach(function (k2) { panels[k2].classList.remove('active'); });
        setTimeout(function () { panels[key].classList.add('active'); }, 70);
      });
    });""", 'life fade switch')

# ============ 3. 进度条颜色：内联终值宽度 ============
rep("""      bars.innerHTML = skills.map(function (s) {
        return '<div class="skill-bar-row"><span class="sb-name">' + s.name + '</span><span class="sb-track"><span class="sb-fill" data-w="' + (s.val * 10) + '"></span></span><span class="sb-num">' + s.val + '</span></div>';
      }).join('');
      setTimeout(function () {
        bars.querySelectorAll('.sb-fill').forEach(function (f) { f.style.width = f.getAttribute('data-w') + '%'; });
      }, 300);""",
"""      bars.innerHTML = skills.map(function (s) {
        return '<div class="skill-bar-row"><span class="sb-name">' + s.name + '</span><span class="sb-track"><span class="sb-fill" style="width:' + (s.val * 10) + '%"></span></span><span class="sb-num">' + s.val + '</span></div>';
      }).join('');""", 'skill bar inline width')

# ============ 4. quote 防重叠 ==========
rep("  #quoteText { font-size: 14px; }",
    "  #quoteText { font-size: 14px; flex: 1; min-width: 0; overflow-wrap: anywhere; word-break: break-word; }", 'quote wrap')

# ============ 5. 人生清单：预设勾选 + 纯展示 ==========
old_bucket = """  (function () {
    var grid = document.getElementById('bucketGrid');
    if (!grid) return;
    var items = ['去看一次现场演唱会', '看一场完整的日出', '学会弹一首完整的曲子', '写一本属于自己的小说', '跑一次五公里', '去一次西藏', '给爸妈买一份大礼物', '养一盆活过一年的绿植', '亲手做一顿年夜饭', '学会一门新的外语', '看一次极光', '独自去一座陌生城市旅行', '学会做咖啡拉花', '给十年后的自己写一封信', '种一棵属于自己的树', '养一只猫', '跳一次伞', '读完《三国演义》', '做一次公益志愿者', '发一张自己的专辑', '开一家小店', '通宵看一次流星雨', '把房间布置成喜欢的样子', '拍一支 Vlog 记录一天'];
    var KEY = 'yaule_bucket';
    var done = {};
    try { done = JSON.parse(localStorage.getItem(KEY) || '{}') || {}; } catch (e) {}
    var doneN = document.getElementById('bkDone');
    var totalN = document.getElementById('bkTotal');
    var fill = document.getElementById('bkFill');
    function refresh() {
      var n = 0;
      grid.querySelectorAll('.bucket-item').forEach(function (el) {
        if (el.classList.contains('done')) n++;
      });
      if (doneN) doneN.textContent = n;
      if (totalN) totalN.textContent = items.length;
      if (fill) fill.style.width = (n / items.length * 100) + '%';
    }
    grid.innerHTML = items.map(function (t, idx) {
      var on = done[idx];
      return '<div class="bucket-item' + (on ? ' done' : '') + '" data-i="' + idx + '" role="button" tabindex="0"><span class="bk-check"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg></span><span class="bk-text">' + t + '</span></div>';
    }).join('');
    grid.addEventListener('click', function (e) {
      var item = e.target.closest('.bucket-item');
      if (!item) return;
      var i = item.getAttribute('data-i');
      item.classList.toggle('done');
      done[i] = item.classList.contains('done') ? 1 : 0;
      try { localStorage.setItem(KEY, JSON.stringify(done)); } catch (err) {}
      refresh();
    });
    grid.addEventListener('keydown', function (e) {
      if ((e.key === 'Enter' || e.key === ' ') && e.target.classList.contains('bucket-item')) {
        e.preventDefault();
        e.target.click();
      }
    });
    refresh();
  })();"""
new_bucket = """  (function () {
    var grid = document.getElementById('bucketGrid');
    if (!grid) return;
    // 预设完成状态：默认写死在程序里（第1行2、3；第2行1、2、3；第3行1、2、3、4；第4行1、2、3、4；第5行2、3、4）
    var items = ['去看一次现场演唱会', '看一场完整的日出', '学会弹一首完整的曲子', '写一本属于自己的小说', '跑一次五公里', '去一次西藏', '给爸妈买一份大礼物', '养一盆活过一年的绿植', '亲手做一顿年夜饭', '学会一门新的外语', '看一次极光', '独自去一座陌生城市旅行', '学会做咖啡拉花', '给十年后的自己写一封信', '种一棵属于自己的树', '养一只猫', '跳一次伞', '读完《三国演义》', '做一次公益志愿者', '发一张自己的专辑', '开一家小店', '通宵看一次流星雨', '把房间布置成喜欢的样子', '拍一支 Vlog 记录一天'];
    var doneMap = {};
    [1, 2, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15, 17, 18, 19].forEach(function (i) { doneMap[i] = 1; });
    var doneN = document.getElementById('bkDone');
    var totalN = document.getElementById('bkTotal');
    var fill = document.getElementById('bkFill');
    function refresh() {
      var n = 0;
      grid.querySelectorAll('.bucket-item').forEach(function (el) {
        if (el.classList.contains('done')) n++;
      });
      if (doneN) doneN.textContent = n;
      if (totalN) totalN.textContent = items.length;
      if (fill) fill.style.width = (n / items.length * 100) + '%';
    }
    grid.innerHTML = items.map(function (t, idx) {
      var on = doneMap[idx];
      return '<div class="bucket-item' + (on ? ' done' : '') + '"><span class="bk-check"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg></span><span class="bk-text">' + t + '</span></div>';
    }).join('');
    refresh();
  })();"""
rep(old_bucket, new_bucket, 'bucket preset done')

# ============ 6. 更新日志：MC 启动器风格 ==========
old_tl = """    <div class="timeline">
      <div class="tl-time">2026-09-25</div>
      <div class="tl-axis"><span class="tl-dot now"></span></div>
      <div class="tl-item"><span class="tl-title">站点增强 v14</span><span class="tl-tag">当前</span><div class="tl-desc">RSS 订阅、访问计数、SEO 标签、作品展开预览、图标呼吸、今年进度环。</div></div>
      <div class="tl-time">2026-09-25</div>
      <div class="tl-axis"><span class="tl-dot"></span></div>
      <div class="tl-item"><span class="tl-title">此刻板块 v12</span><div class="tl-desc">时钟与天气独立成板块，新增翻牌时钟、节日飘浮与专属欢迎语。</div></div>
      <div class="tl-time">2026-09-24</div>
      <div class="tl-axis"><span class="tl-dot"></span></div>
      <div class="tl-item"><span class="tl-title">天气与纪念日 v9</span><div class="tl-desc">接入实时天气（Open-Meteo），纪念日倒计时上线。</div></div>
      <div class="tl-time">2026-09-22</div>
      <div class="tl-axis"><span class="tl-dot"></span></div>
      <div class="tl-item"><span class="tl-title">作品卡片 v3</span><div class="tl-desc">精选作品上架，支持下载与伪进度条进入。</div></div>
      <div class="tl-time">2026-09-19</div>
      <div class="tl-axis"><span class="tl-dot"></span></div>
      <div class="tl-item"><span class="tl-title">生活瞬间 v2</span><div class="tl-desc">瑞幸咖啡、网易云音乐、我的世界三块生活数据。</div></div>
      <div class="tl-time">2026-09-18</div>
      <div class="tl-axis"><span class="tl-dot"></span></div>
      <div class="tl-item"><span class="tl-title">站点上线 v1</span><div class="tl-desc">全世界语言的「欢迎你的到来」打字机欢迎页，部署到 GitHub Pages。</div></div>
    </div>"""
new_tl = """    <div class="mc-log">
      <div class="mc-ver current">
        <div class="mc-ver-head">
          <span class="mc-ver-badge">v14</span>
          <span class="mc-ver-date">2026-09-25 · 当前版本</span>
        </div>
        <ul class="mc-ver-list">
          <li class="cat-new"><b>新增</b>RSS / Atom 订阅源，访客可订阅站点每一次更新。</li>
          <li class="cat-new"><b>新增</b>busuanzi 访问计数，页脚实时显示访客与浏览量。</li>
          <li class="cat-new"><b>新增</b>作品卡展开预览：扩展简介、技术标签，点卡片任意处即展开。</li>
          <li class="cat-new"><b>新增</b>呼吸动效 favicon 与「幸运今日」每日签文。</li>
          <li class="cat-chg"><b>优化</b>SEO：补全 keywords / og / twitter 标签，利于搜索引擎收录。</li>
          <li class="cat-chg"><b>优化</b>卡片「查看详情」改为同页打开，不再被浏览器拦截。</li>
        </ul>
      </div>
      <div class="mc-ver">
        <div class="mc-ver-head">
          <span class="mc-ver-badge">v13</span>
          <span class="mc-ver-date">2026-09-25</span>
        </div>
        <ul class="mc-ver-list">
          <li class="cat-new"><b>新增</b>「今年进度环」：2026 年已过百分比与剩余天数。</li>
          <li class="cat-new"><b>新增</b>今日一言 3 秒自动轮播，点击可复制。</li>
          <li class="cat-new"><b>新增</b>页面加载「Y」一笔画动画。</li>
        </ul>
      </div>
      <div class="mc-ver">
        <div class="mc-ver-head">
          <span class="mc-ver-badge">v12</span>
          <span class="mc-ver-date">2026-09-25</span>
        </div>
        <ul class="mc-ver-list">
          <li class="cat-new"><b>新增</b>「此刻」板块独立：时钟与天气单独成卡。</li>
          <li class="cat-new"><b>新增</b>翻牌时钟与页脚停留计时。</li>
          <li class="cat-new"><b>新增</b>作品下载次数统计（本地记录）。</li>
          <li class="cat-chg"><b>移除</b>语言标签小字，保持欢迎页纯粹。</li>
        </ul>
      </div>
      <div class="mc-ver">
        <div class="mc-ver-head">
          <span class="mc-ver-badge">v10</span>
          <span class="mc-ver-date">2026-09-25</span>
        </div>
        <ul class="mc-ver-list">
          <li class="cat-new"><b>新增</b>节日飘浮：自动拉取中国法定节假日，中秋的月亮与灯笼飘 3 秒。</li>
          <li class="cat-new"><b>新增</b>节日专属欢迎语（春节、端午、中秋等 8 个节日）。</li>
        </ul>
      </div>
      <div class="mc-ver">
        <div class="mc-ver-head">
          <span class="mc-ver-badge">v9</span>
          <span class="mc-ver-date">2026-09-24</span>
        </div>
        <ul class="mc-ver-list">
          <li class="cat-new"><b>新增</b>实时天气（Open-Meteo 免费接口，衢州定位）。</li>
          <li class="cat-new"><b>新增</b>纪念日板块：「活着的第 N 天」与「本站上线第 N 天」。</li>
        </ul>
      </div>
      <div class="mc-ver">
        <div class="mc-ver-head">
          <span class="mc-ver-badge">v7</span>
          <span class="mc-ver-date">2026-09-23</span>
        </div>
        <ul class="mc-ver-list">
          <li class="cat-new"><b>新增</b>「生活瞬间」板块：瑞幸咖啡、网易云音乐、我的世界三块数据。</li>
          <li class="cat-new"><b>新增</b>ROG 幻 16 式错峰滚动：图标先下移进入，文字随后浮现。</li>
          <li class="cat-fix"><b>修复</b>奇异类合集布局错误与键盘异常。</li>
        </ul>
      </div>
      <div class="mc-ver">
        <div class="mc-ver-head">
          <span class="mc-ver-badge">v6</span>
          <span class="mc-ver-date">2026-09-22</span>
        </div>
        <ul class="mc-ver-list">
          <li class="cat-new"><b>新增</b>26 种语言打字机轮播：打出 → 停留 → 逐字消失。</li>
          <li class="cat-new"><b>新增</b>今日一言（hitokoto 联网，失败本地降级）。</li>
          <li class="cat-chg"><b>优化</b>彩蛋模式全部改青色，移除紫色残留。</li>
        </ul>
      </div>
      <div class="mc-ver">
        <div class="mc-ver-head">
          <span class="mc-ver-badge">v4</span>
          <span class="mc-ver-date">2026-09-21</span>
        </div>
        <ul class="mc-ver-list">
          <li class="cat-new"><b>新增</b>精选作品卡片：六个作品上架，支持下载。</li>
          <li class="cat-new"><b>新增</b>5 秒伪进度条，模拟进入作品。</li>
        </ul>
      </div>
      <div class="mc-ver">
        <div class="mc-ver-head">
          <span class="mc-ver-badge">v1</span>
          <span class="mc-ver-date">2026-09-18</span>
        </div>
        <ul class="mc-ver-list">
          <li class="cat-new"><b>新增</b>站点上线：全世界语言的「欢迎你的到来」欢迎页。</li>
          <li class="cat-new"><b>新增</b>深色页脚 + 灰白大字 Yaule，WorkBuddy 风格。</li>
        </ul>
      </div>
    </div>"""
rep(old_tl, new_tl, 'changelog MC style')

# ============ 7. 此刻板块：布局 + 天气详情 ==========
rep(""".now-grid {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 20px;
  }""",
""".now-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
  }
  .now-weather { grid-column: 1 / -1; }""", 'now-grid layout')

rep("""      <div class="now-card">
        <p class="weather-row" id="weatherRow">
          <svg id="weatherIcon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17.5 19H9a7 7 0 1 1 6.71-9h1.79a4.5 4.5 0 1 1 0 9Z"/></svg>
          <span id="weatherText">衢州 · 正在读取天气…</span>
        </p>
      </div>""",
"""      <div class="now-card now-weather">
        <p class="weather-row" id="weatherRow">
          <svg id="weatherIcon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17.5 19H9a7 7 0 1 1 6.71-9h1.79a4.5 4.5 0 1 1 0 9Z"/></svg>
          <span id="weatherText">衢州 · 正在读取天气…</span>
        </p>
        <div class="weather-detail" id="weatherDetail">
          <span>体感 <b id="wFeels">--</b>°C</span>
          <span>湿度 <b id="wHum">--</b>%</span>
          <span>风速 <b id="wWind">--</b> km/h</span>
          <span>紫外线 <b id="wUvi">--</b></span>
        </div>
      </div>""", 'weather detail html')

rep("""    fetch('https://api.open-meteo.com/v1/forecast?latitude=28.94&longitude=118.87&current=temperature_2m,weather_code&timezone=Asia%2FShanghai&forecast_days=1')
      .then(function (r) { if (!r.ok) throw new Error('weather'); return r.json(); })
      .then(function (d) {
        var c = d.current;
        icon.innerHTML = svgFor(c.weather_code);
        txt.innerHTML = '<span>衢州</span><span class="weather-temp">' + Math.round(c.temperature_2m) + '°C</span><span>' + textFor(c.weather_code) + '</span>';
      })
      .catch(function () { txt.textContent = '衢州 · 天气暂时不可用'; });""",
"""    fetch('https://api.open-meteo.com/v1/forecast?latitude=28.94&longitude=118.87&current=temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m,uv_index&timezone=Asia%2FShanghai&forecast_days=1')
      .then(function (r) { if (!r.ok) throw new Error('weather'); return r.json(); })
      .then(function (d) {
        var c = d.current;
        icon.innerHTML = svgFor(c.weather_code);
        txt.innerHTML = '<span>衢州</span><span class="weather-temp">' + Math.round(c.temperature_2m) + '°C</span><span>' + textFor(c.weather_code) + '</span>';
        var fe = document.getElementById('wFeels');
        var hu = document.getElementById('wHum');
        var wi = document.getElementById('wWind');
        var uv = document.getElementById('wUvi');
        if (fe) fe.textContent = Math.round(c.apparent_temperature);
        if (hu) hu.textContent = Math.round(c.relative_humidity_2m);
        if (wi) wi.textContent = Math.round(c.wind_speed_10m);
        if (uv) uv.textContent = Math.round(c.uv_index);
      })
      .catch(function () { txt.textContent = '衢州 · 天气暂时不可用'; });""", 'weather js detail')

# 天气详情 CSS + now 移动端
rep("  .now-card .clock-row {",
"""  .now-weather { padding: 28px 32px; }
  .weather-detail {
    display: flex;
    flex-wrap: wrap;
    gap: 10px 22px;
    margin-top: 18px;
    padding-top: 16px;
    border-top: 1px dashed var(--line);
    font-size: 13.5px;
    color: var(--ink-2);
  }
  .weather-detail span { display: inline-flex; align-items: baseline; gap: 4px; }
  .weather-detail b { color: var(--accent); font-weight: 600; font-variant-numeric: tabular-nums; }
  .now-card .clock-row {""", 'weather detail css')

# ============ 8. 卡片 data-detail + meta 跳详情页 ==========
cards = [
    ('Xinghua%20Middle%20School%20Broadcasting%20Station%20System.html', 'works/xinghua.html'),
    ('Self-service%20accounting%20system%20Pro%20Enhanced%20V6.html', 'works/accounting.html'),
    ('Nayingte%20M4e%20Code%20Writing%20System%20V2.9Pro.html', 'works/code-system.html'),
    ('Fancy-Pattern-Emoji-to-Image-Converter.html', 'works/emoji-converter.html'),
    ('CS-Sens-Calibrator.html', 'works/cs-sens.html'),
    ('Chess-Gomoku-Collection.html', 'works/chess.html'),
]
for href, detail in cards:
    idx = html.find(href)
    if idx < 0: print("FAIL card anchor", href); continue
    start = html.rfind('<div class="card', 0, idx)
    if start < 0: print("FAIL card start", href); continue
    gt = html.find('>', start)
    html = html[:gt] + ' data-detail="' + detail + '"' + html[gt:]
    changed.append('card detail ' + detail)

rep("""      if (e.target.closest('.meta')) {
        var link = this.querySelector('a.card-image');
        if (link) link.click();
        return;
      }""",
"""      if (e.target.closest('.meta')) {
        var dd = this.getAttribute('data-detail');
        if (dd) { window.location.href = dd; return; }
        var link = this.querySelector('a.card-image');
        if (link) link.click();
        return;
      }""", 'meta goto detail')

# ============ 9. 整体美化（适度） ==========
rep("""  .section-head .kicker {""",
""".section-head h2 { position: relative; padding-bottom: 10px; }
  .section-head h2::after {
    content: "";
    position: absolute;
    left: 0;
    bottom: 0;
    width: 46px;
    height: 3px;
    border-radius: 3px;
    background: linear-gradient(90deg, var(--accent), var(--accent-2));
  }
  .section-head { margin-bottom: 34px; }
  .section-head .kicker {""", 'section-head accent')

open(path, "w", encoding="utf-8").write(html)
print("CHANGED:", changed)
