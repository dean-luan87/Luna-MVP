# LUNA — Phone Local Field Batch 001 Sample Matrix v0 (Phase-PhoneLocalFieldBatch-001)

## Purpose
Matrix template for recording per-sample processing results for FieldBatch-001.

Primary source of truth for actual results is:
- `logs/phone_local_field_batch_001_<timestamp>/sample_matrix.json`

This file provides a human-readable table format that can be filled after each batch run.

## Batch run record (placeholder batch)
This phase has one executed batch run used to validate the **batch pipeline**, with **reused existing videos** copied from `input_videos/sidewalk/` into `input_videos/phone_local_batch_001/`.

- **batch_summary_path**: `/Users/luanlei/LunaRuntime/logs/phone_local_field_batch_001_20260424_154409/batch_summary.json`
- **sample_matrix_path**: `/Users/luanlei/LunaRuntime/logs/phone_local_field_batch_001_20260424_154409/sample_matrix.json`
- **sample_source_type**: `reused_existing_video` (占位批次；不是新拍摄外场样本)

## Table (fill per sample)
| sample_id | source_video_path | bundle_root | archive_root | bundle_validator | archive_validator | evidence_type | controlled_live_stream | phone_local_capture | pending_real_sidewalk_run | hard_blockers | soft_followups |
|---|---|---|---|---|---|---|---|---|---|---|---|
| phone_local_001_clear_path | `/Users/luanlei/Desktop/Luna-Workspace-Min/input_videos/phone_local_batch_001/phone_local_001_clear_path.mp4` | `logs/phone_local_field_batch_001_20260424_154409/bundles/phone_local_001_clear_path` | `logs/phone_local_field_batch_001_20260424_154409/archives/phone_local_001_clear_path` | go | go | phone_local_controlled_capture | false | true | true | [] | [] |
| phone_local_002_minor_obstacle | `/Users/luanlei/Desktop/Luna-Workspace-Min/input_videos/phone_local_batch_001/phone_local_002_minor_obstacle.mp4` | `logs/phone_local_field_batch_001_20260424_154409/bundles/phone_local_002_minor_obstacle` | `logs/phone_local_field_batch_001_20260424_154409/archives/phone_local_002_minor_obstacle` | go | go | phone_local_controlled_capture | false | true | true | [] | [] |
| phone_local_003_narrow_path | `/Users/luanlei/Desktop/Luna-Workspace-Min/input_videos/phone_local_batch_001/phone_local_003_narrow_path.mp4` | `logs/phone_local_field_batch_001_20260424_154409/bundles/phone_local_003_narrow_path` | `logs/phone_local_field_batch_001_20260424_154409/archives/phone_local_003_narrow_path` | go | go | phone_local_controlled_capture | false | true | true | [] | [] |
| phone_local_004_people_far | input_videos/phone_local_batch_001/phone_local_004_people_far.mp4 | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
| phone_local_005_low_confidence_safe | input_videos/phone_local_batch_001/phone_local_005_low_confidence_safe.mp4 | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |

## Minimal acceptance reminder
Batch-level **GO** requires:
- processed samples ≥ 3
- every processed sample: bundle validator = go AND archive validator = go
- evidence_type preserved
- controlled_live_stream=false
- pending_real_sidewalk_run=true
- no hard blockers

