# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Non-Effect Wiring Implementation v0（非副作用接线：最小实现版）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_NON_EFFECT_WIRING_IMPLEMENTATION_V0.md`  
**性质**：Phase-Next-88：non-effect wiring 的最小非动作实现说明（落代码但不触发真实副作用）

关联（设计冻结）：
- non-effect wiring v0：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_NON_EFFECT_WIRING_V0.md`
- skeleton v0：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_SKELETON_V0.md`
- admission & acceptance v0：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_ADMISSION_AND_ACCEPTANCE_V0.md`

---

## A. 实现落点（写死）

最小 wiring builder 落在：

- `capabilities/mid_platform/runtime/navigation_governance_action_release_control_first_live_guarded_implementation_wiring_v0.py`

原因：

- mid_platform/runtime 已承担多处 gate / wiring 的聚合与 recognize-only 评估职责。
- wiring builder 只做“收束”，不做任何真实执行，放在 mid_platform 最不易失控。

---

## B. 输入（写死；只读标准化对象）

实现只消费（只读）：

- `result.metadata["navigation_governance_action_release_control_first_live_enablement_approval_gate_v0"]`
- `result.metadata["navigation_governance_action_release_control_first_live_launch_dry_run_v0"]`
- `result.metadata["navigation_governance_action_release_control_live_release_gate_v0"]`
- `result.metadata["navigation_governance_action_release_control_side_effect_release_gate_v0"]`
- skeleton identity / capability（来自 `capabilities/governance/runtime/...skeleton_v0.py` 的固定 identity）
- `result.metadata["navigation_governance_action_release_control_execution_state_v0"]`
- `result.metadata["navigation_governance_action_release_control_result_v0"]`

并写死：

- 不读取 `request_* / approved_* / raw metadata` 作为输入来源。

---

## C. 输出（写死）

实现写入：

- `result.metadata["navigation_governance_action_release_control_first_live_guarded_implementation_wiring_v0"]`

最小结构固定为：

```json
{
  "release_control_first_live_guarded_implementation_wiring_attempted": true,
  "release_control_first_live_guarded_implementation_wiring_scope": "navigation_governance_action_release_control_first_live_guarded_implementation_wiring_v0",
  "wiring_status": "first_live_guarded_wired_ready|first_live_guarded_wired_not_ready|first_live_guarded_wired_blocked",
  "side_effects_released": false,
  "reason": "..."
}
```

---

## D. relevant-only 规则（写死）

- 当上述“核心上游对象”完全不存在时：不写入 wiring（relevant-only）。
- 一旦任何核心对象存在：产出 attempted wiring 对象，并收敛为三态之一。

---

## E. 禁止面（写死）

- 不允许打开 `side_effects_released`
- 不允许执行真实 `release_control`
- 不允许触发 `rollback` / `interrupt`
- 不允许 route / voice / memory / migration
- 不允许越过标准对象吐散字段

