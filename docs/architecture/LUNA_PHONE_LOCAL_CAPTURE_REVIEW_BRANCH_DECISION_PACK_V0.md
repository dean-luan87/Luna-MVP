# LUNA — Phone Local Capture Review Branch Decision Pack v0 (Phase-PhoneLocalReview-001)

## Pack intent
This pack consolidates the Review-001 evidence review, the quality matrix, and the route policy, and records the formal branch decision.

This phase is documentation-only. No runtime changes.

## Inputs (artifacts)
- Evidence review:
  - `docs/architecture/LUNA_PHONE_LOCAL_CONTROLLED_CAPTURE_EVIDENCE_REVIEW_V0.md`
- Evidence quality matrix:
  - `docs/architecture/LUNA_PHONE_LOCAL_CONTROLLED_CAPTURE_EVIDENCE_QUALITY_MATRIX_V0.md`
- Field collection route policy:
  - `docs/architecture/LUNA_PHONE_LOCAL_CAPTURE_AS_FIELD_COLLECTION_ROUTE_POLICY_V0.md`

## Evidence set reviewed (DeviceEnv-005 outputs)
- `logs/phone_archive_sidewalk_001_clear_path_20260424_152834`
- `logs/phone_archive_sidewalk_002_minor_obstacle_20260424_152834`
- `logs/phone_archive_sidewalk_003_narrow_path_20260424_152834`

## Review questions (must-answer checklist)
1. Three phone_local archives all validator=go? **YES**
2. evidence_type preserved as phone_local_controlled_capture? **YES**
3. Any controlled_live_stream mislabel? **NO**
4. pending_real_sidewalk_run incorrectly set false? **NO**
5. source_bundle_id and source media lineage preserved? **YES**
6. execute/default-on/side effects leakage? **NO (assertions true; candidate-only artifacts)**
7. allow phone_local as primary field route now? **YES (under constraints)**
8. still need controlled_live_stream route? **YES (not replaced; deferred)**
9. allow new batch of newly captured phone_local samples? **YES (Option A only; no scenario expansion)**
10. allow scenario expansion now? **NO**

## Branch decision
### Decision
**GO**

### Approved next phase
- **Phase-PhoneLocalFieldBatch-001: Option A Phone Local Field Capture Batch v0**

### Disallowed actions (unchanged)
- No realtime upload
- No controlled_live_stream
- No full controlled trial
- No open user testing
- No default-on
- No side effects surface expansion
- No Option A expansion (no new scenarios)

## Rationale (one paragraph)
DeviceEnv-005 produced three `phone_local_controlled_capture` archives with complete required files, manifest integrity pass, stable evidence-type boundaries, preserved lineage, and all validators/verifier results passing. Under the real constraint “Mac cannot go outside”, phone_local is the most practical governed field collection route, while controlled_live_stream remains a separate future route requiring its own adapter and governance gate.

## Boundary statement (explicit)
- Default path remains disabled.
- Full controlled trial not entered.
- Real side effects surface not expanded.
- No controlled_live_stream executed.
- This pack only records Review-001 decisions.

