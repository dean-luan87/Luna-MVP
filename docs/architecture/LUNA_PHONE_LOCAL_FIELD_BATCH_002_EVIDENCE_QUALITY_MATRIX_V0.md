# LUNA — Phone Local Field Batch 002 Evidence Quality Matrix v0 (Phase-PhoneLocalReview-002)

## Evidence set
- batch_summary_path: `logs/phone_local_field_batch_002_20260427_111431/batch_summary.json`
- sample_matrix_path: `logs/phone_local_field_batch_002_20260427_111431/sample_matrix.json`

Samples:
- `phone_local_001_clear_path`
- `phone_local_002_minor_obstacle`
- `phone_local_003_narrow_path`

## Matrix (per sample)
Legend:
- ✅ satisfied
- ❌ violated

| field | phone_local_001_clear_path | phone_local_002_minor_obstacle | phone_local_003_narrow_path |
|---|---:|---:|---:|
| source_video_path | ✅ `input_videos/phone_local_batch_002/phone_local_001_clear_path.mp4` | ✅ `input_videos/phone_local_batch_002/phone_local_002_minor_obstacle.mp4` | ✅ `input_videos/phone_local_batch_002/phone_local_003_narrow_path.mp4` |
| bundle_root | ✅ | ✅ | ✅ |
| archive_root | ✅ | ✅ | ✅ |
| bundle_validator_recommendation | ✅ go | ✅ go | ✅ go |
| archive_validator_recommendation | ✅ go | ✅ go | ✅ go |
| bundle_manifest_pass (`integrity_status=pass`, `bundle_ready=true`, missing/mismatch empty) | ✅ | ✅ | ✅ |
| archive_manifest_pass (`integrity_status=pass`, `archive_ready=true`, missing/mismatch empty) | ✅ | ✅ | ✅ |
| required_files_complete (bundle) | ✅ | ✅ | ✅ |
| required_files_complete (archive) | ✅ | ✅ | ✅ |
| evidence_type_preserved (`phone_local_controlled_capture`) | ✅ | ✅ | ✅ |
| controlled_live_stream_false | ✅ | ✅ | ✅ |
| phone_local_capture_true | ✅ | ✅ | ✅ |
| pending_real_sidewalk_run_true | ✅ | ✅ | ✅ |
| source_bundle_id_preserved | ✅ | ✅ | ✅ |
| source_media_reference_preserved (`source_media_path` + `source_original_video_filename`) | ✅ | ✅ | ✅ |
| no_execute_leakage_assertion | ✅ | ✅ | ✅ |
| no_default_on_assertion | ✅ | ✅ | ✅ |
| no_side_effect_expansion_assertion | ✅ | ✅ | ✅ |
| privacy_area_checked | ✅ (bundle metadata enforced by validator) | ✅ | ✅ |
| environment_allowed | ✅ (bundle metadata enforced by validator) | ✅ | ✅ |
| hard_blockers | ✅ none | ✅ none | ✅ none |
| soft_followups | ✅ none | ✅ none | ✅ none |

## Batch-level summary (from batch_summary.json)
- `sample_count_total=3`, `sample_count_processed=3`
- `sample_count_go=3`, `sample_count_no_go=0`
- `hard_blocker_count=0`, `soft_followup_count=0`
- `sample_count_partial=true`
- rates: all `1.0` (bundle_go_rate, archive_go_rate, evidence_type_preserved_rate, controlled_live_stream_false_rate, phone_local_capture_true_rate, pending_real_sidewalk_run_true_rate, safety_assertion_pass_rate)

