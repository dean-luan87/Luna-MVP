# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Live Implementation Controlled Trial Shadow Trial Implementation v0（最小实现说明）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_SHADOW_TRIAL_IMPLEMENTATION_V0.md`  
**性质**：Phase-Next-139：shadow trial 的最小实现说明（observe-only；no-op writers；relevant-only metadata 追加；默认不开）

---

## A. 实现目标（写死）

把真实 minimal trial enablement code 以 observe-only 方式旁路运行：

- 强制替换三类 writer 为 no-op（仅内存 dict 返回）
- 不打开 `side_effects_released`
- 不改变主链输出，只追加一个 shadow trial 对象到 `result.metadata[...]`

---

## B. 代码落点（写死）

- shadow adapter：`capabilities/governance/runtime/navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_shadow_v0.py`
- dispatcher relevant-only 挂接：`capabilities/voice/runtime/voice_final_text_dispatcher.py`

---

## C. 输出（写死）

固定写入：

- `result.metadata["navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_shadow_v0"]`

三态：

- `shadow_trial_executed | shadow_trial_not_ready | shadow_trial_blocked`

并带 would-have 指标（由真实代码 trace 推导）。

---

## D. 默认不开（写死）

缺 `shadow_trial_enable_signal_v0` 时，必须输出 `shadow_trial_not_ready`（而不是执行）。

---

## E. 自测（写死）

- `tools/verify_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_shadow_v0.py`
- 覆盖：
  - relevant-only（无核心对象）
  - blocked（side_effects_released != False）
  - not_ready（缺 shadow_trial_enable_signal）
  - executed（前提齐备 + no-op writers）

