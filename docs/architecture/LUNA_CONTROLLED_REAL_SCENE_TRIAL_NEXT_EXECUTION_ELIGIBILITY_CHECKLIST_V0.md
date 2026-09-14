# Phase-RealSceneReview-002 — Controlled Real Scene Trial Next Execution Eligibility Checklist v0（下一次执行资格清单冻结）

**目的**：定义是否允许进入“下一次 controlled live run evidence collection execution”的资格 checklist。  
**注意**：这不是扩场景；仍严格限定 Option A；不进入 full controlled trial；不开放用户。  

---

## A. Scope（必须全部满足）

- `selected_option=Option A`
- `no_scope_expansion=true`
- `no_new_scenario=true`
- `no_high_risk_environment=true`
- `no_open_user_test=true`

---

## B. Evidence Pipeline（必须全部满足）

- `controlled_live_evidence_contract_ready=true`
- `archive_manifest_schema_ready=true`
- `validation_tool_ready=true`
- `operator_notes_template_ready=true`
- `risk_events_template_ready=true`
- `post_run_summary_template_ready=true`

---

## C. Safety Boundary（必须全部满足）

- `no_default_on=true`
- `no_execute_release_retry_reopen_path=true`
- `no_side_effects_expansion=true`
- `candidate_only=true`
- `operator_required=true`
- `safety_observer_required=true`
- `record_owner_required=true`

---

## D. Execution Control（必须全部满足）

- `timebox_required=true`
- `abort_triggers_configured=true`
- `fallback_degraded_available=true`
- `no_immediate_retry_without_review=true`
- `archive_root_path_configured=true`

---

## Checklist 失败策略（写死）

任一项不满足：
- 禁止进入 controlled live execution
- 必须记录失败原因（reason_codes + operator note）
- 分流回 Fix Sprint 或 Pause（由分流策略决定）

