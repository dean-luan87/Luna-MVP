# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Live Implementation Controlled Trial Shadow Evaluation Gate Implementation v0（最小非动作实现说明）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_SHADOW_EVALUATION_GATE_IMPLEMENTATION_V0.md`  
**性质**：Phase-Next-140：controlled trial shadow evaluation gate 的最小实现说明（只读、三态、relevant-only；不启用真实 trial）

---

## A. 实现目标（写死）

把 controlled trial shadow 结果收束成一个标准化 gate 对象：

- 输出三态：`shadow_eval_go | shadow_eval_no_go | shadow_eval_blocked`
- 只做“是否允许进入下一阶段真实 controlled trial 准备态”的资格判断
- **不执行**任何真实启用/写入
- **不打开** `side_effects_released`

---

## B. 代码落点（写死）

gate builder 固定落在：

- `capabilities/mid_platform/runtime/navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_shadow_evaluation_gate_v0.py`

核心入口：

- `evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_shadow_evaluation_gate_v0(...)`

---

## C. relevant-only（写死）

- 如果 none of（shadow / gates / signals / side_effects_released）存在，则返回 `(False, None)`
- 否则返回 `(True, payload)`，payload 为 attempted gate 对象（三态之一）

---

## D. 最小输出对象结构（摘要）

- `controlled_trial_shadow_eval_attempted: true`
- `controlled_trial_shadow_eval_scope: <scope>`
- `controlled_trial_shadow_eval_status: first_live_minimal_real_effect_controlled_trial_shadow_eval_go | ..._no_go | ..._blocked`
- `side_effects_released: false`
- `reason: str`
- `inputs_summary: { ... }`
- `consistency: { ... }`

---

## E. 判定规则（最小；写死）

- **blocked**：`side_effects_released is not False`
- **no_go**：缺任一主前提 / 缺 evaluation signal / shadow 未达到质量线（executed + would-have 符合）
- **go**：主前提齐备 + shadow 质量线满足 + 与上游状态不冲突

---

## F. 自测（写死）

- `tools/verify_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_shadow_evaluation_gate_v0.py`
- 覆盖：relevant-only / blocked / no_go / go

