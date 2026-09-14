# LUNA：风险打断闭环最小实现方案（V1）

## 1. 目标

本方案面向第一优先场景（见《`docs/architecture/cross_domain/LUNA_CROSS_DOMAIN_SCENARIO_PRIORITY_V1.md`》）：

> **行走中遇到风险打断闭环**

回答一个实现面问题：

> 如果前方出现高风险事件，系统最小要怎么完成：识别 → 提权 → 抢占播报 → 任务挂起 → 风险解除后恢复？

本文件只输出**最小实现方案**：足够接近工程实现，但仍然**不写代码、不接新模型、不改现有主链逻辑**。

## 2. 最小闭环定义（必须包含的链路环节）

闭环至少包含：

1. 风险输入进入（来自视角风险/行为层）
2. 风险等级判断（至少 danger/caution/safe）
3. 进入统一输出裁决口，触发抢占（preempt）
4. 当前任务链挂起（pause/suspend）
5. 风险解除（clear / cooldown）
6. 任务恢复（resume）或重算（replan）

## 3. 最小输入（当前阶段最小依赖）

### 3.1 视角风险事件（必需）

概念对象：`RiskEvent`

最小字段语义（不锁代码字段名）：

- `ts_ms`
- `risk_level`：`safe|caution|danger`
- `risk_type`：如 `fast_approaching_vehicle` / `crowd_collision` / `step_hazard` / `road_edge`（可先粗枚举）
- `risk_reasons[]`：可解释原因（可为空但建议至少 1 条）
- `recommended_behavior`：`stop|slow_down|move_left|move_right|wait`（最小集合）
- `interrupt_required`：bool（等价于“必须抢占”）
- `confidence`
- `evidence_sources[]`（至少 `vision_scene`）

### 3.2 当前任务链状态（必需）

概念对象：`TaskChainStateSnapshot`

最小字段语义：

- `task_chain_id`
- `task_type`（导航/找路/找物等）
- `task_status`：`running|paused|waiting_user|completed`
- `task_interruptible`：bool（原则上 risk=danger 可覆盖该值）
- `current_step_digest`：当前播报/步骤摘要（用于白盒与恢复）

### 3.3 当前播报状态（必需）

概念对象：`FeedbackStateSnapshot`

最小字段语义：

- `speaking`：是否正在播报
- `current_output_id`
- `current_output_category`：安全/任务关键/解释/其他
- `cooldown_until_ts_ms`：避免重复播报的冷却窗口（可选但建议）

### 3.4 当前运行态（必需）

概念对象：`RuntimeModeSnapshot`

最小字段语义：

- `safety_first_enabled`：默认 true
- `whitebox_enabled`：默认 true（至少在最小实现阶段）
- `degrade_level`：用于降级策略（可选）

## 4. 最小状态机（V1）

> 状态机用于把“抢占/挂起/恢复”做成可控、可观测、可回放的过程。

### 4.1 状态定义

- **S0 正常任务执行中**：任务链 running，输出裁决按常规
- **S1 风险待确认**：收到 risk=caution 或 risk 信息不足（可只入白盒）
- **S2 风险抢占中**：risk=danger 触发抢占，准备打断当前播报
- **S3 任务已挂起**：任务链被挂起，进入风险处置窗口
- **S4 风险解除待恢复**：风险信号消失但需要 cooldown/确认
- **S5 任务恢复中**：恢复原任务或触发最小重算

### 4.2 状态迁移（最小规则）

- S0 → S2：`risk_level=danger` 或 `interrupt_required=true`
- S0 → S1：`risk_level=caution`（是否外显由裁决口决定）
- S2 → S3：抢占播报触发成功，并写入“任务挂起”标记
- S3 → S4：风险信号消失（或 risk_level 回落到 safe）
- S4 → S5：cooldown 满足或用户确认“继续”
- S5 → S0：恢复完成（或重算完成）

## 5. 打断规则（抢占/压下/恢复）

### 5.1 哪些风险等级可直接抢占

- **danger**：必须抢占（preempt）
- **caution**：默认不抢占，可插入短提示；若处于高风险环境（车流/低光/拥挤）可升级为抢占
- **safe**：不播报，仅白盒/上下文更新

### 5.2 哪些风险只入白盒不播报

- 低置信度、不可解释、且不影响安全行为建议的风险候选
- 短时间内重复出现且无新增信息（去重/冷却）

