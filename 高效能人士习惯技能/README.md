# 高效能人士习惯技能（柯维核心四部曲）

从史蒂芬·柯维（Stephen R. Covey）四部方法论著作蒸馏而成的 Agent Skill 组，场景已适配**中国高校学生自主学习**。

## 来源书目

| 代号 | 书名 | 年份 | 在体系中的角色 |
|---|---|---|---|
| S1 | 高效能人士的七个习惯 | 1989 | 主干：依赖 → 独立 → 互赖的成熟模型 |
| S2 | 要事第一 | 1994 | 习惯三的展开：从时钟到罗盘 |
| S3 | 第八个习惯 | 2004 | 从效能到卓越：心声与全人思维 |
| S4 | 第3选择 | 2011 | 统合综效的操作化：不妥协的共同创造 |

## 目录结构

采用 **compact pack** 形态：1 个来源路由入口 + 7 个可独立发现的晋级 Skill，共 8 个可发现入口（入口预算 8，用满）。

```
高效能人士习惯技能/
├── README.md                    # 本文件
├── DIGEST.md                    # 精华长文（约 1 万字，按书骨架组织）
├── PIPELINE_STATE.md            # 蒸馏流水线全记录与质量门结果
├── capability-destinations.json # 发布审计清单
├── covey-habits/                # ★ 来源路由入口（内含全部 16 张能力卡）
│   ├── SKILL.md
│   └── references/
│       ├── overview.md          # 整书理解
│       ├── glossary.md          # 术语表
│       ├── cheatsheet.md        # 决策规则速查
│       ├── capability-index.md  # 完整意图/关键词索引
│       └── capabilities/*.md    # 16 张 RIA++ 能力卡
├── covey-circle-of-influence/   # 影响圈切分与三类问题归因
├── covey-paradigm-shift/        # 范式定位与换镜检查表
├── covey-find-your-voice/       # 心声四要素交汇定位
├── covey-empathic-listening/    # 移情倾听 / 诊断先于开方
├── covey-emotional-bank-account/ # 情感账户六种存款
├── covey-third-alternative/     # 第3选择四步协同
└── covey-weekly-first-things/   # 第二象限周计划四步骤
```

## 8 个入口的分工

| 入口 | 解决什么问题 | 单元 |
|---|---|---|
| `covey-habits` | 路由：拿到任何柯维域的问题先读它 | — |
| `covey-circle-of-influence` | 焦虑很大但动不了，先分清「归谁管」 | f01 |
| `covey-paradigm-shift` | 在同一套错误假定里反复加码 | f03 |
| `covey-find-your-voice` | 卡在「往哪投入」而不是「怎么执行」 | f08 |
| `covey-empathic-listening` | 开口就吵、安慰越说越糟、说服失败 | p06 |
| `covey-emotional-bank-account` | 关系长期余额为零或透支 | p05 |
| `covey-third-alternative` | 两个方案僵住，不想加权平均 | p07 |
| `covey-weekly-first-things` | 要的是「排哪天、排几小时」 | p02 |

另有 9 张能力卡仅经路由入口可达：P/PC 平衡、选择回路、时钟罗盘、双赢审计、GET 陷阱、不断更新、自我授权七级、个人使命宣言、说不。

## 安装

各目录都是标准的 Agent Skill（`SKILL.md` + `references/`），复制到宿主 skills 目录即可：

```bash
# 用户级（所有项目可用）
cp -r 高效能人士习惯技能/covey-* ~/.workbuddy/skills/

# 或只装单个入口
cp -r 高效能人士习惯技能/covey-weekly-first-things ~/.workbuddy/skills/
```

**不要同时装 single 与 pack 两套**——两套 description 会重复覆盖意图。本仓库是 pack。

## 质量门（不是书摘，是蒸馏）

| 阶段 | 结果 |
|---|---|
| 三重验证（V1 跨域 / V2 预测力 / V3 独特性） | 20 候选通过 16，淘汰 3，合并 1 |
| 引文核验 | 抽查 10/10 命中原文语料，零编造 |
| 晋级门（5 判据） | 7 promoted / 9 router，入口数 8 = 预算 8 |
| 压力测试 | 29 用例独立盲测，7×F1 = 1.000，同包混淆率 0 |

**刻意保留的批判**：每张能力卡的 B 段都写了作者的时代局限——权力不对等场景中「无交易」只对强势方开放（导师—学生尤其致命）、真正的零和场景（唯一保研名额）里双赢不可得、个人主义归因低估结构性约束、证据是轶事性的。详见 `DIGEST.md` 第七节。

## 蒸馏工具

[cangjie-skill](https://github.com/) v2.5.0 六阶段流水线（整书理解 → 并行提取 → 三重验证 → 晋级门 → RIA++ 能力卡 → Zettelkasten 链接 → 压力测试 → 编译交付）。中间产物见 `PIPELINE_STATE.md`。
