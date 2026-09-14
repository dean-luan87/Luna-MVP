# LUNA Offline Mainline Observability Report Schema v0

## Scope

冻结 EF-005 的输出 schema（机器可读），用于回归校验与跨阶段引用稳定。

本 schema 为 **v0 最小结构**：优先保证 refs 不断裂、聚合字段可用、可验证。

## File: `observability_report.json`

必须包含以下字段（不得伪造缺失）：

- `report_id`: string
- `generated_at_s`: number (epoch seconds)
- `normal_root`: string (abs path)
- `fallback_root`: string (abs path)
- `pipeline_version`: string
- `input_sample_count`: number
- `roots_readiness`: object
  - `normal_root_readable`: boolean
  - `fallback_root_readable`: boolean
  - `normal_root`: string
  - `fallback_root`: string
- `stage_readiness`: object
  - `perception`: boolean
  - `scene_context`: boolean
  - `scene_task`: boolean
  - `fusion`: boolean
  - `output`: boolean
- `source_policy_summary`: object
  - `normal_source_distribution`: object
  - `fallback_source_distribution`: object
  - `fallback_count`: number
- `chain_completeness_summary`: object
  - `normal_stage_complete_rates`: object|null
  - `fallback_stage_complete_rates`: object|null
- `schema_integrity_summary`: object
  - `normal_schema_valid_rates`: object|null
  - `fallback_schema_valid_rates`: object|null
- `sample_chain_matrix_ref`: string (relative path)
- `stage_artifact_index_ref`: string (relative path)
- `normal_vs_fallback_comparison_ref`: string (relative path)
- `trace_index_summary`: object
- `replay_index_summary`: object
- `whitebox_index_summary`: object
- `safety_boundary_summary_ref`: string (relative path)
- `evidence_boundary_summary_ref`: string (relative path)
- `hard_blockers`: array
- `soft_followups`: array
- `recommendation`: string enum: `go|conditional_go|no_go`

## File: `sample_chain_matrix.json`

Top-level:

- `samples`: array of sample row objects

Each sample row must include:

- `sample_id`: string
- `normal_source_selected`: string|null
- `fallback_source_selected`: string|null
- `normal_all_stages_complete`: boolean
- `fallback_all_stages_complete`: boolean
- `normal_output_candidate_present`: boolean
- `fallback_output_candidate_present`: boolean
- `normal_allows_execute_now_false`: boolean
- `fallback_allows_execute_now_false`: boolean
- `normal_real_tts_invoked_false`: boolean
- `fallback_real_tts_invoked_false`: boolean
- `normal_safety_leakage_count`: number
- `fallback_safety_leakage_count`: number
- `normal_evidence_boundary_ok`: boolean
- `fallback_evidence_boundary_ok`: boolean
- `stage_refs`: object
  - `normal`: object with keys `perception|scene_context|scene_task|fusion|output` (string refs)
  - `fallback`: object with keys `perception|scene_context|scene_task|fusion|output` (string refs)

## File: `stage_artifact_index.json`

必须包含：

- `normal`: object
  - `stage_outputs_root`: string
  - `stage_paths`: object
  - `stage_paths_exist`: object
- `fallback`: object
  - `stage_outputs_root`: string
  - `stage_paths`: object
  - `stage_paths_exist`: object
- `trace_files`: object
- `index_files`: object
- `missing_artifacts`: array
- `broken_refs`: array

## File: `normal_vs_fallback_comparison.json`

必须包含：

- `normal_source_distribution`: object
- `fallback_source_distribution`: object
- `normal_detection_count_total`: number
- `fallback_detection_count_total`: number
- `normal_chain_complete_rate`: number
- `fallback_chain_complete_rate`: number
- `normal_output_candidate_rate`: number
- `fallback_output_candidate_rate`: number
- `normal_safety_leakage_total`: number
- `fallback_safety_leakage_total`: number
- `normal_boundary_ok_rate`: number
- `fallback_boundary_ok_rate`: number

## File: `safety_boundary_summary.json`

必须包含：

- `execute_leakage_count_total`: number
- `default_on_leakage_count_total`: number
- `release_retry_reopen_leakage_count_total`: number
- `side_effects_expansion_count_total`: number
- `forced_navigation_action_count_total`: number
- `forbidden_output_semantic_count_total`: number
- `allows_execute_now_false_rate`: number
- `real_tts_invoked_false_rate`: number

## File: `evidence_boundary_summary.json`

必须包含：

- `evidence_type_preserved_rate`: number
- `controlled_live_stream_false_rate`: number
- `phone_local_capture_true_rate`: number
- `pending_real_sidewalk_run_true_rate`: number
- `evidence_type_mutation_count`: number
- `pending_closed_count`: number

