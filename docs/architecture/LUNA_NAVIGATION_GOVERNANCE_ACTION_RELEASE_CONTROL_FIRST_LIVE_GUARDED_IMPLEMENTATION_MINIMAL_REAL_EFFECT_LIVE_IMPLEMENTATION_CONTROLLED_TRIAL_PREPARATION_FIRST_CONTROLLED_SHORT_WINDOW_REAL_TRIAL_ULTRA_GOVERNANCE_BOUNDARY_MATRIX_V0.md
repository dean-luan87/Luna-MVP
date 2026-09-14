# Phase-Next-183 — Ultra-Governance Boundary Matrix v0（边界矩阵冻结）

**用途**：将 ultra-governance 的进入条件、前置条件、allowed/forbidden outcomes、以及 remain_closed/require_new_evidence/escalate/block/next-prep 的触发条件矩阵化，防止后续实现漏掉硬边界。  
**注意**：本矩阵是定义冻结的一部分；不是实现；不授予运行时放行能力。  

---

## 1) 关键字段（实现不得少于此）

- `explicit_ultra_governance_entry_intent_v0`（非默认入口）
- `supra_governance_completed_seen`
- `supra_governance_legality_seen`
- `closed_safe_state_seen`
- `evidence_complete_seen`
- `audit_trace_intact_seen`
- `default_path_enabled`（必须为 false）
- `boundary_violation_seen` / `structural_risk_seen`
- `widening_needed`
- `forbidden_signals`（含 implicit reopen/retry/widen/long-running/default-on 等）

---

## 2) Entry-to-Ultra Conditions Matrix（唯一入口）

| 条件 | 必须为真？ | 若不满足，必须行为 |
|---|---:|---|
| 显式入口意图 | 是 | `remain_closed_safe` + 标记非法进入 |
| supra 完成 | 是 | `remain_closed_safe` + 标记非法进入 |
| supra 合法性 | 是 | `remain_closed_safe` + 标记非法进入 |
| closed-safe | 是 | `block_further_real_action_until_manual_override` 或 `remain_closed_safe`（保守） |
| default path disabled | 是 | `block_further_real_action_until_manual_override`（视为安全违规） |
| 审计 trace 可用 | 是（最低） | `require_new_evidence_before_any_further_governance` |

---

## 3) Allowed Outcomes Matrix（白名单）

| outcome_id | allowed | 必须保持 closed-safe | allows_next_runtime_now |
|---|---:|---:|---:|
| remain_closed_safe | 是 | 是 | **false** |
| require_new_evidence_before_any_further_governance | 是 | 是 | **false** |
| escalate_for_new_governance_definition | 是 | 是 | **false** |
| allow_next_governance_preparation_under_same_guardrails | 是 | 是 | **false** |
| block_further_real_action_until_manual_override | 是 | 是 | **false** |

---

## 4) Forbidden Outcomes / Signals Matrix（黑名单）

| forbidden_id | 必须阻断？ | 阻断后的强制回落 outcome |
|---|---:|---|
| implicit_reopen | 是 | block_further_real_action_until_manual_override |
| implicit_retry_runtime | 是 | block_further_real_action_until_manual_override |
| implicit_widening | 是 | block_further_real_action_until_manual_override |
| implicit_full_trial_continuation | 是 | block_further_real_action_until_manual_override |
| implicit_default_on_transition | 是 | block_further_real_action_until_manual_override |
| implicit_long_running_enablement | 是 | block_further_real_action_until_manual_override |
| open_release_window | 是 | block_further_real_action_until_manual_override |
| trigger_execute / trigger_retry / trigger_reopen | 是 | block_further_real_action_until_manual_override |
| enable_default_path / enable_long_running | 是 | block_further_real_action_until_manual_override |

---

## 5) Outcome Selection Rules Matrix（五分支规则）

| 场景条件（优先级从高到低） | 必须选择的 outcome |
|---|---|
| 任一 forbidden_signals 存在 | block_further_real_action_until_manual_override |
| boundary_violation_seen 或 structural_risk_seen 为真 | block_further_real_action_until_manual_override |
| widening_needed 为真（继续推进必须改定义/扩窗/扩面） | escalate_for_new_governance_definition |
| audit_trace_intact_seen 为假 或 evidence_complete_seen 为假 | require_new_evidence_before_any_further_governance |
| entry/prerequisites 全满足且无风险且无 widening 且证据完备 | allow_next_governance_preparation_under_same_guardrails |
| 其他任何不明/缺字段/不一致状态 | remain_closed_safe |

---

## 6) Post-Governance Safety State Matrix（强制安全态）

| 维度 | 强制要求 |
|---|---|
| keeps_system_closed | true |
| closed_safe_state_preserved | true |
| allows_next_runtime_now | **false** |
| default_path_enabled | 必须仍为 false |
| side effects window | 不得打开（无新增真实副作用面） |
| 隐式链条 | 禁止（无 hidden auto retry/reopen/continuation） |

