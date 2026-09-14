# LUNA — Phone Local Field Batch 001 Reused Sample Boundary Note v0 (Phase-PhoneLocalFieldBatch-001)

## Purpose
Record the explicit boundary that FieldBatch-001 (current executed run) used **reused existing videos** as a placeholder batch, and therefore must not be described as “newly captured field batch completed”.

## What happened (facts)
- A batch run was executed to validate the **phone_local batch pipeline** end-to-end:
  - phone video → bundle → archive_root → validator → batch summary/matrix
- Input videos were **not newly recorded for this batch**.
- Instead, they were copied from:
  - `input_videos/sidewalk/`
  into:
  - `input_videos/phone_local_batch_001/`

Batch outputs:
- `batch_summary_path`: `/Users/luanlei/LunaRuntime/logs/phone_local_field_batch_001_20260424_154409/batch_summary.json`
- `sample_matrix_path`: `/Users/luanlei/LunaRuntime/logs/phone_local_field_batch_001_20260424_154409/sample_matrix.json`

## What this placeholder batch can prove
- The FieldBatch-001 **batch processing toolchain** is functioning and stable:
  - processed samples: 3/3
  - bundle/archive validators: go
  - boundary fields preserved (`phone_local_controlled_capture`, `controlled_live_stream=false`, `pending_real_sidewalk_run=true`)
  - safety assertions pass
  - no hard blockers

## What this placeholder batch cannot prove
- It does not prove the stability/completeness of **newly recorded** phone field samples for the batch.
- It does not constitute completion of “new field sample collection”.

## Required follow-up (must be done next)
- Record **3–5 newly captured** Option A phone videos and place them in:
  - `input_videos/phone_local_batch_002/`
- Run the same batch toolchain and produce:
  - `batch_summary.json`
  - `sample_matrix.json`
- Then perform review and record the decision for Batch-002.

## Non-negotiable boundaries (still true)
- No realtime upload; no controlled_live_stream.
- No full controlled trial.
- No open user testing.
- No default-on.
- No real side effects surface expansion.
- No Option A expansion.

