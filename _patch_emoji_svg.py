# -*- coding: utf-8 -*-
"""作品 emoji -> SVG 图标（Lucide 风格 stroke 24x24，class=em 相对字号 1em）
- 静态 HTML / JS innerHTML 模板：直接替换
- JS textContent 赋值含 emoji：改为 innerHTML + SVG
- Fancy 转换器：placeholder/输入区示例 emoji（😀🎉🌍）是核心功能，豁免保留
"""
import re, glob, sys

# emoji -> svg inner（stroke 图标）
S = '<svg class="em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{inner}</svg>'
EMOJI_MAP = {
    '🎙': '<path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" y1="19" x2="12" y2="22"/>',
    '📋': '<rect x="5" y="3" width="14" height="18" rx="2"/><path d="M9 8h6M9 12h6M9 16h4"/>',
    '🌞': '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
    '🌆': '<path d="M17 18a5 5 0 0 0-10 0"/><line x1="12" y1="9" x2="12" y2="2"/><line x1="4.22" y1="10.22" x2="5.64" y2="11.64"/><line x1="1" y1="18" x2="3" y2="18"/><line x1="21" y1="18" x2="23" y2="18"/><line x1="18.36" y1="11.64" x2="19.78" y2="10.22"/><line x1="23" y1="22" x2="1" y2="22"/>',
    '📊': '<line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/>',
    '📤': '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/>',
    '🗑': '<polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>',
    '🖊': '<path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4z"/>',
    '🎲': '<rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8" cy="8" r="1"/><circle cx="16" cy="8" r="1"/><circle cx="12" cy="12" r="1"/><circle cx="8" cy="16" r="1"/><circle cx="16" cy="16" r="1"/>',
    '👥': '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    '🎵': '<path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/>',
    '🔍': '<circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>',
    '🔄': '<polyline points="23 4 23 10 17 10"/><path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/>',
    '🔊': '<polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M15.54 8.46a5 5 0 0 1 0 7.07"/>',
    '🔁': '<polyline points="17 1 21 5 17 9"/><path d="M3 11V9a4 4 0 0 1 4-4h14"/><polyline points="7 23 3 19 7 15"/><path d="M21 13v2a4 4 0 0 1-4 4H3"/>',
    '📜': '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/>',
    '📝': '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/>',
    '🎛': '<line x1="4" y1="21" x2="4" y2="14"/><line x1="4" y1="10" x2="4" y2="3"/><line x1="12" y1="21" x2="12" y2="12"/><line x1="12" y1="8" x2="12" y2="3"/><line x1="20" y1="21" x2="20" y2="16"/><line x1="20" y1="12" x2="20" y2="3"/><line x1="1" y1="14" x2="7" y2="14"/><line x1="9" y1="8" x2="15" y2="8"/><line x1="17" y1="16" x2="23" y2="16"/>',
    '✅': '<circle cx="12" cy="12" r="10"/><polyline points="8 12 11 15 16 9"/>',
    '🗓': '<rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/>',
    '🔐': '<rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
    '🟢': '<circle cx="12" cy="12" r="6" fill="currentColor" stroke="none"/>',
    '📁': '<path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/>',
    '📂': '<path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/><line x1="6" y1="14" x2="18" y2="14"/>',
    '✕': '<line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>',
    '🔂': '<polyline points="17 1 21 5 17 9"/><path d="M3 11V9a4 4 0 0 1 4-4h14"/><line x1="5" y1="19" x2="5" y2="21"/>',
    '❌': '<circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/>',
    '✏': '<path d="M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5z"/>',
    '📦': '<path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/>',
    '👤': '<path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>',
    '📈': '<polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/>',
    '💾': '<path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/>',
    '➕': '<line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>',
    '💡': '<path d="M9 18h6"/><path d="M10 22h4"/><path d="M15.09 14c.18-.98.65-1.74 1.41-2.5A4.65 4.65 0 0 0 18 8 6 6 0 0 0 6 8c0 1 .23 2.23 1.5 3.5.76.76 1.23 1.52 1.41 2.5"/>',
    '⚡': '<polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>',
    '📥': '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/>',
    '🖨': '<polyline points="6 9 6 2 18 2 18 9"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/>',
    '⚠': '<path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>',
    '❓': '<circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/>',
    '📐': '<path d="M3 3v18h18z"/><line x1="3" y1="9" x2="15" y2="21"/><line x1="9" y1="3" x2="9" y2="15"/>',
    '📏': '<path d="M12 3L21 12 12 21 3 12z"/><line x1="8.5" y1="7.5" x2="10" y2="9"/><line x1="12" y1="3.5" x2="13.5" y2="5"/>',
    '🧭': '<circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/>',
    '🚩': '<path d="M4 22V2"/><path d="M4 6h16l-3 4 3 4H4"/>',
    '🏁': '<path d="M4 22V4a1 1 0 0 1 1-1h15l-3 4 3 4H5"/><line x1="4" y1="10" x2="20" y2="10"/>',
    '📍': '<path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>',
    '🧹': '<path d="M12 3L4 11l9 9 8-8z"/><line x1="8" y1="10" x2="10" y2="8"/>',
    '🗺': '<polygon points="1 6 1 22 8 18 16 22 23 18 23 2 16 6 8 2 1 6"/><line x1="8" y1="2" x2="8" y2="18"/><line x1="16" y1="6" x2="16" y2="22"/>',
    '📌': '<path d="M8 2h8l-1 6 3 3H6l3-3z"/><line x1="12" y1="11" x2="12" y2="22"/>',
    '🧠': '<path d="M12 4a4 4 0 0 0-4 4 3 3 0 0 0-1 6 3 3 0 0 0 1 6 4 4 0 0 0 8 0 3 3 0 0 0 1-6 3 3 0 0 0-1-6 4 4 0 0 0-4-4z"/><path d="M12 4v16"/>',
    '📖': '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>',
    '🎨': '<path d="M12 22a10 10 0 1 1 10-10c0 2-1.5 3-3 3h-2.5a2 2 0 0 0-1.5 3.5 2 2 0 0 0 1.5 3.5H15a2 2 0 0 1 2 2z"/><circle cx="7.5" cy="10.5" r="1"/><circle cx="12" cy="7.5" r="1"/><circle cx="16.5" cy="10.5" r="1"/>',
    '😀': '<circle cx="12" cy="12" r="10"/><path d="M8 14s1.5 2 4 2 4-2 4-2"/><line x1="9" y1="9" x2="9.01" y2="9"/><line x1="15" y1="9" x2="15.01" y2="9"/>',
    '🎉': '<path d="M20 2l-2 6 6 2-6 2 2 6-6-2-2 6-2-6-6 2 2-6-6-2 6-2-2-6 6 2 2-6z"/>',
    '🌍': '<circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>',
    '➡': '<line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/>',
}

