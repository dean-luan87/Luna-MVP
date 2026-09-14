# Phase-RealSceneFix-001 — Controlled Live Run Evidence Capture Contract v0（真实证据采集契约冻结）

**目的**：冻结 controlled live input 的最小真实 run evidence 采集字段、落盘要求与归档要求，保证后续 review 可基于真实 evidence，而非 fixture-only。  
**注意**：本契约只约束证据采集与归档，不引入任何执行放权。  

---

## 0) 硬边界（写死）

- 不扩场景 scope（仍为 Option A 范围）
- candidate-only
- no execute leakage / no default-on / no side effects expansion（断言必须存在且为 true）
- 必须可回放、可审计、可归档

---

## 1) run_evidence.json（顶层字段，必须全部存在）

每次 controlled live run 必须产出一个 `run_evidence.json`，至少包含：

- `run_id`
- `scenario_id`
- `selected_option`：固定为 `OptionA_sidewalk_short_walk_observe`
- `evidence_type`：固定为 `controlled_live`
- `explicit_trial_intent`：必须为 true
- `entry_token`
- `mode_entry_event_present`：必须为 true
- `controlled_live_input_started`：必须为 true
- `controlled_live_input_ended`：必须为 true
- `operator_id`
- `safety_observer_id`
- `record_owner_id`
- `start_time_ms`
- `end_time_ms`
- `duration_ms`
- `timebox_ms`

文件路径字段（必须存在且非空字符串）：
- `trace_file_path`
- `replay_file_path`
- `whitebox_file_path`
- `model_candidate_trace_path`
- `output_candidate_trace_path`
- `operator_notes_path`
- `risk_events_path`
- `archive_manifest_path`
- `post_run_summary_path`

安全断言（必须全部为 true）：
- `no_execute_leakage_assertion=true`
- `no_default_on_assertion=true`
- `no_side_effect_expansion_assertion=true`

run 状态字段（必须存在）：
- `abort_triggered`（bool）
- `abort_reason`（string or null；若 abort_triggered=true 则必须非空）
- `fallback_triggered`（bool）
- `degraded_triggered`（bool）

---

## 2) 落盘文件清单（required_files，写死）

每次 controlled live run 的归档根目录（archive_root）下必须包含：
- `run_evidence.json`
- `trace.jsonl`
- `replay.jsonl`
- `whitebox.jsonl`
- `model_candidate_trace.jsonl`
- `output_candidate_trace.jsonl`
- `operator_notes.(md|json)`
- `risk_events.jsonl`（若无风险，必须写入 `risk_events_status=none_observed` 的记录）
- `post_run_summary.(md|json)`
- `archive_manifest.json`

---

## 3) explicit entry 真实落盘要求（写死）

必须在 evidence 中可验证：
- `explicit_trial_intent=true` 与 `entry_token` 存在
- `mode_entry_event_present=true`
- `controlled_live_input_started/ended=true`

缺任一项：视为 hard fail。

---

## 4) abort / fallback / degraded 证据要求（写死）

- 不要求真实 run 必须触发 abort/fallback/degraded  
- 但必须保证 schema 支持记录，并且：
  - 若未触发：字段必须为 `false`/`null` 明确落盘
  - 若触发：必须能保全 trace 并产出 post-run summary
- 必须提供 synthetic evidence 用于验证工具识别（属于 Fix Sprint 的验证范围）

