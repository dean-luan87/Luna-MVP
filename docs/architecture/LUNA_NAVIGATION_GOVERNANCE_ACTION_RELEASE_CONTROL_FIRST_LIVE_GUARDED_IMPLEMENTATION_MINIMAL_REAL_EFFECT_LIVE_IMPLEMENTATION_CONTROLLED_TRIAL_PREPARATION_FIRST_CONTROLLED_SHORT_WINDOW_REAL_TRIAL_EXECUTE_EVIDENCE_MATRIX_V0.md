# Phase-Next-162 — First Controlled Short-Window Real Trial Execute Evidence Matrix v0

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_FIRST_CONTROLLED_SHORT_WINDOW_REAL_TRIAL_EXECUTE_EVIDENCE_MATRIX_V0.md`  
**用途**：把 151 / 155 / 158 / 159 / 160 / 161 的关键证据矩阵化，支撑 Phase-Next-162 execute go/no-go pack 的结论（只读证据整理，不新增实现）。

---

## 字段说明（写死）

- **requirement_id**：本矩阵的要求条目 ID（X-xxx）
- **source_phase**：证据来源阶段（151/155/158/159/160/161）
- **source_artifact**：证据来源产物（文档/代码/工具）
- **evidence_summary**：证据摘要（可复盘、可定位）
- **boundary_type**：`entry_gate | readiness_gate | started | release | stop_abort | recovery | final_close | default_path_control | non_expansion`
- **status**：`satisfied | partially_satisfied | not_satisfied`
- **blocker_level**：`hard_blocker | soft_followup | informational`

---

## 证据矩阵（v0）

| requirement_id | source_phase | source_artifact | evidence_summary | boundary_type | status | blocker_level |
|---|---:|---|---|---|---|---|
| X-151-START-UNIQUE | 151 | `docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_FIRST_MINIMAL_REAL_ENABLEMENT_DEFINITION_V0.md` | `start_event_observed` 定义为唯一 started 判据；started 后必须 closure。 | started | satisfied | informational |
| X-151-RELEASE-CLOSE | 151 | 同上 | release 只能在合法 started 后短时打开；final close 后 se=false。 | release | satisfied | informational |
| X-155-GUARDRAIL-FROZEN | 155 | `docs/architecture/...FIRST_CONTROLLED_SHORT_WINDOW_TRIAL_GUARDRAIL_DEFINITION_V0.md` | allow/deny、window、abort/recovery/closure 强制策略冻结。 | stop_abort | satisfied | informational |
| X-158-READINESS-GO | 158 | `docs/architecture/...CONTROLLED_SHORT_WINDOW_REAL_TRIAL_READINESS_GO_NO_GO_PACK_V0.md` | readiness pack 结论为 go（readiness ≠ execute）。 | readiness_gate | satisfied | informational |
| X-159-EXECUTE-CONSTITUTION | 159 | `docs/architecture/...REAL_TRIAL_EXECUTE_DEFINITION_V0.md` | execute 唯一进入条件、白/黑名单、stop/finalization policy 冻结。 | entry_gate | satisfied | informational |
| X-160-EXECUTE-RUNTIME-EXISTS | 160 | `capabilities/governance/runtime/...first_controlled_short_window_real_trial_execute_v0.py` | execute runtime 存在：显式入口+intent+approval+readiness_go+窗口/次数/范围约束+强制收口。 | entry_gate | satisfied | informational |
| X-160-GATE-NONBYPASS | 160 | 同上 | execute intent + approval + readiness_go gate 缺失即 abort，不可绕过。 | entry_gate | satisfied | informational |
| X-160-START-UNIQUE-KEPT | 160 | 同上 | started 仅由 152 产出 start_event_observed 驱动；无 start_event 却 started 即 abort。 | started | satisfied | informational |
| X-160-ALLOWLIST-SURFACES | 160 | 同上 | requested_surfaces 只允许三类（state/result/exception_failure），未授权 surface 即 abort。 | release | satisfied | informational |
| X-160-STOP-ON-TIMEOUT | 160 | 同上 | execute_window_timeout 触发 abort 并收口（closed=true, se=false）。 | stop_abort | satisfied | informational |
| X-160-STOP-ON-AUDIT | 160 | 同上 | audit 不可审计（参数/trace）触发 abort 并收口。 | stop_abort | satisfied | informational |
| X-160-FINAL-CLOSE | 160 | 同上 | success/failure/abort 均最终 closed=true 且 se=false。 | final_close | satisfied | informational |
| X-161-VALIDATION-TOOL | 161 | `tools/validate_...real_trial_execute_shadowed_validation_evaluation_v0.py` | 161 复用 160 runtime + 160 verifier；A–M 场景结构化评估输出。 | non_expansion | satisfied | informational |
| X-161-A-M-PASS | 161 | 同上 | 161 overall evaluation = go；13/13 场景通过；entry/readiness/started/release/stop/recovery/final_close 完整性均为 true。 | stop_abort | satisfied | informational |
| X-DEFAULT-PATH-OFF | 160/161 | 160 runtime + 161 L 场景 | 默认路径未开启：无显式 intent 不会进入 execute。 | default_path_control | satisfied | informational |
| X-NON-EXPANSION | 151–161 | 产物范围审计 | 162 阶段只新增文档/只读汇总，不新增 runtime 主实现，不扩大 side effects 面。 | non_expansion | satisfied | informational |

---

## v0 结论映射

- **Hard blockers**：无（见主 pack v0）
- **Soft follow-ups**：证据归档、reason code 口径、runbook/checklist（不影响当前 go）

