# Phase-Next-181 — Supra-Governance Shadowed Validation Test Matrix v0（短文件名承载）

**状态**：测试矩阵冻结（v0）  
**范围**：仅用于验证 Phase-Next-180 `supra-governance runtime` 是否遵守 Phase-Next-179 边界  

---

## 0. 短文件名等价承载声明

本文件为长命名目标测试矩阵的**短文件名等价承载**：

- 长命名目标（等价）：  
  `docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_FIRST_CONTROLLED_SHORT_WINDOW_REAL_TRIAL_SUPRA_GOVERNANCE_SHADOWED_VALIDATION_TEST_MATRIX_V0.md`
- 短文件名实际承载（本文件）：  
  `docs/architecture/LUNA_RELEASE_CONTROL_SUPRA_GOVERNANCE_SHADOWED_VALIDATION_TEST_MATRIX_V0.md`

---

## 1. 核心不变量（所有场景都必须满足）

- `keeps_system_closed == true`
- `allows_next_runtime_now == false`
- `closed_safe_state_preserved == true`
- `allowed_supra_governance_outcome_selected` ∈ allowlist（179 白名单）

---

## 2. 场景矩阵（A–M）

### A. `no_legal_meta_completion`
- **输入变化**：`governance_completed=false`
- **预期**：
  - `illegal_state_detected=true`
  - `allowed_supra_governance_outcome_selected=remain_closed_safe`
  - 不进入 supra-governance 默认路径（显式入口也不得绕过 meta prerequisite）

### B. `closed_safe_not_preserved`
- **输入变化**：`closed_safe_state_preserved=false`
- **预期**：
  - `illegal_state_detected=true`
  - `allowed_supra_governance_outcome_selected=block_further_real_action_until_manual_override`

### C. `evidence_incomplete`
- **输入变化**：`evidence_complete=false`
- **预期**：
  - `allowed_supra_governance_outcome_selected=require_new_evidence_before_any_further_governance`（或更保守 remain_closed_safe；本 repo 180 预期为 require_new_evidence）

### D. `clean_supra_case`
- **输入变化**：无（base bundle）
- **预期**：
  - `allowed_supra_governance_outcome_selected=allow_next_governance_preparation_under_same_guardrails`
  - 但必须仍满足：`allows_next_runtime_now=false`（证明“不自动进入下一阶段 runtime”）

### E. `governance_boundary_violation_case`
- **输入变化**：`boundary_violation_seen=true`
- **预期**：
  - `allowed_supra_governance_outcome_selected=block_further_real_action_until_manual_override`

### F. `widening_needed_case`
- **输入变化**：`widening_needed=true`
- **预期**：
  - `allowed_supra_governance_outcome_selected=escalate_for_new_governance_definition`

### G. `forbidden_reopen_probe`
- **输入变化**：`forbidden_signals=["implicit_reopen"]`
- **预期**：
  - `forbidden_supra_governance_outcome_blocked=true`
  - `illegal_state_detected=true`
  - `allowed_supra_governance_outcome_selected=block_further_real_action_until_manual_override`

### H. `forbidden_retry_runtime_probe`
- **输入变化**：`forbidden_signals=["implicit_retry_runtime"]`
- **预期**：
  - `forbidden_supra_governance_outcome_blocked=true`
  - `illegal_state_detected=true`
  - `allowed_supra_governance_outcome_selected=block_further_real_action_until_manual_override`

### I. `forbidden_widen_probe`
- **输入变化**：`forbidden_signals=["implicit_widening"]`
- **预期**：
  - `forbidden_supra_governance_outcome_blocked=true`
  - `illegal_state_detected=true`
  - `allowed_supra_governance_outcome_selected=block_further_real_action_until_manual_override`

### J. `forbidden_long_running_probe`
- **输入变化**：`forbidden_signals=["implicit_long_running_enablement"]`
- **预期**：
  - `forbidden_supra_governance_outcome_blocked=true`
  - `illegal_state_detected=true`
  - `allowed_supra_governance_outcome_selected=block_further_real_action_until_manual_override`

### K. `default_path_probe`

#### K1. not explicit entry
- **输入变化**：`explicit_supra_governance_entry_intent_v0=false`
- **预期**：
  - `explicit_supra_governance_entry_seen=false`
  - `illegal_state_detected=true`
  - `allowed_supra_governance_outcome_selected=remain_closed_safe`

#### K2. default path enabled
- **输入变化**：`default_path_enabled=true`
- **预期**：
  - `illegal_state_detected=true`
  - `allowed_supra_governance_outcome_selected=block_further_real_action_until_manual_override`

### L. `require_new_evidence_case`
- **输入变化**：`audit_trace_intact=false`
- **预期**：
  - `allowed_supra_governance_outcome_selected=require_new_evidence_before_any_further_governance`

### M. `structural_block_case`
- **输入变化**：`structural_risk_seen=true`
- **预期**：
  - `allowed_supra_governance_outcome_selected=block_further_real_action_until_manual_override`

