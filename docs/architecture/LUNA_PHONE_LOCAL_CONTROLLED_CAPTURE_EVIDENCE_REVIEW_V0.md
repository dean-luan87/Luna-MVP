# LUNA — Phone Local Controlled Capture Evidence Review v0 (Phase-PhoneLocalReview-001)

## Phase
- Phase: **Phase-PhoneLocalReview-001**
- Name: **Phone Local Controlled Capture Evidence Review v0**
- Evidence type under review: **`phone_local_controlled_capture`**

## Scope (What this review does)
This review is a **documentation-only evidence review** of three `phone_local_controlled_capture` archives produced by **Phase-DeviceEnv-005**.

The review answers:
1. Whether the three archives are **validator=go** and **manifest-pass**.
2. Whether boundaries are preserved:
   - `evidence_type=phone_local_controlled_capture`
   - `controlled_live_stream=false`
   - `phone_local_capture=true`
   - `pending_real_sidewalk_run=true` (must NOT be auto-closed)
3. Whether source lineage is preserved:
   - `source_bundle_id`
   - `source_bundle_manifest_path`
   - `source_media_path`
   - `source_original_video_filename`
4. Whether any **execute / default-on / side effects** leakage appears in evidence artifacts.
5. Whether `phone_local_controlled_capture` is eligible to become the **primary field collection route** under current constraints (phone goes out; Mac stays; post-hoc import).

## Non-goals (Hard boundaries)
Must remain true for this phase:
- No new runtime implementation.
- No realtime upload.
- No `controlled_live_stream`.
- No entry into full controlled trial.
- No open user testing.
- No default-on path enabled.
- No expansion of real side effects surface.
- No scope expansion beyond Option A intent (this phase does not expand Option A; it only reviews evidence).

## Evidence set under review (DeviceEnv-005 outputs)
Timestamp cohort: **`20260424_152834`**

### Bundles
- `logs/phone_bundle_sidewalk_001_clear_path_20260424_152834`
- `logs/phone_bundle_sidewalk_002_minor_obstacle_20260424_152834`
- `logs/phone_bundle_sidewalk_003_narrow_path_20260424_152834`

### Archives
- `logs/phone_archive_sidewalk_001_clear_path_20260424_152834`
- `logs/phone_archive_sidewalk_002_minor_obstacle_20260424_152834`
- `logs/phone_archive_sidewalk_003_narrow_path_20260424_152834`

## High-level findings (Summary)
### 1) Validator outcome
- All three **bundle validators**: **`go`**
- All three **archive validators**: **`go`**
- DeviceEnv-005 verifier A–L: **`ok`**

### 2) Boundary preservation
Across all three archives (from `run_evidence.json`):
- `evidence_type`: **`phone_local_controlled_capture`** (preserved)
- `controlled_live_stream`: **false** (preserved)
- `phone_local_capture`: **true** (preserved)
- `pending_real_sidewalk_run`: **true** (preserved; not auto-closed)

### 3) Source lineage preservation
Across all three archives:
- `source_bundle_id`: present
- `source_bundle_manifest_path`: present
- `source_media_path`: present (`media/video.mp4`)
- `source_original_video_filename`: present (matches each sample file name)

### 4) Safety assertions
Across all three archives:
- `no_execute_leakage_assertion=true`
- `no_default_on_assertion=true`
- `no_side_effect_expansion_assertion=true`

### 5) Manifest integrity
Across all three:
- `archive_manifest.json`: `integrity_status=pass`, `missing_files=[]`, `hash_mismatches=[]`, `archive_ready=true`
- `bundle_manifest.json`: `integrity_status=pass`, `missing_files=[]`, `hash_mismatches=[]`, `bundle_ready=true`

## What phone_local_capture can prove (in current governance)
It can prove:
- A **real-world phone-recorded video** can be transformed into a governed bundle and imported into a RealScene-style archive with:
  - stable `evidence_type` boundary
  - stable `pending_real_sidewalk_run` semantics
  - complete required files + manifest integrity
  - reproducible validator results
- The **evidence/archive/validator chain** is viable under the constraint “Mac cannot go outside”.

## What phone_local_capture cannot prove
It cannot prove:
- Realtime controlled capture stability (no realtime transport, no live capture loop).
- Any “controlled_live_stream” properties (latency, network stability, live abort/interrupt monitoring).
- Wearable viewpoint correctness (badge/phone mounting, on-body dynamics) beyond what the recorded video happens to show.
- Any execution authority or navigation correctness in the real world (this pipeline remains candidate-only, no action execution).

## Relationship to controlled_live_stream (explicit boundary statement)
- `phone_local_controlled_capture` **is not** `controlled_live_stream`.
- `phone_local_controlled_capture` **must not** be mislabeled as controlled live.
- `phone_local_controlled_capture` **must not** auto-close `pending_real_sidewalk_run`.
- `phone_local_controlled_capture` may serve as the **primary field collection route** when the real constraint is:
  - phone goes outside and records
  - Mac imports afterwards for archiving + validation

## Decision (Phase conclusion)
### Recommendation
**GO** to accept `phone_local_controlled_capture` as the current phase’s **primary field collection route** (phone-out / Mac-import) under strict boundaries.

### Conditions (still enforced)
- Still no realtime upload / no controlled_live_stream.
- Still candidate-only.
- Still Option A intent only (no scenario expansion in this decision).
- Still no default-on and no real side effects expansion.

## Follow-ups (Soft)
- Enrich `device_info.json` and operator notes templates for higher forensic quality (non-blocking).
- Add a lightweight “evidence pack” command that prints a one-page digest for a given archive_root (documentation tooling only; optional).

## Required companion documents
- Evidence quality matrix: `docs/architecture/LUNA_PHONE_LOCAL_CONTROLLED_CAPTURE_EVIDENCE_QUALITY_MATRIX_V0.md`
- Field collection route policy: `docs/architecture/LUNA_PHONE_LOCAL_CAPTURE_AS_FIELD_COLLECTION_ROUTE_POLICY_V0.md`
- Branch decision pack: `docs/architecture/LUNA_PHONE_LOCAL_CAPTURE_REVIEW_BRANCH_DECISION_PACK_V0.md`

