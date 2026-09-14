# Luna — Navigation Governance Action Release Control Live Release Gate Minimal Implementation v0（放行门：最小非动作实现）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_LIVE_RELEASE_GATE_IMPLEMENTATION_V0.md`  
**性质**：Phase-Next-76：把 `live release gate` 从设计冻结推进为统一对象的最小非动作实现（落代码；不触发真实动作）

关联：
- gate 冻结：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_LIVE_RELEASE_GATE_V0.md`
- guarded live stub：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_GUARDED_LIVE_STUB_V0.md`
- executor input bridge（最小实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_EXECUTOR_INPUT_BRIDGE_IMPLEMENTATION_V0.md`
- execution state / result（实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_EXECUTION_STATE_IMPLEMENTATION_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_RESULT_OBJECT_IMPLEMENTATION_V0.md`

---

## A. 文档定位（写死）

- 这是 `release_control live release gate` 的最小非动作实现文档。
- 当前目标：把 gate 从冻结文档推进到最小非动作实现（统一对象输出）。
- 当前不做真实 `release_control`。
- 当前不做 `rollback` / `interrupt`。
- 当前不接地图。
- 当前不驱动语音/记忆。
- 当前不改变现有主线行为。

---

## B. 为什么现在要先实现 live release gate

- guarded live stub 已存在（可进入 candidate，但 side effects 锁死）。
- executor input bridge 已有实现输出位。
- execution state / result object 都已有 implemented object。
- gate 的合法输入与结果集合已冻结。
- 若没有最小实现，后续真实 live implementation 会回到各模块各自判断“是否可以放开 side effect”，边界会脏。
- 因此必须先把 gate 对象实现出来，但当前仍不能触发任何真实治理动作。

---

## C. implemented live release gate 的最小定义（写死）

- 它不是真实 `release_control` 执行器。
- 不是真实批准链。
- 它是“guarded live stub 之后、真实 live execution 之前的最后一道放行门”的最小非动作实现版。
- 作用：把 bridge、guarded live candidate、execution state、result object、identity/capability 统一收束成 `live_release_ready|not_ready|blocked` 结果。

---

## D. 当前最小输入依据（写死：只读标准化对象）

主输入：

1) `navigation_governance_action_release_control_executor_input_bridge_v0`（必须 `executor_input_bridge_ready`）  
2) guarded live stub 状态（必须已 entered candidate 且 `side_effects_released == false`）  
3) `navigation_governance_action_release_control_execution_state_v0`（在位）  
4) `navigation_governance_action_release_control_result_v0`（在位）  
5) identity/capability（minimal executor + guarded live stub，均必须保守且不可真实执行）  

可选只读：
- readiness gate、wiring（仅一致性观测，不扩权）

---

## E. 当前最小输出位（写死）

写入：
- `result.metadata["navigation_governance_action_release_control_live_release_gate_v0"]`

最小结构：

```json
{
  "release_control_live_release_gate_attempted": true,
  "release_control_live_release_gate_scope": "navigation_governance_action_release_control_live_release_gate_v0",
  "live_release_status": "live_release_ready|live_release_not_ready|live_release_blocked",
  "side_effects_released": false,
  "reason": "..."
}
```

写死：
- `side_effects_released` 必须保持 `false`
- `live_release_ready` 不等于动作开始

---

## F. 代码落点（本轮落地）

- Builder：`capabilities/mid_platform/runtime/navigation_governance_action_release_control_live_release_gate_v0.py`
- 聚合写入：`capabilities/voice/runtime/voice_final_text_dispatcher.py`
- guarded live stub recognize-only：`capabilities/governance/runtime/navigation_governance_action_release_control_guarded_live_stub_v0.py`

