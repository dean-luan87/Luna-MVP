# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Live Implementation Controlled Trial Preparation Minimal Enablement Dry-Run Implementation v0（启用入口干跑最小实现说明）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_MINIMAL_ENABLEMENT_DRY_RUN_IMPLEMENTATION_V0.md`  
**性质**：Phase-Next-150：把 preparation enablement dry-run 从设计冻结推进为最小非动作实现说明（只演练顺序；不启用；不进默认路径）

---

## 1) 目标（写死）

- 在 `preparation go/no-go == go` 且 enablement runner `accept == ready` 的前提下，演练 enablement 入口固定 4 步顺序：
  - accept -> enter -> checks -> exit
- 输出统一的三态 dry-run 结果对象：
  - executed / not_ready / blocked

---

## 2) 代码落点（写死）

- dry-run runner：`capabilities/governance/runtime/navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_enablement_dry_run_v0.py`

---

## 3) relevant-only 策略（写死）

- 若输入侧核心对象均不存在（且 `side_effects_released` 未显式违约），返回 `(False, None)`
- 一旦检测到核心对象存在，则返回 `(True, attempted_object)`，attempted_object 内含三态 dry-run 状态

---

## 4) 固定顺序与 trace（写死）

- 必须记录并返回 `dry_run_trace.order`，顺序固定：
  1) `accept_first_live_minimal_real_effect_controlled_trial_preparation_enablement_input`
  2) `enter_first_live_controlled_trial_preparation_enablement_placeholder`
  3) `perform_first_live_controlled_trial_preparation_enablement_checks_placeholder`
  4) `exit_first_live_controlled_trial_preparation_enablement_placeholder`

---

## 5) 必须阻断的条件（写死）

- `side_effects_released is not False` → blocked

---

## 6) 必须 not_ready 的条件（写死）

- 缺少 `controlled_trial_preparation_enablement_dry_run_signal_v0`（显式干跑信号/批准）
- enablement runner `accept` 未返回 `{"ok": True, "status": "ready"}`（不得继续 enter/checks/exit）

---

## 7) 明确禁止（写死）

- 不允许打开 `side_effects_released`
- 不允许真实 preparation/trial 启用/默认路径启用
- 不允许真实写入 / route / voice / memory / migration
- 不允许 rollback / interrupt

