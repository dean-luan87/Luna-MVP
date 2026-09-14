# Phase-Next-158 — Controlled Short-Window Real Trial Readiness Evidence Matrix v0

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_CONTROLLED_SHORT_WINDOW_REAL_TRIAL_READINESS_EVIDENCE_MATRIX_V0.md`  
**用途**：把 151–157 的关键证据矩阵化，支撑 Phase-Next-158 readiness go/no-go pack 的结论（只读证据整理，不新增实现）。

---

## 字段说明（写死）

- **requirement_id**：本矩阵的要求条目 ID（R-xxx）
- **source_phase**：证据来源阶段（151–157）
- **source_artifact**：证据来源产物（文档/代码/工具）
- **evidence_summary**：证据摘要（可复盘、可定位）
- **boundary_type**：`entry_gate | started | release | abort | recovery | closure | default_path_control | non_expansion`
- **status**：`satisfied | partially_satisfied | not_satisfied`
- **blocker_level**：`hard_blocker | soft_followup | informational`

---

## 证据矩阵（v0）

| requirement_id | source_phase | source_artifact | evidence_summary | boundary_type | status | blocker_level |
|---|---:|---|---|---|---|---|
| R-151-START-UNIQUE | 151 | `docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_FIRST_MINIMAL_REAL_ENABLEMENT_DEFINITION_V0.md` | `start_event_observed` 被定义为唯一 started 判据；区分 ready vs started；started 后必须 closure。 | started | satisfied | informational |
| R-151-RELEASE-BOUNDARY | 151 | 同上 | side_effects_released 只能在合法 started 后短时打开；closure 后必须回落为 false。 | release | satisfied | informational |
| R-151-CLOSURE-MANDATORY | 151 | 同上 | started 之后必须进入 closure；不允许 started 而不 closed。 | closure | satisfied | informational |
| R-152-MIN-ENABLEMENT-EXISTS | 152 | `capabilities/governance/runtime/...first_minimal_real_enablement..._v0.py`（既有） | minimal real enablement runtime 存在，并实现 arming/start_event/release-window/closure。 | started | satisfied | informational |
| R-153-ENABLEMENT-VALIDATION-GO | 153 | `docs/architecture/...FIRST_MINIMAL_REAL_ENABLEMENT_SHADOWED_LIVE_VALIDATION_EVALUATION_V0.md`（既有） | minimal enablement 的 shadowed validation/evaluation 结论为 go。 | started | satisfied | informational |
| R-154-PREP-GONOGO-GO | 154 | `docs/architecture/...CONTROLLED_SHORT_WINDOW_TRIAL_PREPARATION_GO_NO_GO_PACK_V0.md` | 进入 short-window trial preparation 的治理裁决包为 go，且含 allow/deny 与阻断项定义。 | entry_gate | satisfied | informational |
| R-155-GUARDRAIL-FROZEN | 155 | `docs/architecture/...FIRST_CONTROLLED_SHORT_WINDOW_TRIAL_GUARDRAIL_DEFINITION_V0.md` | short-window trial guardrail 宪法冻结：窗口/次数/范围/allowlist/denylist/abort/recovery/closure 策略。 | abort | satisfied | informational |
| R-156-RUNTIME-EXISTS | 156 | `capabilities/governance/runtime/...first_controlled_short_window_trial_v0.py`（既有） | 156 runtime 存在，并显式执行 entry gate + short-window 护栏与 abort/recovery/closure。 | entry_gate | satisfied | informational |
| R-156-INTENT-APPROVAL-NONBYPASS | 156 | 同上 | 156 将 intent + approval 作为显式入口条件；缺失即 abort，不可绕过。 | entry_gate | satisfied | informational |
| R-156-START-UNIQUE-KEPT | 156 | 同上 | started 只能由 start_event_observed 驱动（复用 152 start 边界），避免 “无 start_event 却 started”。 | started | satisfied | informational |
| R-156-ABORT-TIMEOUT | 156 | 同上 | 超过短窗窗口（observed_elapsed_ms > trial_window_max_ms）触发 abort（trial_window_timeout）。 | abort | satisfied | informational |
| R-156-ABORT-UNAUTHORIZED | 156 | 同上 | unauthorized surface 触发 abort（unauthorized_side_effect_surface）。 | abort | satisfied | informational |
| R-156-ABORT-AUDIT-TRACE | 156 | 同上 | 窗口参数不可审计或 trace 缺失触发 abort（audit_trace_missing_or_broken）。 | abort | satisfied | informational |
| R-156-RECOVERY-CLOSURE | 156 | 同上 | abort/success/failure 路径均要求 closed=true 且 side_effects_released=false（收口契约）。 | closure | satisfied | informational |
| R-157-VALIDATION-TOOL | 157 | `tools/validate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_first_controlled_short_window_trial_shadowed_validation_evaluation_v0.py` | 157 复用 156 runtime + 156 verifier；A–K 场景结构化评估输出。 | non_expansion | satisfied | informational |
| R-157-AK-ENTRY-GATES | 157 | 同上（A/B/J 场景） | A no_intent、B no_approval、J default_path_probe：不 started、不 release、closed=true，证明 gate 不可绕过且默认路径不误触发。 | entry_gate | satisfied | informational |
| R-157-START-BOUNDARY | 157 | 同上（C/D/E 场景） | C armed_not_started：无 start_event 则不 started；D/E：started 时 start_event_observed=true。 | started | satisfied | informational |
| R-157-ABORT-INTEGRITY | 157 | 同上（F/G/I 场景） | F timeout、G unauthorized、I audit break：均 abort 并闭合（closed=true，se=false）。 | abort | satisfied | informational |
| R-157-CLOSURE-INTEGRITY | 157 | 同上（D/E 场景） | success/failure 均 closed=true，且最终 se=false。 | closure | satisfied | informational |
| R-157-ILLEGAL-PROBE | 157 | 同上（H/K synthetic probe） | H：未 started 却 release 为 illegal；K：started 但缺 closure 为 illegal（用于证明非法态识别口径）。 | release | satisfied | informational |
| R-DEFAULT-PATH-OFF | 156/157 | 156 runtime + 157 J 场景 | 默认路径未开启：无显式 intent 不会自动进入试运行。 | default_path_control | satisfied | informational |
| R-NON-EXPANSION | 151–157 | 产物范围审计 | 158 阶段只新增文档/只读汇总，不新增 runtime 主实现，不扩大 side effects 面。 | non_expansion | satisfied | informational |

---

## v0 结论映射

- **Hard blockers**：无（见主 pack v0）
- **Soft follow-ups**：证据归档/可读性补强（不影响当前 readiness 成立）

