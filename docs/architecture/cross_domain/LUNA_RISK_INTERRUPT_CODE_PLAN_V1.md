# LUNA：风险打断闭环最小代码实现计划（V1）

## 1. 第一版代码目标

本计划基于：

- 切片定义：《`docs/architecture/cross_domain/LUNA_RISK_INTERRUPT_IMPLEMENTATION_SLICE_V1.md`》
- 统一裁决口：《`docs/architecture/cross_domain/LUNA_UNIFIED_OUTPUT_ARBITRATION_V1.md`》

### V1 要落成什么（写死）

在非常小的范围内实现：

1. 接收统一风险事件
2. 判断是否需要抢占（high/critical）
3. 打断当前普通输出
4. 给任务链打 `paused_by_risk` 标记
5. 输出 1 条风险提示（类别=safety）
6. 白盒完整留痕

### V1 不做什么（写死）

- 不做风险解除自动恢复
- 不做多风险合并/排队/恢复队列
- 不做轨迹预测
- 不做复杂裁决器与多模型融合
- 不做重规划/自动重算

### 为什么这样切

- 验证“统一输出裁决口”是否成立
- 验证任务链能否被打断/挂起（先不恢复）
- 不污染主链：可一键降级为“只入白盒”

## 2. 建议代码落点（先接哪个入口、代码先落在哪）

> 目标是“最小侵入 + 易回退 + 易白盒观测”。本计划给出建议落点，不要求一次到位。

### 2.1 风险事件入口（建议新增一个旁路入口）

建议新增一个**跨域风险事件输入接口**（先不接模型，仅供后续注入/测试）：

- 位置建议：`capabilities/cross_domain/risk_interrupt/`（新目录，后续实现时创建）
- 入口建议：`handle_risk_interrupt_event(event, ctx)`（函数级）

理由：

- 与 voice/vision 的具体实现解耦
- 便于先做 mock/脚本验证

### 2.2 输出裁决口（复用“输出决策观测”概念）

当前仓库里已有 placeholder 观测对象：

- `capabilities/voice/observations/output_decision_observation.py`

V1 实现建议：

- 裁决逻辑先落在“跨域 risk_interrupt 模块内部”（不改语义主链、不改任务链）
- 仅把裁决结果与白盒字段写进一个 `metadata`/observation 结构，供后续统一化

### 2.3 任务链挂起标记落点（先不改任务链实现）

V1 只要求“打 `paused_by_risk` 标记”，不要求真实控制任务执行。

建议落点：

- 先以“跨域运行态上下文”记录：`paused_by_risk=true`（例如存在 `runtime_context` / `task_context` 的 metadata 字段时）
- 若没有统一 runtime_context：先把标记写进白盒 observation（保证可观测），并在下一阶段再真正接任务链状态机

### 2.4 白盒记录落点（复用 metadata / observation）

参考 voice 已有“metadata + routing_observation”的写法（例如 `capabilities/voice/runtime/voice_final_text_dispatcher.py`）。

V1 建议：

- 统一把风险打断链的字段放到一个键下（例如 `risk_interrupt_observation`），避免污染顶层字段。

## 3. 最小状态字段（V1 需要先写哪些状态）

V1 需要的最小状态（可先存在运行时上下文/内存态/白盒态）：

- `current_output_state`：当前是否正在播报、播报类别、digest（用于判断是否可中断）
- `risk_interrupt_active`：是否处于风险抢占窗口（V1 可简化为一次性事件）
- `paused_by_risk`：任务链是否被风险挂起标记（V1 仅标记）
- `active_risk_event_id`：当前活跃风险事件 ID（可用 timestamp+hash 简化）
- `last_risk_level`：用于冷却/去重（V1 可选）

## 4. 最小白盒字段（V1 必须留哪些观测字段）

至少包含（与切片一致）：

- `event_timestamp`
- `original_output`
- `risk_event_summary`
- `interrupt_applied`
- `task_paused`
- `final_spoken_output`

建议额外补 2 个字段（便于排障）：

- `interrupt_reason`
- `preempt_rule_hit`（命中哪条规则：high/critical）

## 5. 最小执行顺序（文字版时序）

1. 风险事件进入（RiskInterruptEventV1）
2. 进入裁决口（unified output arbitration）
3. 判断是否抢占（high/critical → preempt）
4. 若当前播报为普通任务提示：
   - 中断当前输出
   - 输出 1 条风险提示（safety）
5. 写入 `paused_by_risk=true`（先标记，不做恢复）
6. 写白盒 observation（全字段）

## 6. 验证入口（怎么验证不污染主链）

### 6.1 最小验证方式（不接模型）

建议提供一个最小验证脚本（后续实现阶段再写代码，这里先定义口径）：

- 构造：`current_output_state=task_tip(speaking=true)` + `RiskInterruptEventV1(high)`
- 断言：
  - `interrupt_applied=true`
  - `final_spoken_output_category=safety`
  - `task_paused=true`
  - 白盒字段齐全

### 6.2 不污染主链的验证

V1 必须支持一键降级到：

- “风险事件只入白盒、不抢占、不挂起”

验证点：

- 降级开关生效后，主链输出行为不变（只多白盒记录）

## 7. 回退边界（最小回退方式）

出现问题时的最小回退：

1. 关闭风险抢占（preempt=false）
2. 风险事件只入白盒（仍保留证据）
3. 不影响默认主链（不改变语义/任务链现有逻辑）

## 8. 当前阶段不做项（再次写死）

- 不做复杂恢复
- 不做自动重算
- 不做复杂排队
- 不做多风险融合
- 不做复杂文案系统

## 一句话收束

先把风险打断闭环的代码落点、最小状态/白盒字段、验证入口与回退边界写清楚，下一步再进入小范围开发：只做“风险进入→抢占输出→任务挂起标记→白盒留痕”。

