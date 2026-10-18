#!/usr/bin/env python3
"""校验知识单元列表，生成 knowledge-map.md 与 state.json。

用法:
  python distill.py --topic "课题名" --ku kus.json [--root study]
                    [--days-per-week 5] [--minutes 60] [--weeks 8]
                    [--intensity gentle]
"""
import argparse
import json
import os

VALID_TYPE = {"concept", "procedure", "case", "drill", "exposure"}
VALID_BLOOM = {"理解", "应用", "迁移"}


def load_ku(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        return data
    for key in ("kus", "knowledge_units", "units"):
        if key in data:
            return data[key]
    raise SystemExit("无法在 JSON 中找到 KU 列表（支持顶层数组或 kus 字段）")


def normalize(kus):
    out = []
    for i, k in enumerate(kus, 1):
        k = dict(k)
        k["id"] = k.get("id") or "KU-%03d" % i
        k["title"] = k.get("title", "未命名")
        k["source"] = k.get("source", "")
        k["type"] = k.get("type", "concept")
        k["bloom"] = k.get("bloom", "理解")
        k["minutes"] = int(k.get("minutes", 30))
        k["difficulty"] = float(k.get("difficulty", 1.0))
        k["prereqs"] = list(k.get("prereqs") or [])
        k["evidence"] = k.get("evidence", "")
        k["mastery"] = int(k.get("mastery", 0))
        k["interval_idx"] = int(k.get("interval_idx", 0))
        k["review_due"] = k.get("review_due")
        k["attempts"] = list(k.get("attempts") or [])
        k["status"] = k.get("status", "pending")
        out.append(k)
    return out


def validate(kus):
    problems = []
    seen = set()
    ids = {k["id"] for k in kus}
    for k in kus:
        if k["id"] in seen:
            problems.append("重复 id: %s" % k["id"])
        seen.add(k["id"])
        exposure = k["type"] == "exposure"
        if not exposure and not k["evidence"]:
            problems.append("%s 缺少 evidence（无验收产出，应改为 exposure 或补写）" % k["id"])
        if k["type"] not in VALID_TYPE:
            problems.append("%s type 非法: %s（应为 %s）" % (k["id"], k["type"], "/".join(sorted(VALID_TYPE))))
        if not exposure and k["bloom"] not in VALID_BLOOM:
            problems.append("%s bloom 非法: %s（应为 理解/应用/迁移）" % (k["id"], k["bloom"]))
        if not exposure and not (10 <= k["minutes"] <= 60):
            problems.append("%s minutes=%s 越界（应 10-60，超出需再切，不足需合并）" % (k["id"], k["minutes"]))
        if k["difficulty"] not in (1.0, 1.3, 1.6):
            problems.append("%s difficulty=%s 非标准值（应为 1.0/1.3/1.6）" % (k["id"], k["difficulty"]))
        for p in k["prereqs"]:
            if p not in ids:
                problems.append("%s 的前置 %s 不存在" % (k["id"], p))
    return problems


def topo_layers(kus):
    ids = [k["id"] for k in kus]
    idset = set(ids)
    prereq = {k["id"]: [p for p in k["prereqs"] if p in idset] for k in kus}
    layers = []
    remaining = set(ids)
    cyclic = False
    while remaining:
        ready = sorted(i for i in remaining if all(p not in remaining for p in prereq[i]))
        if not ready:
            cyclic = True
            ready = sorted(remaining)
            layers.append(ready)
            break
        layers.append(ready)
        remaining -= set(ready)
    return layers, cyclic


def total_minutes(kus):
    train = [k for k in kus if k["type"] != "exposure"]
    return int(sum(k["minutes"] * k["difficulty"] for k in train) * 1.15)


def render_map(topic, kus, layers):
    by_id = {k["id"]: k for k in kus}
    exposure = [k for k in kus if k["type"] == "exposure"]
    train = [k for k in kus if k["type"] != "exposure"]
    lines = [
        "# 知识单元图谱 · %s" % topic,
        "",
        "> 共 %d 个 KU，其中训练类 %d 个，通读类（exposure）%d 个。" % (len(kus), len(train), len(exposure)),
        "> 依赖层级 %d 层。" % len(layers),
        "",
    ]
    for n, layer in enumerate(layers, 1):
        lines.append("## 第 %d 层%s" % (n, "（无前置）" if n == 1 else ""))
        lines.append("")
        lines.append("| ID | 标题 | 前置 | 来源 | 类型 | 层次 | 分钟 | 难度 | 验收产出（evidence） |")
        lines.append("|---|---|---|---|---|---|---|---|---|")
        for kid in layer:
            k = by_id[kid]
            pre = ", ".join(k["prereqs"]) or "—"
            ev = k["evidence"] or "（通读）"
            lines.append("| %s | %s | %s | %s | %s | %s | %d | %.1f | %s |"
                         % (kid, k["title"], pre, k["source"] or "—", k["type"],
                            k["bloom"] if k["type"] != "exposure" else "—",
                            k["minutes"], k["difficulty"], ev))
        lines.append("")
    if exposure:
        lines.append("## 通读类（不训练，不计掌握度）")
        lines.append("")
        lines.append("| ID | 内容 | 来源 | 分钟 |")
        lines.append("|---|---|---|---|")
        for k in exposure:
            lines.append("| %s | %s | %s | %d |" % (k["id"], k["title"], k["source"] or "—", k["minutes"]))
        lines.append("")
    lines.append("## 统计")
    lines.append("")
    lines.append("- 总耗时（含 15%% 理解损耗）：%d 分钟" % total_minutes(kus))
    lines.append("- 训练类 KU：%d 个" % len(train))
    lines.append("")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--topic", required=True)
    ap.add_argument("--root", default="study")
    ap.add_argument("--ku", required=True)
    ap.add_argument("--days-per-week", type=int, default=5)
    ap.add_argument("--minutes", type=int, default=60)
    ap.add_argument("--weeks", type=int, default=8)
    ap.add_argument("--intensity", default="gentle", choices=["gentle", "standard", "hardcore"])
    args = ap.parse_args()

    kus = normalize(load_ku(args.ku))
    problems = validate(kus)
    layers, cyclic = topo_layers(kus)
    if cyclic:
        problems.append("检测到依赖环，环内 KU 已放在最后一层（需人工拆环：先整体跑通，再回补细节）")

    total = total_minutes(kus)
    new_days = max(args.days_per_week - 1, 1)
    capacity = args.weeks * new_days * args.minutes * 0.8
    ratio = total / capacity if capacity else 0

    d = os.path.join(args.root, args.topic)
    os.makedirs(os.path.join(d, "daily"), exist_ok=True)
    os.makedirs(os.path.join(d, "quizzes"), exist_ok=True)
    os.makedirs(os.path.join(d, "reviews"), exist_ok=True)

    with open(os.path.join(d, "knowledge-map.md"), "w", encoding="utf-8") as f:
        f.write(render_map(args.topic, kus, layers))

    state = {
        "topic": args.topic,
        "manifest": {
            "days_per_week": args.days_per_week,
            "daily_minutes": args.minutes,
            "weeks": args.weeks,
            "intensity": args.intensity,
            "total_minutes": total,
            "capacity_minutes": int(capacity),
            "ratio": round(ratio, 2),
        },
        "kus": kus,
        "layers": layers,
        "log": [],
        "schedule": {},
    }
    with open(os.path.join(d, "state.json"), "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

    print("输出目录: %s" % d)
    print("KU 总数: %d  训练类: %d  层级: %d" % (len(kus), len([k for k in kus if k["type"] != "exposure"]), len(layers)))
    print("总耗时 %d 分 / 可用容量 %d 分 = 比值 %.2f" % (total, int(capacity), ratio))
    if ratio > 1.2:
        print("[容量预警] 比值 >1.2，必须三选一：延长周期 / 缩减 KU 范围 / 降低验收标准")
    elif ratio <= 0.8:
        print("[容量宽裕] 可提高产出要求或缩短周期")
    else:
        print("[容量正常]")
    if problems:
        print("\n校验问题 %d 条：" % len(problems))
        for p in problems:
            print("  - %s" % p)
    else:
        print("校验通过，无问题")


if __name__ == "__main__":
    main()
