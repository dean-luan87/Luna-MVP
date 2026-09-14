# Phase-RealScenePrep-001 — Controlled Real Scene Trial Observability & Evidence Contract v0（观测与证据契约冻结）

**目的**：定义受控真实场景试验前置必须记录的观测/证据字段，保证可审计、可回放、可复现，并写死关键断言。  

---

## 1) 每次试验必须具备的顶层字段（写死）

- `run_id`
- `operator_id`（可为 placeholder）
- `safety_observer_id`（可为 placeholder）
- `record_owner_id`（可为 placeholder）
- `scenario_id`
- `mode`（必须是受控模式，不得 default/uncontrolled）
- `timebox`（含单次/单日/连续运行上限）
- `start_timestamp_ms`
- `end_timestamp_ms`
- `enabled_modules`（列表）
- `disabled_modules`（列表）
- `input_source`（replay/controlled_live/fixture）

---

## 2) 必须记录的链路 trace（写死）

必须覆盖：
- `scene/task/fusion/output trace`
- `model candidate trace`（若 model shadow 启用）
- `fallback/degraded events`
- `abort events`（如发生）

并且 trace 至少要满足：
- 可按 `frame_or_event_id` 与 `timestamp_ms` 排序
- 每条 trace 有 `reason_codes` 与（尽可能）`confidence`

---

## 3) Replay/Whitebox 证据（写死）

必须具备：
- `replay_record`（可回放索引/引用）
- `whitebox_trace`（errors/fallback_events/stage_timings_ms）
- `operator_notes`（结构化；允许简短）
- `risk_events`（结构化；允许为空数组）

---

## 4) 三条硬断言（必须记录且为 true，写死）

- `no_execute_leakage_assertion=true`
- `no_default_on_assertion=true`
- `no_side_effect_expansion_assertion=true`

任何断言为 false：直接视为 abort + no-go。

---

## 5) Post-run 归档要求（写死）

必须具备：
- `post_run_summary_ready=true`
- `archive_path`
- `hash_or_manifest`（v0 可为占位字符串；只要求可追踪）

