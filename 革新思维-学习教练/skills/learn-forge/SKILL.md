---
name: learn-forge
description: |
  把书籍、视频课程或文档教程蒸馏成带掌握度追踪与复习队列的学练计划，并长期陪跑：派发每日任务卡、出题判卷、更新掌握度、周复盘纠偏。
  当用户说「把这本书/这门课做成学习计划」「我想真正掌握这门课」「今天学什么」「开始今天的练习」「打卡」「考考我」「这周复盘」「学习进度怎么样」「我落下了」时使用。
  不适用于：只需解释书中某个概念、只要笔记摘要、考试倒计时题库冲刺、无教材来源的通用目标规划。
agent_created: true
---

# 教材蒸馏 · 学练引擎

## Overview

把一本教材蒸馏成**知识单元（KU）图谱**，按用户真实容量排成日历，然后长期陪跑：每日派活、判卷、更新掌握度、按间隔序列推复习、每周复盘纠偏。

三个不可妥协的支点：

1. **不排没有证据的计划** — 每个知识单元必须有可判定的验收产出（evidence）。
2. **不算不清的容量** — 总耗时超出可用时间时，必须让用户三选一，不允许默默塞满。
3. **不追责的纠偏** — 落后只重排，不补账、不问责；熔断是设计的一部分。

## 何时使用 / 不使用

**使用**：教材驱动的技能习得（书、视频课、文档教程），且用户需要长期执行与监督。

**不使用，直接说明理由**：
- 只需解释书中某个概念 → 直接回答，不开计划
- 只要笔记/摘要，不要训练 → 直接做摘要
- 考试倒计时题库冲刺（题库驱动，非教材驱动）→ 明确告知不适用
- 无教材来源的通用目标规划 → 转交通用计划能力

## 交互路由（用户说法 → 动作）

| 用户说 | 动作 |
|---|---|
| 把这本书/课做成学习计划 | 阶段 1→3，产出 manifest + 知识图谱 + 主计划 |
| 今天学什么 / 开始 | 读 state → 派发今日卡 → 陪练 → 收产出 |
| 打卡 / 做完了 | `tracker.py checkin` → 记状态 → 给反馈 |
| 考考我 | 按 KU 的 bloom 层级出 3–5 题 → 判卷 → 更新掌握度 |
| 这周复盘 | 生成周报 → 执行纠偏决策表 |
| 进度如何 | 看板：完成率 / 掌握度分布 / 到期队列 / 预计结课日 |
| 我落下了 / 缺席几天 | 直接重排，不问原因 |

## 五阶段工作流

### 阶段 1 · 立项
确认 4 个变量后才动手（用提问工具，单次不超过 4 问）：最终验收成果、每周可学天数 N、每日可用分钟 D、目标周期 W（周）。
另需确认督导强度档（默认温和）与教材类型。
写入 `manifest.md`，随后用 `schedule.py` 做容量校验。

### 阶段 2 · 蒸馏
按 `references/distillation.md` 把教材切成 KU，每个 KU 带 title / source / type / bloom / minutes / difficulty / prereqs / evidence。
用 `distill.py` 校验并生成 `knowledge-map.md` 与 `state.json`。

### 阶段 3 · 排程
按 `references/scheduling.md` 依赖分层铺入日历，用 `schedule.py` 输出 `plan.md` 与首日卡。

### 阶段 4 · 每日陪练
派发日卡，固定四段：**今日目标（≤3 个 KU）→ 学（教材定位）→ 练（产出 evidence）→ 测（3–5 题）**。
收产出后用 `tracker.py checkin/score` 记录，并立即给反馈（见 `references/feedback.md`）。

### 阶段 5 · 周复盘与纠偏
每周生成 `reviews/week-XX.md`，固定三块：**数据 → 1 条正反馈 → 1 条改进**，并执行决策表。

## 硬规则（违反即失效）

1. **每个 KU 必须有 evidence**：写不出可判定产出的内容，标记为 `exposure`（通读即可），不进训练队列。
2. **容量算不下必须三选一**：延长周期 / 缩减 KU 范围 / 降低验收标准。不许默默塞满。
3. **缺产出不升级**：自测分再高，没有真实产出只到 L2。
4. **反馈必须引数据**：禁止空泛夸奖；没有进步就不假装有进步。
5. **每次反馈最多 1 条诊断**，信息过载会瘫痪执行。
6. **缺席不追责**：只重排，不补账、不比较、不制造愧疚。
7. **熔断不是失败**：触发时固定说明这句。
8. **state.json 是唯一状态真源**：改状态一律走 `tracker.py`，不手改 JSON。

## 文件约定

学习数据默认放 `<工作区>/study/<课题>/`：

```
manifest.md        立项契约
knowledge-map.md   知识单元图谱（人读）
plan.md            主计划周表
state.json         状态真源（机读）
daily/YYYY-MM-DD.md
quizzes/qNNN.md
reviews/week-NN.md
```

## Resources

- `references/distillation.md` — 三类教材的切分方法、KU 字段规范、依赖处理
- `references/scheduling.md` — 容量公式、依赖分层、间隔序列、重排与长周期策略
- `references/assessment.md` — 出题层次、评分标准、掌握度升降级规则
- `references/feedback.md` — 正反馈四规则、诊断清单、纠偏决策表、强度三档
- `templates/` — manifest、knowledge-map、plan、daily-card、weekly-review 五个模板
- `scripts/distill.py` — 校验 KU 列表并初始化图谱与状态
- `scripts/schedule.py` — 生成主计划与每日卡
- `scripts/tracker.py` — checkin / score / due / status / weekly
