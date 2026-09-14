# Phase-Next-173 — Higher-Order Governance Shadowed Validation Test Matrix v0（短文件名）

**文件**：`docs/architecture/LUNA_RELEASE_CONTROL_HIGHER_ORDER_GOVERNANCE_SHADOWED_VALIDATION_TEST_MATRIX_V0.md`  
**阶段**：Phase-Next-173  
**说明**：此文件为长命名 test matrix 的等价承载（因 macOS 文件名长度限制）。

---

## 场景矩阵（A–M）

| scenario | 核心输入触发 | 预期 outcome | entry_gate | prerequisite(lower-order+closed-safe) | allowlist-only | forbidden-blocking | keeps_closed | allows_next_runtime_now |
|---|---|---|---|---|---|---|---|---|
| A.no_legal_lower_order_completion | governance_completed=false | remain_closed_safe | pass(显式入口) | fail => 不得推进 | pass | n/a | true | false |
| B.closed_safe_not_preserved | closed_safe_state_preserved=false | block_further_real_action_until_manual_override | pass | fail => block | pass | n/a | true | false |
| C.evidence_incomplete | evidence_complete=false | require_new_evidence_before_any_further_governance 或 remain_closed_safe | pass | pass | pass | n/a | true | false |
| D.clean_higher_order_case | 全部正常 | allow_next_governance_preparation_under_same_guardrails | pass | pass | pass | pass | true | false |
| E.governance_boundary_violation_case | boundary_violation_seen=true | block_further_real_action_until_manual_override 或 remain_closed_safe | pass | pass | pass | n/a | true | false |
| F.widening_needed_case | widening_needed=true | escalate_for_new_governance_definition | pass | pass | pass | n/a | true | false |
| G.forbidden_reopen_probe | forbidden_signals含 implicit_reopen | block... + blocked=true | pass | pass | pass | pass(必须阻断) | true | false |
| H.forbidden_retry_runtime_probe | forbidden_signals含 implicit_retry_runtime | block... + blocked=true | pass | pass | pass | pass(必须阻断) | true | false |
| I.forbidden_widen_probe | forbidden_signals含 implicit_widening | block... + blocked=true | pass | pass | pass | pass(必须阻断) | true | false |
| J.forbidden_long_running_probe | forbidden_signals含 implicit_long_running_enablement | block... + blocked=true | pass | pass | pass | pass(必须阻断) | true | false |
| K.default_path_probe.not_explicit_entry | explicit_entry=false | remain_closed_safe | fail(应拦截) | n/a | pass | n/a | true | false |
| K.default_path_probe.default_path_enabled | default_path_enabled=true | block... | fail(应拦截) | n/a | pass | n/a | true | false |
| L.require_new_evidence_case | audit_trace_intact=false | require_new_evidence_before_any_further_governance | pass | pass | pass | n/a | true | false |
| M.structural_block_case | structural_risk_seen=true | block_further_real_action_until_manual_override | pass | pass | pass | n/a | true | false |

