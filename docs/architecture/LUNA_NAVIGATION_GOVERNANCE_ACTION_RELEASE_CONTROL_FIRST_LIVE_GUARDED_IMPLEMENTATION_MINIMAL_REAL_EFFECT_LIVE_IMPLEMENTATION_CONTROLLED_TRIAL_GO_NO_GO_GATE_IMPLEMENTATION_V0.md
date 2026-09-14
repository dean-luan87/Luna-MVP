# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Live Implementation Controlled Trial Go/No-Go Gate Implementation v0（最小非动作实现说明）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_GO_NO_GO_GATE_IMPLEMENTATION_V0.md`  
**性质**：Phase-Next-133：controlled trial go/no-go gate 的最小实现说明（只读、三态、relevant-only；不启用真实写入/默认路径）

---

## A. 实现目标（写死）

把“trial 已被准入（admitted）之后，本次是否真正启动 trial”收束成一个标准化 gate 对象：

- 输出三态：`controlled_trial_go | ..._no_go | ..._blocked`
- 只做“本次是否允许真正开始第一阶段受控真实 trial”的启动决策
- **不执行**任何真实写入
- **不打开** `side_effects_released`
- **不启用**任何默认路径

---

## B. 代码落点（写死）

gate builder 固定落在：

- `capabilities/mid_platform/runtime/navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_go_no_go_gate_v0.py`

核心入口：

- `evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_go_no_go_gate_v0(...)`

---

## C. relevant-only（写死）

- 如果 none of（trial_admission_gate / shadow_eval_gate / go-no-go / code-path-dry-run / wiring / live-dry-run / chain objects / signal）存在，则返回 `(False, None)`
- 否则返回 `(True, payload)`，其中 payload 为 attempted gate 对象（三态之一）

---

## D. 最小输入（写死）

只消费标准化对象（均只读）：

- controlled trial admission gate（必须 admitted）
- shadow evaluation gate（必须 eval_go）
- real-write go/no-go gate（必须 go）
- live code path dry-run（必须 executed）
- live implementation wiring（必须 wired_ready）
- live implementation dry-run execution（必须 executed）
- admission / launch / pre-commit / commit / activation 链路对象（必须 admitted/ready）
- rollout plan 在位（语义在位；本 gate 不实现 rollout）
- `side_effects_released`（必须 == False，否则 blocked）
- **controlled-trial go/no-go approval/signal**（默认不开；缺失则 no_go）

---

## E. 最小输出对象结构（摘要）

- `controlled_trial_go_no_go_attempted: true`
- `controlled_trial_go_no_go_scope: <scope>`
- `controlled_trial_go_no_go_status: first_live_minimal_real_effect_controlled_trial_go | ..._no_go | ..._blocked`
- `side_effects_released: false`
- `reason: str`
- `inputs_summary: { ... }`
- `consistency: { ... }`

---

## F. 判定规则（最小；写死）

- **blocked**：
  - `side_effects_released is not False`
- **no_go**：
  - 缺任一主前提（admission != admitted、shadow_eval != go、go/no-go != go、dry-run != executed、wiring != ready、链路不 ready/admitted、缺 go/no-go signal）
- **go**：
  - 主前提齐备 + go/no-go signal 在位

---

## G. 自测（写死）

- `tools/verify_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_go_no_go_gate_v0.py`
- 覆盖：
  - relevant-only（无任何对象）
  - blocked（side_effects_released != False）
  - no_go（缺 signal；或 admission != admitted；或 shadow_eval != go）
  - go（全条件满足）

