# Phase-Next-171 — Higher-Order Governance Boundary Matrix v0

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_FIRST_CONTROLLED_SHORT_WINDOW_REAL_TRIAL_HIGHER_ORDER_GOVERNANCE_BOUNDARY_MATRIX_V0.md`  
**阶段**：Phase-Next-171  
**用途**：将 higher-order governance 的进入条件、允许/禁止 outcome、以及 remain_closed/require_new_evidence/escalate/block/next-preparation 条件矩阵化，防止后续实现漏掉硬边界。

---

## 矩阵字段（写死）

- **matrix_id**
- **layer**：`entry_to_higher_order_governance | governance_inputs | allowed_outcomes | forbidden_outcomes | post_governance_safety`
- **boundary_type**：`entry_gate | evidence | audit | outcome | remain_closed | require_new_evidence | escalate | block | next_preparation | default_path_control | non_expansion`
- **requirement**
- **must_hold**
- **violation_outcome**：`remain_closed_safe | require_new_evidence_before_any_further_governance | block_further_real_action_until_manual_override | no_go`
- **evidence_source**：`151/155/158/159/162/163/166/167/168/169/170/171`

---

## Boundary Matrix（v0）

| matrix_id | layer | boundary_type | requirement | must_hold | violation_outcome | evidence_source |
|---|---|---|---|---:|---|---|
| H-ENTRY-01 | entry_to_higher_order_governance | entry_gate | 只能在 post-decision governance 已合法完成后进入（governance_completed=true 且可复盘） | true | remain_closed_safe | 167/168/169/170/171 |
| H-ENTRY-02 | entry_to_higher_order_governance | evidence | 必须处于 closed-safe state（无 release window、无 auto retry/reopen） | true | block_further_real_action_until_manual_override | 151/163/167/168/171 |
| H-ENTRY-03 | entry_to_higher_order_governance | audit | audit trace intact；缺失不得输出 allow_next_preparation | true | require_new_evidence_before_any_further_governance | 155/167/169/171 |
| H-ENTRY-04 | entry_to_higher_order_governance | default_path_control | 默认路径仍禁用是硬前提 | true | block_further_real_action_until_manual_override | 151–170/171 |
| H-ENTRY-05 | entry_to_higher_order_governance | evidence | 170 go/no-go pack 为 go/conditional_go 作为资格信号 | true | remain_closed_safe | 170/171 |
| H-IN-01 | governance_inputs | evidence | lower-order outcome 必须属于 allowlist 且不触发 forbidden | true | remain_closed_safe | 167/168/169/171 |
| H-OUT-01 | allowed_outcomes | outcome | outcome 只能落在 allowlist（remain_closed/require_new_evidence/escalate/next_preparation/block） | true | no_go | 171 |
| H-OUT-02 | forbidden_outcomes | outcome | 禁止 implicit reopen / implicit retry runtime / implicit widening / implicit full-trial / implicit default-on / implicit long-running approval | true | no_go | 171 |
| H-REM-01 | allowed_outcomes | remain_closed | evidence/audit 不完整或 closed-safe 不可信 => remain_closed_safe | true | remain_closed_safe | 171 |
| H-REQ-01 | allowed_outcomes | require_new_evidence | 证据不足以支持推进/升级结论 => require_new_evidence... | true | require_new_evidence_before_any_further_governance | 171 |
| H-ESC-01 | allowed_outcomes | escalate | 继续前需要任何扩围/扩窗/扩频/扩面/改策略 => escalate_for_new_governance_definition | true | escalate_for_new_governance_definition | 155/167/171 |
| H-BLK-01 | allowed_outcomes | block | 结构性安全问题/default-on 风险/forbidden probe => block_further_real_action_until_manual_override | true | block_further_real_action_until_manual_override | 151/155/167/171 |
| H-NEXT-01 | allowed_outcomes | next_preparation | 仅在证据完整+无越界+无需新定义时允许 allow_next_governance_preparation_under_same_guardrails | true | require_new_evidence_before_any_further_governance | 155/167/170/171 |
| H-SAFE-01 | post_governance_safety | non_expansion | governance 完成后必须保持 closed-safe state，不得成为打开 release window/触发 execute 的通道 | true | no_go | 151/163/171 |

