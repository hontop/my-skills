# -*- coding: utf-8 -*-
"""
把 20 张能力卡（R/I/A1/A2/E/B 六段）解析为知识库数据 knowledge.json。
内容 100% 取自己安装的能力卡原文，不做人工复述。
"""
import json
import os
import re

SKILLS = r"C:/Users/hontop1/.workbuddy/skills"
OUT = r"C:/Users/hontop1/WorkBuddy/2026-10-17-23-30-17/knowledge-base/knowledge.json"

BOOKS = [
    {
        "slug": "coaching-habit",
        "title": "关键7问",
        "orig": "The Coaching Habit",
        "author": "[加] 迈克尔·邦吉·斯坦尼尔",
        "role": "跟人说话",
        "oneliner": "少给建议，多问七个固定问题——把主导权交还给对方",
        "ask_object": "人（对话对象，或你自己）",
        "ask_purpose": "让对方自己想清楚",
        "color": "#2563eb",
    },
    {
        "slug": "questions-are-the-answer",
        "title": "问题即答案",
        "orig": "Questions Are the Answer",
        "author": "[美] 赫尔·葛瑞格森",
        "role": "自己卡住",
        "oneliner": "卡住时缺的不是答案而是问题——换一种问法，改变答案的搜索空间",
        "ask_object": "问题本身",
        "ask_purpose": "换一种问法，改变答案的搜索空间",
        "color": "#7c3aed",
    },
    {
        "slug": "asking-the-right-questions",
        "title": "学会提问",
        "orig": "Asking the Right Questions",
        "author": "[美] 尼尔·布朗 & 斯图尔特·基利",
        "role": "判断真假",
        "oneliner": "用固定的批判性问题清单，把海绵式思维升级为淘金式思维",
        "ask_object": "别人的主张／论证",
        "ask_purpose": "判断它值不值得信",
        "color": "#ea580c",
    },
]

SECTIONS = ["R", "I", "A1", "A2", "E", "B"]

# 重要度与中文名（来自 capability-index.md）
META = {
    "coaching-habit": {
        "awe-question": ("AWE 追问：还有什么吗", "critical"),
        "focus-question-for-you": ("焦点问题：对你而言真正的挑战是什么", "critical"),
        "strategic-question-yes-no": ("战略问题：说了「好」，对什么说了「不」", "high"),
        "advice-monster-interception": ("建议怪兽拦截", "high"),
        "lazy-question-how-can-i-help": ("懒惰问题：我可以如何帮助你", "medium"),
        "new-habit-formula": ("新习惯公式：把「知道但做不到」变成可执行替换", "high"),
        "kickstart-3p": ("开场问题与 3P 定位", "medium"),
        "learning-question-double-loop": ("学习问题与双回路收尾", "medium"),
    },
    "questions-are-the-answer": {
        "question-burst": ("问题风暴：4 分钟只问不答", "critical"),
        "reframe-the-question": ("问题重构：换一把钥匙", "critical"),
        "catalytic-question-recipes": ("催化性问题配方", "high"),
        "manufacture-discomfort": ("主动制造不适：改变输入而不是更用力地想", "medium"),
        "broadcast-to-receive": ("广播模式 → 接收模式", "medium"),
        "make-errors-visible": ("让错误可见", "medium"),
    },
    "asking-the-right-questions": {
        "critical-questions-checklist": ("十大批判性问题清单", "critical"),
        "surface-hidden-assumptions": ("挖出未说出口的假设", "critical"),
        "alternative-causes": ("替代原因与竞争性假说", "high"),
        "argument-triple": ("论证三件套拆解", "high"),
        "evidence-and-data-check": ("证据效力与数据欺骗性", "medium"),
        "gray-thinking-conditional": ("灰度思维：条件化结论", "medium"),
    },
}


def parse_card(path):
    text = open(path, encoding="utf-8").read()
    lines = text.split("\n")
    secs = {}
    cur = None
    buf = []
    for ln in lines:
        m = re.match(r"^## ([RIA][0-9]?|B|E)\s*[—\-–]\s*(.*)$", ln)
        if m:
            if cur:
                secs[cur] = "\n".join(buf).strip()
            cur = m.group(1)
            buf = []
        else:
            if cur:
                buf.append(ln)
    if cur:
        secs[cur] = "\n".join(buf).strip()
    return secs


