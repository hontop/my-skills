# -*- coding: utf-8 -*-
"""把 knowledge.json 注入 template.html，产出单文件 index.html（离线可用）。"""
import json
import os

BASE = r"C:/Users/hontop1/WorkBuddy/2026-10-17-23-30-17/knowledge-base"

kb = json.load(open(os.path.join(BASE, "knowledge.json"), encoding="utf-8"))
tpl = open(os.path.join(BASE, "template.html"), encoding="utf-8").read()

data = json.dumps(kb, ensure_ascii=False, separators=(",", ":"))
# 防止 </script> 提前闭合
data = data.replace("</", "<\\/")

out = tpl.replace("__KB_DATA__", data)
p = os.path.join(BASE, "index.html")
with open(p, "w", encoding="utf-8") as f:
    f.write(out)

print("written:", p, os.path.getsize(p), "bytes")
print("cards:", len(kb["cards"]), "books:", len(kb["books"]))
