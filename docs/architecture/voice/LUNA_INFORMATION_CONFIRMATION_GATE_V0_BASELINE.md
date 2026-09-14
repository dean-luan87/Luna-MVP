# Information Confirmation Gate v0 Baseline / Freeze（引用对象缺失/歧义准入冻结面）

**文件**：`docs/architecture/voice/LUNA_INFORMATION_CONFIRMATION_GATE_V0_BASELINE.md`  
**性质**：Topic 02 下已落地的第一个 gate 冻结面（可维护、可回归）  
**目标**：把当前已实现并验证通过的「引用对象缺失/歧义 → pre-submit confirmation gate」固定边界、输入、落点与验证入口，防止 Topic 02 后续扩展漂移。  

上位约束（必须服从）：  
- `docs/architecture/voice/LUNA_CONFLICT_GOVERNANCE_CONSTITUTION_V0.md`  
- `docs/architecture/voice/LUNA_CONFLICT_TOPIC_02_INFORMATION_SUFFICIENCY_GATE_V0.md`  
- `docs/architecture/voice/LUNA_VOICE_MAINLINE_BASELINE.md`  

---

## A. 当前基线范围

**当前只批准 Topic 02 下一个最小 gate**：Information Confirmation Gate v0  

**当前只覆盖**：  
- 明显指代词命中（v0 最小集合）  
- 且当前无唯一绑定事实  
- 因此不得进入 submit，标记“需要确认”  

**当前未覆盖（明确不做）**：  
- 通用 `required_fields_missing` 框架  
- 目标地点/任务参数的完整 schema 化缺失判断  
- 历史记忆自动补对象绑定  
- 视觉补对象绑定  
- `resume/repeat` 高歧义 intent  
- 文本 vs 视角冲突处理  

---

## B. 当前系统定位

- 这是一个 **pre-submit information confirmation gate**：只决定“是否允许进入 submit”。  
- 它不是主链裁决器：  
  - 不改 `dispatch_type`  
  - 不改 `bridge_decision.route`  
  - 不改 proposal 语义（如 `proposal.device_action`）  
- 它不改 reply；不改语义层规则集合；不替代 reference resolution 系统；不是对话管理器。  
- 它只影响：是否调用 `_maybe_submit_real_output_v1(...)`。

---

## C. 当前唯一输入依据（v0）

当前只读：  
- 用户当前输入文本（本轮 request）：`event.wake_word_stripped | event.normalized_text | event.raw_text`  
- `VoiceV1SessionStateAnchor`（只读事实锚；v0 不用于猜绑定）  
- 当前 dispatch 结果事实（尤其 `bridge_decision` 与 `proposal`）  

### C1. 最小指代词集合（v0）

仅识别（简单包含匹配）：  
- `这个`  
- `那个`  
- `这里`  
- `那里`  

> 命中不等于拦截；只有在“无唯一绑定事实”时才拦截。

### C2. “唯一绑定事实”判断口径（v0 极保守）

- **不从** `last_user_text` / `last_system_text` 猜绑定  
- **不使用** 历史记忆或视觉摘要补绑定  
- **仅当** `proposal` 中存在显式目标标识（如 `target_id/object_id/place_id/destination_id/reference_id`）才视为已绑定  
- 在当前 Stage-1 下，多数 proposal 不携带上述 id，因此命中指代词时通常视为“不足以唯一绑定”并触发确认

---

## D. 当前 gate 行为（写死）

### 拦截条件

同时满足：  
- 用户输入命中最小指代词集合  
- 且当前无唯一绑定事实（按 §C2 口径）  

则：  
- 不得进入 submit  
- 写入 `information_confirmation_gate_v0`  
- `requires_confirmation = true`  

### 放行条件

- 未命中上述拦截条件：放行  
- 当前策略为 **relevant-only**：未命中时默认不写 `information_confirmation_gate_v0`（最小侵入）  

### 拦截范围（写死）

- gate 只拦截：`_maybe_submit_real_output_v1(...)`  
- gate 不改变：`dispatch_type` / `bridge_decision.route` / `proposal.device_action`

---

## E. `information_confirmation_gate_v0` 最小结构（metadata）

当命中拦截条件时写入：`VoiceFinalTextDispatchResult.metadata["information_confirmation_gate_v0"]`

```json
{
  "gate_passed": false,
  "gate_reason": "missing_or_ambiguous_reference",
  "gate_scope": "pre_submit_information_confirmation_v0",
  "requires_confirmation": true
}
```

约束：  
- 未命中时默认不写该字段  
- 不包含 `timestamp/location/position/coordinate/lat/lng` 等字段  

---

## F. 当前明确禁止项（写死）

- 不允许因为上下文“看起来像”就脑补唯一绑定  
- 不允许因为历史记忆存在就跳过必要确认  
- 不允许视觉摘要替代用户提供关键对象  
- 不允许在本 baseline 上直接扩成通用引用解析系统  
- 不允许在本 baseline 上顺手混入 `resume/repeat`  
- 不允许把该 gate 做成协商策略器  

---

## G. 当前验证入口（必须重跑）

改到 gate 落点、指代词规则、唯一绑定事实判断口径、submit 准入逻辑时必须重跑：

- `tools/verify_voice_confirmation_gate_v0.py`  
- `tools/verify_voice_v1_minimal_flow.py`  

这两个脚本构成当前阶段最小验证入口。

---

## H. 与 Resource Gate 的关系（顺序冻结）

- Resource Gate v0：先判定“**能不能执行**”（资源可行性）  
- Information Confirmation Gate v0：后判定“**是否已足够明确到可以执行**”（引用缺失/歧义）  
- 两者都属于 pre-submit admission gate，但职责不同；后续扩展不得打乱顺序，除非专项设计另行评审。  

参考：`docs/architecture/voice/LUNA_RESOURCE_SUFFICIENCY_GATE_V0_BASELINE.md`

---

## I. 下一阶段前置条件（Topic 02 扩展门槛）

- 若进入通用参数缺失 gate：必须单开专项设计与评审  
- 若进入目标地点/任务对象缺失的 schema 化 gate：必须单开专项设计与评审  
- 若要使用历史记忆辅助绑定：必须单开专项设计与评审  
- Topic 02 后续任何扩展必须以本 baseline 为冻结面，不得直接叠加复杂逻辑  

---

## 代码落点（事实索引）

- 判定逻辑：`capabilities/voice/runtime/voice_information_gate_v0.py`（`evaluate_missing_or_ambiguous_reference_v0`）  
- gate 落点：`capabilities/voice/runtime/voice_final_text_dispatcher.py`（`_apply_information_sufficiency_confirmation_gate_v0`；dispatch 后、submit 前）  
- 验证：`tools/verify_voice_confirmation_gate_v0.py`

