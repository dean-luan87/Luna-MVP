# LUNA — Phone Local Field Batch 002 Sample Matrix v0 (Phase-PhoneLocalFieldBatch-002)

## Batch run record
- **batch_summary_path**: `logs/phone_local_field_batch_002_20260427_111431/batch_summary.json`
- **sample_matrix_path**: `logs/phone_local_field_batch_002_20260427_111431/sample_matrix.json`
- **sample_source_type**: `new_phone_local_field_samples`（新拍摄 phone_local 样本批次；非 reused existing video）

## Batch counts / rates (from batch_summary.json)
### counts
- `sample_count_total=3`
- `sample_count_processed=3`
- `sample_count_go=3`
- `sample_count_no_go=0`
- `hard_blocker_count=0`
- `soft_followup_count=0`
- `sample_count_partial=true`（目标建议 5 条；本次为 3 条）

### rates (all 1.0)
- `bundle_go_rate=1.0`
- `archive_go_rate=1.0`
- `evidence_type_preserved_rate=1.0`
- `controlled_live_stream_false_rate=1.0`
- `phone_local_capture_true_rate=1.0`
- `pending_real_sidewalk_run_true_rate=1.0`
- `safety_assertion_pass_rate=1.0`

## Per-sample matrix (from sample_matrix.json)
| sample_id | source_video_path | bundle_root | archive_root | bundle_validator | archive_validator | evidence_type | controlled_live_stream | phone_local_capture | pending_real_sidewalk_run | hard_blockers | soft_followups |
|---|---|---|---|---|---|---|---|---|---|---|---|
| phone_local_001_clear_path | `input_videos/phone_local_batch_002/phone_local_001_clear_path.mp4` | `logs/phone_local_field_batch_002_20260427_111431/bundles/phone_local_001_clear_path` | `logs/phone_local_field_batch_002_20260427_111431/archives/phone_local_001_clear_path` | go | go | phone_local_controlled_capture | false | true | true | [] | [] |
| phone_local_002_minor_obstacle | `input_videos/phone_local_batch_002/phone_local_002_minor_obstacle.mp4` | `logs/phone_local_field_batch_002_20260427_111431/bundles/phone_local_002_minor_obstacle` | `logs/phone_local_field_batch_002_20260427_111431/archives/phone_local_002_minor_obstacle` | go | go | phone_local_controlled_capture | false | true | true | [] | [] |
| phone_local_003_narrow_path | `input_videos/phone_local_batch_002/phone_local_003_narrow_path.mp4` | `logs/phone_local_field_batch_002_20260427_111431/bundles/phone_local_003_narrow_path` | `logs/phone_local_field_batch_002_20260427_111431/archives/phone_local_003_narrow_path` | go | go | phone_local_controlled_capture | false | true | true | [] | [] |

## Boundary statement (must remain true)
- Default path remains disabled.
- Full controlled trial not entered.
- Real side effects surface not expanded.
- No controlled_live_stream executed.
- Option A not expanded.

