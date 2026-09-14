# LUNA — Option A Phone Local Perception Evaluation Go/No-Go Pack v0 (Phase-PerceptionEval-001)

## Inputs
- Definition:
  - `docs/architecture/LUNA_OPTION_A_PHONE_LOCAL_PERCEPTION_EVALUATION_DEFINITION_V0.md`
- Signal eval contract:
  - `docs/architecture/LUNA_OPTION_A_PHONE_LOCAL_PERCEPTION_SIGNAL_EVAL_CONTRACT_V0.md`
- Evaluation matrix:
  - `docs/architecture/LUNA_OPTION_A_PHONE_LOCAL_PERCEPTION_EVALUATION_MATRIX_V0.md`
- Baseline sample_matrix:
  - `logs/phone_local_field_batch_002_20260427_111431/sample_matrix.json`

## Required evaluation outputs (per run)
- `logs/perception_eval_option_a_phone_local_001_<timestamp>/perception_evaluation_summary.json`
- `logs/perception_eval_option_a_phone_local_001_<timestamp>/per_sample_results.json`
- `logs/perception_eval_option_a_phone_local_001_<timestamp>/signal_trace.jsonl`
- `logs/perception_eval_option_a_phone_local_001_<timestamp>/evaluation_notes.md`

## Decision record (fill after running tool)
- evaluation_output_root: `logs/perception_eval_option_a_phone_local_001_20260427_113330/`
- perception_runtime_mode: `baseline_or_mock`
- not_model_claimed: `true`
- recommendation: **CONDITIONAL_GO**
- hard_blockers: `[]`
- soft_followups:
  - `baseline_or_mock_mode_in_effect`
- recommended next phase:
  - **Phase-SceneTaskEval-001** (allowed by criteria; do not enter automatically)

## Go / Conditional-Go / No-Go criteria (frozen)
### GO
Allows entering `SceneTaskEval-001` (not executed here) if:
- all samples readable
- five signals present (or explicit `not_available` where allowed)
- no fabricated unavailable capabilities
- leakage counts all 0
- evidence boundary preserved
- outputs reproducible and complete
- hard_blockers=[]

### CONDITIONAL_GO
Allowed if `perception_runtime_mode=baseline_or_mock` and `not_model_claimed=true`, as long as:
- schema complete
- zero leakage
- evidence boundary preserved

### NO_GO
Any of:
- sample read failure
- schema incomplete without explicit `not_available`
- any leakage
- evidence boundary rewrite/mislabel
- low confidence forced action outputs
- outputs missing/unreproducible

## Boundary statement (must remain true)
- Default path remains disabled.
- Full controlled trial not entered.
- Real side effects surface not expanded.
- No controlled_live_stream executed.
- Option A not expanded.
- No navigation action execution.

