# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Dry-Run Execution Implementation v0（干跑执行链：最小实现说明）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_DRY_RUN_EXECUTION_IMPLEMENTATION_V0.md`  
**性质**：Phase-Next-94：minimal real-effect dry-run execution 的最小非动作实现说明（落代码但不触发真实副作用）

关联（设计冻结）：
- dry-run execution v0：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_DRY_RUN_EXECUTION_V0.md`
- minimal real-effect stub：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_STUB_V0.md`
- minimal real-effect wiring：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_NON_EFFECT_WIRING_V0.md`

---

## A. 实现落点（写死）

Dry-run runner 落在：

- `capabilities/governance/runtime/navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_dry_run_execution_v0.py`

原因：

- 与「non-effect execution」同属 **governance/runtime** 下的受控执行链评估；干跑链直接调用 **minimal real-effect stub** 占位 API，放在同一治理层边界内最连续。
- 不放入 `mid_platform`：本层不是 gate 收束，而是 stub 调用顺序验证，与 stub 同包系更不易误用为“中台策略”。

**不单独拆 helper 文件**：本轮顺序固定、体量小；若后续膨胀再拆 `*_runner_helpers`。

---

## B. 输入（写死；只读标准化对象）

实现只消费（只读）：

- `result.metadata["navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_wiring_v0"]`
- minimal real-effect stub identity（`get_release_control_first_live_guarded_implementation_minimal_real_effect_stub_identity()`）
- `result.metadata["navigation_governance_action_release_control_execution_state_v0"]`
- `result.metadata["navigation_governance_action_release_control_result_v0"]`

并写死：

- 不读取 `request_* / approved_* / raw metadata` 作为输入来源。

---

## C. 输出（写死）

写入：

- `result.metadata["navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_dry_run_execution_v0"]`

`execution_trace.execution_chain_order` 固定为三步（与设计文档一致）。

---

## D. relevant-only 规则（写死）

- 当 `minimal real_effect_wiring_v0`、`execution_state_v0`、`result_v0` **全部**缺失（且不把代码内固定的 stub identity 算作 metadata 上游）时：`voice_final_text_dispatcher` 不调用评估、不写入 dry-run 对象。
- 一旦任一核心 metadata 对象存在：产出 attempted 对象并收敛为三态之一。

---

## E. Dispatcher 串联位置（写死）

- 在 `_maybe_attach_..._minimal_real_effect_wiring_v0` **之后**调用 dry-run execution，保证 wiring 对象已写入（若链路产生）。

---

## F. 禁止面（写死）

同设计文档 G 节；实现层强制 `side_effects_released: false`。
