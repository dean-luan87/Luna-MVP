# Phase-RealSceneTrial-001 — Controlled Real Scene Trial Execution Evidence Schema v0（执行证据 schema 冻结）

**目的**：定义 RealSceneTrial-001 每次 run 必须产出的 evidence schema（结构化 JSON），用于验证 checklist/边界/可观测/可回放/可中止。  

---

## 1) 顶层字段（必须全部存在）

- `run_id`
- `scenario_id`
- `selected_option`
- `start_time_ms`
- `end_time_ms`
- `duration_ms`
- `operator_id`
- `safety_observer_id`
- `record_owner_id`
- `mode`
- `timebox_ms`
- `checklist_completed`（bool）
- `abort_triggered`（bool）
- `abort_reason`（string or null）
- `fallback_triggered`（bool）
- `degraded_triggered`（bool）
- `no_execute_leakage_assertion`（bool；必须为 true）
- `no_default_on_assertion`（bool；必须为 true）
- `no_side_effect_expansion_assertion`（bool；必须为 true）
- `trace_ready`（bool）
- `replay_ready`（bool）
- `whitebox_ready`（bool）
- `model_candidate_trace_ready`（bool）
- `output_candidate_trace_ready`（bool）
- `privacy_area_checked`（bool）
- `post_run_summary_ready`（bool）
- `overall_run_status`（枚举：`completed` / `aborted` / `degraded`）

---

## 2) 扩展字段（v0 允许但不强制）

- `scope_allowlist_match`（bool）
- `operator_notes`（string）
- `risk_events`（array）
- `archive_path`（string）
- `manifest_or_hash`（string）
- `enabled_modules`（array）
- `disabled_modules`（array）

---

## 3) 硬规则（写死）

- 任一断言为 false → 必须视为 abort + no-go
- `mode` 不得为 default/uncontrolled（必须是受控模式）
- 缺少关键字段（run_id/timebox/checklist/trace-replay/summary）→ no-go

