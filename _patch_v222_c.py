# -*- coding: utf-8 -*-
"""v22.2 脚本 C：热力图改为 GitHub 官方 API 跨仓库聚合（jogruber 404 弃用）"""
p = "index.html"
s = open(p, encoding="utf-8").read()

start_marker = "  /* ========== 开源足迹 · GitHub 贡献热力图 ========== */"
end_marker = "  /* ========== 幸运今日（按日期固定） ========== */"
i0 = s.index(start_marker)
i1 = s.index(end_marker)
assert i0 < i1, "markers order wrong"

new_block = """  /* ========== 开源足迹 · GitHub 贡献热力图（官方 API 跨仓库聚合） ========== */
  (function () {
    var grid = document.getElementById('hmGrid');
    var totalEl = document.getElementById('hmTotal');
    if (!grid || !totalEl) return;
    var lastSum = 0;
    var WEEKS = 53, DAYS = 7;
    function paint(days) {
      var html = '';
      var sum = 0;
      var today = new Date();
      var start = new Date(today.getFullYear(), today.getMonth(), today.getDate() - 364);
      while (start.getDay() !== 0) start.setDate(start.getDate() - 1);
      var cell = new Date(start);
      for (var w = 0; w < WEEKS; w++) {
        for (var d = 0; d < DAYS; d++) {
          var iso = cell.toISOString().slice(0, 10);
          var c = days[iso] || 0;
          sum += c;
          var lvl = c === 0 ? 0 : (c <= 2 ? 1 : c <= 4 ? 2 : c <= 7 ? 3 : 4);
          html += '<span class="hm-cell l' + lvl + '" title="' + iso + ': ' + c + '"></span>';
          cell.setDate(cell.getDate() + 1);
        }
      }
      lastSum = sum;
      grid.innerHTML = html;
      if (window.__renderHmTotal) window.__renderHmTotal();
    }
    window.__renderHmTotal = function () {
      if (!totalEl) return;
      var en = window.YAULE_LANG === 'en';
      totalEl.textContent = window.__hmFallback
        ? (en ? 'Preview data (API unavailable)' : '预览数据（接口暂不可用）')
        : (en ? 'Contributions in the last year: ' + lastSum : '过去一年累计贡献：' + lastSum);
    };
    function fetchJson(url) {
      return fetch(url).then(function (r) { if (!r.ok) throw new Error(String(r.status)); return r.json(); });
    }
    function collect() {
      var days = {};
      fetchJson('https://api.github.com/users/Yaule-Rate/repos?per_page=30&sort=pushed')
        .then(function (repos) {
          if (!repos || !repos.length) throw new Error('no repos');
          var jobs = repos.slice(0, 6).map(function (repo) {
            return fetchJson('https://api.github.com/repos/' + repo.full_name + '/commits?per_page=100')
              .then(function (list) {
                return (list || []).map(function (c) {
                  return c && c.commit && c.commit.committer && c.commit.committer.date;
                }).filter(Boolean);
              })
              .catch(function () { return []; });
          });
          return Promise.all(jobs);
        })
        .then(function (groups) {
          var all = [];
          groups.forEach(function (g) { all = all.concat(g); });
          if (!all.length) throw new Error('empty');
          all.forEach(function (dt) {
            var iso = new Date(dt).toISOString().slice(0, 10);
            days[iso] = (days[iso] || 0) + 1;
          });
          paint(days);
        })
        .catch(function () {
          window.__hmFallback = true;
          var fake = {};
          var d = new Date();
          var cnt = 0;
          for (var i = 0; i < 365; i++) {
            d.setDate(d.getDate() - 1);
            var w = d.getDay();
            var n = 0;
            if (i % 13 === 0) n = 3 + (i % 5);
            else if (i % 29 === 0) n = 1;
            if (w === 0 || w === 6) n = 0;
            if (n > 0) { fake[d.toISOString().slice(0, 10)] = n; cnt++; }
          }
          paint(fake);
        });
    }
    collect();
  })();

"""
s = s[:i0] + new_block + s[i1:]
open(p, "w", encoding="utf-8").write(s)
print("C ok")
