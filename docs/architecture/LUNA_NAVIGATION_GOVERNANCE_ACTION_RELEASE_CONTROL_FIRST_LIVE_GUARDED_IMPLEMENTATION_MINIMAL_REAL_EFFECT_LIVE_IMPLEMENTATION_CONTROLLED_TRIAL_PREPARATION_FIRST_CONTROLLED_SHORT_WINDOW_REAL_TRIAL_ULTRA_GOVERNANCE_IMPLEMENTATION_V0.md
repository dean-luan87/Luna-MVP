# Phase-Next-184 — Ultra-Governance Implementation v0（只读治理 runtime；非默认入口）

**阶段名**：First Controlled Short-Window Real Trial Ultra-Governance Implementation v0  
**性质**：实现（runtime）但只读治理；不新增运行时放行能力；不启用默认路径；不进入 full controlled trial；不扩大真实 side effects 面  
**受约束冻结链**：151/155/158/159/162/163/166/167/170/171/174/175/178/179/182/183  

---

## 1) 本阶段唯一 runtime（代码路径）

- `capabilities/governance/runtime/navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_first_controlled_short_window_real_trial_ultra_governance_v0.py`

该文件是 Phase-Next-184 唯一 ultra-governance runtime。

---

## 2) 明确非目标（避免误读）

本实现 **不**做：
- 不开启默认路径（default-on 禁止）
- 不打开新的 real side-effects window
- 不触发 execute / retry / reopen / runtime continuation
- 不提供 long-running enablement
- 不进入 full controlled trial
- 不修改 151/155/…/183 的任何冻结语义与结论

---

## 3) 184 如何逐条映射 183 宪法（硬边界映射）

### 3.1 Non-default explicit entry（183-E）

- 输入对象字段：`explicit_ultra_governance_entry_intent_v0`  
- runtime 输出字段：`explicit_ultra_governance_entry_seen`  
若入口不显式，强制回落：`remain_closed_safe`，并标记 `illegal_state_detected=true`。

### 3.2 Supra-governance legality prerequisite（183-E/F）

184 只接受 `supra_governance_bundle`，并要求：
- `supra_governance_completed_seen=true`
- `supra_governance_legality_seen=true`

不满足则不得进入 ultra-governance judgement，强制保守输出并标记非法。

### 3.3 Closed-safe prerequisite（183-E/K）

184 要求 bundle 显示 closed-safe 成立：
- `closed_safe_state_seen=true`

不满足时，强制：
- `block_further_real_action_until_manual_override`
- `illegal_state_detected=true`
- 并保持 closed-safe 不变量（见 3.6）。

### 3.4 Evidence / audit prerequisites（183-J）

184 读取：
- `evidence_complete_seen`
- `audit_trace_intact_seen`

若证据或审计 trace 不完整，则输出：
- `require_new_evidence_before_any_further_governance`
并保持 `allows_next_runtime_now=false`。

### 3.5 Allowed outcomes only（183-G）

184 只能输出白名单五项：
- `remain_closed_safe`
- `require_new_evidence_before_any_further_governance`
- `escalate_for_new_governance_definition`
- `allow_next_governance_preparation_under_same_guardrails`
- `block_further_real_action_until_manual_override`

任何 allowlist 外 outcome 都会被强制回落到 `remain_closed_safe` 并标记非法。

### 3.6 Forbidden outcome blocking（183-H）

184 检测 `forbidden_signals`（以及兼容的字段变体），若命中 forbidden 集合：
`implicit_reopen / implicit_retry_runtime / implicit_widening / implicit_full_trial_continuation / implicit_default_on_transition / implicit_long_running_enablement ...`

则强制：
- `forbidden_ultra_governance_outcome_blocked=true`
- `allowed_ultra_governance_outcome_selected=block_further_real_action_until_manual_override`
- `illegal_state_detected=true`

### 3.7 No-next-runtime-now（183-G/K）

184 硬写死：
- `allows_next_runtime_now=false`

即使输出 `allow_next_governance_preparation_under_same_guardrails` 也不自动进入下一阶段 runtime。

### 3.8 Post-governance safety state（183-K）

184 硬写死：
- `keeps_system_closed=true`
- `closed_safe_state_preserved=true`

确保治理完成后仍处于 closed-safe。

---

## 4) 184 runtime 输出字段（可见性要求）

184 输出至少包含并保持语义：
- `explicit_ultra_governance_entry_seen`
- `supra_governance_completed_seen`
- `supra_governance_legality_seen`
- `closed_safe_state_seen`
- `evidence_complete_seen`
- `boundary_violation_seen`
- `allowed_ultra_governance_outcome_selected`
- `forbidden_ultra_governance_outcome_blocked`
- `human_confirmation_required`
- `requires_new_governance_definition`
- `allows_next_runtime_now`
- `closed_safe_state_preserved`
- `illegal_state_detected`
- `governance_completed`

---

## 5) 验证工具与覆盖（A–M）

Verifier：
- `tools/verify_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_first_controlled_short_window_real_trial_ultra_governance_v0.py`

覆盖场景：
- A no_legal_supra_completion
- B closed_safe_not_preserved
- C evidence_incomplete
- D clean_ultra_case
- E governance_boundary_violation_case
- F widening_needed_case
- G forbidden_reopen_probe
- H forbidden_retry_runtime_probe
- I forbidden_widen_probe
- J forbidden_long_running_probe
- K default_path_probe（not explicit entry / default_path_enabled）
- L require_new_evidence_case（audit trace not intact）
- M structural_block_case

并对所有场景断言硬不变量：
- `keeps_system_closed=true`
- `allows_next_runtime_now=false`
- `closed_safe_state_preserved=true`
- outcome ∈ allowlist

---

## 6) 明确声明（与阶段限制一致）

- 默认路径仍未开启  
- 本阶段未进入 full controlled trial  
- 本阶段未扩大真实 side effects 面  
- 本阶段只是 first ultra-governance implementation（只读治理），不代表自动继续运行  

