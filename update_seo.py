# -*- coding: utf-8 -*-
"""update_seo.py —— Yaule 失眠夜空间 SEO 自动维护工具

用法（每次改版后运行一次）:
    python update_seo.py

做什么:
    1. 扫描 index.html「更新日志」的版本列表 -> 重写 atom.xml 的更新条目（取最近 6 个版本）
    2. 扫描 works/*.html 的 <title> 与 <meta description> -> 重写 atom.xml 的作品条目
    3. 汇总全部页面 -> 重写 sitemap.xml（含 lastmod / changefreq / priority）
输出: atom.xml, sitemap.xml（UTF-8，与仓库同步推送即可）
"""
import re
import glob
import subprocess
import datetime

BASE = "https://Yaule-Rate.github.io"
TZ = "+08:00"

def git_last_commit_date():
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            capture_output=True, text=True, encoding="utf-8", timeout=10,
        ).stdout.strip()
        return out[:10] if out else datetime.date.today().isoformat()
    except Exception:
        return datetime.date.today().isoformat()

def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;").replace("'", "&apos;"))

def iso(dt_str):
    """'2026-09-25 14:05:11' -> '2026-09-25T14:05:11+08:00'"""
    m = re.match(r"(\d{4}-\d{2}-\d{2})[ T](\d{2}:\d{2}:\d{2})", dt_str)
    if m:
        return m.group(1) + "T" + m.group(2) + TZ
    return dt_str + "T00:00:00" + TZ

# ---------- 1. 读取版本日志 ----------
html = open("index.html", encoding="utf-8").read()
vers = re.findall(
    r'<span class="mc-ver-badge">(v\d+)</span>\s*<span class="mc-ver-date">([\d\- :]+)',
    html,
)
# [(ver, date)]，v16 -> v1 顺序

# ---------- 2. 读取作品详情页 ----------
works = []
for f in sorted(glob.glob("works/*.html")):
    s = open(f, encoding="utf-8").read()
    t = re.search(r"<title>(.*?)</title>", s)
    d = re.search(r'<meta name="description" content="(.*?)">', s)
    if t:
        name = re.sub(r"\s*·\s*Yaule.*$", "", t.group(1)).strip()
        works.append({
            "name": name,
            "url": BASE + "/works/" + f.replace("\\", "/").split("/")[-1],
            "desc": d.group(1) if d else name,
        })

lastmod = git_last_commit_date()

# ---------- 3. sitemap.xml ----------
pages = [
    (BASE + "/", "1.0", "weekly"),
    (BASE + "/space.html", "0.9", "weekly"),
    (BASE + "/changelog.html", "0.8", "weekly"),
]
for w in works:
    pages.append((w["url"], "0.7", "monthly"))
root_works = [
    "Xinghua%20Middle%20School%20Broadcasting%20Station%20System.html",
    "Self-service%20accounting%20system%20Pro%20Enhanced%20V6.html",
    "Nayingte%20M4e%20Code%20Writing%20System%20V2.9Pro.html",
    "Fancy-Pattern-Emoji-to-Image-Converter.html",
    "CS-Sens-Calibrator.html",
    "Chess-Gomoku-Collection.html",
]
for rw in root_works:
    pages.append((BASE + "/" + rw, "0.6", "monthly"))

sitemap = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for url, pri, freq in pages:
    sitemap.append("  <url>")
    sitemap.append("    <loc>%s</loc>" % url)
    sitemap.append("    <lastmod>%s</lastmod>" % lastmod)
    sitemap.append("    <changefreq>%s</changefreq>" % freq)
    sitemap.append("    <priority>%s</priority>" % pri)
    sitemap.append("  </url>")
sitemap.append("</urlset>")
open("sitemap.xml", "w", encoding="utf-8").write("\n".join(sitemap) + "\n")
print("sitemap.xml: %d 个页面" % len(pages))

# ---------- 4. atom.xml ----------
entries = []
# 版本更新条目（最近 6 个版本）
recent = vers[:6] if vers else []
for i, (ver, dt) in enumerate(recent):
    tag = "[ADD] / [INFO] / [FIX]"
    entries.append({
        "title": "Yaule 失眠夜空间更新 %s" % ver,
        "url": BASE + "/",
        "id": BASE + "/update-" + ver + "-" + dt.replace(" ", "-").replace(":", ""),
        "updated": iso(dt),
        "summary": "版本 %s（%s）上线：主页完整更新日志已同步，可在 %s 查看全部记录与时间戳。" % (ver, dt, BASE + "/changelog.html"),
    })
# 详情日志页条目
entries.append({
    "title": "新增详细日志页：全版本时间戳一览",
    "url": BASE + "/changelog.html",
    "id": BASE + "/changelog",
    "updated": iso(recent[0][1]) if recent else lastmod + "T00:00:00" + TZ,
    "summary": "独立的更新日志页面，收录 v1 至当前版本的全部改动记录，每条带完整时间戳与 [ADD] / [INFO] / [FIX] 标签，与主页实时同步。",
})
# 作品条目
for w in works:
    entries.append({
        "title": w["name"],
        "url": w["url"],
        "id": w["url"],
        "updated": iso(recent[0][1]) if recent else lastmod + "T00:00:00" + TZ,
        "summary": w["desc"],
    })

feed = ['<?xml version="1.0" encoding="utf-8"?>',
        '<feed xmlns="http://www.w3.org/2005/Atom">',
        "  <title>Yaule 的个人空间</title>",
        "  <subtitle>欢迎你的到来 · 记录咖啡、音乐、游戏与作品</subtitle>",
        "  <link href=\"%s/\"/>" % BASE,
        '  <link rel="self" href="%s/atom.xml"/>' % BASE,
        "  <id>%s/</id>" % BASE,
        "  <updated>%s</updated>" % (entries[0]["updated"] if entries else lastmod + "T00:00:00" + TZ),
        "  <author>",
        "    <name>Yaule</name>",
        "    <email>1957784559@qq.com</email>",
        "  </author>"]
for e in entries:
    feed.append("  <entry>")
    feed.append("    <title>%s</title>" % esc(e["title"]))
    feed.append("    <link href=\"%s\"/>" % e["url"])
    feed.append("    <id>%s</id>" % e["id"])
    feed.append("    <updated>%s</updated>" % e["updated"])
    feed.append("    <summary>%s</summary>" % esc(e["summary"]))
    feed.append("  </entry>")
feed.append("</feed>")
open("atom.xml", "w", encoding="utf-8").write("\n".join(feed) + "\n")
print("atom.xml: %d 条 entry" % len(entries))
print("DONE")
