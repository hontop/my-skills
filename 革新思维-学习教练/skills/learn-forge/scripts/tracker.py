#!/usr/bin/env python3
"""学练状态追踪：打卡、判分、到期复习、看板、周报数据。

用法:
  python tracker.py checkin --topic T --date 2026-10-19 --kus KU-001,KU-002 --minutes 55
  python tracker.py score   --topic T --ku KU-001 --pct 85 [--produce] [--varied] [--taught] [--date ...]
  python tracker.py due     --topic T [--date ...]
  python tracker.py status  --topic T
  python tracker.py weekly  --topic T [--week 1]
"""
import argparse
import json
import os
from datetime import date, timedelta

INTERVALS = [1, 3, 7, 16, 35, 90]
MASTERY_NAME = ["L0 未接触", "L1 认得", "L2 复述", "L3 照做", "L4 变通", "L5 迁移"]


def paths(root, topic):
    d = os.path.join(root, topic)
    return d, os.path.join(d, "state.json")


def load(root, topic):
    _, p = paths(root, topic)
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f), p


def save(state, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def parse_date(s):
    if not s:
        return date.today()
    y, m, d = (int(x) for x in s.split("-"))
    return date(y, m, d)


def find(state, kid):
    for k in state["kus"]:
        if k["id"] == kid:
            return k
    return None


def cmd_checkin(a):
    state, path = load(a.root, a.topic)
    day = a.date or date.today().isoformat()
    kids = [x.strip() for x in a.kus.split(",") if x.strip()]
    for kid in kids:
        k = find(state, kid)
        if not k:
            print("[警告] 未找到 %s，已跳过" % kid)
            continue
        k["status"] = "learning"
    state["log"].append({"date": day, "kus": kids, "minutes": a.minutes, "note": a.note})
    save(state, path)
    print("打卡 %s：%s，%d 分钟" % (day, ", ".join(kids) or "（无 KU）", a.minutes))
    print("累计打卡 %d 次" % len(state["log"]))


def cmd_score(a):
    state, path = load(a.root, a.topic)
    k = find(state, a.ku)
    if not k:
        raise SystemExit("未找到 KU：%s" % a.ku)
    day = a.date or date.today().isoformat()
    old = k["mastery"]
    k["attempts"].append([day, a.pct])

    if a.pct >= 80:
        if k["mastery"] == 0:
            k["mastery"] = 1
        elif k["mastery"] == 1:
            k["mastery"] = 2
        elif k["mastery"] == 2 and (a.produce or a.varied or a.taught):
            k["mastery"] = 3
        elif k["mastery"] == 3 and (a.varied or a.taught):
            k["mastery"] = 4
        elif k["mastery"] == 4 and a.taught:
            k["mastery"] = 5
        k["interval_idx"] = min(k["interval_idx"] + 1, len(INTERVALS) - 1)
        if k["mastery"] >= 3:
            k["status"] = "done"
    elif a.pct < 60:
        k["mastery"] = max(k["mastery"] - 1, 0)
        k["interval_idx"] = max(k["interval_idx"] - 1, 0)
    d = parse_date(day)
    k["review_due"] = (d + timedelta(days=INTERVALS[k["interval_idx"]])).isoformat()
    save(state, path)

    print("%s 自测 %d%%：%s → %s" % (a.ku, a.pct, MASTERY_NAME[old], MASTERY_NAME[k["mastery"]]))
    print("下次复习：%s（第 %d 档，间隔 %d 天）" % (k["review_due"], k["interval_idx"] + 1, INTERVALS[k["interval_idx"]]))
    if a.pct >= 80 and not (a.produce or a.varied or a.taught) and k["mastery"] == 2:
        print("[卡在 L2] 分数够了，但没有产出 evidence。交出实际产物才能升到 L3。")
    if a.pct < 60:
        print("[降级] 间隔档回退，下次复习提前。")


def cmd_due(a):
    state, _ = load(a.root, a.topic)
    today = parse_date(a.date).isoformat()
    due = [k for k in state["kus"] if k.get("review_due") and k["review_due"] <= today]
    if not due:
        print("今日无到期复习")
        return
    print("到期复习 %d 个（截至 %s）：" % (len(due), today))
    for k in sorted(due, key=lambda x: x["review_due"]):
        last = k["attempts"][-1][1] if k["attempts"] else "—"
        print("  %s  %s  当前 %s  上次 %s%%  到期 %s" % (k["id"], k["title"], MASTERY_NAME[k["mastery"]], last, k["review_due"]))


def cmd_status(a):
    state, _ = load(a.root, a.topic)
    train = [k for k in state["kus"] if k["type"] != "exposure"]
    dist = [0] * 6
    for k in train:
        dist[k["mastery"]] += 1
    today = date.today()
    overdue = [k for k in train if k.get("review_due") and k["review_due"] < today.isoformat()]
    done = [k for k in train if k["mastery"] >= 3]
    logs = state["log"]
    sch = state.get("schedule", {}).get("days", [])
    planned = [d for d in sch if d["date"] <= today.isoformat()]
    rate = (len(logs) / len(planned) * 100) if planned else 0.0

    print("课题：%s" % state["topic"])
    print("进度：%d/%d 个 KU 达到 L3+（%.0f%%）" % (len(done), len(train), len(done) / len(train) * 100 if train else 0))
    print("掌握度分布：" + "  ".join("L%d:%d" % (i, dist[i]) for i in range(6)))
    print("打卡：%d 次　计划日：%d　完成率：%.0f%%" % (len(logs), len(planned), rate))
    print("逾期未复习：%d 个" % len(overdue))
    for k in overdue[:5]:
        print("  - %s %s（应于 %s 复习）" % (k["id"], k["title"], k["review_due"]))
    if state["schedule"].get("leftover"):
        print("未排入计划：%s" % ", ".join(state["schedule"]["leftover"]))
    if rate < 60 and len(planned) >= 7:
        print("[纠偏提示] 完成率 <60%%，若连续 2 周则触发熔断：每日 15 分钟，只留 2 条主线。")
    elif rate >= 90 and len(planned) >= 14:
        print("[纠偏提示] 完成率 ≥90%% 连续 2 周，可上调容量 15%% 或提前结课。")


def cmd_weekly(a):
    state, _ = load(a.root, a.topic)
    logs = state["log"]
    if not logs:
        print("本周无记录。先做最小一步：今天 15 分钟，只做 1 个 KU 的复述。")
        return
    week = a.week
    sch = state.get("schedule", {}).get("days", [])
    if week and sch:
        wd = [d for d in sch if d["week"] == week]
        planned = len(wd) or 1
        wl = [l for l in logs if any(d["date"] == l["date"] and d["week"] == week for d in wd)]
    else:
        planned = 7
        wl = logs[-7:]
    dist = [0] * 6
    for k in state["kus"]:
        if k["type"] != "exposure":
            dist[k["mastery"]] += 1
    today = date.today().isoformat()
    overdue = [k for k in state["kus"] if k.get("review_due") and k["review_due"] < today]
    print("第 %s 周复盘 · %s" % (week or "近 7 日", state["topic"]))
    print("打卡：%d/%d　完成率：%.0f%%" % (len(wl), planned, len(wl) / planned * 100))
    print("掌握度分布：" + "  ".join("L%d:%d" % (i, dist[i]) for i in range(6)))
    print("逾期未复习：%d 个" % len(overdue))
    print("建议：改进只写 1 条，具体到改哪个参数（容量/粒度/练习形式/时间/强度档）")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("checkin")
    p.add_argument("--topic", required=True)
    p.add_argument("--root", default="study")
    p.add_argument("--date")
    p.add_argument("--kus", default="")
    p.add_argument("--minutes", type=int, default=0)
    p.add_argument("--note", default="")
    p.set_defaults(fn=cmd_checkin)

    p = sub.add_parser("score")
    p.add_argument("--topic", required=True)
    p.add_argument("--root", default="study")
    p.add_argument("--ku", required=True)
    p.add_argument("--pct", type=int, required=True)
    p.add_argument("--date")
    p.add_argument("--produce", action="store_true", help="已交出 evidence 实际产物")
    p.add_argument("--varied", action="store_true", help="变条件题做对")
    p.add_argument("--taught", action="store_true", help="已讲给他人或迁移到新领域")
    p.set_defaults(fn=cmd_score)

    p = sub.add_parser("due")
    p.add_argument("--topic", required=True)
    p.add_argument("--root", default="study")
    p.add_argument("--date")
    p.set_defaults(fn=cmd_due)

    p = sub.add_parser("status")
    p.add_argument("--topic", required=True)
    p.add_argument("--root", default="study")
    p.set_defaults(fn=cmd_status)

    p = sub.add_parser("weekly")
    p.add_argument("--topic", required=True)
    p.add_argument("--root", default="study")
    p.add_argument("--week", type=int)
    p.set_defaults(fn=cmd_weekly)

    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
