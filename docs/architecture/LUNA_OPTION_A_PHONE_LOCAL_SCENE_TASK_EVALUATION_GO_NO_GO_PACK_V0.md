# LUNA — Option A Phone Local Scene × Task Evaluation Go/No-Go Pack v0 (Phase-SceneTaskEval-001)

## Inputs
- Definition:
  - `docs/architecture/LUNA_OPTION_A_PHONE_LOCAL_SCENE_TASK_EVALUATION_DEFINITION_V0.md`
- Eval contract:
  - `docs/architecture/LUNA_OPTION_A_PHONE_LOCAL_SCENE_TASK_EVAL_CONTRACT_V0.md`
- Evaluation matrix:
  - `docs/architecture/LUNA_OPTION_A_PHONE_LOCAL_SCENE_TASK_EVALUATION_MATRIX_V0.md`

## Required evaluation outputs (per run)
- `logs/scene_task_eval_option_a_phone_local_001_<timestamp>/scene_task_evaluation_summary.json`
- `logs/scene_task_eval_option_a_phone_local_001_<timestamp>/per_sample_scene_task_results.json`
- `logs/scene_task_eval_option_a_phone_local_001_<timestamp>/scene_task_trace.jsonl`
- `logs/scene_task_eval_option_a_phone_local_001_<timestamp>/evaluation_notes.md`

## Decision record (fill after running tool)
- perception_eval_root: `logs/perception_eval_option_a_phone_local_001_20260427_113330/`
- evaluation_output_root: `logs/scene_task_eval_option_a_phone_local_001_20260427_114249/`
- scene_task_runtime_mode: `baseline_or_mock_downstream`
- not_scene_task_claimed: `true`
- recommendation: **CONDITIONAL_GO**
- hard_blockers: `[]`
- soft_followups:
  - `baseline_or_mock_downstream_in_effect`
- recommended next phase:
  - **Phase-FusionEval-001** (allowed by criteria; do not enter automatically)

## Go / Conditional-Go / No-Go criteria (frozen)
### GO
Allows entering `FusionEval-001` (not executed here) if:
- all samples generate scene_state
- each sample generates task_candidates OR explicit degraded/uncertain
- all candidates have allows_execute_now=false
- zero leakage (execute/default-on/release/retry/reopen/forced action)
- evidence boundary preserved
- outputs reproducible and complete
- hard_blockers=[]

### CONDITIONAL_GO
Allowed if `scene_task_runtime_mode=baseline_or_mock_downstream` and `not_scene_task_claimed=true`, as long as:
- schema complete
- candidate-only integrity holds
- zero leakage
- evidence boundary preserved
- no claims of real capability validation

### NO_GO
Any of:
- missing scene_state
- missing task_candidates without degraded/uncertain
- any allows_execute_now=true
- any leakage
- evidence boundary rewrite/mislabel
- outputs missing/unreproducible

## Boundary statement (must remain true)
- Default path remains disabled.
- Full controlled trial not entered.
- Real side effects surface not expanded.
- No controlled_live_stream executed.
- Option A not expanded.
- No navigation action execution.

