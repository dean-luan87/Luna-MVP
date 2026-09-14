# LUNA — Option A Phone Local End-to-End Offline Eval Contract v0 (Phase-EndToEndOfflineEval-001)

## Purpose
Freeze:
- the five-stage checklist
- required input/output paths
- end-to-end boundary assertions
- forbidden semantics
- per-sample checks and batch metrics

## Stage checklist (must all be present per sample)
1. FieldBatch (bundle/archive validators are go via batch summary)
2. PerceptionEval (per-sample perception results exist; five signals schema present)
3. SceneTaskEval (per-sample scene_state + task_candidates exist)
4. FusionEval (per-sample fusion_decision_candidate exists)
5. OutputEval (per-sample navigation_output_candidate exists)

## Global boundaries (must hold)
- Offline evaluation only.
- Candidate-only integrity:
  - `allows_execute_now=false` for scene_task candidates, fusion candidate, output candidate
- No real TTS:
  - `real_tts_invoked=false` for output candidates
- Forbidden semantics must never appear:
  - execute / release / retry / reopen
  - default-on enablement
  - direct navigation action directives (turn_now, cross_now, force_walk, etc.)
- Evidence boundary must remain true:
  - `evidence_type=phone_local_controlled_capture`
  - `controlled_live_stream=false`
  - `phone_local_capture=true`
  - `pending_real_sidewalk_run=true` (must not auto-close)

## Tool inputs (required flags)
The tool must accept:
- `--field-batch-root`
- `--perception-eval-root`
- `--scene-task-eval-root`
- `--fusion-eval-root`
- `--output-eval-root`
- `--output-root`

## Per-sample checks (minimum)
For each `sample_id`, record:
- identity/paths:
  - `sample_id`
  - `archive_root`
  - `source_video_path`
- stage presence:
  - `bundle_archive_go` (from field batch counts; assume true if sample present and batch is go)
  - `perception_result_present`
  - `scene_task_result_present`
  - `fusion_result_present`
  - `output_result_present`
- runtime modes:
  - `perception_runtime_mode`
  - `scene_task_runtime_mode`
  - `fusion_runtime_mode`
  - `output_runtime_mode`
- schema flags:
  - `perception_signal_schema_ok`
  - `scene_state_schema_ok`
  - `task_candidate_schema_ok`
  - `fusion_candidate_schema_ok`
  - `output_candidate_schema_ok`
- candidate-only / no-TTS:
  - `allows_execute_now_false_all_stages`
  - `real_tts_invoked_false`
- leakage totals (must be zero):
  - `direct_execute_leakage_count_total`
  - `release_retry_reopen_leakage_count_total`
  - `default_on_leakage_count_total`
  - `side_effects_expansion_count_total`
  - `forced_navigation_action_count_total`
  - `forbidden_output_semantic_count_total`
- evidence boundary:
  - `evidence_type_preserved_all_stages`
  - `controlled_live_stream_false_all_stages`
  - `phone_local_capture_true_all_stages`
  - `pending_real_sidewalk_run_true`
- `reason_codes_present`
- `hard_blockers`
- `soft_followups`

## Batch metrics (minimum)
- Completeness rates:
  - `sample_chain_complete_rate`
  - `perception_stage_complete_rate`
  - `scene_task_stage_complete_rate`
  - `fusion_stage_complete_rate`
  - `output_stage_complete_rate`
- Schema integrity rates:
  - `perception_schema_valid_rate`
  - `scene_task_schema_valid_rate`
  - `fusion_schema_valid_rate`
  - `output_schema_valid_rate`
- Candidate-only integrity rates:
  - `allows_execute_now_false_all_stages_rate`
  - `candidate_only_integrity_rate`
  - `real_tts_invoked_false_rate`
- Evidence boundary rates:
  - `evidence_type_preserved_all_stages_rate`
  - `controlled_live_stream_false_all_stages_rate`
  - `phone_local_capture_true_all_stages_rate`
  - `pending_real_sidewalk_run_true_rate`
- Leakage totals (must be zero):
  - all totals listed above

