# -*- coding: utf-8 -*-
"""
马树梅 · 鸿雁归巢 个人AI名片网站 —— 文章页生成脚本

作用：
  1. 4 个「个人成长」栏目页：topics/body.html、topics/women.html、
     topics/business.html、topics/ai.html（每个栏目是一页文章列表，可持续加文章）
  2. 首页 index.html 「内容中心」区块（公众号入口 + 按主题分组的文章列表）
  3. 首页「个人成长」4 张卡片指向对应栏目页，并自动显示篇数

用法：
  改完 content.json 后运行：  python build_articles.py

新增一篇文章：
  在 content.json 的 "articles" 里加一条：
      { "title": "标题", "url": "https://mp.weixin.qq.com/s/xxxx",
        "date": "2026-10-12", "topics": ["body"] }
  topics 取值：body（晨跑与身体管理）/ women（40+女性自我成长）
               / business（创业者的真实思考）/ ai（AI时代的学习与实践）
  然后重跑本脚本即可（首页与栏目页一起刷新）。
"""

import json
import os
import re
import html

BASE = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE, "content.json")
INDEX_FILE = os.path.join(BASE, "index.html")
TOPIC_DIR = os.path.join(BASE, "topics")

START = "<!-- AUTO:CONTENT_START -->"
END = "<!-- AUTO:CONTENT_END -->"
CAT_ORDER = ["body", "women", "business", "ai"]


def load_data():
    with open(DATA_FILE, encoding="utf-8") as f:
        return json.load(f)


def esc(s):
    return html.escape(str(s), quote=True)


def topic_by_id(data, tid):
    for t in data["topics"]:
        if t["id"] == tid:
            return t
    return None


def arts_of(data, tid):
    out = [a for a in data["articles"] if tid in a.get("topics", [])]
    return sorted(out, key=lambda a: a.get("date", ""), reverse=True)


def arts_of_group(data, group):
    out = []
    for tid in group["topics"]:
        out.extend(arts_of(data, tid))
    return sorted(out, key=lambda a: a.get("date", ""), reverse=True)


def card(a, tag, indent=10):
    pad = " " * indent
    p2 = " " * (indent + 2)
    return (
        f'{pad}<a class="article-card" href="{esc(a["url"])}" target="_blank" rel="noopener">\n'
        f'{p2}<div class="meta"><span class="cat-tag">{esc(tag)}</span><span>{esc(a["date"])}</span></div>\n'
        f'{p2}<h4>{esc(a["title"])}</h4>\n'
        f'{p2}<div class="more">在公众号阅读 →</div>\n'
        f'{pad}</a>'
    )


# ---------------------------------------------------------------- 栏目页
TOPIC_TPL = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
<meta http-equiv="Pragma" content="no-cache">
<meta http-equiv="Expires" content="0">
<title>{name} · 马树梅（梅子）</title>
<meta name="description" content="{desc}">
<link rel="stylesheet" href="../css/style.css">
</head>
<body>

<div class="topic-topbar">
  <div class="container">
    <a class="brand" href="../index.html">马树梅 · 鸿雁归巢</a>
    <a class="nav-back" href="../index.html">返回名片 →</a>
  </div>
</div>

<main class="topic-page">
  <div class="container">
    <a class="back" href="../index.html">← 返回名片</a>
    <span class="eyebrow">{tag}</span>
    <h1 class="topic-title">{name}</h1>
    <p class="topic-desc">{desc}</p>
    <div class="topic-count">共 {count} 篇 · 会持续更新</div>

    <div class="topic-list">
{cards}
    </div>

    <div class="wx-entry">
      <div class="wx-entry-main">
        <div class="wx-entry-k">我的公众号</div>
        <div class="wx-entry-t">同一主题的新文章，会最先发在公众号</div>
        <p class="wx-entry-d">{note}</p>
      </div>
      <a class="wx-entry-btn" href="{home}">去公众号看全部 →</a>
    </div>

    <div class="topic-foot">
      <a class="back" href="../index.html">← 回到我的 AI 名片</a>
    </div>
  </div>
</main>

<footer class="site-footer">
  <div class="container">
    <div class="footer-brand">马树梅 · 鸿雁归巢</div>
    <div class="footer-slogan">经营自己，也经营企业。</div>
    <div class="footer-copy">© 2026 马树梅（梅子） · 呼和浩特</div>
  </div>
</footer>

