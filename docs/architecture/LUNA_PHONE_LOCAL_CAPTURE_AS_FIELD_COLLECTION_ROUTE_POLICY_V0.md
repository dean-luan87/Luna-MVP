# LUNA — Phone Local Capture as Field Collection Route Policy v0 (Phase-PhoneLocalReview-001)

## Purpose
Define whether `phone_local_controlled_capture` may be used as the **primary field collection route** under current constraints, and explicitly define its relationship to `controlled_live_stream`.

This is a governance/policy document only. It does not add runtime.

## Definitions (frozen terms)
- **phone_local_controlled_capture**:
  - Phone records media locally (system camera).
  - Media is transferred to Mac manually.
  - Mac builds a governed bundle and imports into an `archive_root`.
  - Validators must pass.
  - Candidate-only; no execution authority.
- **controlled_live_stream**:
  - Realtime capture and/or realtime transport.
  - Live abort/interrupt monitoring expectations.
  - Different evidence semantics and risk profile.

## Hard boundaries (must remain true)
- `phone_local_controlled_capture` is **NOT** `controlled_live_stream`.
- It must preserve:
  - `evidence_type=phone_local_controlled_capture`
  - `controlled_live_stream=false`
  - `phone_local_capture=true`
- It must NOT:
  - be mislabeled as controlled live
  - auto-close `pending_real_sidewalk_run`
  - enable default-on
  - expand real side effects surface
  - grant model execution authority

## Eligibility policy: Can phone_local be the primary field route now?
### Policy decision
**YES — allowed as the primary field collection route** for the current stage, defined as:
> “phone-out capture, Mac-import archiving, validator-gated evidence”

### Preconditions (must be satisfied per archive)
- Bundle validator: `go`
- Archive validator: `go`
- Manifests: `integrity_status=pass`, `missing_files=[]`, `hash_mismatches=[]`
- Lineage preserved:
  - `source_bundle_id` present
  - `source_bundle_manifest_path` present
  - `source_media_path` present
  - `source_original_video_filename` present
- Safety assertions all `true`
- `pending_real_sidewalk_run` remains `true` unless a later governance phase explicitly changes semantics

## Relationship to pending_real_sidewalk_run (governance semantics)
### Current meaning (v0)
`pending_real_sidewalk_run=true` indicates:
- We have not executed a **realtime** controlled live sidewalk run.
- phone_local evidence is valuable and real, but it does not replace realtime controlled-live semantics.

### Allowed evolution (future; not in this phase)
A later governance decision may introduce:
- `pending_realtime_controlled_live_run` (more precise)
- separate pending flags for “field capture done” vs “realtime controlled live done”

This document does not change existing semantics; it only constrains them.

## Does phone_local remove the need for controlled_live_stream?
### Current policy (v0)
**NO.** `phone_local_controlled_capture` does not eliminate the need for a future controlled live stream route if/when:
- realtime safety monitoring is required,
- live abort/interrupt triggers must be validated end-to-end,
- or additional “live” evidence semantics are needed.

### Practical interpretation
Use phone_local as the main practical route today; defer controlled_live_stream until a separate governance-approved adapter exists and the environment allows it.

## Allowed next step (under this policy)
If Review-001 yields GO (as defined by the evidence quality matrix and boundary checks), the next allowed phase is:
- **Phase-PhoneLocalFieldBatch-001: Option A Phone Local Field Capture Batch v0**
  - collect a new batch of phone-recorded sidewalk videos (Option A only)
  - import/validate each via the existing bundle→archive toolchain
  - no scenario expansion
  - no controlled_live_stream
  - candidate-only; no execution authority; no default-on

