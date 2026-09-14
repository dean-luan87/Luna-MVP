# Phase-Next-166 — First Controlled Short-Window Real Trial Post-Execute Decision Evidence Matrix v0

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_FIRST_CONTROLLED_SHORT_WINDOW_REAL_TRIAL_POST_EXECUTE_DECISION_EVIDENCE_MATRIX_V0.md`  
**用途**：把 151 / 155 / 158 / 159 / 162 / 163 / 164 / 165 的关键证据矩阵化，支撑 Phase-Next-166 post-execute decision go/no-go pack 的结论（只读证据整理，不新增实现）。

---

## 字段说明（写死）

- **requirement_id**：本矩阵的要求条目 ID（D-xxx）
- **source_phase**：证据来源阶段（151/155/158/159/162/163/164/165）
- **source_artifact**：证据来源产物（文档/代码/工具）
- **evidence_summary**：证据摘要（可复盘、可定位）
- **boundary_type**：`entry_gate | final_close_prerequisite | allowed_outcome | forbidden_blocking | closed_safe_state | no_auto_retry | default_path_control | non_expansion`
- **status**：`satisfied | partially_satisfied | not_satisfied`
- **blocker_level**：`hard_blocker | soft_followup | informational`

---

## 证据矩阵（v0）

| requirement_id | source_phase | source_artifact | evidence_summary | boundary_type | status | blocker_level |
|---|---:|---|---|---|---|---|
| D-151-CLOSE-SEFALSE | 151 | `docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_FIRST_MINIMAL_REAL_ENABLEMENT_DEFINITION_V0.md` | close 后 `side_effects_released=false` 的强约束（安全闭合态）作为 decision 前置原则。 | final_close_prerequisite | satisfied | informational |
| D-155-GUARDRAIL-FROZEN | 155 | `docs/architecture/...FIRST_CONTROLLED_SHORT_WINDOW_TRIAL_GUARDRAIL_DEFINITION_V0.md` | guardrail allow/deny/abort/recovery/final close 策略冻结，为 decision 的证据解释提供护栏语义基线。 | non_expansion | satisfied | informational |
| D-158-READINESS-GO | 158 | `docs/architecture/...CONTROLLED_SHORT_WINDOW_REAL_TRIAL_READINESS_GO_NO_GO_PACK_V0.md` | readiness=go（但 readiness≠execute≠decision）。 | non_expansion | satisfied | informational |
| D-159-EXECUTE-BOUNDARY | 159 | `docs/architecture/...REAL_TRIAL_EXECUTE_DEFINITION_V0.md` | execute completion / final close 与后续决策边界不混写；为 decision 的“只读治理性”提供前置约束。 | final_close_prerequisite | satisfied | informational |
| D-162-EXECUTE-PACK-GO | 162 | `docs/architecture/...REAL_TRIAL_EXECUTE_GO_NO_GO_PACK_V0.md` | execute legality pack = go，作为 decision chain 的资格信号之一（不等于继续运行授权）。 | entry_gate | satisfied | informational |
| D-163-DECISION-CONSTITUTION | 163 | `docs/architecture/...POST_EXECUTE_DECISION_DEFINITION_V0.md` | decision 宪法冻结：allowed outcomes、forbidden outcomes、closed-safe-state、no-auto-retry。 | allowed_outcome | satisfied | informational |
| D-163-OUTCOME-POLICY | 163 | `docs/architecture/...POST_EXECUTE_DECISION_OUTCOME_POLICY_V0.md` | 每个 outcome 的前置条件与“保持关闭/不自动重试/不得隐式 reopen”硬规则冻结。 | forbidden_blocking | satisfied | informational |
| D-164-DECISION-RUNTIME | 164 | `capabilities/governance/runtime/...post_execute_decision_v0.py` | decision runtime 存在：显式入口+final close prerequisite+证据完整性检查+allowed outcomes only+forbidden probe blocking+closed-safe。 | entry_gate | satisfied | informational |
| D-164-FINAL-CLOSE-PREREQ | 164 | 同上 | `closed=true` 且 `side_effects_released=false` 才 eligible；否则 remain_closed_safe。 | final_close_prerequisite | satisfied | informational |
| D-164-ALLOWLIST-ONLY | 164 | 同上 | outcome 只能落在 allowlist 集合（remain_closed_safe/retry_allowed/retry_not_allowed/escalate/stop_and_block）。 | allowed_outcome | satisfied | informational |
| D-164-FORBIDDEN-BLOCK | 164 | 同上 | forbidden probes（implicit reopen/retry/widen/full-trial/default-on）一律 blocked 并降级 remain_closed_safe。 | forbidden_blocking | satisfied | informational |
| D-164-CLOSED-SAFE | 164 | 同上 | decision 后强制 `closed_safe_state_preserved=true`。 | closed_safe_state | satisfied | informational |
| D-164-NO-AUTO-RETRY | 164 | 同上 | decision 后强制 `allows_retry_now=false`（retry_allowed != auto retry）。 | no_auto_retry | satisfied | informational |
| D-165-VALIDATION-GO | 165 | `tools/validate_release_control_post_execute_decision_shadowed_validation_evaluation_v0.py` + `docs/architecture/..._POST_EXECUTE_DECISION_SHADOWED_VALIDATION_EVALUATION_V0.md` | 165 shadowed validation/evaluation = go；A–M 场景通过；allowed/forbidden/closed-safe/no-auto-retry 完整性为 true。 | closed_safe_state | satisfied | informational |
| D-DEFAULT-PATH-OFF | 164/165 | 164 runtime + 165 J 场景 | 无显式入口不得进入 decision（default path probe blocked）。 | default_path_control | satisfied | informational |
| D-NON-EXPANSION | 151–165 | 产物范围审计 | 166 阶段只新增文档/只读汇总，不新增 runtime 主实现，不扩大 side effects 面。 | non_expansion | satisfied | informational |

---

## v0 结论映射

- **Hard blockers**：无（见主 pack v0）
- **Soft follow-ups**：证据归档、reason code 口径、runbook/checklist（不影响当前 go）

