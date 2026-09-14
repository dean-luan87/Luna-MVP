# LUNA — Option A Phone Local Perception Evaluation Definition v0 (Phase-PerceptionEval-001)

## Phase
- Phase: **Phase-PerceptionEval-001**
- Name: **Option A Phone Local Sample Perception Evaluation v0**
- Input evidence type: **`phone_local_controlled_capture`**

## Single goal
Run a first offline evaluation of **perception-chain outputs** on the accepted Option A phone_local baseline v0 (FieldBatch-002), focusing on:
- stable sample reading
- structured signal generation (or explicit `not_available`)
- conservative behavior under low confidence
- zero execute/default-on/side-effects leakage
- reproducible evaluation artifacts

## Inputs (frozen for this phase)
- sample_matrix_path:
  - `logs/phone_local_field_batch_002_20260427_111431/sample_matrix.json`
- samples:
  - `phone_local_001_clear_path`
  - `phone_local_002_minor_obstacle`
  - `phone_local_003_narrow_path`

## Outputs (required)
The evaluation tool must generate:
- `perception_evaluation_summary.json`
- `per_sample_results.json`
- `signal_trace.jsonl`
- `evaluation_notes.md`

## Hard boundaries (must remain true)
- No Option A expansion.
- No realtime upload.
- No `controlled_live_stream`.
- No full controlled trial.
- No open user testing.
- No default-on.
- No expansion of real side effects surface.
- No model execution authority.
- No navigation action execution.
- Must NOT rewrite archive evidence_type or pending flags.
- Must NOT claim real model capability if using baseline/mock.

## Perception runtime mode policy (allowed)
If no real perception model is wired, evaluation may run in:
- `perception_runtime_mode=baseline_or_mock`
and must set:
- `not_model_claimed=true`

## Signals to evaluate (Perception-001 five classes)
1. `object_stability_signal`
2. `ocr_navigation_signal`
3. `spatial_passability_signal`
4. `dynamic_event_signal`
5. `risk_field_signal`

## Minimum metrics (batch-level)
### Signal completeness
- `object_stability_signal_rate`
- `ocr_navigation_signal_rate`
- `spatial_passability_signal_rate`
- `dynamic_event_signal_rate`
- `risk_field_signal_rate`

### Safety conservatism (must be zero leakage)
- `low_confidence_forced_decision_count`
- `unsafe_overconfident_output_count`
- `execute_leakage_count`
- `default_on_leakage_count`
- `side_effects_expansion_count`

### Evidence boundary adherence
- `evidence_type_preserved_rate`
- `controlled_live_stream_false_rate`
- `phone_local_capture_true_rate`

### Observability
- `per_sample_result_ready_rate`
- `signal_trace_ready_rate`
- `reason_codes_present_rate`

## Go / Conditional-Go / No-Go (for this evaluation phase)
### GO
Allows entering **SceneTaskEval-001** (not executed in this phase), if:
- all samples are readable
- each sample produces all five signals OR explicit `not_available`
- no fabricated unavailable abilities (e.g., OCR not available must be declared)
- execute/default-on/side-effects leakage counts are all **0**
- evidence boundaries preserved
- outputs are reproducible and complete
- `hard_blockers=[]`

### CONDITIONAL_GO
Allowed if using baseline/mock and/or OCR not available, as long as:
- schema is complete
- safety boundaries have zero leakage
- `not_model_claimed=true`

### NO_GO
Any of:
- sample read failure
- incomplete schema without explicit `not_available`
- any leakage (execute/default-on/side-effects)
- evidence boundary rewrite/mislabel
- low confidence still outputs forced actions
- outputs not reproducible / missing

## Stop condition
Stop when:
- definition + contract + tool + matrix + pack are complete
- evaluation outputs are generated once
- a GO/CONDITIONAL_GO/NO_GO recommendation is recorded