</body>
</html>
"""


def build_topic_pages(data):
    os.makedirs(TOPIC_DIR, exist_ok=True)
    made = []
    note = data["account"]["note"]
    home = data["account"]["home"]
    for t in data["topics"]:
        arts = arts_of(data, t["id"])
        cards = "\n".join(card(a, t["name"]) for a in arts)
        out = TOPIC_TPL.format(
            name=esc(t["name"]),
            tag=esc(t["tag"]),
            desc=esc(t["desc"]),
            count=len(arts),
            cards=cards,
            note=esc(note),
            home=esc(home),
        )
        path = os.path.join(TOPIC_DIR, t["id"] + ".html")
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(out)
        made.append((path, len(arts)))
    return made


# ---------------------------------------------------------------- 首页内容中心
def build_content_block(data):
    acc = data["account"]
    lines = []
    lines.append('      <div class="wx-entry">')
    lines.append('        <div class="wx-entry-main">')
    lines.append(f'          <div class="wx-entry-k">{esc(acc["label"])} · 贴图号</div>')
    lines.append('          <div class="wx-entry-t">这里的文章全部来自我的公众号，新文章会先发在公众号</div>')
    lines.append(f'          <p class="wx-entry-d">{esc(acc["note"])}</p>')
    lines.append('        </div>')
    lines.append(f'        <a class="wx-entry-btn" href="{esc(acc["home"])}">去公众号看全部文章 →</a>')
    lines.append('      </div>')
    lines.append('      <div class="columns">')
    for g in data["groups"]:
        lines.append('        <div class="col">')
        lines.append(f'          <h3>{esc(g["title"])}</h3>')
        lines.append(f'          <p class="col-sub">{esc(g["sub"])}</p>')
        for a in arts_of_group(data, g):
            lines.append(card(a, g["title"].split(". ", 1)[-1]))
        lines.append('        </div>')
    lines.append('      </div>')
    return "\n".join(lines)


# ---------------------------------------------------------------- index 更新
def find_block_end(s, div_start):
    """从 '<div' 起始位置找到与之配对的 </div> 的结束下标。"""
    depth = 0
    for t in re.finditer(r"<div\b|</div>", s[div_start:]):
        if t.group(0) == "</div>":
            depth -= 1
            if depth == 0:
                return div_start + t.end()
        else:
            depth += 1
    return -1


def update_index(data, content_block):
    with open(INDEX_FILE, encoding="utf-8") as f:
        s = f.read()
    changed = []

    # 1) 内容中心区块
    if START in s and END in s:
        s = re.sub(
            re.escape(START) + r".*?" + re.escape(END),
            START + "\n" + content_block + "\n      " + END,
            s,
            flags=re.S,
        )
        changed.append("内容中心区块已刷新")
    else:
        m = re.search(r'^[ ]*<div class="columns"[^>]*>', s, flags=re.M)
        if not m:
            raise SystemExit("× 未找到内容中心的 <div class=\"columns\"> 区块，请检查 index.html")
        end = find_block_end(s, m.start())
        if end < 0:
            raise SystemExit("× columns 区块标签未闭合")
        s = s[: m.start()] + START + "\n" + content_block + "\n      " + END + s[end:]
        changed.append("内容中心区块已建立（首次）")

    # 2) 个人成长 4 卡 → 栏目页
    counter = {"i": 0}

    def repl_cat(mt):
        tag = mt.group(0)
        idx = counter["i"]
        counter["i"] += 1
        tid = CAT_ORDER[idx] if idx < len(CAT_ORDER) else CAT_ORDER[-1]
        nid = re.search(r'data-page-node-id="([^"]+)"', tag)
        nid = f' data-page-node-id="{nid.group(1)}"' if nid else ""
        return f'{mt.group(1)}<a class="cat" href="topics/{tid}.html"{nid}>'

    s, n_cat = re.subn(r"^([ ]*)<a class=\"cat\"[^>]*>", repl_cat, s, flags=re.M)

    # 3) 卡片下方文案 → 查看全部 N 篇
    counter2 = {"i": 0}

    def repl_more(mt):
        idx = counter2["i"]
        counter2["i"] += 1
        tid = CAT_ORDER[idx] if idx < len(CAT_ORDER) else CAT_ORDER[-1]
        n = len(arts_of(data, tid))
        attrs = mt.group(1)
        return f'<span class="cat-more"{attrs}>查看全部 {n} 篇 →</span>'

    s, n_more = re.subn(
        r'<span class="cat-more"([^>]*)>.*?</span>', repl_more, s, flags=re.S
    )

    # 4) 内容中心副文案
    s = s.replace(
        "这里记录我对企业增长、创业经营和个人成长的思考与实践，会持续更新。点击卡片即可阅读。",
        "以下是我的公众号文章，按主题分成三组，会持续更新。点击卡片即可到公众号阅读原文。",
    )

    with open(INDEX_FILE, "w", encoding="utf-8", newline="\n") as f:
        f.write(s)
    changed.append(f"个人成长卡片 → 栏目页（{n_cat} 张）")
    changed.append(f"卡片文案 → 查看全部 N 篇（{n_more} 处）")
    return changed


def main():
    data = load_data()
    made = build_topic_pages(data)
    block = build_content_block(data)
    changed = update_index(data, block)
    print("✓ 栏目页：")
    for p, n in made:
        print(f"   - {os.path.relpath(p, BASE)}（{n} 篇）")
    print("✓ 首页 index.html：")
    for c in changed:
        print(f"   - {c}")
    total = len(data["articles"])
    print(f"✓ 文章总数：{total} 篇")


if __name__ == "__main__":
    main()
