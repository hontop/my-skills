---
name: probabilistic-thinking
description: |
  当用户在不确定性下要**估算可能性并决定投入多少**时使用：有多大把握、该投多少资源、值不值得赌、
  要不要防极端情况。典型问法：「有多大概率」「胜算多大」「该投多少」「值得赌一把吗」
  (what are the odds, expected value, base rate, fat tail, how much should I bet)。
  不适用于列出行动的后果链条（用 second-order-thinking），也不适用于判断两件事是不是因果（用 correlation-causation）。
metadata:
  cangjie.generated-by: cangjie-tools v2.5.0
  cangjie.capability-id: cap.sikao-de-kuangjia.probabilistic-thinking
  cangjie.capability-revision: 1
  cangjie.bundle-id: bundle.sikao-de-kuangjia
  cangjie.source-title: 思考的框架（第 1 册 + 第 2 册）
  cangjie.tags: mental-model, decision, quantitative
---
# 概率思维

## R — 原文

> "Probabilistic thinking is essentially trying to estimate, using some tools of math and logic, the likelihood of any specific outcome coming to pass."
> 直译：概率思维，本质上是尝试用数学和逻辑工具，估算某个特定结果成为现实的可能性。
> —— 思维模型 06 概率思维，https://fs.blog/probabilistic-thinking/

> "Successfully thinking in shades of probability means roughly identifying what matters, coming up with a sense of the odds, doing a check on our assumptions, and then deciding."
> 直译：以概率的灰度思考，意味着大致确定什么最重要、形成对赔率的感觉、检验一遍假设，然后才做决定。
> —— 思维模型 06 章末 Conclusion，https://innovae.school/OpenCampus/readings/chapters/the-great-mental-models-volume-1-core-decision-models.pdf

## I — 自述

未来由无数看不见的因素决定，你永远拿不全信息。这套方法不消灭不确定性，而是把它量化，让你在信息不全时仍能排序和出手。

四条骨架：
1. 把"会不会发生"改写成"概率是多少"，给每个结果一个明确数字——说 63%，不说"大概能行"。
2. 任何概率先找同类历史频率做锚，这个锚叫基准率；新证据不是推翻旧判断，而是按强度把概率挪一段。
3. 判断身处薄尾还是肥尾——身高偏离有上限，财富与战争的极端值没有上限，后者误差可差几个数量级。
4. 既然预测必错、且误差偏向乐观，就把重心从"预测准"换成"输得起"。

产出不是答案，而是"概率 + 仓位"的组合。

## A1 — 书中案例

**1. 薇拉·阿特金斯与英国特别行动处（SOE）法国处（二战）**
- 问题：她任 SOE 法国处副指挥，须挑选特工空投进德占法国；失败的代价是死亡，而手上的信息天然不可靠——粗糙照片、多人转手的便条、操作员高压下无法核实的电报。
- 用法：给各项因素分配权重（谁会法语、自信程度是否合适、家庭牵绊多深、有无临场解题能力），汇总成"谁有像样成功机会"的概率评估；同时想"发生了什么"与"可能发生什么"。
- 结果：她派出的报务员在法国的平均预期寿命只有六周，400 名特工中有 100 人被俘并被处死。作者定论：概率思维只能把你带到大致正确的范围；关键注脚是"情报不是证据"。

**2. 楼梯摔倒 vs 恐怖袭击（肥尾）**：某年摔下楼梯摔破头而死 1000 人、死于恐怖袭击 500 人，有人据此说恐怖风险很低。但楼梯死亡属薄尾，恐怖暴力属肥尾、极端值没有上限；结论是不能穷举尾部情景，而要把自己放到能在不可测的未来中活下来的位置上。

## A2 — 未来触发

1. **触发场景**：① 信息不全时要分配资源（投多少、招不招、要不要 All in）；② 拿耸动标题或单个极端故事问"是不是真的很危险"；③ 所处领域存在十倍百倍量级的极端结果，却在做点预测。

2. **语言信号**
   - 中文："把握有多大""有几成胜算""该投多少""以前从没出过事"。
   - 英文：how likely / what are the odds / worst case / it's never happened before。
   - 关键 trigger 词中英双写：**概率 probability / 赔率 odds / 基准率 base rate / 肥尾 fat tails / 仓位 position sizing**。

3. **与相邻能力的区分**：**vs 二阶思维**——本卡给"可能性与仓位"，二阶给"后果链条"；问"有多大把握、该投多少"→ 概率，问"之后会发生什么"→ 二阶。**vs 奥卡姆剃刀**——奥卡姆砍掉变量只留一个最简解释，概率思维要保留多个结果并各自赋权。**vs 可证伪性**——后者问"能不能被推翻"，本卡问"还没被推翻时该信到几分"。

## E — 执行步骤

1. **列因素并绑定推翻条件**（不超过 5 条）。完成标准：每条后接一句"若 X 变为 __，我的结论变为 __"，写不出这句的变量一律删掉。
2. **先报先验（基准率）**：找至少一个同类历史频率数字。完成标准：数字后面有出处。**判停点：写不出有出处的数字，本步未通过，禁止进入第 3 步——感觉不构成概率。**
3. **报赔率**：给每个关键结果一个整数百分比。完成标准：全部用数字，不出现"大概/可能"，且概率之和为 100%。
4. **元概率体检**：问"我这类估计历史上错多少、偏向哪边"。完成标准：给出区间（如 40%，区间 20%–60%）并说明偏向。
5. **判薄尾还是肥尾**：若判为肥尾，须写出"最坏损失上限 = __，不超过可支配资源的 __%"。**判停点：肥尾域一律停止点预测，只调仓位与冗余。**

## B — 边界

1. **什么时候不要使用**：单次结果已发生、有人正拿概率给这次结果"定罪"时（400 人中死 100 人是概率思维的正常工作结果）；纯情感与人际承诺场景；要求确定性口径的法律、合规场合。
2. **书中警告过的失败模式**：把情报当证据（阿特金斯章的核心教训）；无视基准率、只看耸动标题；先验僵化，或被单一新证据立刻推翻；用"最近几年都没出过事"外推肥尾域——最典型的自杀式用法；硬精确到小数点。
3. **相邻但容易混淆的方法论**：二阶思维（推后果链条，而非给可能性）；奥卡姆剃刀（精简解释，而非分发概率）；可证伪性（判断命题可不可被推翻，而非当前该信几分）。
