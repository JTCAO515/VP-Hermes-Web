# VisePanda Agent Transfer Index

## 1. 文档目的

这份目录页是写给下一个 coding agent 的总入口。  
它不是新的项目总览，也不重复 `HANDOFF.md` 的内容，而是解决一个更实际的问题：

> **当仓库里已经有不少交接文档时，新的接手者应该先看什么，后看什么，哪些是当前主用材料，哪些只是历史参考。**

如果没有这份目录页，接手者很容易遇到两个问题：

1. 看到很多文档，但不知道当前哪几份是最值得优先阅读的  
2. 误把历史计划、旧迭代材料或背景文档，当成当前主入口

这份文档的目标，就是把整个交接包重新排成一个更好进入的结构。

## 2. 怎么使用这份目录

这份目录不是让你一次性从头读到尾，而是按场景使用。

### 如果你是第一次接手这个项目

先看：

1. `HANDOFF.md`
2. 工程附录
3. 首周接手清单
4. 高风险文件指南

这样做的原因是：

- `HANDOFF.md` 先帮你建立全局认知
- 工程附录告诉你当前主链路实际在哪里
- 首周清单告诉你别一上来做错节奏
- 高风险文件指南提醒你先别碰哪些地方

### 如果你准备开始改代码

优先看：

1. 工程附录
2. 高风险文件修改指南
3. 模块责任建议表
4. 技术债边界说明

因为这时最重要的不是“看完所有背景”，而是：

- 先知道你要改的模块属于哪一层
- 先知道这个改动最容易误伤哪里
- 先知道哪些债现在不要顺手重构

### 如果你准备上线或做回归

优先看：

1. 线上回归检查手册
2. `HANDOFF.md` 中的当前问题部分
3. 最近稳定性相关 spec / plan

### 如果你准备做未来 2-4 周规划

优先看：

1. 未来 2-4 周推荐迭代顺序
2. 技术债边界说明
3. 商用升级路线

## 3. 第一层：当前主用交接包

这一层是**当前真正应该优先看的文档**。  
如果你只打算快速建立接手能力，基本先围绕这里展开。

### [HANDOFF.md](../HANDOFF.md)

这份文档是项目总交接入口。  
它解决的是“这个项目是什么、当前做到什么、当前问题是什么、接下来应该怎么接”的问题。

优先级：

- 第一次接手时最先看
- 不确定项目当前状态时先回来看

### [2026-06-20-engineering-handoff-notes.md](2026-06-20-engineering-handoff-notes.md)

这份文档解决的是“当前真正活跃的工程主链路在哪里”。  
它比 `HANDOFF.md` 更工程化，适合在你准备打开代码之前先建立技术地图。

优先级：

- 准备改代码前优先看
- 对文件职责不确定时回来看

### [2026-06-20-first-week-takeover-checklist.md](2026-06-20-first-week-takeover-checklist.md)

这份文档是给新接手者的节奏说明。  
它的价值不是“列任务”，而是防止接手者第一周就走偏。

优先级：

- 第一次接手时优先看
- 如果你刚进入项目但还没形成判断，先照这个顺序来

### [2026-06-20-high-risk-files-guide.md](2026-06-20-high-risk-files-guide.md)

这份文档解决的是“哪些文件别乱动、改之前先确认什么、改完至少测什么”。

优先级：

- 准备改核心文件前必看
- 尤其在碰 `web/app.js`、`api/auth.py`、`api/chat.py` 时

### [2026-06-20-production-regression-manual.md](2026-06-20-production-regression-manual.md)

这份文档是发布前后和线上复测时的人工回归参考。  
它不替代自动化测试，但能让接手者知道“应该重点看哪里”。

优先级：

- 准备上线前看
- 线上出现问题后做复测时看

### [2026-06-20-next-2-4-weeks-priority-guide.md](2026-06-20-next-2-4-weeks-priority-guide.md)

这份文档解决的是“接下来 2-4 周最合理的推进顺序是什么”。  
它适合用来避免一接手就同时开太多线。

优先级：

- 开始排下一步工作时看
- 当你犹豫先补稳定性、先做联动还是先做商用准备时看

### [2026-06-20-technical-debt-boundaries.md](2026-06-20-technical-debt-boundaries.md)

