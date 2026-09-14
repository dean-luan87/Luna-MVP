# LUNA — Phone Local Field Batch 001 Plan v0 (Phase-PhoneLocalFieldBatch-001)

## Phase
- Phase: **Phase-PhoneLocalFieldBatch-001**
- Name: **Option A Phone Local Field Capture Batch v0**
- Evidence type: **`phone_local_controlled_capture`**

## Goal (single goal)
Collect a first batch of **newly recorded** Option A sidewalk-short-walk observation videos on phone, then use the existing phone_local toolchain to produce governed bundle + archive evidence and batch-level review signals.

Pipeline:
**phone video → bundle → archive_root → validator → batch review**

## Hard boundaries (must remain true)
- No new runtime.
- No realtime upload.
- No `controlled_live_stream`.
- No full controlled trial.
- No open user testing.
- No default-on.
- No expansion of real side effects surface.
- No Option A expansion (no new scenarios).

## Allowed capture scope (Option A only)
- Sidewalk short distance, observe-only.
- No crossing streets.
- No complex intersections.
- No high-density crowds.
- No sensitive privacy areas.
- No night / rain / extreme conditions.

## Suggested batch (target 5; minimum 3)
Each 30–60s, begin/end still 1–2s, no editing, keep original file.

Recommended naming (input):
- `phone_local_001_clear_path.mp4`
- `phone_local_002_minor_obstacle.mp4`
- `phone_local_003_narrow_path.mp4`
- `phone_local_004_people_far.mp4`
- `phone_local_005_low_confidence_safe.mp4`

Input directory (recommended):
- `input_videos/phone_local_batch_001/`

## Processing success criteria (per sample)
Must all be true for a sample to count as **processed-go**:
- bundle validator = `go`
- archive validator = `go`
- `evidence_type=phone_local_controlled_capture`
- `controlled_live_stream=false`
- `phone_local_capture=true`
- `pending_real_sidewalk_run=true`
- safety assertions all true
- source lineage preserved (bundle id + source media reference)

## Batch-level go / conditional_go / no_go
### GO
- processed samples ≥ 3
- all processed samples bundle/archive validator = go
- evidence_type preserved rate = 1.0
- controlled_live_stream false rate = 1.0
- pending_real_sidewalk_run true rate = 1.0
- hard_blocker_count = 0

### CONDITIONAL_GO
- processed samples ≥ 3 but < 5
- no boundary confusion
- no safety assertion failures
- hard_blocker_count = 0

### NO_GO
- processed samples < 3, OR
- any boundary confusion (mislabel controlled_live, controlled_live_stream=true), OR
- any pending_real_sidewalk_run incorrectly set false, OR
- any safety assertions false, OR
- any archive not verifiable, OR
- any source lineage loss

## Stop condition
Stop when:
- at least 3 new samples complete the full pipeline with validator=go, OR
- the batch produces a clear no_go with specific blockers.

