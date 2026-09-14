# Phase-RealScenePrep-001 — Controlled Real Scene Trial Entry Checklist v0（入口清单冻结）

**目的**：写死进入 RealSceneTrial-001 execution 之前必须满足的 checklist（不满足即禁止进入）。  

---

## A. 系统状态（必须全部满足）

- `default_path_disabled=true`
- `full_controlled_trial=false`
- `side_effects_expansion=false`
- `model_execution_authority=false`
- `candidate_only=true`

---

## B. 链路状态（必须全部满足）

- `Device-001 closed-loop validation available=true`
- `trace/replay/whitebox available=true`
- `fallback/degraded available=true`
- `output timing policy available=true`
- `fusion conflict policy available=true`

---

## C. 试验状态（必须全部满足）

- `explicit_trial_intent=true`（显式试验意图/entry_token）
- `operator_assigned=true`
- `safety_observer_assigned=true`
- `record_owner_assigned=true`
- `timebox_configured=true`（单次/单日/连续运行上限）
- `abort_triggers_configured=true`
- `scope_configured=true`（仅允许 1–2 场景，且属于 allowlist）
- `replay_archive_path_configured=true`

---

## D. 风险状态（必须全部满足）

- `weather_environment_acceptable=true`
- `route_scenario_allowed=true`
- `high_risk_area_excluded=true`
- `emergency_stop_available=true`
- `manual_override_available=true`
- `privacy_sensitive_area_policy_ready=true`（若涉及）

---

## Checklist 失败策略（写死）

任一项不满足：
- 禁止进入 execution
- 必须记录失败原因（reason_codes + operator note）
- 允许回退到 replay/fixture 验证，不允许“带病进入真实场景”

