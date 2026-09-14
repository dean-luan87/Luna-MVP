# LUNA — Real Perception Model Input/Output Contract v0 (Phase-ModelPerception-001)

## Purpose
Freeze the integration boundary contract so a future real perception model can only:
- read permitted inputs
- emit permitted perception signals (candidate-only)
and cannot:
- execute actions
- bypass governance/SceneContext gates

Definition-only; no runtime.

## Input boundary (allowed)
Model may read only:
- phone_local source media **references** (paths/uris within archive; no new evidence types)
- sampled frames (or frame references), frame timestamps
- archive/sample metadata needed for replay/audit (sample_id, capture_metadata summary)
- non-sensitive scene context summaries (previous_macro_scene, degraded flags) as **read-only hints**
- previous perception signal summaries (read-only; for temporal smoothing candidates)
- evaluation mode flags (e.g., `baseline_or_mock`, `shadow_mode`) as non-privileged indicators
- `model_config_id` (opaque id)
- explicit candidate-only constraints (non-privileged)

## Input boundary (forbidden)
Model must NOT receive:
- release gates / execute permission / side-effects controls
- default-on switches
- governance override fields
- any hidden system control fields
- operator credentials beyond non-privileged ids
- unrelated private user data
- any field that enables bypassing SceneContext or governance

## Output boundary (must map to PerceptionEval-001 five signal categories)
Model output MUST be mappable to:
1. `object_stability_signal`
2. `ocr_navigation_signal`
3. `spatial_passability_signal`
4. `dynamic_event_signal`
5. `risk_field_signal`

Allowed output content (candidate-only):
- object detections/tracks (with confidence/uncertainty)
- OCR text candidates (with confidence/uncertainty)
- passability candidates (with confidence/uncertainty; may be `not_available`)
- dynamic event candidates (with confidence/uncertainty)
- risk candidates (with confidence/uncertainty)
- `reason_codes` (whitebox)
- `not_available` markers

## Output boundary (hard forbidden)
Model output must NOT contain semantics or fields that imply:
- `execute_now`
- `walk_now`, `turn_now`, `cross_now`
- `force_action`
- `release_side_effects`
- `retry_now`, `reopen_now`
- `enable_default_path`
- `override_governance`
- `final_navigation_instruction`
- `actual_tts`

If present, adapter must **block + fallback** (policy defined elsewhere).

## Candidate-only invariants
Regardless of model:
- downstream must see **signals only**, never executable instructions
- `allows_execute_now` must remain `false` in any normalized outputs produced by adapter/gates

## Minimal raw model output envelope (v0)
This does not constrain internal model format; it constrains the wrapper for audit/replay:
- `model_run_id`
- `model_config_id`
- `input_media_refs` (list)
- `frame_window` (start/end timestamp)
- `raw_outputs` (object; model-specific)
- `model_reported_confidence` (0..1; optional)
- `not_available` (bool; optional)
- `reason_codes` (list; optional)

## Minimal normalized output envelope (v0)
Adapter must produce:
- `normalized_perception_signals` (five categories; each can be not_available)
- `schema_validation_result`
- `forbidden_output_scan_result`
- `confidence_calibration_summary`
- `fallback_used` (bool)
- `model_disabled` (bool)
- `adapter_error` (string|null)
- `replay_record_ref` (string)
- `whitebox_record_ref` (string)

