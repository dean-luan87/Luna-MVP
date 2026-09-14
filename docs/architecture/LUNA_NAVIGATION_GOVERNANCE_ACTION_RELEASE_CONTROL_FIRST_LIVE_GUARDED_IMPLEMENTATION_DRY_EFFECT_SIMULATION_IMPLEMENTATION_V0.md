# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Dry-Effect Simulation Implementation v0（Dry-Effect Simulation：最小实现版）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_DRY_EFFECT_SIMULATION_IMPLEMENTATION_V0.md`  
**性质**：Phase-Next-90：dry-effect simulation 的最小非动作实现说明（落代码但不触发真实副作用）

关联（设计冻结）：
- dry-effect simulation v0：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_DRY_EFFECT_SIMULATION_V0.md`
- minimal non-effect execution v0：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_NON_EFFECT_EXECUTION_V0.md`
- side-effect release contract v0：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_SIDE_EFFECT_RELEASE_CONTRACT_V0.md`
- skeleton v0：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_SKELETON_V0.md`

---

## A. 实现落点（写死）

最小 dry simulator 落在：

- `capabilities/governance/runtime/navigation_governance_action_release_control_first_live_guarded_implementation_dry_effect_simulation_v0.py`

原因：

- 这是 guarded implementation 的 companion simulator（只模拟未来副作用落点），放在 governance/runtime 最连续。
- simulator 不执行任何真实动作，只生成 targets 与禁止面检查结果，天然可锁死。

---

## B. 输入（写死；只读标准化对象）

实现只消费（只读）：

- `result.metadata["navigation_governance_action_release_control_first_live_guarded_implementation_non_effect_execution_v0"]`
- skeleton identity / capability（固定 identity；必须保守能力）
- `result.metadata["navigation_governance_action_release_control_execution_state_v0"]`
- `result.metadata["navigation_governance_action_release_control_result_v0"]`

并写死：

- 禁止读取 `request_* / approved_* / raw metadata` 作为输入来源。

---

## C. 输出（写死）

实现写入：

- `result.metadata["navigation_governance_action_release_control_first_live_guarded_implementation_dry_effect_simulation_v0"]`

最小结构固定为：

```json
{
  "release_control_first_live_guarded_implementation_dry_effect_simulation_attempted": true,
  "release_control_first_live_guarded_implementation_dry_effect_simulation_scope": "navigation_governance_action_release_control_first_live_guarded_implementation_dry_effect_simulation_v0",
  "simulation_status": "first_live_guarded_dry_effect_simulated|first_live_guarded_dry_effect_not_ready|first_live_guarded_dry_effect_blocked",
  "side_effects_released": false,
  "simulation_targets": [
    "execution_state_update_target",
    "result_object_update_target",
    "failure_or_exception_path_target"
  ],
  "reason": "..."
}
```

---

## D. 禁止面检查（写死）

- `simulation_targets` 必须严格落在三类允许目标内。
- 任何 route/voice/memory/migration/rollback/interrupt/map 目标一旦出现，必须判定 `blocked`。

