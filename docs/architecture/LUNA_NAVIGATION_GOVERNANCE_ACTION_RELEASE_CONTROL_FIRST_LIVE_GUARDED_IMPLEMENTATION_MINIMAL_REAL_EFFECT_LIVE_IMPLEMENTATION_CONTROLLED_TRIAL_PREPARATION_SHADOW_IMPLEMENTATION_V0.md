# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Live Implementation Controlled Trial Preparation Shadow Implementation v0（准备态真实代码 shadow 最小实现说明）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_SHADOW_IMPLEMENTATION_V0.md`  
**性质**：Phase-Next-145：把 preparation shadow plan 推进到最小 observe-only 实现说明（不接默认路径；不改 dispatcher）

---

## 1) 目标（写死）

- 旁路调用真实 minimal preparation code，但把三类写入器全部替换为 no-op writer
- 产出标准化 `preparation_shadow_*` 对象，包含 would-have flags 与 live 结果回传（仅用于观察）

---

## 2) 代码落点（写死）

- shadow adapter：`capabilities/governance/runtime/navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_shadow_v0.py`

---

## 3) relevant-only 策略（写死）

- 若输入侧核心对象均不存在，则返回 `(False, None)`
- 一旦检测到核心对象存在，则返回 `(True, attempted_object)`，attempted_object 内含三态 shadow 状态

---

## 4) 三态输出（写死）

- `preparation_shadow_executed`
- `preparation_shadow_not_ready`
- `preparation_shadow_blocked`

---

## 5) 关键硬边界（写死）

- `side_effects_released is not False`：shadow 直接 blocked
- 无显式 `preparation_shadow_enable_signal_v0`：not_ready
- 真实 preparation 执行入口必须以 no-op writers 调用（禁止真实写入）
- 不接默认路径、不改变主链输出

