# -*- coding: utf-8 -*-
"""v16b: 更新日志 MC 启动器风格 CSS"""
path = "index.html"
html = open(path, encoding="utf-8").read()
anchor = "  /* ===== 人生清单 ===== */"
add_css = """  /* ===== 更新日志（我的世界启动器风格） ===== */
  .mc-log { display: flex; flex-direction: column; gap: 14px; max-width: 860px; margin: 0 auto; }
  .mc-ver {
    background: var(--card-bg);
    border: 1px solid var(--line);
    border-radius: 16px;
    padding: 20px 26px 14px;
    position: relative;
    transition: border-color 0.18s ease;
  }
  .mc-ver:hover { border-color: rgba(2,132,199,0.45); }
  .mc-ver.current { border-color: rgba(2,132,199,0.55); box-shadow: 0 0 0 3px rgba(2,132,199,0.08); }
  .mc-ver-head { display: flex; align-items: center; gap: 12px; margin-bottom: 12px; flex-wrap: wrap; }
  .mc-ver-badge {
    font-family: "Noto Serif SC", Georgia, serif;
    font-weight: 700;
    font-size: 16px;
    color: #fff;
    background: linear-gradient(135deg, var(--accent), var(--accent-2));
    padding: 4px 14px;
    border-radius: 9px;
    letter-spacing: 0.5px;
    box-shadow: 0 4px 12px rgba(2,132,199,0.28);
  }
  .mc-ver.current .mc-ver-badge { animation: badgeGlow 2.4s ease infinite; }
  @keyframes badgeGlow { 0%,100% { box-shadow: 0 4px 12px rgba(2,132,199,0.28); } 50% { box-shadow: 0 4px 20px rgba(56,189,248,0.55); } }
  .mc-ver-date { font-size: 12.5px; color: var(--ink-2); letter-spacing: 0.4px; }
  .mc-ver-list { list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 7px; }
  .mc-ver-list li {
    position: relative;
    padding-left: 17px;
    font-size: 13.5px;
    color: var(--ink-2);
    line-height: 1.75;
  }
  .mc-ver-list li::before {
    content: "";
    position: absolute;
    left: 0;
    top: 0.72em;
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--line-strong);
  }
  .mc-ver-list li b {
    font-weight: 600;
    font-size: 12px;
    color: var(--ink);
    border: 1px solid var(--line);
    border-radius: 6px;
    padding: 0 7px;
    margin-right: 8px;
    background: var(--bg);
  }
  .mc-ver-list li.cat-new b { color: #15803d; border-color: rgba(34,197,94,0.35); background: rgba(34,197,94,0.06); }
  .mc-ver-list li.cat-new::before { background: #22c55e; }
  .mc-ver-list li.cat-chg b { color: var(--accent); border-color: rgba(2,132,199,0.35); background: rgba(2,132,199,0.06); }
  .mc-ver-list li.cat-chg::before { background: var(--accent); }
  .mc-ver-list li.cat-fix b { color: #c2410c; border-color: rgba(249,115,22,0.35); background: rgba(249,115,22,0.06); }
  .mc-ver-list li.cat-fix::before { background: #f97316; }

  /* ===== 人生清单 ===== */"""
if anchor in html:
    html = html.replace(anchor, add_css, 1)
    open(path, "w", encoding="utf-8").write(html)
    print("OK")
else:
    print("FAIL anchor")
