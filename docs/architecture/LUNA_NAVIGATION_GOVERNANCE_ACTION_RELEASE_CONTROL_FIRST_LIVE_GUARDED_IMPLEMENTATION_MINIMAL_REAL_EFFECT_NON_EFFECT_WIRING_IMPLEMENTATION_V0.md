# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Non-Effect Wiring Implementation v0（Minimal Real-Effect：非副作用接线最小实现说明）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_NON_EFFECT_WIRING_IMPLEMENTATION_V0.md`  
**性质**：Phase-Next-93：minimal real-effect non-effect wiring 的最小非动作实现说明（落代码但不触发真实副作用）

关联（设计冻结）：
- minimal real-effect non-effect wiring v0：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_NON_EFFECT_WIRING_V0.md`
- minimal real-effect stub v0：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_STUB_V0.md`
- dry-effect simulation：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_DRY_EFFECT_SIMULATION_V0.md`

---

## A. 实现落点（写死）

最小 wiring builder 落在：

- `capabilities/mid_platform/runtime/navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_wiring_v0.py`

原因：

- 与 Phase-Next-88 skeleton wiring 同一聚合层：只做“收束判定”，不做真实写入。
- stub 留在 `governance/runtime` 作为未来写入器壳子；接线评估放在 mid_platform 与既有 gate 组合模式一致，最小且连续。

---

## B. 输入（写死；只读标准化对象）

实现只消费（只读）：

- `result.metadata["navigation_governance_action_release_control_first_live_enablement_approval_gate_v0"]`
- `result.metadata["navigation_governance_action_release_control_first_live_launch_dry_run_v0"]`
- `result.metadata["navigation_governance_action_release_control_live_release_gate_v0"]`
- `result.metadata["navigation_governance_action_release_control_side_effect_release_gate_v0"]`
- `result.metadata["navigation_governance_action_release_control_first_live_guarded_implementation_dry_effect_simulation_v0"]`
- minimal real-effect stub identity（`get_release_control_first_live_guarded_implementation_minimal_real_effect_stub_identity()`）
- `result.metadata["navigation_governance_action_release_control_execution_state_v0"]`
- `result.metadata["navigation_governance_action_release_control_result_v0"]`

并写死：

- 不读取 `request_* / approved_* / raw metadata` 作为输入来源。

---

## C. 输出（写死）

实现写入：

- `result.metadata["navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_wiring_v0"]`

最小结构固定为：

```json
{
  "release_control_first_live_guarded_implementation_minimal_real_effect_wiring_attempted": true,
  "release_control_first_live_guarded_implementation_minimal_real_effect_wiring_scope": "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_wiring_v0",
  "wiring_status": "first_live_minimal_real_effect_wired_ready|first_live_minimal_real_effect_wired_not_ready|first_live_minimal_real_effect_wired_blocked",
  "side_effects_released": false,
  "reason": "..."
}
```

---

## D. relevant-only 规则（写死）

- 当上述来自 `metadata` 的核心上游对象（不含代码内固定的 stub identity）**全部**缺失时：`voice_final_text_dispatcher` 不调用评估、不写入 wiring。
- 一旦任一核心对象存在：产出 attempted wiring 对象，并收敛为三态之一。

---

## E. 禁止面（写死）

- 不允许打开 `side_effects_released`
- 不允许执行真实 `release_control`
- 不允许触发 `rollback` / `interrupt`
- 不允许 route / voice / memory / migration
- 不允许越过标准对象吐散字段

---

## F. Dispatcher 串联位置（写死）

- 在 `_maybe_attach_..._dry_effect_simulation_v0` **之后** 调用 minimal real-effect wiring，保证 dry-effect simulation 对象已就位（若链路产生）。
