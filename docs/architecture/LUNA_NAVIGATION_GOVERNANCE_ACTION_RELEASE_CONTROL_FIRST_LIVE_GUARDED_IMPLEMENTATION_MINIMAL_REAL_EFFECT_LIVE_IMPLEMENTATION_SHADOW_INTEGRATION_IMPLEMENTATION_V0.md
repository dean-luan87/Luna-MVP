# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Live Implementation Shadow Integration Implementation v0（旁路观察最小实现）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_SHADOW_INTEGRATION_IMPLEMENTATION_V0.md`  
**性质**：Phase-Next-130：把 Phase-Next-129 的 shadow integration plan 落成 **observe-only** 最小实现（只追加 metadata；不真实写入；不影响主链输出；默认不开）

---

## A. 本实现的唯一目标（写死）

把第一版真实最小写入代码：

- `capabilities/governance/runtime/navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_v0.py`

以 **shadow / observe-only** 方式旁路挂到主链旁边，只输出一个 shadow 结果对象到 `result.metadata[...]`，并且：

- **不打开** `side_effects_released`
- **不做任何真实写入**（三类写入全部替换为 no-op writer）
- **不改变主链输出**（主链最终文本/主链语义不变）

---

## B. 代码落点（写死）

### B1. Shadow adapter / runner

- **新增**：`capabilities/governance/runtime/navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_shadow_v0.py`
- **核心入口**：`evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_shadow_v0(...)`

### B2. 主链挂接点（relevant-only metadata 追加）

- **修改**：`capabilities/voice/runtime/voice_final_text_dispatcher.py`
- **行为**：在已有 relevant-only 逻辑处追加：
  - `result.metadata["navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_shadow_v0"] = <shadow payload>`

---

## C. 最小输入（写死；只消费标准对象）

Shadow adapter 只允许消费下列标准对象（缺任一关键前提都不得输出 `shadow_executed`）：

- `navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_real_write_go_no_go_gate_v0`
  - 需要：`real_write_status == "first_live_minimal_real_effect_real_write_go"`
- `navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_code_path_dry_run_v0`
  - 需要：`dry_run_status == "first_live_minimal_real_effect_live_code_path_dry_run_executed"`
- `side_effects_released` 必须是 `False`
- **显式 shadow enable/signal**（默认不开）：
  - `navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_shadow_enable_signal_v0`（dict）
- 三个核心对象（保持与真实最小写入入口一致）：
  - `navigation_governance_action_release_control_execution_state_v0`
  - `navigation_governance_action_release_control_result_v0`
  - `exception_or_failure_path_v0`

---

## D. 最小输出（写死；三态）

固定写入：

- `result.metadata["navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_shadow_v0"]`

最小结构（字段名写死）：

- `shadow_attempted: true`
- `shadow_scope: "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_shadow_v0"`
- `shadow_status: "shadow_executed" | "shadow_not_ready" | "shadow_blocked"`
- `side_effects_released: false`
- `reason: str`
- `would_have_entered_real_write: bool`
- `would_have_written_execution_state: bool`
- `would_have_written_result_object: bool`
- `would_have_written_exception_or_failure: bool`
- `live_implementation_result: <dict>`（observe-only 运行结果；只用于对比，不改变主链语义）

---

## E. 最小执行策略（写死）

当且仅当所有前提满足时，shadow adapter 才会：

1) 以 `shadow_enable_signal_v0` 作为 `real_write_approval_or_signal_v0`，调用真实最小写入入口（但 writer 被替换为 no-op）  
2) 记录真实最小写入返回的 `trace.order` 以推导 would-have 指标  
3) 将 shadow payload 写入 metadata（observe-only）

其中：

- no-op writer **必须只返回内存内 dict**，不得触达文件/网络/外部存储
- `side_effects_released` 在 shadow 全程保持 `False`（不允许进入任何真实激活语义）

---

## F. 自测（写死）

- **新增**：`tools/verify_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_shadow_v0.py`
- 覆盖：
  - executed（所有前提满足 + no-op writers）
  - not_ready（缺 shadow signal / 缺 go-no-go / 缺 code path dry-run）
  - blocked（side_effects_released != False）
  - relevant-only（无核心对象时不输出）

同时回归运行：

- `tools/verify_voice_v1_minimal_flow.py`

确保主链输出与既有 metadata 不被破坏（仅新增一个 shadow metadata 键，且默认不触发 `shadow_executed`）。

