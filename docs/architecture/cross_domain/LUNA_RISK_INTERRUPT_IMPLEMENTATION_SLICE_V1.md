# LUNA：风险打断闭环实现切片（V1）

## 1. 第一版目标（只实现什么 / 不实现什么 / 为什么这样切）

本切片是对《`docs/architecture/cross_domain/LUNA_RISK_INTERRUPT_MIN_IMPLEMENTATION_V1.md`》的进一步收敛：把“最小实现方案”切成**可跑、可验证、可回退**的第一版落地范围。

### V1 只实现（写死）

1. 接收统一风险事件（单一入口，不关心来源是规则还是模型）
2. 风险提权（最小规则：high/critical 抢占；medium 只白盒/必要时播报；low 仅留痕）
3. 打断当前普通输出（若正在播报“普通任务提示”，直接中断并播报风险句）
4. 挂起当前任务链（打 `paused_by_risk` 标记，不做复杂恢复策略）
5. 输出一条风险提示（不做复杂文案生成）
6. 白盒完整留痕（可回放）

### V1 不实现（写死）

1. 风险解除后的自动恢复
2. 多风险事件合并/排队/队列恢复
3. 复杂轨迹预测
4. 复杂裁决器/多模型融合
5. 自动重算/重规划

### 为什么这样切

- 安全优先：先验证“能抢占、能挂起、能留痕”
- 对复杂感知依赖最小：即使风险信号来源很粗，也能验证跨链机制
- 回退简单：允许把风险事件降级为“只入白盒”

## 2. 最小输入事件（统一风险事件 V1）

概念对象：`RiskInterruptEventV1`（只定义字段语义，不锁最终代码字段名）

- `timestamp`：事件时间（ms 或秒，统一为毫秒更易对齐）
- `risk_type`：风险类型（粗粒度即可）
- `risk_level`：`low|medium|high|critical`
- `direction_hint`：方向提示（如 left/right/front/back/unknown）
- `distance_band`：距离分段（如 near/medium/far/unknown）
- `confidence`：0~1

## 3. 最小处理规则（提权 + 抢占）

### 3.1 提权规则（V1 固定）

- `high|critical`：
  - `preempt=true`
  - 进入“即时安全播报”类别
  - 压制一切非风险输出
- `medium`：
  - `preempt=false`
  - 默认只入白盒
  - 允许在“当前无播报 + 风险类型明确”时播报一句短提示（可选开关，但 V1 先默认不播）
- `low`：
  - 只入白盒，不播报，不影响任务链

### 3.2 抢占规则（V1 固定）

当 `preempt=true` 且当前正在播报**普通任务提示**：

- 立即中断当前播报
- 输出风险提示（单句）
- 写入任务链 `paused_by_risk=true`

不做：

- 不排队、不合并、不恢复队列

## 4. 最小状态变化（必须可观测）

V1 必须产生以下状态变化（哪怕仅写入内存态/白盒态）：

- `interrupt_applied=true/false`
- `task_paused=true/false`（paused_by_risk）
- `final_spoken_output_category=safety`（若抢占成功）

## 5. 最小输出（V1）

- **风险即时播报**（仅 high/critical）
- **任务挂起标记**：`paused_by_risk=true`（写入任务链状态或等价处）
- **白盒事件摘要**：必须包含“抢占是否发生、原输出是什么、最终说了什么”

## 6. 当前不实现项（再次写死）

- 不做复杂恢复（风险解除后不自动恢复）
- 不做多风险合并
- 不做轨迹预测
- 不做复杂调度/排队系统
- 不做自动重算

## 7. 白盒最小字段（V1 必须）

至少记录：

- `event_timestamp`
- `original_output`（被中断前在播什么：category + digest）
- `risk_event_summary`（type/level/direction/distance/confidence）
- `interrupt_applied`
- `task_paused`（paused_by_risk）
- `final_spoken_output`（最终播报内容摘要 + 类别）

## 8. 验证方式（V1 如何证明“切片可用”）

### 8.1 最小验证入口（建议）

- 用一个最小 mock/脚本构造：
  - 正在播报普通任务提示的 `current_output_state`
  - 一个 `RiskInterruptEventV1(high/critical)`
  - 一个可写入的“任务链状态快照”

### 8.2 必须验证的结果

- 白盒字段齐全（能回放）
- high/critical 风险能抢占成功（interrupt_applied=true）
- 被中断的原输出被记录（original_output 非空）
- 任务链被打 paused_by_risk 标记（task_paused=true）
- 用户只听到 1 条风险提示（不叠加、不重复）

### 8.3 回退验证（必须）

将策略降级为“风险只入白盒”（不抢占、不挂起）后：

- 默认主链行为不变
- 白盒仍可记录风险事件（用于后续排障/评估）

## 一句话收束

V1 先做“能抢占、能播报、能挂起、能留痕”，不做恢复与复杂裁决；用最小切片先验证跨链机制，再进入下一版扩展。

