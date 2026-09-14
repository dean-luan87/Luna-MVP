# LUNA — Option A Phone Local Field Baseline Policy v0 (Phase-PhoneLocalReview-002)

## Purpose
Define whether FieldBatch-002 is accepted as the current **Option A phone_local field baseline v0**, and define how it may be used for subsequent evaluation phases (perception/scene-chain evaluation) without expanding scope.

This is a policy/governance document only. No runtime changes.

## Definitions
- **Baseline (Option A / phone_local / v0)**:
  - A minimal curated set of **newly captured** phone_local samples that:
    - pass validators,
    - preserve boundaries and lineage,
    - are stable enough to start evaluation work (perception/scene-chain),
    - do not imply realtime controlled live capability.

## Hard boundaries (must remain true)
- `phone_local_controlled_capture` is not `controlled_live_stream`.
- `pending_real_sidewalk_run` must not be auto-closed.
- No Option A expansion (no new scenario types).
- No controlled_live_stream, no full controlled trial, no open user testing.
- No default-on and no real side effects surface expansion.

## Baseline candidate
- FieldBatch-002 outputs:
  - `logs/phone_local_field_batch_002_20260427_111431/batch_summary.json`
  - `logs/phone_local_field_batch_002_20260427_111431/sample_matrix.json`

Samples (3):
- `phone_local_001_clear_path`
- `phone_local_002_minor_obstacle`
- `phone_local_003_narrow_path`

## Acceptance policy decision
### Decision
**ACCEPT** FieldBatch-002 as **Option A phone_local field baseline v0**.

### Rationale (why acceptable at v0)
- All three samples are validator=go and manifest-pass.
- Evidence boundaries are preserved:
  - `evidence_type=phone_local_controlled_capture`
  - `controlled_live_stream=false`
  - `pending_real_sidewalk_run=true`
- Lineage is preserved (`source_bundle_id`, `source_media_path`, original filename).
- Safety assertions are true (candidate-only posture is maintained).

### Sample count note
- `sample_count_partial=true` (3 samples) is accepted for baseline v0.
- Adding 2 more samples (to reach 5) is a **soft follow-up**, not a blocker.

## Allowed next phase type (evaluation-only)
If Review-002 is GO, the next phase may be:
- **Phase-PerceptionEval-001: Option A Phone Local Sample Perception Evaluation v0**

Constraints for evaluation phases:
- must not introduce runtime execution authority,
- must not enable default-on,
- must not expand scenario scope,
- must keep evidence-type semantics intact (do not relabel as controlled live).

## Explicit non-claims (must be stated)
Accepting the baseline does NOT claim:
- realtime controlled live stability,
- navigation action correctness,
- readiness for full controlled trial,
- readiness for open user testing.

