# LUNA — Phone Local Controlled Capture Evidence Quality Matrix v0 (Phase-PhoneLocalReview-001)

## Scope
This matrix records evidence-quality and boundary-adherence signals for the three `phone_local_controlled_capture` samples produced in **Phase-DeviceEnv-005**.

Evidence cohort timestamp: **`20260424_152834`**

## Evidence set
| sample_id | source_video | bundle_root | archive_root |
|---|---|---|---|
| sidewalk_001_clear_path | `/Users/luanlei/Desktop/Luna-Workspace-Min/input_videos/sidewalk/sidewalk_001_clear_path.mp4` | `logs/phone_bundle_sidewalk_001_clear_path_20260424_152834` | `logs/phone_archive_sidewalk_001_clear_path_20260424_152834` |
| sidewalk_002_minor_obstacle | `/Users/luanlei/Desktop/Luna-Workspace-Min/input_videos/sidewalk/sidewalk_002_minor_obstacle.mp4` | `logs/phone_bundle_sidewalk_002_minor_obstacle_20260424_152834` | `logs/phone_archive_sidewalk_002_minor_obstacle_20260424_152834` |
| sidewalk_003_narrow_path | `/Users/luanlei/Desktop/Luna-Workspace-Min/input_videos/sidewalk/sidewalk_003_narrow_path.mp4` | `logs/phone_bundle_sidewalk_003_narrow_path_20260424_152834` | `logs/phone_archive_sidewalk_003_narrow_path_20260424_152834` |

## Quality matrix (per sample)

Legend:
- ✅ = satisfied
- ❌ = violated
- N/A = not applicable in phone_local pipeline

| field | sidewalk_001_clear_path | sidewalk_002_minor_obstacle | sidewalk_003_narrow_path |
|---|---:|---:|---:|
| bundle_validator_recommendation | go ✅ | go ✅ | go ✅ |
| archive_validator_recommendation | go ✅ | go ✅ | go ✅ |
| bundle_manifest_pass (`bundle_ready=true`, `missing_files=[]`, `hash_mismatches=[]`) | ✅ | ✅ | ✅ |
| archive_manifest_pass (`archive_ready=true`, `missing_files=[]`, `hash_mismatches=[]`) | ✅ | ✅ | ✅ |
| required_files_complete (bundle) | ✅ | ✅ | ✅ |
| required_files_complete (archive) | ✅ | ✅ | ✅ |
| evidence_type_preserved (`phone_local_controlled_capture`) | ✅ | ✅ | ✅ |
| controlled_live_stream_false | ✅ | ✅ | ✅ |
| phone_local_capture_true | ✅ | ✅ | ✅ |
| pending_real_sidewalk_run_true | ✅ | ✅ | ✅ |
| source_bundle_id_preserved | ✅ (`bundle_dd0457da84`) | ✅ (`bundle_e869fc08e6`) | ✅ (`bundle_f7ddb2c8b3`) |
| source_bundle_manifest_path_present | ✅ | ✅ | ✅ |
| source_media_reference_preserved (`source_media_path`, `source_original_video_filename`) | ✅ | ✅ | ✅ |
| no_execute_leakage_assertion | ✅ | ✅ | ✅ |
| no_default_on_assertion | ✅ | ✅ | ✅ |
| no_side_effect_expansion_assertion | ✅ | ✅ | ✅ |
| privacy_area_checked | ✅ | ✅ | ✅ |
| environment_allowed | ✅ | ✅ | ✅ |
| controlled_live_mislabel_detected | ❌ | ❌ | ❌ |
| pending_real_sidewalk_run_auto_closed | ❌ | ❌ | ❌ |
| hard_blockers | none ✅ | none ✅ | none ✅ |
| soft_followups | none ✅ | none ✅ | none ✅ |

## Notes
### Archive manifest integrity (hash layer)
All three archives report:
- `integrity_status=pass`
- `missing_files=[]`
- `hash_mismatches=[]`

### Source lineage (field collection traceability)
All three archives record:
- `source_bundle_id`
- `source_bundle_manifest_path`
- `source_media_path`
- `source_original_video_filename`

This is sufficient for v0 “phone-out / Mac-import” forensic traceability under current governance.

