# LUNA — YOLO Shadow Adapter Evaluation Matrix v0 (Phase-ModelPerception-002B)

## Purpose
Matrix the expected outputs for running YOLO shadow adapter on **FieldBatch-002** samples.

This document is a template + expectation contract; actual runs may be:
- real YOLO invoked (if dependencies/weights available and disable switch false), OR
- fallback (disable switch true or dependency unavailable)

## Inputs
- FieldBatch sample matrix (example):
  - `logs/phone_local_field_batch_002_20260427_111431/sample_matrix.json`

## Outputs (per run root)
- `yolo_shadow_summary.json`
- `per_sample_yolo_shadow_results.json`
- `yolo_shadow_trace.jsonl`
- `yolo_shadow_replay.jsonl`
- `yolo_shadow_whitebox.jsonl`
- `evaluation_notes.md`

## Per-sample expectations (FieldBatch-002)

### Sample: phone_local_001_clear_path
- expected:
  - evidence_type preserved: phone_local_controlled_capture
  - controlled_live_stream false
  - five signals present (OCR/dynamic may be not_available)
  - allows_execute_now=false
  - gate_required=true and gate_status=not_executed_in_002b
  - disable_yolo=true ⇒ yolo_invoked=false, fallback_used=true, fallback_reason=yolo_disabled

### Sample: phone_local_002_minor_obstacle
- expected: same structural expectations as above

### Sample: phone_local_003_narrow_path
- expected: same structural expectations as above

## Signal coverage expectations (v0)
- object_stability_signal: present, may be empty under fallback
- spatial_passability_signal: present; must be conservative:
  - passability_source=object_detection_only
  - depth_unavailable=true
  - must not claim confirmed_passable
- risk_field_signal: present; class-based candidates only:
  - collision_risk_not_confirmed=true
- ocr_navigation_signal: status=not_available
- dynamic_event_signal: status=not_available

## Notes
Detection quality is not a v0 blocker.
The evaluation focus is:
- contract correctness
- disable/fallback correctness
- artifact completeness (replay/whitebox)
- no forbidden semantics leakage

