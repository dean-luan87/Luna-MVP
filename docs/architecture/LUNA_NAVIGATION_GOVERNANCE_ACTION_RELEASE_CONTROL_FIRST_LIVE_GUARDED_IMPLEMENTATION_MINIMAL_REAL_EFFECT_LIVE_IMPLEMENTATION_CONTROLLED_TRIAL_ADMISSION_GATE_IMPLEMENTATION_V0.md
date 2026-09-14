# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Live Implementation Controlled Trial Admission Gate Implementation v0（最小非动作实现说明）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_ADMISSION_GATE_IMPLEMENTATION_V0.md`  
**性质**：Phase-Next-132：controlled trial admission gate 的最小实现说明（只读、三态、relevant-only；不启用真实写入/默认路径）

---

## A. 实现目标（写死）

把“从 shadow 观察阶段 → controlled trial（受控真实试运行准备态）”收束成一个标准化 gate 对象：

- 输出三态：`controlled_trial_admitted | ...not_admitted | ...blocked`
- 只做“是否允许进入 controlled trial 准备态”的资格判断
- **不执行**任何真实写入
- **不打开** `side_effects_released`
- **不启用**任何默认路径

---

## B. 代码落点（写死）

gate builder 固定落在：

- `capabilities/mid_platform/runtime/navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_admission_gate_v0.py`

核心入口：

- `evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_admission_gate_v0(...)`

---

## C. relevant-only（写死）

- 如果 none of（shadow / shadow_eval_gate / go-no-go / code-path-dry-run / wiring / live-dry-run / chain objects / signals）存在，则返回 `(False, None)`（不产出 gate 对象）
- 否则返回 `(True, payload)`，其中 payload 为 attempted gate 对象（三态之一）

---

## D. 最小输入（写死）

只消费标准化对象（均只读）：

- shadow object：`...live_implementation_shadow_v0`
- shadow evaluation gate：`...shadow_evaluation_gate_v0`（必须 eval_go）
- real-write go/no-go gate（必须 go）
- live code path dry-run（必须 executed）
- live implementation wiring（必须 wired_ready）
- live implementation dry-run execution（必须 executed）
- admission / launch / pre-commit / commit / activation 链路对象（必须 admitted/ready）
- rollout plan 在位（语义在位；本 gate 不实现 rollout）
- `side_effects_released`（必须 == False，否则 blocked）
- **controlled-trial admission signal**（默认不开；缺失则 not_admitted）

---

## E. 最小输出对象结构（摘要）

- `controlled_trial_attempted: true`
- `controlled_trial_scope: <scope>`
- `controlled_trial_status: first_live_minimal_real_effect_controlled_trial_admitted | ..._not_admitted | ..._blocked`
- `side_effects_released: false`
- `reason: str`
- `inputs_summary: { ... }`（只放“是否存在/是否匹配”的摘要）
- `consistency: { ... }`（与上游状态是否一致的布尔摘要）

---

## F. 判定规则（最小；写死）

- **blocked**：
  - `side_effects_released is not False`
- **not_admitted**：
  - 缺任一主前提（shadow_eval != go、go/no-go != go、code path dry-run != executed、wiring != wired_ready、live dry-run != executed、链路不 ready/admitted、缺 admission signal）
  - 或 shadow 质量线不满足（例如 would-have 指标缺失/不一致）
- **admitted**：
  - 主前提齐备 + shadow_eval_go + admission signal 在位 + shadow 指标满足最小质量线

---

## G. 自测（写死）

- `tools/verify_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_admission_gate_v0.py`
- 覆盖：
  - relevant-only（无任何对象）
  - blocked（side_effects_released != False）
  - not_admitted（缺 signal；或 shadow_eval != go；或上游状态不匹配）
  - admitted（全条件满足）

