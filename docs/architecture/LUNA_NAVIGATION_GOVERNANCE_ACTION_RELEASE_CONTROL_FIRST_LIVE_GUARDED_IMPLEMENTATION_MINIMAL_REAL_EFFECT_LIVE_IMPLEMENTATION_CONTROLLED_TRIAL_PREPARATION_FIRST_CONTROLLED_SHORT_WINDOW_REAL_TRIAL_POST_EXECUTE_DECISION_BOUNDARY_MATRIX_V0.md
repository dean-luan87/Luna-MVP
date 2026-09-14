# Phase-Next-163 — First Controlled Short-Window Real Trial Post-Execute Decision Boundary Matrix v0

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_FIRST_CONTROLLED_SHORT_WINDOW_REAL_TRIAL_POST_EXECUTE_DECISION_BOUNDARY_MATRIX_V0.md`  
**用途**：将进入条件、允许 outcome、禁止 outcome、retry/escalate/stop/remain_closed 条件矩阵化，防止后续 post-execute implementation 漏掉决策硬边界。

---

## 矩阵字段（写死）

- **matrix_id**
- **layer**：`entry_to_decision | decision_inputs | allowed_outcomes | forbidden_outcomes | post_decision_safety`
- **boundary_type**：`entry_gate | evidence | audit | outcome | retry | escalate | stop | remain_closed | default_path_control | non_expansion`
- **requirement**：要求描述（可被审计/验证）
- **must_hold**：必须成立（true/false）
- **violation_outcome**：违规必须产生的结果（remain_closed_safe / escalate / stop / no_go）
- **evidence_source**：关联证据来源（151/155/158/159/160/161/162/163）

---

## Boundary Matrix（v0）

| matrix_id | layer | boundary_type | requirement | must_hold | violation_outcome | evidence_source |
|---|---|---|---|---:|---|---|
| D-ENTRY-01 | entry_to_decision | entry_gate | decision 只能在 execute 已合法 final close 后进入（closed=true 且 se=false） | true | remain_closed_safe / escalate | 151 / 159 / 160 / 161 / 163 |
| D-ENTRY-02 | entry_to_decision | evidence | 必须引用 162 execute go/no-go pack（go/conditional_go）作为资格信号 | true | remain_closed_safe | 162 / 163 |
| D-ENTRY-03 | entry_to_decision | default_path_control | 默认路径仍禁用是 decision 的硬前提 | true | stop_and_block_further_real_action | 151–162 / 163 |
| D-IN-01 | decision_inputs | audit | audit trace intact；缺失不得给出 retry_allowed_under_same_guardrails | true | remain_closed_safe / escalate | 155 / 160 / 161 / 163 |
| D-IN-02 | decision_inputs | evidence | 必须有 execute 结果分类（success/failure/aborted + trigger/reason） | true | remain_closed_safe | 160 / 161 / 163 |
| D-IN-03 | decision_inputs | evidence | 必须有 started 判据一致性证据（start_event_observed 与 started） | true | stop_and_block_further_real_action | 151 / 160 / 161 / 163 |
| D-OUT-01 | allowed_outcomes | outcome | outcome 只能落在白名单集合（remain_closed_safe / retry_allowed... / retry_not_allowed... / escalate... / stop_and_block...） | true | no_go | 163 |
| D-OUT-02 | forbidden_outcomes | outcome | 禁止 implicit_reopen / implicit_retry / implicit_widening / implicit_full_trial / implicit_default_on | true | no_go | 163 |
| D-RETRY-01 | allowed_outcomes | retry | 仅在 final close 成立 + 证据完整 + 无越界 + 不扩面/不改定义 下允许 retry_allowed_under_same_guardrails | true | retry_not_allowed_until_new_definition | 155 / 159 / 160 / 161 / 163 |
| D-RETRY-02 | forbidden_outcomes | retry | decision 不得自动触发 retry（只能输出“允许/不允许”的治理结论） | true | no_go | 163 |
| D-ESC-01 | allowed_outcomes | escalate | 需要改变定义/护栏/范围才能继续时，必须 escalate_for_new_governance_definition | true | escalate_for_new_governance_definition | 155 / 159 / 163 |
| D-STOP-01 | allowed_outcomes | stop | 发现默认路径风险/结构性安全问题 => stop_and_block_further_real_action | true | stop_and_block_further_real_action | 151 / 155 / 163 |
| D-SAFE-01 | post_decision_safety | remain_closed | decision 完成后必须保持 closed-safe state（不打开 release window） | true | no_go | 151 / 159 / 163 |
| D-SAFE-02 | post_decision_safety | non_expansion | decision 不得成为扩大时长/频率/范围/副作用类别的通道 | true | no_go | 155 / 159 / 163 |

