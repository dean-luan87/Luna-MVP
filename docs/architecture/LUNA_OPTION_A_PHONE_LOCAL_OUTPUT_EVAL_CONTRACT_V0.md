# LUNA — Option A Phone Local Output Eval Contract v0 (Phase-OutputEval-001)

## Purpose
Freeze minimal schema, timing rules, and forbidden semantics for OutputEval-001.

## Global boundaries (must hold)
- Output must be **`navigation_output_candidate` only** (candidate-only).
- No real TTS: `real_tts_invoked=false` always.
- Forbidden semantics (must never appear):
  - execute / release / retry / reopen
  - default-on enablement
  - direct navigation action directives (turn_now, cross_now, force_walk, etc.)
  - `actual_tts_emit`, `play_audio_now`
- `allows_execute_now=false` always.
- Must preserve evidence semantics:
  - do not rewrite `evidence_type`
  - do not relabel as `controlled_live_stream`
  - do not auto-close `pending_real_sidewalk_run`

## Runtime mode downstream rule
If upstream is baseline/mock:
- `output_runtime_mode=baseline_or_mock_downstream`
- `not_output_claimed=true`

## Per-sample output schema (minimum)
Each per-sample output result must include:
- `sample_id`
- `archive_root`
- `source_video_path`
- `perception_runtime_mode`
- `scene_task_runtime_mode`
- `fusion_runtime_mode`
- `output_runtime_mode`
- `not_output_claimed` (bool)
- `fusion_candidate_id`
- `navigation_output_candidate` (object; schema below)
- extracted convenience fields:
  - `output_type`
  - `priority`
  - `message_template_id`
  - `message_text_candidate`
  - `validity_window_ms`
  - `repeat_policy`
  - `suppression_reason`
  - `requires_user_confirmation`
  - `requires_human_help`
  - `confidence`
  - `candidate_only`
  - `allows_execute_now`
  - `real_tts_invoked`
- leakage counters (must be zero):
  - `direct_execute_leakage_count`
  - `release_retry_reopen_leakage_count`
  - `default_on_leakage_count`
  - `side_effects_expansion_count`
  - `forbidden_output_semantic_count`
- evidence boundary booleans:
  - `evidence_type_preserved`
  - `controlled_live_stream_false`
  - `phone_local_capture_true`
- `reason_codes` (non-empty list)
- `hard_blockers` (list)
- `soft_followups` (list)

## navigation_output_candidate minimal schema
Must include:
- `output_candidate_id`
- `source_fusion_candidate_id`
- `source_type="fusion_decision_candidate"`
- `output_type` (one of):
  - `safety_warning_candidate`
  - `navigation_instruction_candidate`
  - `status_confirmation`
  - `low_confidence_notice`
  - `ask_for_help_prompt`
  - `wait_or_observe`
  - `silence`
- `priority` (one of): `critical | high | medium | low | silent`
- `message_template_id`
- `message_text_candidate`
- `generated_at_ms`
- `expires_at_ms`
- `validity_window_ms`
- `repeat_policy`
- `suppression_reason`
- `requires_user_confirmation`
- `requires_human_help`
- `confidence` (float in [0,1])
- `reason_codes` (list)
- `allows_execute_now=false`
- `real_tts_invoked=false`

## Timing integrity rules (must pass)
- `validity_window_ms` present and > 0
- `expires_at_ms > generated_at_ms`
- `expires_at_ms - generated_at_ms == validity_window_ms` (exact for v0)

## v0 validity_window defaults (ms)
- `safety_warning_candidate`: 2500
- `dynamic_event` (if represented via output): 1500
- `navigation_instruction_candidate`: 8000
- `status_confirmation`: 12000
- `low_confidence_notice`: 5000
- `ask_for_help_prompt`: 10000
- `wait_or_observe`: 3000
- `silence`: 2000