### 5.3 哪些风险要覆盖当前任务提示

- danger：覆盖所有非安全输出（任务关键提示/解释/补充）
- caution：覆盖解释与低优先级补充；任务关键提示可排队或合并

### 5.4 被打断的播报是否恢复、如何恢复（最小策略）

- **被打断的任务关键提示**：
  - 允许恢复，但需要“过时检查”（例如步骤是否已变化）
  - 恢复时可降级为一句摘要（避免重复）
- **被打断的解释性内容**：
  - 默认不恢复原样；改为合并摘要或留作追问

## 6. 最小输出（V1）

至少定义以下输出类别（与《统一输出裁决口》对齐）：

1. **即时安全播报**（danger）
2. **任务挂起标记**（对任务链/上层可见）
3. **风险解除后的恢复提示**（可选：例如“可以继续了”或“继续导航”）
4. **白盒事件记录**（全量）

> 备注：本阶段不设计最终文案，只定义类别与触发条件。

## 7. 与任务链的关系（挂起 / 恢复 / 重算）

### 7.1 任务链如何被挂起（最小版）

- 接收到 risk preempt 成功后，任务链进入 `paused`
- 记录 `pause_reason=risk_interrupt`
- 记录 `paused_at_step_digest`

### 7.2 任务链如何恢复（最小版）

恢复触发条件：

- 风险解除（risk_level 回落到 safe）
- cooldown 满足（防止“刚解除又复发”导致抖动）

恢复方式（优先级）：

1. **恢复原任务**（resume）：若任务上下文未变化、步骤未过时
2. **最小重算**（replan-lite）：若任务已过时/位置发生变化（本阶段可只标记“需要重算”，不实现复杂重规划）

### 7.3 什么时候必须重算而不是恢复

- 挂起期间用户已经偏离路线/场景变化显著（由上层状态判定）
- 用户明确改变目标
- 恢复时发现“当前步骤已过时”

## 8. 与统一输出裁决口的关系（入口与压制）

### 8.1 风险事件如何进入裁决口

- 风险事件作为最高优先级候选输出进入裁决口
- 裁决口根据 `risk_level` 决定：
  - 是否抢占
  - 打断哪条正在播报的输出
  - 丢弃/延后哪些非风险输出

### 8.2 为什么当前阶段风险链拥有更高优先级（写死）

- 安全优先：danger 必须抢占
- 任务链与语义解释不得延迟安全提醒
- 细节/OCR 默认降级或中断

### 8.3 哪些非风险输出必须被压下去

- 当前任务下一步提示（若与 danger 冲突）
- 解释性补充
- OCR/细节结果

## 9. 白盒要求（最小集合）

至少记录：

- 风险事件进入时间 `risk_ts_ms`
- 风险等级/类型/置信度
- 是否抢占成功（preempt=true/false）与失败原因（如有）
- 被中断的原输出是什么（output_id / category / digest）
- 任务是否挂起（task_status running→paused）
- 风险解除与 cooldown
- 是否恢复/是否重算（resume vs replan-lite）
- 最终用户听到什么（输出类别序列）

## 10. 当前阶段不做项（写死）

- 不做复杂轨迹预测
- 不做多风险源融合学习
- 不做复杂恢复策略（先最小可用）
- 不做多模型裁决
- 不做完整世界模型参与

## 11. 最小时序图（文字版）

1. 风险事件出现（视角风险层产出 `RiskEvent(risk_level=danger)`）
2. 风险层上报 → 候选输出进入统一裁决口
3. 裁决口判断：danger → **抢占**当前输出（若正在播报则打断）
4. 裁决口触发：**即时安全播报**（输出类别=safety）
5. 同步写入：任务链挂起（task_status=paused, pause_reason=risk_interrupt）
6. 风险持续：保持挂起；补充链/OCR 降级或中断
7. 风险解除：risk_level→safe，进入 cooldown
8. cooldown 满足：触发恢复（resume）或标记最小重算（replan-lite）
9. 恢复任务：输出裁决决定是否播报“继续导航/已恢复”，并恢复任务关键提示（可降级合并）

## 一句话收束

先把“风险打断闭环”的最小实现方案写到足够可落地（输入、状态、打断、恢复、输出、白盒、时序），再进入真正的工程实现阶段。

