#!/usr/bin/env python3
"""按容量与依赖顺序排程，生成 plan.md 与每日任务卡。

用法:
  python schedule.py --topic "课题名" --start 2026-10-19 [--root study]
                     [--detail-weeks 4] [--cards 7]
"""
import argparse
import json
import os
from datetime import date, timedelta

WEEKDAY = ["一", "二", "三", "四", "五", "六", "日"]


def load(root, topic):
    p = os.path.join(root, topic, "state.json")
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f), p


def parse_date(s):
    y, m, d = (int(x) for x in s.split("-"))
    return date(y, m, d)


def label(it):
    return it["id"] + ("(%s)" % it["part"] if it["part"] else "")


def build_schedule(state, start):
    m = state["manifest"]
    n, dmin, weeks = m["days_per_week"], m["daily_minutes"], m["weeks"]
    cap = dmin * 0.8
    by_id = {k["id"]: k for k in state["kus"]}

    order = []
    for layer in state.get("layers", []):
        order.extend(layer)
    queue, seen = [], set()
    for i in order:
        k = by_id.get(i)
        if k and k["type"] != "exposure" and i not in seen:
            queue.append(i)
            seen.add(i)

    items = []
    for kid in queue:
        cost = by_id[kid]["minutes"] * by_id[kid]["difficulty"]
        if cost > cap:
            half = cost / 2.0
            items.append({"id": kid, "part": "上", "min": half})
            items.append({"id": kid, "part": "下", "min": half})
        else:
            items.append({"id": kid, "part": None, "min": cost})

    days = []
    qi = 0
    for w in range(weeks):
        for d in range(n):
            cur = start + timedelta(days=w * 7 + d)
            makeup = (d == n - 1)
            new, load = [], 0.0
            if not makeup:
                while qi < len(items) and len(new) < 3:
                    it = items[qi]
                    if load + it["min"] > cap and new:
                        break
                    new.append(it)
                    load += it["min"]
                    qi += 1
            days.append({
                "date": cur.isoformat(),
                "week": w + 1,
                "dow": WEEKDAY[cur.weekday()],
                "new": new,
                "review": [],
                "makeup": makeup,
                "minutes": int(load) if load else (int(cap * 0.5) if makeup else 0),
            })
    leftover = sorted({items[i]["id"] for i in range(qi, len(items))})
    exposure = [k["id"] for k in state["kus"] if k["type"] == "exposure"]
    return days, leftover, exposure