def clean_md(s):
    """转成轻量 HTML 友好的文本：保留段落、列表、引用、粗体。"""
    if not s:
        return []
    out = []
    para = []
    for ln in s.split("\n"):
        t = ln.rstrip()
        if not t.strip():
            if para:
                out.append({"t": "p", "v": " ".join(para)})
                para = []
            continue
        if t.lstrip().startswith(">"):
            if para:
                out.append({"t": "p", "v": " ".join(para)})
                para = []
            out.append({"t": "q", "v": t.lstrip("> ").strip()})
            continue
        m = re.match(r"^(\s*)(\d+)\.\s+(.*)$", t)
        if m:
            if para:
                out.append({"t": "p", "v": " ".join(para)})
                para = []
            out.append({"t": "li", "v": m.group(3).strip()})
            continue
        m = re.match(r"^(\s*)[-*]\s+(.*)$", t)
        if m:
            if para:
                out.append({"t": "p", "v": " ".join(para)})
                para = []
            out.append({"t": "ul", "v": m.group(2).strip()})
            continue
        para.append(t.strip())
    if para:
        out.append({"t": "p", "v": " ".join(para)})
    return out


def first_sentences(s, n=2):
    """取前 n 句作为摘要。只剥离 markdown 标记符号，保留数字/标点/比较符。"""
    if not s:
        return ""
    t = re.sub(r"[#*`>]", "", s)          # 仅去掉 md 标记
    t = re.sub(r"\s+", " ", t).strip()
    t = re.sub(r"^\d+[\.、]\s*", "", t)    # 去掉可能的列表编号
    parts = re.split(r"(?<=[。！？])", t)
    parts = [p.strip() for p in parts
             if len(p.strip()) > 4 and not re.match(r"^(\d+[\.、]|[-*])\s*", p.strip())]
    return "".join(parts[:n])


def extract_signals(a2):
    """从 A2 段抽取『什么时候用』的条目作为触发信号。"""
    if not a2:
        return []
    items = []
    grab = False
    for ln in a2.split("\n"):
        t = ln.strip()
        if "什么时候用" in t:
            grab = True
            continue
        if t.startswith("**") and grab and "什么时候" not in t:
            grab = False
        if grab:
            m = re.match(r"^\d+\.\s+(.*)$", t)
            if m:
                items.append(m.group(1).strip())
    return items


def extract_steps(e):
    """从 E 段抽取编号步骤。"""
    if not e:
        return []
    out = []
    for ln in e.split("\n"):
        m = re.match(r"^\s*(\d+)\.\s+(.*)$", ln.strip())
        if m:
            out.append(m.group(2).strip())
    return out


def main():
    kb = {"books": [], "cards": []}
    for b in BOOKS:
        meta = META[b["slug"]]
        cards = []
        for cid, (cname, imp) in meta.items():
            p = os.path.join(SKILLS, b["slug"], "references", "capabilities", cid + ".md")
            secs = parse_card(p)
            a2 = secs.get("A2", "")
            e = secs.get("E", "")
            cards.append({
                "id": cid,
                "book": b["slug"],
                "name": cname,
                "importance": imp,
                "summary": first_sentences(secs.get("I", ""), 2),
                "signals": extract_signals(a2),
                "steps": extract_steps(e),
                "sections": {k: clean_md(secs.get(k, "")) for k in SECTIONS},
            })
        order = list(meta.keys())
        cards.sort(key=lambda c: order.index(c["id"]))
        b = dict(b)
        b["cards"] = cards
        kb["books"].append(b)
        kb["cards"].extend(cards)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(kb, f, ensure_ascii=False, indent=1)

    for b in kb["books"]:
        print(b["title"], len(b["cards"]), "张卡")
        for c in b["cards"]:
            print("   %-34s sig=%d steps=%d" % (c["id"], len(c["signals"]), len(c["steps"])))
    print("total cards:", len(kb["cards"]))


if __name__ == "__main__":
    main()
