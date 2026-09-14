# risk_interrupt_v1 试点观察面缺口补齐清单（V1）

## 目标

在 `tools/analyze_risk_interrupt_v1_pilot.py` 已能做最小聚合（按 `request_id + pilot path`）的基础上，明确：

- 当前哪些指标已能从 trace **稳定直接统计**
- 哪些关键指标仍**不可直接统计**（导致报告“半盲”）
- 后续若要补齐，需要补的**最小 telemetry**是什么、落点在哪、为什么是最小

本文件**只做缺口收口**，不改 analyzer、不改试点逻辑、不放宽边界。

---

## 1. 当前已可直接统计的指标（analyzer 可稳定产出）

以下指标在当前 trace 事件形态下可直接按 `request_id` 聚合得到（已在 analyzer V1 中实现或可无歧义实现）：

### 1.1 路径/触发类

- **`preempt_before_submit_count`**  
  - 来源：`output_decision.reason == "risk_interrupt_v1_level2_pilot_preempt_before_submit"`
- **`cancel_replace_attempt_count`**  
  - 来源：`output_decision.reason == "risk_interrupt_v1_cancel_replace_pilot_evaluated"` 且 `metadata.cancel_replace_on == true`
- **`cancel_replace_chain_closed_count`** / **`cancel_replace_chain_closed_rate`**  
  - 来源：同上，`metadata.cancel_replace_chain_closed == true`
- **`fallback_to_preempt_before_submit_count`**（若 `metadata.fallback_to_preempt_before_submit` 为 true）  
  - 来源：同上，`metadata.fallback_to_preempt_before_submit == true`

### 1.2 约束对账类（当前可做“是否越界”的最小检查）

- **`high_critical_trigger_count`**（当前主要基于 preempt 观测）  
  - 来源：preempt 的 `output_decision.metadata.risk_level`
- **`prompt_confirmation_target_count`**（当前主要基于 preempt 观测）  
  - 来源：preempt 的 `output_decision.metadata.preempted_output_category`

### 1.3 样本导出入口（用于人工复核）

- **成功样本**：preempt 命中 或 cancel+replace 链闭合（按 `request_id`）
- **fallback 样本**：cancel+replace attempt 但链不闭合/或显式 fallback
- **可疑样本**：越界（非 high/critical、非 prompt/confirmation）、链不闭合但无 reason、replacement trace 缺失等

---

## 2. 当前仍不可直接统计的指标（关键缺口）

### 2.1 `fallback_to_level1_count`（关键缺口）

**结论**：当前无法从 trace 中稳定直接统计“试点回退到 Level 1”的次数。

**原因**：

- 当前可观察到的是“某条试点路径是否尝试/是否闭合/是否回退到 preempt（Level 2A）”，但**没有一条明确的、可机器识别的事件**表示“已执行回退到 Level 1”。
- Level 1 回退通常通过**开关**实现（例如关闭 `LUNA_ENABLE_RISK_INTERRUPT_V1_LEVEL2_PILOT`），但这属于运行配置动作，若不写 telemetry，报告层无法知道“是否发生过回退”。

### 2.2 `fallback_to_level0_count`（关键缺口）

**结论**：当前无法从 trace 中稳定直接统计“试点终止并回到 Level 0”的次数。

**原因**：

- Level 0 回退同样是配置/运维动作（例如关闭 `LUNA_ENABLE_RISK_INTERRUPT_V1` 或 `LUNA_ENABLE_REAL_OUTPUT_SUBMIT_V1`），trace 中目前缺少一个显式事件去记录这次动作的发生、原因与关联范围。

---

## 3. 缺的最小 telemetry（建议补齐方式）

> 目标是“让回退真的发生过”成为**机器可统计事实**，而不是让 analyzer 去猜。

### 3.1 最小新增事件：`pilot_state_transition`（推荐）

新增一个极小观测事件（建议也走 JSONL envelope），字段最小化：

- `timestamp`
- `transition`：`"level2b_to_level2a"` / `"level2a_to_level1"` / `"any_to_level0"` 等
- `reason`：固定枚举（例如 `"operator_toggle"`, `"auto_exit_threshold"`, `"guardrail_violation"`, `"observation_chain_broken"`）
- `related_request_id`（可选）：若这次回退由某个 request 触发/发现，可带上；否则为空
- `metadata`（可选）：包含当时关键开关快照（仅 boolean 列表）

**落点建议**：

- 优先落在“执行回退动作”的地方（例如统一的 runtime mode/开关治理入口，而不是散落在试点逻辑里）。

**为什么这是最小补充**：

- 不要求修改试点逻辑判断
- 不要求修改 request/playback 真源
- 不要求建立复杂状态机，只记录“状态切换发生过”

### 3.2 备选（更小但更弱）：复用 `output_decision` 记录回退动作

如果暂时不想引入新 type，可在回退动作发生时写一条 `output_decision`：

- `reason="risk_interrupt_v1_pilot_fallback_to_level1"` 或 `..._to_level0`
- `metadata` 包含 `why` + 开关快照

**代价**：语义上不如专用事件清晰，但依然可统计。

### 3.3 对 cancel+replace 的补充字段（可后补）

当前 cancel+replace eval 的 `output_decision` metadata 已包含闭合与 failure_reason，但缺少：

- `risk_level`
- `target_output_category`

这会导致 analyzer 只能基于 preempt 的字段统计 `high_critical_trigger_count` / `prompt_confirmation_target_count`，对 cancel+replace 这条路径的“越界检查”不完整。

建议作为**次优先**补齐：在 `risk_interrupt_v1_cancel_replace_pilot_evaluated` 的 metadata 中补充上述两个字段（不改变行为，仅增强观测）。

---

## 4. 优先级（先补什么）

按“对试点评审的必要性 + 成本最低”排序：

1. **P0：补齐 `fallback_to_level1_count` / `fallback_to_level0_count` 的显式 telemetry**  
   - 这是“回退真的发生过”的关键系统事实，否则观察面长期半盲。
2. **P1：补齐 cancel+replace 路径的越界检查字段（risk_level / output_category）**  
   - 用于按 pilot path 做一致的边界对账。
3. **P2：更深的闭合与一致性指标（如用户最终听到文本一致性、链路闭合率分桶等）**  
   - 在 P0/P1 完成后再做，不应抢先。

---

## 5. 不做项（写死）

- 不直接改 `tools/analyze_risk_interrupt_v1_pilot.py` 的统计口径来“猜测回退”
- 不改现有试点边界/实现
- 不放宽 started playback / 输出类型 / 风险等级等任何限制

---

## 一句话收束

先把“回退到 Level 1 / Level 0”补成可观测、可统计的最小 telemetry 系统事实，再谈是否要在观察窗口内继续维持或进一步评审。

