# Phase-Next-167 — First Controlled Short-Window Real Trial Post-Decision Governance Boundary Matrix v0

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_FIRST_CONTROLLED_SHORT_WINDOW_REAL_TRIAL_POST_DECISION_GOVERNANCE_BOUNDARY_MATRIX_V0.md`  
**用途**：将进入条件、允许 outcome、禁止 outcome、remain_closed/escalate/block/next-governance-preparation 条件矩阵化，防止后续 governance implementation 漏掉治理硬边界。

---

## 矩阵字段（写死）

- **matrix_id**
- **layer**：`entry_to_governance | governance_inputs | allowed_outcomes | forbidden_outcomes | post_governance_safety`
- **boundary_type**：`entry_gate | evidence | audit | outcome | remain_closed | escalate | block | next_preparation | default_path_control | non_expansion`
- **requirement**：要求描述（可审计/验证）
- **must_hold**：必须成立（true/false）
- **violation_outcome**：违规必须产生的结果（remain_closed_safe / require_new_evidence / block / no_go）
- **evidence_source**：关联证据来源（151/155/158/159/162/163/164/165/166/167）

---

## Boundary Matrix（v0）

| matrix_id | layer | boundary_type | requirement | must_hold | violation_outcome | evidence_source |
|---|---|---|---|---:|---|---|
| G-ENTRY-01 | entry_to_governance | entry_gate | governance 只能在 post-execute decision 已合法完成后进入（decision_completed=true 且可复盘） | true | remain_closed_safe | 163/164/165/166/167 |
| G-ENTRY-02 | entry_to_governance | evidence | 系统必须处于 closed-safe state（无 release window、无 auto retry） | true | block_further_real_action_until_manual_override | 163/164/165/167 |
| G-ENTRY-03 | entry_to_governance | audit | audit trace intact；缺失不得输出 allow_next_governance_preparation | true | require_new_evidence_before_any_further_governance | 155/163/165/167 |
| G-ENTRY-04 | entry_to_governance | default_path_control | 默认路径仍禁用是硬前提 | true | block_further_real_action_until_manual_override | 151–166/167 |
| G-ENTRY-05 | entry_to_governance | evidence | 166 post-execute decision go/no-go pack 为 go/conditional_go 作为资格信号 | true | remain_closed_safe | 166/167 |
| G-IN-01 | governance_inputs | evidence | decision outcome 必须属于 163 allowlist 且不触发 forbidden | true | remain_closed_safe | 163/164/165/167 |
| G-OUT-01 | allowed_outcomes | outcome | outcome 只能落在 allowlist（remain_closed_safe / escalate / require_new_evidence / allow_next_preparation / block...） | true | no_go | 167 |
| G-OUT-02 | forbidden_outcomes | outcome | 禁止 implicit reopen / implicit retry runtime / implicit widening / implicit full-trial / implicit default-on / implicit long-running approval | true | no_go | 167 |
| G-REM-01 | allowed_outcomes | remain_closed | 证据不足/审计破损/closed-safe 不可信 => remain_closed_safe | true | remain_closed_safe | 167 |
| G-ESC-01 | allowed_outcomes | escalate | 需要改变定义/护栏/范围才能继续 => escalate_for_new_governance_definition | true | escalate_for_new_governance_definition | 155/159/163/167 |
| G-BLK-01 | allowed_outcomes | block | 结构性安全问题/default-on 风险 => block_further_real_action_until_manual_override | true | block_further_real_action_until_manual_override | 151/155/167 |
| G-NEXT-01 | allowed_outcomes | next_preparation | 仅在证据完整+无越界+无需新定义时允许 allow_next_governance_preparation_under_same_guardrails | true | require_new_evidence_before_any_further_governance | 155/163/165/166/167 |
| G-SAFE-01 | post_governance_safety | non_expansion | governance 完成后必须保持 closed-safe state，不得成为打开 release window/触发 execute 的通道 | true | no_go | 151/163/167 |

