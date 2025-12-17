V1_4_8_FREEZE_LIST.md（Final）

1. 冻结目的（Why Freeze）

本冻结清单用于明确：

哪些行为在 v1.4.8 中被视为“版本级契约”，
不允许在不升级版本号的情况下发生变化。

冻结的不是代码文件，而是行为结果。

⸻

2. 总冻结原则（Global Freeze Rules）

在 v1.4.8 中，以下原则永久冻结：
	1.	Vision 是唯一节奏主权
	2.	Expression 永远不能领先 Vision
	3.	GPS 不参与任何节奏决策
	4.	TURNING 状态具有最高抑制优先级
	5.	表达调度必须可预测、可复现

违反以上任一条，必须升级版本号。

⸻

3. 行为级冻结项（Behavior Freezes）

3.1 视觉状态冻结

项目	冻结内容
视觉状态集合	仅允许 STABLE / TURNING / MOVING
TURNING 行为	TURNING 状态下禁止非关键表达
状态主权	任何模块不得绕过 Vision State

⸻

3.2 C-5 Scheduler 冻结项（核心）

队列机制

项目	冻结值
最大队列长度	2
队列类型	非 FIFO
重复策略	REPLACE 优先
视觉变化	状态变化立即 flush

延迟策略

项目	冻结值
延迟来源	仅 Vision
延迟分桶	{0, 100, 200, 300} ms
固定延迟	禁止

⸻

3.3 TURNING 覆盖规则冻结

项目	冻结内容
非关键表达	永久 DROP
关键表达	允许 0ms 覆盖
判断顺序	critical → turning block

⸻

3.4 表达调度边界冻结

C-5 Scheduler 在 v1.4.8 中 明确禁止：
	•	改写表达文本
	•	合成新表达
	•	基于历史学习
	•	基于用户画像调整策略
	•	与情感系统产生耦合

⸻

4. GPS 冻结项

4.1 功能冻结

项目	冻结内容
角色	验证 / 佐证
节奏参与	禁止
表达触发	禁止

4.2 场景冻结

场景	GPS 状态
室内	强制关闭
≤50m	verify_only
>50m 室外	仅验证

⸻

5. 配置与规则冻结

以下配置在 v1.4.8 中视为只读：
	•	c5_rules.json 的规则语义
	•	critical / normal / low 的分级含义
	•	Vision speed → delay 的映射逻辑

允许修改的只有：
	•	数值微调（不改变分桶结构）
	•	文案文本（不改变行为）

⸻

6. 允许的变更范围（不升级版本）

在 不升级版本号 的前提下，仅允许：
	•	Bug 修复（不改变行为结果）
	•	日志增强
	•	性能优化（不改变时序）
	•	Demo / 测试补充

⸻

7. 版本升级触发条件

以下任一情况发生，必须升级 minor 或 major 版本：
	•	新增视觉状态
	•	修改 TURNING 行为规则
	•	改变延迟分桶结构
	•	允许 GPS 参与节奏
	•	C-5 引入学习或记忆
	•	表达调度与情感系统产生耦合

⸻

8. 冻结声明（Version Lock）

This document freezes the behavioral surface of Luna Badge v1.4.8.
Any change violating this list
requires a new minor or major version.

⸻

状态说明
	•	P0-2：完成（可入库）
	•	与 V1_4_8_BEHAVIOR_SPEC.md 共同构成 1.4.8 的行为契约
