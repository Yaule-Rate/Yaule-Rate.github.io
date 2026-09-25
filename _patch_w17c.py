# -*- coding: utf-8 -*-
"""v17c: 详情页下载计数（与主页共用 localStorage yaule_dl_count，按 download 文件名统计）"""
import glob, os

SCRIPT = """<script>
(function () {
  var KEY = 'yaule_dl_count';
  var store = {};
  try { store = JSON.parse(localStorage.getItem(KEY) || '{}') || {}; } catch (e) {}
  document.querySelectorAll('a[download]').forEach(function (a) {
    a.addEventListener('click', function () {
      var name = this.getAttribute('download') || 'unknown';
      store[name] = (store[name] || 0) + 1;
      try { localStorage.setItem(KEY, JSON.stringify(store)); } catch (e) {}
    });
  });
})();
</script>
</body>
"""

for f in glob.glob("works/*.html"):
    html = open(f, encoding="utf-8").read()
    if "yaule_dl_count" in html:
        print("skip (already):", f)
        continue
    if "</body>" not in html:
        print("FAIL no body:", f)
        continue
    html = html.replace("</body>", SCRIPT, 1)
    open(f, "w", encoding="utf-8").write(html)
    print("OK:", f)
print("DONE")
