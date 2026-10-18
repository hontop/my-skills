# 流水线状态 — 柯维核心四部曲

**来源**：S1《高效能人士的七个习惯》(1989) / S2《要事第一》(1994) / S3《第八个习惯》(2004) / S4《第3选择》(2011)
**蒸馏模式**：pack（1 个来源路由入口 + 7 个晋级 Skill）
**场景适配**：中国高校学生自主学习
**工具版本**：cangjie-tools v2.5.0
**完成时间**：2026-10-18

## 阶段进度

| 阶段 | 内容 | 状态 | 产物 |
|---|---|---|---|
| 0 | 整书理解（Adler） | ✅ | `BOOK_OVERVIEW.md` |
| — | 语料固化 | ✅ | `SOURCES.md`（原文摘录 + 20+ 书中案例） |
| 1 | 5 提取器并行 | ✅ | `candidates/{frameworks,principles,cases,counter-examples,glossary}.md` |
| 1.5 | 三重验证 | ✅ | `verified.md`（16 通过）/ `rejected/{p04,p08,p09}.md`（3 淘汰） |
| 1.6 | 晋级门 | ✅ | 7 promoted / 9 router，入口数 8 = 预算 8 |
| 2 | RIA++ 能力卡 | ✅ | `.cangjie/capabilities/cards/*.md`（16 张） |
| 3 | Zettelkasten 链接 | ✅ | `verified.yaml`（20 条关系）/ `LINKS.md` / `GLOSSARY.md` |
| 4 | 压力测试 | ✅ | `evals/trigger/`（29 用例盲测，7×F1=1.000，混淆率 0） |
| 5 | 编译 + DIGEST + 安装 | ✅ | `output/`（8 入口）/ `DIGEST.md`（9,967 字）/ 已安装到 `~/.workbuddy/skills/` |

## 产物清单

### 可发现入口（8 个，已安装到 `C:/Users/hontop1/.workbuddy/skills/`）

| 入口 | 类型 | 单元 | 重要度 |
|---|---|---|---|
| `covey-habits` | 来源路由入口 | —（含 16 张能力卡 + 术语表 + 速查） | — |
| `covey-circle-of-influence` | 晋级 Skill | f01 影响圈切分与三类问题归因 | critical |
| `covey-paradigm-shift` | 晋级 Skill | f03 范式定位与换镜检查表 | critical |
| `covey-weekly-first-things` | 晋级 Skill | p02 第二象限周计划四步骤 | critical |
| `covey-empathic-listening` | 晋级 Skill | p06 移情倾听 / 诊断先于开方 | critical |
| `covey-third-alternative` | 晋级 Skill | p07 第3选择四步协同 | critical |
| `covey-find-your-voice` | 晋级 Skill | f08 心声四要素交汇定位 | high |
| `covey-emotional-bank-account` | 晋级 Skill | p05 情感账户六种存款 | high |

### 仅经路由入口可达的能力卡（9 张）

`covey-pc-balance`(f02) · `covey-response-ability`(f04) · `covey-clock-compass`(f05) · `covey-win-win-audit`(f06) · `covey-get-trap`(f07) · `covey-sharpen-the-saw`(f09，已合并 p10) · `covey-self-empowerment`(f10) · `covey-personal-mission`(p01) · `covey-say-no`(p03)

### 淘汰（通过知识验证前即被 1.5 拦下，仅留审计）

- `p04` 责任型授权五要素 — 与 p07/f06 内容重叠，V2 预测力不独立（内容已并入 f06 的协议支柱）
- `p08` 发言权杖沟通协议 — 与 p06 重叠，降为移情倾听的多人场合变体
- `p09` Q3 的 5D 处理法 — **唯一真正的 V3 失败**：五条逐条为时间管理公共知识（内容已并入周计划的留白保护）

## 阶段 4 压力测试结果

| 指标 | 结果 |
|---|---|
| 用例数 | 29（21 should_trigger + 5 兄弟诱饵 + 3 纯诱饵，含 2 条边界） |
| 盲测方式 | 2 个未参与蒸馏的独立 sub-agent，仅给 8 个入口的 name+description |
| 7 个晋级 Skill F1 | **全部 1.000** |
| 兄弟混淆率 | **0.000（0/21）** |
| 诱饵 | 3 条纯诱饵全部判 `none`（考研报名时间 / 冒泡排序 / 今晚吃什么） |

> 说明：29/29 全中偏理想。原因是晋级卡 A2 段显式写了「何时不调用：走 covey-xxx」的互斥近邻负例，
> 而盲测 prompt 恰好落在该设计的判定区内。真实语料的鲁棒性需在后续使用中观察，
> 建议下次用 `run_trigger_evals.py prepare` 扩到 60+ 条并做 3 次重复运行。

## 后续

- 持续进化：`cangjie.py evolve`（会用 `evals/trigger/*.suite.json` 做 ratcheting）
- 若想把某张路由卡升级为独立 Skill：`cangjie.py replan-output --dry-run`
