# LUNA — Real Perception Model Adapter & Fallback Policy v0 (Phase-ModelPerception-001)

## Purpose
Define the adapter responsibilities so real model outputs can be integrated safely by:
- normalization into the existing Perception-001 five-signal shape
- schema validation + forbidden-output scanning
- confidence calibration and not_available handling
- disable switch
- fallback to baseline/mock
- rollback-to-baseline policy
- replay/audit/whitebox recording

Definition-only; no runtime.

## Adapter outputs (must be produced for every run)
Adapter must output (whitebox/audit-friendly):
- `raw_model_output` (verbatim; stored as artifact reference)
- `normalized_perception_signal` (five categories; not_available allowed)
- `schema_validation_result` (pass/fail + reasons)
- `forbidden_output_scan_result` (pass/fail + matches)
- `confidence_calibration_summary` (what was adjusted; no hidden knobs)
- `not_available_handling` (explicit)
- `fallback_used` (bool)
- `model_disabled` (bool)
- `adapter_error` (string|null)
- `replay_record` (what inputs were used; deterministic references)
- `whitebox_record` (reason_codes, decisions, policy version ids)

## Disable switch (hard requirement)
Must exist and be auditable:
- `model_disabled=true` forces baseline/mock outputs
- must not require model invocation to determine disabled state
- must be reversible without changing evidence types

## Failure / fallback triggers (hard requirements)
Fallback MUST be used if any of the following occurs:
- non-parseable output (not JSON or unreadable)
- schema missing required elements for mapping
- forbidden semantics/fields detected (execute/release/retry/reopen/default-on/governance override)
- timeout
- exception
- low-confidence below policy threshold (threshold deferred) AND cannot mark not_available safely
- output not auditable / replay record incomplete

Fallback behavior:
- `fallback_used=true`
- normalized outputs come from baseline/mock perception source
- adapter must still write a replay/whitebox record explaining fallback reasons

## Forbidden output scanning (minimum)
Scan must detect:
- `execute_now`, `walk_now`, `turn_now`, `cross_now`
- `release_side_effects`
- `enable_default_path`
- `override_governance`
- `retry_now`, `reopen_now`
- `final_navigation_instruction`, `actual_tts`

On match:
- block model output
- fallback
- record matched tokens/fields in `forbidden_output_scan_result`

## Not-available & uncertainty handling
Allowed:
- output category-level `not_available=true` (e.g., OCR unavailable)
Hard constraint:
- must not fabricate signals to fill missing categories

If low confidence:
- adapter may downgrade to `uncertain` or `not_available`
- must not up-convert low confidence into certainty

## Normalization & mapping (conceptual)
Adapter must map raw model outputs into the existing five categories without changing downstream contracts:
- object detections/tracks → `object_stability_signal`
- OCR candidates → `ocr_navigation_signal`
- geometry/free-space candidates → `spatial_passability_signal`
- dynamic events/tracks → `dynamic_event_signal`
- risk candidates → `risk_field_signal`

## Rollback-to-baseline policy
Rollback is defined as:
- switching perception source back to baseline/mock **without altering evidence artifacts**
- producing replay/whitebox records showing the switch

Rollback triggers (examples):
- repeated fallback events rate above threshold (threshold deferred)
- persistent forbidden output matches
- repeated non-auditable runs

## Audit & replay invariants (must hold)
- every model attempt must produce a replayable record of:
  - input refs (media/frame window)
  - model_config_id
  - policy version ids
  - adapter decisions (normalize/fallback/disable)
- no hidden execution permission can be introduced via adapter

