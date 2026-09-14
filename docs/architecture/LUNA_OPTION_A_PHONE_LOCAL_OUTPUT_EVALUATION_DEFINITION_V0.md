# LUNA — Option A Phone Local Output Candidate Evaluation Definition v0 (Phase-OutputEval-001)

## Phase
- Phase: **Phase-OutputEval-001**
- Name: **Option A Phone Local Output Candidate Evaluation v0**

## Single goal
Offline-evaluate whether Output layer can consume `fusion_decision_candidate` and produce a compliant:
- `navigation_output_candidate`
with:
- candidate-only integrity
- timing/validity windows
- priority + suppression/silence handling
- no forbidden semantics (execute/release/retry/reopen/default-on)
- **no real TTS** (`real_tts_invoked=false`)
- evidence boundary preserved

## Inputs (for this phase)
FusionEval-001 output root:
- `logs/fusion_eval_option_a_phone_local_001_20260427_115320/`
  - `fusion_evaluation_summary.json`
  - `per_sample_fusion_results.json`
  - `fusion_trace.jsonl`

## Outputs (required)
OutputEval-001 tool must generate:
- `output_evaluation_summary.json`
- `per_sample_output_results.json`
- `output_trace.jsonl`
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
- Must not rewrite archive evidence_type or pending flags.
- Must not claim “real output policy validated” if upstream is baseline/mock.

## Runtime mode downstream rule
If upstream is baseline/mock:
- `output_runtime_mode=baseline_or_mock_downstream`
- `not_output_claimed=true`

## Timing / priority minimal rules (v0)
Must populate:
- `generated_at_ms`
- `expires_at_ms`
- `validity_window_ms`
and require:
- `expires_at_ms > generated_at_ms`

Default validity windows (ms):
- `safety_warning_candidate`: 2500
- `dynamic_event`: 1500
- `navigation_instruction_candidate`: 8000
- `status_confirmation`: 12000
- `low_confidence_notice`: 5000
- `ask_for_help_prompt`: 10000
- `wait_or_observe`: 3000
- `silence`: 2000

## Go / Conditional-Go / No-Go
### GO
Allows entering EndToEndOfflineEval-001 if:
- all samples generate `navigation_output_candidate`
- schema valid
- `allows_execute_now=false` for all
- `real_tts_invoked=false` for all
- timing fields complete and consistent
- forbidden semantics count = 0
- zero leakage (execute/default-on/release/retry/reopen/side effects)
- evidence boundary preserved
- outputs reproducible and complete
- hard_blockers=[]

### CONDITIONAL_GO
Allowed if downstream is baseline/mock, as long as:
- schema complete
- candidate-only + no-real-TTS integrity holds
- zero leakage and forbidden semantics
- evidence boundary preserved
- no claims of real output policy validation

### NO_GO
Any of:
- missing navigation_output_candidate
- schema incomplete
- `allows_execute_now=true`
- `real_tts_invoked=true`
- forbidden semantics present
- any leakage
- evidence boundary rewrite/mislabel
- timing fields missing/inconsistent

## Stop condition
Stop when:
- definition + contract + tool + matrix + pack are complete
- evaluation outputs generated once
- recommendation recorded

