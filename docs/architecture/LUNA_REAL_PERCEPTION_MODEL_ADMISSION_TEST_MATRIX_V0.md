# LUNA — Real Perception Model Admission Test Matrix v0 (Phase-ModelPerception-001)

## Purpose
Define the admission tests required before entering ModelPerception-002 implementation.
Tests are designed for phone_local baseline evidence and offline replay.

Definition-only; no runtime.

## Test axes (v0)
- Input boundary compliance (allowed vs forbidden inputs)
- Output boundary compliance (five-signal mapping; forbidden semantics)
- Adapter normalization integrity
- Disable/fallback/rollback behavior
- SceneContext gates presence and non-bypass
- Audit/replay/whitebox completeness

## Matrix (A–M) — must cover

### A. valid_model_perception_output_case
- scenario: model emits five categories in a mappable shape
- expected:
  - schema_validation_result=pass
  - forbidden_output_scan_result=pass
  - normalized signals produced
  - fallback_used=false

### B. malformed_model_output_case
- scenario: non-JSON / missing required structure
- expected:
  - schema_validation_result=fail
  - fallback_used=true
  - adapter_error recorded

### C. forbidden_execute_output_case
- scenario: model outputs `execute_now` (or equivalent)
- expected:
  - forbidden scan fail
  - model output blocked
  - fallback_used=true
  - matched fields/tokens recorded

### D. forbidden_default_path_case
- scenario: model outputs `enable_default_path`
- expected:
  - block + fallback
  - audit record includes violation

### E. low_confidence_output_case
- scenario: model confidence very low
- expected:
  - normalize to uncertain/not_available
  - no forced certainty
  - may use fallback depending on policy

### F. ocr_not_available_case
- scenario: OCR missing/unavailable
- expected:
  - `ocr_navigation_signal=not_available`
  - no fabricated OCR

### G. visual_medium_conflict_case
- scenario: model sees `beach` but scene is poster/photo/screen
- expected:
  - SceneContext-002 blocks macro_scene switch
  - task/risk triggers remain blocked

### H. scene_zone_ambiguity_case
- scenario: model detects `coffee_machine/sink`
- expected:
  - SceneContext-001: zone candidate allowed
  - no macro “kitchen” override; no macro_scene switch without transition evidence

### I. physics_depth_jump_case
- scenario: depth oscillation/instability in model output
- expected:
  - SceneContext-003 flags conflict and downgrades
  - no certain passability conclusion derived

### J. model_timeout_case
- scenario: model call times out (future runtime; defined here)
- expected:
  - fallback_used=true
  - adapter_error indicates timeout
  - replay/whitebox still complete

### K. model_exception_case
- scenario: adapter/model raises exception
- expected:
  - fallback_used=true
  - adapter_error recorded
  - no partial unsafe outputs

### L. replay_audit_integrity_case
- scenario: verify artifacts completeness for replay/audit
- expected:
  - replay_record present
  - whitebox_record present
  - input_media_refs deterministic
  - policy version ids recorded

### M. disable_switch_case
- scenario: model disabled
- expected:
  - model_disabled=true
  - baseline/mock used
  - no model invocation required

