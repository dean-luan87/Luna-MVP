# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Implementation Non-Effect Wiring Implementation v0（实现说明）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_IMPLEMENTATION_NON_EFFECT_WIRING_IMPLEMENTATION_V0.md`  
**性质**：Phase-Next-97：implementation non-effect wiring 的最小非动作实现说明（落代码但不触发真实副作用）

关联（设计冻结）：
- implementation non-effect wiring v0：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_IMPLEMENTATION_NON_EFFECT_WIRING_V0.md`
- implementation skeleton v0：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_IMPLEMENTATION_SKELETON_V0.md`

---

## A. 实现落点（写死）

Wiring builder 落在：

- `capabilities/mid_platform/runtime/navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_wiring_v0.py`

原因（写死）：

- 这是“标准化对象的收束/接线 builder”，语义上与既有 gate / wiring builder 的放置方式一致。
- 该层只产出三态 wiring 结果，不执行任何治理动作；放在 `mid_platform/runtime` 更不易被误用为“实现层”。

聚合写入仍由：

- `capabilities/voice/runtime/voice_final_text_dispatcher.py`

原因：

- 本仓库约定：运行时标准化对象写入统一从 dispatcher 汇聚到 `result.metadata[...]`，避免多点写入。

---

## B. 输入（写死；只读标准化对象）

实现只消费（只读）：

- `result.metadata["navigation_governance_action_release_control_first_live_enablement_approval_gate_v0"]`
- `result.metadata["navigation_governance_action_release_control_first_live_launch_dry_run_v0"]`
- `result.metadata["navigation_governance_action_release_control_live_release_gate_v0"]`
- `result.metadata["navigation_governance_action_release_control_side_effect_release_gate_v0"]`
- `result.metadata["navigation_governance_action_release_control_first_live_guarded_implementation_dry_effect_simulation_v0"]`
- `result.metadata["navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_dry_run_execution_v0"]`
- implementation skeleton identity（通过 `get_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_identity()` 获取；只读）
- `result.metadata["navigation_governance_action_release_control_execution_state_v0"]`
- `result.metadata["navigation_governance_action_release_control_result_v0"]`

并写死：

- 禁止直接读取 `request_* / approved_* / raw metadata` 作为输入来源。

---

## C. 输出（写死）

写入：

- `result.metadata["navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_wiring_v0"]`

最小结构（写死）：

```json
{
  "release_control_first_live_guarded_implementation_minimal_real_effect_implementation_wiring_attempted": true,
  "release_control_first_live_guarded_implementation_minimal_real_effect_implementation_wiring_scope": "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_wiring_v0",
  "wiring_status": "first_live_minimal_real_effect_implementation_wired_ready|first_live_minimal_real_effect_implementation_wired_not_ready|first_live_minimal_real_effect_implementation_wired_blocked",
  "side_effects_released": false,
  "reason": "..."
}
```

---

## D. relevant-only 规则（写死）

- 当 approval/launch/release/simulation/dry-run/state/result 等核心对象 **全部缺失**（且 skeleton identity 也无法获取）时：dispatcher 不调用评估、不写入 wiring 对象。
- 一旦任一核心对象存在：产出 attempted wiring 对象并收敛为三态之一。

---

## E. Dispatcher 串联位置（写死）

- 在 `minimal real-effect dry-run execution v0` **之后**接入 implementation wiring，保证 dry-run 对象可作为 wiring 的输入前提之一。

---

## F. 禁止面（写死）

实现层强制：

- `side_effects_released: false`
- 不触发真实 `release_control / rollback / interrupt`
- 不改路线、不做语音/记忆/中台迁移

