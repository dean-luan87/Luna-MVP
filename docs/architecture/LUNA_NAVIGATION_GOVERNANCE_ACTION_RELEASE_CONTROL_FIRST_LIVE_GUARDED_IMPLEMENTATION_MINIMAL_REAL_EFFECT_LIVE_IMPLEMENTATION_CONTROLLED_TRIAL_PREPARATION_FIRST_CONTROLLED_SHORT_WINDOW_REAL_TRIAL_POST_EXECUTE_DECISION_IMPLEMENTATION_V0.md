# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Live Implementation Controlled Trial Preparation First Controlled Short-Window Real Trial Post-Execute Decision Implementation v0

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_FIRST_CONTROLLED_SHORT_WINDOW_REAL_TRIAL_POST_EXECUTE_DECISION_IMPLEMENTATION_V0.md`  
**阶段**：Phase-Next-164  
**性质**：第一版 post-execute decision runtime（只读治理性），严格受 151/155/158/159/162/163 约束。  
**非目标**：不 default-on、不 full controlled trial continuation、不打开 release window、不触发自动 retry/reopen/widen、不扩大 side effects 面。

---

## 1) 本阶段新增产物

- **164 runtime**：`capabilities/governance/runtime/navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_first_controlled_short_window_real_trial_post_execute_decision_v0.py`
- **164 verifier**：`tools/verify_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_first_controlled_short_window_real_trial_post_execute_decision_v0.py`

---

## 2) 164 如何映射 163 decision constitution（逐条对齐）

### 2.1 非默认显式入口

- 164 runtime 强制 `explicit_post_execute_decision_entry_v0` 为 dict 且 `intent=true`，否则 `blocked` 且 outcome 固定为 `remain_closed_safe`。

### 2.2 只能在 execute 已合法 final close 后进入 decision

- 164 runtime 从 `execute_result_v0.payload.state` 读取并强制：
  - `closed == true`
  - `side_effects_released == false`
- 任一不满足 => `not_eligible` 且 outcome = `remain_closed_safe`。

### 2.3 只读治理性：不得打开新的 release window / 不得触发真实动作

- 164 runtime **不调用任何写入器**，不触发任何执行/重试，仅输出治理 outcome。
- 强制 `closed_safe_state_preserved=true` 且 `allows_retry_now=false`（无自动重试通道）。

### 2.4 evidence completeness / audit integrity

- 164 runtime 以最小证据集合判定 `evidence_complete_seen`（至少要求 trace.order 非空 + status/reason 存在）。
- 证据不完整 => outcome = `remain_closed_safe`（保守）。

### 2.5 allowed outcomes only（163 白名单）

- 164 runtime 只允许输出：
  - `remain_closed_safe`
  - `retry_allowed_under_same_guardrails`
  - `retry_not_allowed_until_new_definition`
  - `escalate_for_new_governance_definition`
  - `stop_and_block_further_real_action`
- 任一非白名单 outcome 会被视为 illegal 并强制降级到 `remain_closed_safe`。

### 2.6 forbidden outcomes blocking（163 黑名单）

- 164 runtime 支持 `requested_forbidden_outcome_probe`（用于验证），若命中：
  - `implicit_reopen`
  - `implicit_execute_retry`
  - `implicit_widening`
  - `implicit_full_trial_continuation`
  - `implicit_default_on_transition`
 立即 `blocked`，并标记 `forbidden_outcome_blocked=true`，outcome 固定为 `remain_closed_safe`。

### 2.7 retry / escalate / stop / remain_closed 的边界

- 若发现 boundary violation（从 execute abort/stop trigger 推断）或 execute_legality 不确定：
  - outcome = `retry_not_allowed_until_new_definition`
- 若 `widening_needed=true`：
  - outcome = `escalate_for_new_governance_definition`
- 若 `structural_safety_issue=true`：
  - outcome = `stop_and_block_further_real_action`
- 干净证据路径：
  - outcome = `retry_allowed_under_same_guardrails`，并强制：
    - `human_confirmation_required=true`
    - `allows_retry_now=false`（仅治理结论，不自动重试）

---

## 3) 164 的真实入口是什么

- `run_first_controlled_short_window_real_trial_post_execute_decision_v0(...)`（显式调用；无默认路径）

---

## 4) 验证覆盖（verifier）

164 verifier 覆盖 A–K 场景，重点断言：

- 无合法 final close => 不得进入 decision（remain_closed_safe）
- se 不为 false => 不得进入 decision（remain_closed_safe）
- 证据不完整 => remain_closed_safe
- 干净证据 => 可输出 retry_allowed_under_same_guardrails，但不允许自动重试（allows_retry_now=false）
- boundary violation => retry_not_allowed_until_new_definition
- widening_needed => escalate_for_new_governance_definition
- forbidden probes => blocked + remain_closed_safe
- default_path_probe => blocked
- structural safety => stop_and_block_further_real_action

---

## 5) 明确声明（写死）

- 默认路径仍未开启
- 本阶段未进入 full controlled trial
- 本阶段未扩大真实 side effects 面
- 本阶段只是 post-execute decision implementation v0，不代表自动继续运行