这份文档解决的是“哪些技术债现在先别碰，哪些可以顺手修”。  
它最重要的作用是防止接手者把“看见问题”误判成“现在必须先重构”。

优先级：

- 准备做结构改动前看
- 觉得某块代码很难受、想大改时先看

### [2026-06-20-module-ownership-guide.md](2026-06-20-module-ownership-guide.md)

这份文档从模块责任中心的角度解释项目。  
它帮助你按 `Home / Chat / Cities / Trips / Tools / Admin / Shared Infra` 理解边界，而不是只看文件树。

优先级：

- 准备按模块改功能时看
- 多 agent / 多人协作时尤其要看

### [2026-06-20-commercial-upgrade-plan.md](2026-06-20-commercial-upgrade-plan.md)

这份文档不是当前开发主线，但对中期判断很重要。  
它解决的是“为什么当前继续保留 `Vercel`，以后什么时候需要逐步迁出后端和资源”。

优先级：

- 准备讨论商用升级时看
- 不要把它当作当前开发主线入口

## 4. 第二层：历史文档与参考材料

这一层不是说“不重要”，而是说：  
它们不是下一个 coding agent 第一天最该先看的材料。

## 4.1 项目总览与版本材料

### [README.md](../README.md)

适合快速了解项目概况、技术栈和基本入口。  
它比 `HANDOFF.md` 更偏仓库首页说明。

### [CHANGELOG.md](../CHANGELOG.md)

适合了解版本演变，尤其是：

- `v5.0.7`
- `v5.0.8`
- `v5.0.9`

这些与当前项目状态最相关。

## 4.2 最近的 spec / plan

这些文档很重要，但它们更偏“某一轮工作是怎么设计和拆解的”，不是总入口。

推荐重点查看：

- [production stability spec](superpowers/specs/2026-06-20-production-stability-pass-design.md)
- [production stability plan](superpowers/plans/2026-06-20-production-stability-pass.md)
- [handoff restructure spec](superpowers/specs/2026-06-20-handoff-doc-restructure-design.md)
- [handoff package expansion spec](superpowers/specs/2026-06-20-handoff-package-expansion-design.md)
- [agent handoff final layer spec](superpowers/specs/2026-06-20-agent-handoff-final-layer-design.md)

适用场景：

- 你想知道“为什么当时这么写”
- 你准备延续某一轮工作，而不是完全重新规划

## 4.3 ADR 与 agents 材料

### `docs/adr/*`

适合了解一些基础架构和关键决策的背景，例如：

- 为什么用 WSGI
- 为什么选 DeepSeek
- 为什么知识库这么组织

### `docs/agents/*`

更适合需要理解历史 agent 协作结构、issue 分类或 triage 方式时查看。  
普通接手流程里，不需要一开始先看完。

## 4.4 旧的 roadmap / iteration / review 文档

仓库里还有一些更早期或过渡期材料，例如：

- `ROADMAP.md`
- `ITERATION_LOG.md`
- `ITERATION_PLAN.md`
- 若干 `2026-06-19-*` 文档

这些文档仍有参考价值，但更适合在下面这些情况下按需查：

- 想理解项目当时为什么做某次迭代
- 想找旧思路，而不是当前主入口
- 想验证某个方向是不是已经讨论过

不要把这些旧文档误当成当前接手主线。

## 5. 建议阅读路径

### 场景一：第一次接手项目

建议顺序：

1. `HANDOFF.md`
2. 工程附录
3. 首周接手清单
4. 高风险文件修改指南
5. README

### 场景二：准备开始改代码

建议顺序：

1. 工程附录
2. 高风险文件修改指南
3. 模块责任建议表
4. 技术债边界说明

### 场景三：准备做线上回归或发布

建议顺序：

1. 线上回归检查手册
2. `HANDOFF.md` 中的当前问题部分
3. 最近稳定性 spec / plan

### 场景四：准备做未来 2-4 周规划

建议顺序：

1. 未来 2-4 周推荐迭代顺序
2. 技术债边界说明
3. 商用升级路线

## 6. 给下一个 coding agent 的一句话建议

> **先用这份目录页判断“现在该看哪份文档”，再去读文档正文，不要一上来在仓库里盲搜。**