def render_plan(state, days, leftover, exposure, start, detail_weeks):
    m = state["manifest"]
    weeks = m["weeks"]
    lines = [
        "# 主计划 · %s" % state["topic"],
        "",
        "> 起：%s　周可用容量：%d 分钟　周期：%d 周"
        % (start.isoformat(), m["capacity_minutes"] // weeks, weeks),
        "> 缓冲 20%，每周最后一天为补账日（无新内容）。",
        "",
        "## 周表",
        "",
    ]
    for w in range(1, min(weeks, detail_weeks) + 1):
        wd = [x for x in days if x["week"] == w]
        if not any(x["new"] for x in wd):
            lines.append("### 第 %d 周（%s ~ %s）：新学已排完，进入复习与综合产出期"
                         % (w, wd[0]["date"][5:], wd[-1]["date"][5:]))
            lines.append("")
            continue
        lines.append("### 第 %d 周（%s ~ %s）" % (w, wd[0]["date"][5:], wd[-1]["date"][5:]))
        lines.append("")
        lines.append("| 日 | 日期 | 新学 | 复习 | 分钟 |")
        lines.append("|---|---|---|---|---|")
        for x in wd:
            new = "、".join(label(i) for i in x["new"]) or "—"
            lines.append("| %s | %s | %s | %s | %d |"
                         % (x["dow"], x["date"][5:], new, "—", x["minutes"]))
        lines.append("")
        done = [i for x in wd for i in x["new"]]
        lines.append("**本周里程碑**：完成至 %s" % (label(done[-1]) if done else "—"))
        lines.append("")
    if weeks > detail_weeks:
        lines.append("### 第 %d–%d 周（周模板，第 %d 周复盘后细化）"
                     % (detail_weeks + 1, weeks, detail_weeks))
        lines.append("")
        lines.append("- 每周新学：约 %.1f 个（按前 %d 周实测节奏推算）"
                     % (avg_new_per_week(days, detail_weeks), detail_weeks))
        lines.append("- 每周复习：按间隔序列到期清单执行")
        lines.append("- 补账日：每周第 %d 天" % m["days_per_week"])
        lines.append("")
    if leftover:
        lines.append("### 未排入（容量不足，需三选一处理）")
        lines.append("")
        lines.append("以下 KU 在目标周期内排不下：%s" % "、".join(leftover))
        lines.append("")
        lines.append("处理选项：① 延长周期　② 缩减范围（砍这些 KU）　③ 降低验收标准")
        lines.append("")
    if exposure:
        lines.append("### 通读类（安排在无新学空隙，不计掌握度）")
        lines.append("")
        lines.append("%s" % "、".join(exposure))
        lines.append("")
    lines.append("## 里程碑")
    lines.append("")
    lines.append("| 周 | 里程碑 | 验收物 |")
    lines.append("|---|---|---|")
    lines.append("| %d | 完成第 %d 周全部 KU | 1 份 evidence |" % (detail_weeks, detail_weeks))
    lines.append("| %d | 结课 | 综合产出 + 全部核心 KU ≥L3 |" % weeks)
    lines.append("")
    lines.append("## 熔断预案")
    lines.append("")
    lines.append("触发：完成率 <60% 连续 2 周")
    lines.append("最低配：每日 15 分钟，只保留前 2 条 KU 主线，其余冻结。")
    lines.append("")
    return "\n".join(lines)


def avg_new_per_week(days, detail_weeks):
    wd = [x for x in days if x["week"] <= detail_weeks]
    n = len(set(x["week"] for x in wd)) or 1
    return sum(len(x["new"]) for x in wd) / n


def render_card(state, day):
    by_id = {k["id"]: k for k in state["kus"]}
    ids = [i["id"] for i in day["new"]]
    total = sum(int(i["min"]) for i in day["new"])
    lines = [
        "# %s · 第 %d 周 · 周%s" % (day["date"], day["week"], day["dow"]),
        "",
        "**今日目标**：%s" % ("、".join(label(i) for i in day["new"])
                              if day["new"] else "补账日 —— 只做复习与补欠，无新内容"),
        "",
        "---",
        "",
    ]
    if day["new"]:
        lines.append("## 学（%d 分钟）" % total)
        lines.append("")
        lines.append("| KU | 内容 | 教材定位 | 分钟 |")
        lines.append("|---|---|---|---|")
        for i in day["new"]:
            k = by_id[i["id"]]
            lines.append("| %s | %s | %s | %d |"
                         % (label(i), k["title"], k["source"] or "—", int(i["min"])))
        lines.append("")
        lines.append("## 练（产出 evidence）")
        lines.append("")
        for n_, i in enumerate(day["new"], 1):
            k = by_id[i["id"]]
            lines.append("%d. **%s** → 交付物：%s"
                         % (n_, label(i), k["evidence"] or "（补充 evidence）"))
            lines.append("   - 要求：不看提示独立完成")
        lines.append("")
        lines.append("## 测（3–5 题）")
        lines.append("")
        lines.append("1. {理解层题：闭卷复述要点}")
        lines.append("2. {应用层题：给场景做出来}")
        lines.append("3. {迁移层题：换条件怎么做}")
        lines.append("")
    else:
        lines.append("## 补账")
        lines.append("")
        lines.append("- 复习本周到期未做的 KU")
        lines.append("- 重做本周自测 <80% 的题")
        lines.append("")
    lines.append("## 复习到期")
    lines.append("")
    due = [k for k in state["kus"] if k.get("review_due") and k["review_due"] <= day["date"]]
    if due:
        lines.append("| KU | 间隔档 | 上次自测 |")
        lines.append("|---|---|---|")
        for k in due:
            last = k["attempts"][-1][1] if k["attempts"] else "—"
            lines.append("| %s | 第 %d 档 | %s%% |" % (k["id"], k["interval_idx"] + 1, last))
    else:
        lines.append("（暂无到期复习，新学的 KU 将在次日进入间隔序列）")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 完成记录")
    lines.append("")
    lines.append("- 实际用时：{ } 分钟")
    lines.append("- 产出：{有 / 无}")
    lines.append("- 自测：{ } %")
    lines.append("- 卡点：{ }")
    lines.append("")
    lines.append("## 教练反馈")
    lines.append("")
    lines.append("- 数据：{ }")
    lines.append("- 正反馈：{ }")
    lines.append("- 下一步：{ }")
    lines.append("")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--topic", required=True)
    ap.add_argument("--root", default="study")
    ap.add_argument("--start", required=True, help="开始日期 YYYY-MM-DD")
    ap.add_argument("--detail-weeks", type=int, default=4, help="细排到日历的周数，其余用周模板")
    ap.add_argument("--cards", type=int, default=7, help="生成前几天任务卡文件")
    args = ap.parse_args()

    state, path = load(args.root, args.topic)
    start = parse_date(args.start)
    days, leftover, exposure = build_schedule(state, start)

    d = os.path.join(args.root, args.topic)
    with open(os.path.join(d, "plan.md"), "w", encoding="utf-8") as f:
        f.write(render_plan(state, days, leftover, exposure, start, args.detail_weeks))

    for day in days[:args.cards]:
        fn = os.path.join(d, "daily", "%s.md" % day["date"])
        with open(fn, "w", encoding="utf-8") as f:
            f.write(render_card(state, day))

    state["schedule"] = {"start": start.isoformat(), "days": days, "leftover": leftover}
    state["manifest"]["start"] = start.isoformat()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

    total = state["manifest"]["total_minutes"]
    cap = state["manifest"]["capacity_minutes"]
    print("plan.md 已生成：%d 周，%d 个学习日" % (state["manifest"]["weeks"], len(days)))
    print("总耗时 %d 分 / 可用容量 %d 分 = 比值 %.2f" % (total, cap, total / cap if cap else 0))
    print("已生成任务卡：%s ~ %s" % (days[0]["date"], days[min(args.cards, len(days)) - 1]["date"]))
    if leftover:
        print("[容量预警] %d 个 KU 未排入：%s" % (len(leftover), "、".join(leftover)))
        print("           必须三选一：延长周期 / 缩减范围 / 降低验收标准")


if __name__ == "__main__":
    main()
