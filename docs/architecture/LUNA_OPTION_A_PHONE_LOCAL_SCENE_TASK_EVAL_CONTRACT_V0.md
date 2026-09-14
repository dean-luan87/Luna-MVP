# LUNA — Option A Phone Local Scene × Task Eval Contract v0 (Phase-SceneTaskEval-001)

## Purpose
Freeze the minimal schemas and forbidden outputs for SceneTaskEval-001.

## Global boundaries (must hold)
- Output is **state/candidate only**.
- Forbidden semantics (must never appear):
  - execute / release / retry / reopen
  - default-on enablement
  - any direct navigation action directive (turn_now, cross_now, force_walk, etc.)
- Every task candidate must set:
  - `allows_execute_now=false`
- Must preserve evidence semantics:
  - do not rewrite `evidence_type`
  - do not relabel as `controlled_live_stream`
  - do not auto-close `pending_real_sidewalk_run`

## Runtime mode downstream rule
If perception runtime is baseline/mock:
- `scene_task_runtime_mode=baseline_or_mock_downstream`
- `not_scene_task_claimed=true`

## Per-sample output schema (minimum)
Each per-sample scene/task result must include:
- `sample_id`
- `archive_root`
- `source_video_path`
- `perception_runtime_mode`
- `scene_task_runtime_mode`
- `not_scene_task_claimed` (bool)
- `scene_state` (object; schema below)
- `task_candidates` (list; schema below)
- `degraded_scene` (bool)
- `uncertain_scene` (bool)
- `candidate_only` (bool; must be true)
- leakage counters:
  - `direct_execute_leakage_count`
  - `release_retry_reopen_leakage_count`
  - `default_on_leakage_count`
  - `forced_navigation_action_count`
- evidence boundary booleans:
  - `evidence_type_preserved`
  - `controlled_live_stream_false`
  - `phone_local_capture_true`
- `reason_codes` (non-empty list)
- `hard_blockers` (list)
- `soft_followups` (list)

## scene_state minimal schema
Must include:
- `scene_id`
- `scene_type`: `"sidewalk_navigation" | "uncertain_scene"`
- `scene_confidence`: float in [0,1]
- `scene_phase`:
  - `sidewalk_clear_observe`
  - `sidewalk_obstacle_candidate`
  - `sidewalk_narrow_candidate`
  - `sidewalk_uncertain_degraded`
- `active_task_id`
- `task_status`: `"idle" | "candidate_generated"`
- `inserted_task_present=false`
- `recovery_possible` (bool)
- `deviation_detected=false`
- `degraded_mode` (bool)
- `required_perception_signals` (list of signal keys)
- `last_transition_reason` (string)

## task_candidate minimal schema
Each candidate must include:
- `task_candidate_id`
- `task_type` (one of):
  - `continue_observe_candidate`
  - `slow_down_candidate`
  - `keep_clear_path_candidate`
  - `obstacle_attention_candidate`
  - `narrow_path_attention_candidate`
  - `ask_for_help_candidate`
  - `uncertain_observe_candidate`
- `source_scene_id`
- `source_signal_ids` (list; may be empty in baseline/mock but must exist)
- `confidence`: float in [0,1]
- `reason_codes` (list)
- `allows_execute_now=false`

Forbidden fields:
- `execute_now`, `turn_now`, `cross_now`, `force_walk`
- `open_release_window`, `retry_now`, `reopen_now`

