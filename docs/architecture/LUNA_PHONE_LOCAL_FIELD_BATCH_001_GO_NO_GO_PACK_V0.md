# LUNA — Phone Local Field Batch 001 Go/No-Go Pack v0 (Phase-PhoneLocalFieldBatch-001)

## Pack purpose
Consolidate:
- Batch plan
- Runbook
- Sample matrix
- Batch processing outputs (`batch_summary.json`, `sample_matrix.json`)
and record the formal batch decision.

This pack does not add runtime; it references the batch tool output.

## Inputs
- Plan: `docs/architecture/LUNA_PHONE_LOCAL_FIELD_BATCH_001_PLAN_V0.md`
- Runbook: `docs/architecture/LUNA_PHONE_LOCAL_FIELD_BATCH_001_RUNBOOK_V0.md`
- Sample matrix template: `docs/architecture/LUNA_PHONE_LOCAL_FIELD_BATCH_001_SAMPLE_MATRIX_V0.md`
- Batch tool:
  - `tools/run_phone_local_field_batch_001_v0.py`

## Required batch outputs (per run)
- `logs/phone_local_field_batch_001_<timestamp>/batch_summary.json`
- `logs/phone_local_field_batch_001_<timestamp>/sample_matrix.json`

## Executed batch run record (placeholder batch)
- **batch_summary_path**: `/Users/luanlei/LunaRuntime/logs/phone_local_field_batch_001_20260424_154409/batch_summary.json`
- **sample_matrix_path**: `/Users/luanlei/LunaRuntime/logs/phone_local_field_batch_001_20260424_154409/sample_matrix.json`
- **sample_source_type**: `reused_existing_video` (占位批次；从 `input_videos/sidewalk/` 复制复用，不等同新拍摄外场批次)

## Go / Conditional-Go / No-Go criteria (frozen)
### GO
Must all hold:
- processed samples ≥ 3
- each processed sample:
  - bundle validator = `go`
  - archive validator = `go`
  - `evidence_type=phone_local_controlled_capture`
  - `controlled_live_stream=false`
  - `phone_local_capture=true`
  - `pending_real_sidewalk_run=true`
  - safety assertions true
  - lineage preserved (bundle id + source media reference)
- `hard_blocker_count=0`

### CONDITIONAL_GO
Allowed:
- processed samples = 3 or 4 (target is 5)
- device_info and operator_notes remain v0 defaults
But must hold:
- no boundary confusion
- no safety assertion failures
- `hard_blocker_count=0`

### NO_GO
Any of:
- processed samples < 3
- any `controlled_live_stream=true`
- any evidence_type mislabel / confusion with controlled_live
- any `pending_real_sidewalk_run=false`
- any safety assertion false
- any archive not verifiable
- any lineage loss
- any hard blocker present

## Decision record (fill after running batch)
- Batch output root: `logs/phone_local_field_batch_001_20260424_154409/`
- Decision (multi-axis):
  - **pipeline_validation_recommendation**: `go`
  - **placeholder_batch_recommendation**: `go`
  - **new_field_sample_collection_recommendation**: `conditional_go`
- Hard blockers: `[]`
- Soft follow-ups:
  - `need_new_phone_local_field_samples` (手机新拍 3–5 条真实 batch 样本后再跑同一套 batch tool)
- Recommended next phase:
  - **Phase-PhoneLocalFieldBatch-002: Option A New Phone Local Field Sample Collection v0**

## Boundary statement (must remain true)
- Default path remains disabled.
- Full controlled trial not entered.
- Real side effects surface not expanded.
- No controlled_live_stream executed.
- Option A not expanded.

