# -*- coding: utf-8 -*-
"""校验 I18N zh/en 键一致 + 所有 data-i18n 键在字典中有定义"""
import re, json

p = "index.html"
s = open(p, encoding="utf-8").read()

# 提取 I18N 对象（zh 与 en）
m = re.search(r'var I18N = \{(.*?)\n  \};', s, re.S)
assert m, "I18N 对象未找到"
body = m.group(1)
# 找 zh: {...} 和 en: {...}
zh = re.search(r'zh: \{(.*?)\n    \}', body, re.S)
en = re.search(r'en: \{(.*?)\n    \}', body, re.S)
assert zh and en, "zh/en 块未找到"
zh_txt = zh.group(1)
en_txt = en.group(1)

def keys(t):
    return set(re.findall(r"'([A-Za-z0-9_.]+)':", t))

zk, ek = keys(zh_txt), keys(en_txt)
print("zh 键数:", len(zk), "| en 键数:", len(ek))
print("zh 有而 en 无:", sorted(zk - ek))
print("en 有而 zh 无:", sorted(ek - zk))

# data-i18n 键全覆盖
used = set(re.findall(r'data-i18n="([^"]+)"', s))
print("data-i18n 使用键数:", len(used))
print("未在 zh 字典:", sorted(used - zk))
print("未在 en 字典:", sorted(used - ek))
