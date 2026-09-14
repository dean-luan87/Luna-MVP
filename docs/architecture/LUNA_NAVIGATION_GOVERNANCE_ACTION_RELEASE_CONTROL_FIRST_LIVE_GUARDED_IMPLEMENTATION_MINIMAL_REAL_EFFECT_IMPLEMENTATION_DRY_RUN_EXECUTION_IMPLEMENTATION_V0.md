# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Implementation Dry-Run Execution Implementation v0（实现说明）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_IMPLEMENTATION_DRY_RUN_EXECUTION_IMPLEMENTATION_V0.md`  
**性质**：Phase-Next-98：implementation dry-run execution 的最小非动作实现说明（落代码但不触发真实副作用）

关联（设计冻结）：
- implementation dry-run execution v0：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_IMPLEMENTATION_DRY_RUN_EXECUTION_V0.md`
- implementation wiring v0：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_IMPLEMENTATION_NON_EFFECT_WIRING_V0.md`
- implementation skeleton v0：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_IMPLEMENTATION_SKELETON_V0.md`

---

## A. 实现落点（写死）

Runner 落在：

- `capabilities/governance/runtime/navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_dry_run_execution_v0.py`

原因（写死）：

- dry-run execution 是 implementation skeleton 的 companion runner（“执行顺序干跑”），语义上属于 implementation 侧（但仍是 non-effect）。
- 放在 `governance/runtime` 更贴近 skeleton，且不会污染 mid_platform 的 gate/wiring builder 语义层。

聚合写入仍由：

- `capabilities/voice/runtime/voice_final_text_dispatcher.py`

原因：

- 运行时标准化对象写入统一从 dispatcher 汇聚到 `result.metadata[...]`，避免多点写入与旁路。

---

## B. 输入（写死；只读标准化对象）

实现只消费（只读）：

- `result.metadata["navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_wiring_v0"]`
- implementation skeleton identity（通过 `get_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_identity()` 获取；只读）
- `result.metadata["navigation_governance_action_release_control_execution_state_v0"]`
- `result.metadata["navigation_governance_action_release_control_result_v0"]`

并写死：

- 禁止直接读取 `request_* / approved_* / raw metadata` 作为输入来源。

---

## C. 输出（写死）

写入：

- `result.metadata["navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_dry_run_execution_v0"]`

最小结构（写死）：

```json
{
  "release_control_first_live_guarded_implementation_minimal_real_effect_implementation_dry_run_execution_attempted": true,
  "release_control_first_live_guarded_implementation_minimal_real_effect_implementation_dry_run_execution_scope": "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_dry_run_execution_v0",
  "execution_status": "first_live_minimal_real_effect_implementation_dry_run_executed|first_live_minimal_real_effect_implementation_dry_run_not_ready|first_live_minimal_real_effect_implementation_dry_run_blocked",
  "side_effects_released": false,
  "execution_trace": {
    "execution_chain_order": [
      "execution_state_real_write_placeholder_call_from_implementation",
      "result_object_real_write_placeholder_call_from_implementation",
      "failure_or_exception_real_write_placeholder_closure_from_implementation"
    ]
  },
  "reason": "..."
}
```

---

## D. relevant-only 规则（写死）

- 当 wiring/state/result 核心对象全部缺失时：不写入 dry-run execution 对象。
- 一旦任一核心对象存在：产出 attempted dry-run object 并收敛为三态之一。

---

## E. 最小执行顺序（写死）

成功时必须固定顺序：

1) `write_first_live_execution_state_real_effect_from_implementation(...)`
2) `write_first_live_result_object_real_effect_from_implementation(...)`
3) `write_first_live_failure_or_exception_real_effect_from_implementation(...)`

并写死：

- 三步均为 skeleton 占位接口调用（placeholder-safe / stop-safe / reported-placeholder）。
- 不插入 route/voice/memory/migration/rollback/interrupt。

---

## F. 禁止面（写死）

实现强制：

- `side_effects_released: false`
- 不触发真实 `release_control / rollback / interrupt`
- 不改路线、不做语音/记忆/中台迁移

