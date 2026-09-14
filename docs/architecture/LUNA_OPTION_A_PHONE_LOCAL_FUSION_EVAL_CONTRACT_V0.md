# LUNA — Option A Phone Local Fusion Eval Contract v0 (Phase-FusionEval-001)

## Purpose
Freeze the minimal schema and forbidden outputs for FusionEval-001.

## Global boundaries (must hold)
- Fusion output is **candidate-only**.
- Forbidden semantics (must never appear):
  - execute / release / retry / reopen
  - default-on enablement
  - any direct navigation action directive (turn_now, cross_now, force_walk, etc.)
- `allows_execute_now` must be **false**.
- Must preserve evidence semantics:
  - do not rewrite `evidence_type`
  - do not relabel as `controlled_live_stream`
  - do not auto-close `pending_real_sidewalk_run`

## Runtime mode downstream rule
If upstream is baseline/mock:
- `fusion_runtime_mode=baseline_or_mock_downstream`
- `not_fusion_claimed=true`

## Per-sample output schema (minimum)
Each per-sample fusion result must include:
- `sample_id`
- `archive_root`
- `source_video_path`
- `perception_runtime_mode`
- `scene_task_runtime_mode`
- `fusion_runtime_mode`
- `not_fusion_claimed` (bool)
- `scene_type`
- `scene_phase`
- `task_candidates` (list; can be copied from input)
- `fusion_decision_candidate` (object; schema below)
- `selected_candidate_type`
- `source_attribution` (object)
- `conflict_detected` (bool)
- `conflict_handling` (object)
- `degraded_or_uncertain_handling` (object)
- `candidate_only` (bool; must be true)
- `allows_execute_now` (bool; must be false)
- leakage counters (must be zero):
  - `direct_execute_leakage_count`
  - `release_retry_reopen_leakage_count`
  - `default_on_leakage_count`
  - `side_effects_expansion_count`
  - `forced_navigation_action_count`
- evidence boundary booleans:
  - `evidence_type_preserved`
  - `controlled_live_stream_false`
  - `phone_local_capture_true`
- `reason_codes` (non-empty list)
- `hard_blockers` (list)
- `soft_followups` (list)

## fusion_decision_candidate minimal schema
Must include:
- `fusion_candidate_id`
- `source_scene_id`
- `source_task_candidate_ids` (list)
- `source_signal_ids` (list; may be empty in baseline/mock but must exist)
- `fusion_candidate_type` (one of):
  - `continue_observe_candidate`
  - `slow_down_candidate`
  - `obstacle_attention_candidate`
  - `narrow_path_attention_candidate`
  - `ask_for_help_candidate`
  - `uncertain_observe_candidate`
- `confidence` (float in [0,1])
- `source_attribution` (object; e.g. {source_layers:[...], upstream_roots:{...}})
- `conflict_detected` (bool)
- `conflict_type` (string)
- `conflict_resolution` (string)
- `degraded_mode` (bool)
- `reason_codes` (list)
- `allows_execute_now=false`

Forbidden fields:
- `execute_now`, `turn_now`, `cross_now`, `force_walk`
- `open_release_window`, `retry_now`, `reopen_now`
- `enable_default_path`