def to_svg(emoji):
    return S.format(inner=EMOJI_MAP[emoji])

CSS_RULE = '\nsvg.em { width: 1em; height: 1em; display: inline-block; vertical-align: -0.15em; }\n'

def replace_all(s, mapping, skip=None):
    """全文本替换 emoji -> svg（skip 为豁免的 emoji 集合）"""
    import re
    pat = re.compile("(" + "|".join(map(re.escape, mapping.keys())) + r")\uFE0F?")
    def repl(m):
        e = m.group(1)
        if skip and e in skip:
            return e
        return to_svg(e)
    return pat.sub(repl, s)

def fix_textcontent(s):
    """JS 里 .textContent = '含 emoji 字符串' -> .innerHTML = '<svg...>...'"""
    import re
    pat = re.compile(r"\.textContent = (['\"])(.*?)\1", re.S)
    def repl(m):
        quote = m.group(1)
        val = m.group(2)
        has_emoji = re.search(r"[\U0001F000-\U0001FAFF\u2600-\u27BF\u2705\u274C]", val)
        if not has_emoji:
            return m.group(0)
        new_val = re.sub(r"[\U0001F000-\U0001FAFF\u2600-\u27BF\u2705\u274C]\uFE0F?", lambda mm: to_svg(mm.group(0).strip('\uFE0F')), val)
        # 若首字符就是图标，保持其后空格
        return ".innerHTML = " + quote + new_val + quote
    return pat.sub(repl, s)

jobs = [
    ("Xinghua Middle School Broadcasting Station System.html", None),
    ("Self-service accounting system Pro Enhanced V6.html", None),
    ("Nayingte M4e Code Writing System V2.9Pro.html", None),
    ("Fancy-Pattern-Emoji-to-Image-Converter.html", {'😀', '🎉', '🌍'}),
]
for fname, skip in jobs:
    try:
        s = open(fname, encoding="utf-8").read()
    except Exception as e:
        print("ERR", fname, e); continue
    s = replace_all(s, EMOJI_MAP, skip)
    s = fix_textcontent(s)
    if 'svg.em' not in s:
        s = s.replace("</style>", CSS_RULE + "</style>", 1)
    open(fname, "w", encoding="utf-8").write(s)
    print("OK  ", fname)
print("DONE")
