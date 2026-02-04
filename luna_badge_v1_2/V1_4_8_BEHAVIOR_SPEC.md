V1_4_8_BEHAVIOR_SPEC.md（Final）

1. 版本定位

Luna Badge v1.4.8 是一个 Vision-Driven、节奏优先、可验证 的导航与表达系统版本。

本版本目标只有三点：
	•	稳定
	•	可预测
	•	可复现

v1.4.8 不追求“更聪明”，只保证不越权。

⸻

2. 核心公理（不可违背）

2.1 视角主权

Vision is the only rhythm authority.
Expression must follow vision, never lead it.

解释：
	•	所有节奏（播报 / 延迟 / 阻断）只由视觉状态决定
	•	任何非视觉模块 不得决定节奏

⸻

2.2 模块边界

模块	允许	禁止
Vision	决定节奏	输出语言
FSM	行为状态	直接播报
GPS	位置验证	决定节奏
Expression	表达内容	领先视角
C-5 Scheduler	说 / 不说 / 何时说	改写语义

⸻

3. 视觉状态定义

v1.4.8 只认三种视觉状态：
	•	STABLE：视角稳定
	•	TURNING：视角转动 / 注意力占用
	•	MOVING：连续行进

⸻

4. 行为矩阵（法律条文）

视觉状态	表达类型	行为	延迟	说明
STABLE	normal	EMIT	100–300ms	由视觉速度决定
STABLE	low	QUEUE	≤300ms	可 replace
TURNING	normal	DROP	0	绝对禁止
TURNING	critical	EMIT	0	安全覆盖
ANY	duplicate	REPLACE	0	非 FIFO

规则说明：
	•	DROP = 永不播报（不是延迟）
	•	QUEUE ≠ FIFO，仅为候选池
	•	REPLACE 优先级高于 QUEUE

⸻

5. 延迟策略

v1.4.8 禁止固定延迟。

延迟仅来自视觉速度分桶：

视觉速度	延迟
高	100ms
中	200ms
低	300ms

约束：
	•	延迟只影响「什么时候说」
	•	不影响「说什么」
	•	GPS 不得参与延迟计算

⸻

6. GPS 的明确地位

6.1 唯一合法角色
	•	位置验证（validation）
	•	异常检测（jump / quality）

6.2 明确禁止

GPS 不得：
	•	决定播报节奏
	•	触发表达
	•	覆盖 Vision 状态

GPS may validate position, but never drives behavior timing in v1.4.8.

6.3 场景规则

场景	GPS
室内	关闭
≤50m	verify_only
>50m 室外	仅验证

⸻

7. C-5 调度器职责边界

v1.4.8 中 C-5 只允许：
	•	决定：说 / 不说 / 何时说
	•	依据：Vision 状态 + 表驱动规则

明确禁止：
	•	改写语义
	•	生成新内容
	•	学习或记忆

⸻

8. 明确不包含的能力

v1.4.8 不包含：
	•	情感调度
	•	多模型仲裁
	•	自学习策略
	•	用户画像驱动表达
	•	动态语言风格切换

⸻

9. 一致性保证

在相同输入下，系统必须：
	•	行为一致
	•	延迟一致
	•	日志一致

这是工程验收标准。

⸻

10. 版本声明

This document defines the behavioral contract of Luna Badge v1.4.8.
Any change that alters these behaviors
requires a new minor or major version.

⸻

状态
	•	P0-1：完成（可入库）
	•	可直接进入 P0-2：Freeze List（冻结清单）
