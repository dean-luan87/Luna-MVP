# LUNA — Option A Phone Local End-to-End Offline Evaluation Definition v0 (Phase-EndToEndOfflineEval-001)

## Phase
- Phase: **Phase-EndToEndOfflineEval-001**
- Name: **Option A Phone Local End-to-End Offline Evaluation v0**

## Single goal
Perform a single end-to-end **offline** verification across the five-stage candidate chain:

`phone_local archive` → `perception signals` → `scene_state/task_candidates` → `fusion_decision_candidate` → `navigation_output_candidate`

and confirm that, for all samples:
- chain completeness holds (all stages present)
- schemas are present/valid at v0 level
- candidate-only integrity holds (`allows_execute_now=false` everywhere)
- no-real-TTS holds (`real_tts_invoked=false`)
- safety leakage is 0 across all stages
- evidence boundary preserved (`evidence_type`, `controlled_live_stream=false`, `phone_local_capture=true`, pending flags not closed)
- no claims of real model capability validation

## Inputs (frozen for this run)
- FieldBatch-002: `logs/phone_local_field_batch_002_20260427_111431/`
- PerceptionEval-001: `logs/perception_eval_option_a_phone_local_001_20260427_113330/`
- SceneTaskEval-001: `logs/scene_task_eval_option_a_phone_local_001_20260427_114249/`
- FusionEval-001: `logs/fusion_eval_option_a_phone_local_001_20260427_115320/`
- OutputEval-001: `logs/output_eval_option_a_phone_local_001_20260427_120617/`

## Outputs (required)
The end-to-end tool must generate:
- `end_to_end_offline_evaluation_summary.json`
- `per_sample_chain_results.json`
- `chain_trace_consistency.json`
- `evaluation_notes.md`

## Hard boundaries (must remain true)
- No Option A expansion.
- No `controlled_live_stream`.
- No full controlled trial.
- No open user testing.
- No default-on.
- No expansion of real side effects surface.
- No model execution authority.
- No navigation action execution.
- No real TTS emission.
- Must not rewrite evidence_type or pending flags.
- Must not claim real model/navigation capability validation.

## Go / Conditional-Go / No-Go
### GO
Allows recommending next phase if:
- 3 samples are complete across all five stages
- schema checks pass
- `allows_execute_now=false` across all stages
- `real_tts_invoked=false` across all stages
- leakage totals are 0
- evidence boundary preserved
- `hard_blockers=[]`

### CONDITIONAL_GO
Allowed if:
- upstream runtime modes are baseline/mock/downstream
- sample_count=3 and sample_count_partial may exist
but must still satisfy:
- chain completeness + safety boundary + evidence boundary + reproducibility

### NO_GO
Any of:
- missing any stage result
- schema invalid/missing without explicit marker
- any `allows_execute_now=true`
- any `real_tts_invoked=true`
- any leakage detected
- evidence boundary rewrite/mislabel
- pending flags incorrectly closed
- outputs missing/unreproducible

## Stop condition
Stop when:
- definition + contract + tool + matrix + pack complete
- one evaluation run completes
- recommendation recorded

