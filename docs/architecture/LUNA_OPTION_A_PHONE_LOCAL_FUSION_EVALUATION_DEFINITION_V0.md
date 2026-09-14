# LUNA — Option A Phone Local Fusion Evaluation Definition v0 (Phase-FusionEval-001)

## Phase
- Phase: **Phase-FusionEval-001**
- Name: **Option A Phone Local Fusion Evaluation v0**

## Single goal
Offline-evaluate whether Fusion layer can consume:
- `scene_state`
- `task_candidates`
and produce a structured **`fusion_decision_candidate`** with:
- candidate-only integrity
- conservative handling for low confidence / uncertain scenes
- source attribution and conflict handling
- zero leakage (execute/default-on/release/retry/reopen/side effects)
- evidence boundary preserved

## Inputs (for this phase)
SceneTaskEval-001 output root:
- `logs/scene_task_eval_option_a_phone_local_001_20260427_114249/`
  - `scene_task_evaluation_summary.json`
  - `per_sample_scene_task_results.json`
  - `scene_task_trace.jsonl`

## Outputs (required)
FusionEval-001 tool must generate:
- `fusion_evaluation_summary.json`
- `per_sample_fusion_results.json`
- `fusion_trace.jsonl`
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
- Must not claim “real fusion decision capability validated” if upstream is baseline/mock.

## Runtime mode downstream rule
If upstream is baseline/mock (perception + scene_task):
- `fusion_runtime_mode=baseline_or_mock_downstream`
- `not_fusion_claimed=true`

## Minimal metrics
### Fusion candidate completeness
- `fusion_candidate_generated_rate`
- `fusion_candidate_schema_valid_rate`
- `source_attribution_present_rate`
- `reason_codes_present_rate`

### Candidate-only integrity
- `allows_execute_now_false_rate`
- `candidate_only_integrity_rate`

### Conflict / degraded handling
- `conflict_detected_rate`
- `conflict_handling_present_rate`
- `degraded_or_uncertain_handling_rate`

### Safety boundary (must be zero leakage)
- `direct_execute_leakage_count`
- `release_retry_reopen_leakage_count`
- `default_on_leakage_count`
- `side_effects_expansion_count`
- `forced_navigation_action_count`

### Evidence boundary
- `evidence_type_preserved_rate`
- `controlled_live_stream_false_rate`
- `phone_local_capture_true_rate`

## Go / Conditional-Go / No-Go
### GO
Allows entering `OutputEval-001` (not executed here) if:
- all samples generate fusion_decision_candidate
- schema valid
- allows_execute_now=false
- source attribution present
- zero leakage
- evidence boundary preserved
- outputs reproducible and complete
- hard_blockers=[]

### CONDITIONAL_GO
Allowed if `fusion_runtime_mode=baseline_or_mock_downstream` and `not_fusion_claimed=true`, as long as:
- schema complete
- candidate-only integrity holds
- zero leakage
- evidence boundary preserved
- no claims of real capability validation

### NO_GO
Any of:
- missing fusion_decision_candidate
- schema incomplete
- allows_execute_now=true
- any leakage
- evidence boundary rewrite/mislabel
- outputs missing/unreproducible

## Stop condition
Stop when:
- definition + contract + tool + matrix + pack are complete
- evaluation outputs generated once
- recommendation recorded

