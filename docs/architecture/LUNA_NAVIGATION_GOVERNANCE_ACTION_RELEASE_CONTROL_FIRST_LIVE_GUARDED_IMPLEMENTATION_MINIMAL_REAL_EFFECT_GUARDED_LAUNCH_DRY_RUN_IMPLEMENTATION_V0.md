# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Guarded Launch Dry-Run Implementation v0（最小实现说明）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_GUARDED_LAUNCH_DRY_RUN_IMPLEMENTATION_V0.md`  
**性质**：Phase-Next-101：guarded launch dry-run 的最小非动作实现说明（落代码但不触发真实副作用）

关联（设计冻结）：
- guarded launch dry-run v0：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_GUARDED_LAUNCH_DRY_RUN_V0.md`

---

## A. 实现落点（写死）

Builder 落在：

- `capabilities/mid_platform/runtime/navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_dry_run_v0.py`

聚合写入仍由：

- `capabilities/voice/runtime/voice_final_text_dispatcher.py`

原因（写死）：

- 本仓库约定：运行时标准化对象统一由 dispatcher 汇聚写入 `result.metadata[...]`，避免多点写入与旁路。

---

## B. 输入（写死；只读标准化对象）

实现只消费（只读）：

- `result.metadata["navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_admission_gate_v0"]`（必须 admitted）
- `result.metadata["navigation_governance_action_release_control_first_live_enablement_approval_gate_v0"]`
- `result.metadata["navigation_governance_action_release_control_first_live_launch_dry_run_v0"]`
- `result.metadata["navigation_governance_action_release_control_live_release_gate_v0"]`
- `result.metadata["navigation_governance_action_release_control_side_effect_release_gate_v0"]`
- `result.metadata["navigation_governance_action_release_control_first_live_guarded_implementation_dry_effect_simulation_v0"]`
- `result.metadata["navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_dry_run_execution_v0"]`
- implementation skeleton identity（只读 `get_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_identity()`）
- `result.metadata["navigation_governance_action_release_control_execution_state_v0"]`
- `result.metadata["navigation_governance_action_release_control_result_v0"]`
- `result.metadata["side_effects_released"]`（若出现 True/异常值 => blocked）

并写死：

- 禁止直接读取 `request_* / approved_* / raw metadata`。

---

## C. 输出（写死）

写入：

- `result.metadata["navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_dry_run_v0"]`

最小结构（写死）：

```json
{
  "release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_dry_run_attempted": true,
  "release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_dry_run_scope": "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_dry_run_v0",
  "launch_status": "first_live_minimal_real_effect_launch_ready|first_live_minimal_real_effect_launch_not_ready|first_live_minimal_real_effect_launch_blocked",
  "side_effects_released": false,
  "reason": "..."
}
```

---

## D. relevant-only 规则（写死）

- 当 admission/gates/simulation/dry-run/state/result 等核心对象全部缺失时：不写入。
- 一旦出现任一核心对象：产出 attempted 对象并收敛为三态之一。

---

## E. 禁止面（写死）

- 不允许打开 `side_effects_released`
- 不允许真实写入/真实 `release_control`
- 不允许 route/voice/memory/migration/rollback/interrupt

