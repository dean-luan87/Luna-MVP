# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Live Implementation Shadow Evaluation Gate Implementation v0（最小非动作实现说明）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_SHADOW_EVALUATION_GATE_IMPLEMENTATION_V0.md`  
**性质**：Phase-Next-131：shadow evaluation gate 的最小实现说明（只读、三态、relevant-only；不启用真实写入）

---

## A. 实现目标（写死）

把 shadow observe-only 结果收束成一个标准化 gate 对象：

- 输出三态：`shadow_eval_go | shadow_eval_no_go | shadow_eval_blocked`
- 只做“是否允许进入下一阶段受控真实试运行前评估”的资格判断
- **不执行**任何真实写入
- **不打开** `side_effects_released`

---

## B. 代码落点（写死）

gate builder 固定落在：

- `capabilities/mid_platform/runtime/navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_shadow_evaluation_gate_v0.py`

核心入口：

- `evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_shadow_evaluation_gate_v0(...)`

---

## C. relevant-only（写死）

- 如果 none of（shadow / go-no-go / code-path-dry-run / wiring / live-dry-run / chain objects / signals）存在，则返回 `(False, None)`（不产出 gate 对象）
- 否则返回 `(True, payload)`，其中 payload 为 attempted gate 对象（三态之一）

---

## D. 最小输入（写死）

只消费标准化对象（均只读）：

- `navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_shadow_v0`
- `...real_write_go_no_go_gate_v0`
- `...live_code_path_dry_run_v0`
- `...live_implementation_wiring_v0`
- `...live_implementation_dry_run_execution_v0`
- admission / launch / pre-commit / commit / activation 链路对象
- `side_effects_released`（必须 == False，否则 blocked）
- `...shadow_evaluation_signal_v0`（默认不开；缺失则 no_go）

---

## E. 最小输出对象结构（摘要）

固定输出键（由上游接线层决定写入 metadata 的 key；gate 本身只返回 payload）：

- `shadow_eval_attempted: true`
- `shadow_eval_scope: <scope>`
- `shadow_eval_status: first_live_minimal_real_effect_shadow_eval_go | ..._no_go | ..._blocked`
- `side_effects_released: false`
- `reason: str`
- `inputs_summary: { ... }`（只放“是否存在/是否匹配”的摘要，不散落原始 request 字段）
- `consistency: { ... }`（与上游状态是否一致的布尔摘要）

---

## F. 判定规则（最小；写死）

- **blocked**：
  - `side_effects_released is not False`
- **no_go**：
  - 缺任一主前提（go/no-go != go、code path dry-run != executed、wiring != wired_ready、live dry-run != executed、链路不 ready/admitted、缺 shadow 对象、缺 shadow evaluation signal）
  - 或 shadow 自身不满足最小质量线（`shadow_status != shadow_executed`、`would_have_entered_real_write != true`、would-have 标记缺失/不一致）
- **go**：
  - 主前提齐备且 shadow 最小质量线满足，且与上游状态不冲突（冲突则 no_go，理由写明）

---

## G. 自测（写死）

- `tools/verify_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_shadow_evaluation_gate_v0.py`
- 覆盖：
  - relevant-only（无任何对象）
  - blocked（side_effects_released != False）
  - no_go（缺 signal；或 shadow_status != executed；或上游状态不匹配）
  - go（全条件满足）

