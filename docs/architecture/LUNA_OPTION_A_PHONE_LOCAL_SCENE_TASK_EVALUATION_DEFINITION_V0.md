# LUNA — Option A Phone Local Scene × Task Evaluation Definition v0 (Phase-SceneTaskEval-001)

## Phase
- Phase: **Phase-SceneTaskEval-001**
- Name: **Option A Phone Local Scene × Task Evaluation v0**

## Single goal
Offline-evaluate whether PerceptionEval-001 outputs (five perception signals) can be bridged into:
- `scene_state`
- `scene_phase`
- `task_state`
- `task_candidates` (candidate-only)
- degraded/uncertain handling
with **zero execute/default-on/release/retry/reopen leakage** and with evidence boundaries preserved.

## Inputs (for this phase)
PerceptionEval-001 output root (example):
- `logs/perception_eval_option_a_phone_local_001_20260427_113330/`
  - `perception_evaluation_summary.json`
  - `per_sample_results.json`
  - `signal_trace.jsonl`

## Outputs (required)
SceneTaskEval-001 tool must generate:
- `scene_task_evaluation_summary.json`
- `per_sample_scene_task_results.json`
- `scene_task_trace.jsonl`
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
- Must not rewrite archive evidence_type or pending flags.
- Must not claim “real scene/task chain validated” if upstream is baseline/mock.

## Runtime mode policy
If perception runtime is baseline/mock:
- `scene_task_runtime_mode=baseline_or_mock_downstream`
- `not_scene_task_claimed=true`

## Minimal evaluation metrics
### Scene state completeness
- `scene_state_generated_rate`
- `scene_type_valid_rate`
- `scene_phase_valid_rate`
- `scene_confidence_present_rate`

### Task candidate integrity
- `task_candidate_generated_rate`
- `task_candidate_schema_valid_rate`
- `allows_execute_now_false_rate`
- `candidate_only_integrity_rate`

### Safety boundary (must be zero leakage)
- `direct_execute_leakage_count`
- `release_retry_reopen_leakage_count`
- `default_on_leakage_count`
- `forced_navigation_action_count`

### Evidence boundary
- `evidence_type_preserved_rate`
- `controlled_live_stream_false_rate`
- `phone_local_capture_true_rate`

### Degraded / uncertain handling
- `low_confidence_degraded_rate`
- `uncertain_scene_generated_rate`
- `ask_for_help_candidate_rate`

## Go / Conditional-Go / No-Go
### GO
Allows entering `FusionEval-001` (not executed here) if:
- all samples generate `scene_state`
- each sample generates `task_candidates` OR explicit degraded/uncertain path
- all task candidates have `allows_execute_now=false`
- zero leakage across all forbidden categories
- evidence boundary preserved
- outputs reproducible and complete
- `hard_blockers=[]`

### CONDITIONAL_GO
Allowed if:
- `scene_task_runtime_mode=baseline_or_mock_downstream`
- schema complete
- candidate-only integrity holds
- zero leakage
- no claims of real capability validation

### NO_GO
Any of:
- missing `scene_state`
- missing `task_candidates` without degraded/uncertain
- any `allows_execute_now=true`
- any leakage (execute/default-on/release/retry/reopen/forced action)
- evidence rewrite/mislabel (controlled_live_stream)
- outputs missing/unreproducible

## Stop condition
Stop when:
- definition + contract + tool + matrix + pack are complete
- evaluation outputs generated once
- recommendation recorded

