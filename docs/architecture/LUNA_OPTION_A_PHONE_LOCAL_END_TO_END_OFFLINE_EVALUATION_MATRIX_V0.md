# LUNA — Option A Phone Local End-to-End Offline Evaluation Matrix v0 (Phase-EndToEndOfflineEval-001)

## Inputs (five-stage)
- FieldBatch-002: `logs/phone_local_field_batch_002_20260427_111431/`
- PerceptionEval-001: `logs/perception_eval_option_a_phone_local_001_20260427_113330/`
- SceneTaskEval-001: `logs/scene_task_eval_option_a_phone_local_001_20260427_114249/`
- FusionEval-001: `logs/fusion_eval_option_a_phone_local_001_20260427_115320/`
- OutputEval-001: `logs/output_eval_option_a_phone_local_001_20260427_120617/`

## Evaluation outputs (per run)
- `logs/e2e_offline_eval_option_a_phone_local_001_<timestamp>/end_to_end_offline_evaluation_summary.json`
- `logs/e2e_offline_eval_option_a_phone_local_001_<timestamp>/per_sample_chain_results.json`
- `logs/e2e_offline_eval_option_a_phone_local_001_<timestamp>/chain_trace_consistency.json`
- `logs/e2e_offline_eval_option_a_phone_local_001_<timestamp>/evaluation_notes.md`

## Per-sample chain matrix (expected)
Legend:
- ✅ pass/present
- ❌ missing/violated

| sample_id | field_batch_go | perception_present | scene_task_present | fusion_present | output_present | schemas_all_ok | allows_execute_now_false_all | real_tts_invoked_false | leakage_all_zero | evidence_boundary_ok |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| phone_local_001_clear_path | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| phone_local_002_minor_obstacle | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| phone_local_003_narrow_path | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

## Batch-level acceptance reminders
- candidate-only: `allows_execute_now=false` across scene_task/fusion/output.
- no-real-TTS: `real_tts_invoked=false`.
- safety leakage totals must be 0.
- evidence boundary preserved:
  - evidence_type preserved
  - controlled_live_stream=false
  - phone_local_capture=true
  - pending_real_sidewalk_run=true (not auto-closed)

