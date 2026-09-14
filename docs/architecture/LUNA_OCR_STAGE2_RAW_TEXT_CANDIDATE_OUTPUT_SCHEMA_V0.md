# LUNA — OCR Stage-2 Raw Text Candidate Output Schema v0

## Phase

- **Phase-Mainline-GuardedTrial-011**

## Schema (raw_text only)

- `candidate_id`
- `source_image_ref`
- `source_approval_ref`
- `provider_name` / `provider_type`
- `raw_text`
- `confidence`
- `reading_order` (empty allowed)
- `bbox_or_region` (null allowed)
- `provider_metadata` (latency/provider_details)
- `error_or_not_available_state` (null | not_available | provider_error)
- hard boundary defaults:
  - `allows_execute_now=false`
  - `semantic_interpretation_enabled=false`
  - `midplatform_forward_enabled=false`
  - `downstream_invocation_count=0`
  - `navigation_action=null`
  - `real_tts_invoked=false`
  - `world_write_invoked=false`
  - `hive_upload_invoked=false`

