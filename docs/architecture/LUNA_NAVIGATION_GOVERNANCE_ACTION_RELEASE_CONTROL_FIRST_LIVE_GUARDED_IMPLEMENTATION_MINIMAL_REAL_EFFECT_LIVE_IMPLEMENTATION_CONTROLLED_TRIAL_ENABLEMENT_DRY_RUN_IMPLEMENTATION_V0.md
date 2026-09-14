# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Live Implementation Controlled Trial Enablement Dry-Run Implementation v0（最小实现说明）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_ENABLEMENT_DRY_RUN_IMPLEMENTATION_V0.md`  
**性质**：Phase-Next-136：enablement dry-run 的最小实现说明（只读、三态、固定顺序；不启用真实 trial；不进默认路径）

---

## A. 实现目标（写死）

把 enablement runner 的 runtime 入口按固定顺序跑通一遍（零副作用）：

- accept → enter → checks → exit
- 输出三态：executed | not_ready | blocked
- 只演练顺序，不做任何真实启用/写入/开关改变

---

## B. 代码落点（写死）

- `capabilities/governance/runtime/navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_enablement_dry_run_v0.py`
- 入口：`evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_enablement_dry_run_v0(...)`

---

## C. relevant-only（写死）

- 若 none of（核心 gate/runner/signal/side_effects_released）存在，则返回 `(False, None)`
- 否则返回 `(True, payload)`（payload 为 attempted dry-run 对象）

---

## D. 输出对象结构（摘要）

- `enablement_dry_run_attempted: true`
- `enablement_dry_run_scope: <scope>`
- `dry_run_status: first_live_minimal_real_effect_controlled_trial_enablement_dry_run_executed | ..._not_ready | ..._blocked`
- `side_effects_released: false`
- `reason: str`
- `dry_run_trace: { order: [...], accept: {...}, enter: {...}, checks: {...}, exit: {...} }`

---

## E. 固定顺序（写死）

1) `accept_first_live_minimal_real_effect_controlled_trial_enablement_input`  
2) `enter_first_live_controlled_trial_enablement_placeholder`  
3) `perform_first_live_controlled_trial_enablement_checks_placeholder`  
4) `exit_first_live_controlled_trial_enablement_placeholder`

---

## F. 自测（写死）

`tools/verify_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_enablement_dry_run_v0.py`

- relevant-only：无对象
- blocked：side_effects_released != False
- not_ready：accept != ready / 缺 dry-run signal
- executed：accept ready 且四步顺序走通

