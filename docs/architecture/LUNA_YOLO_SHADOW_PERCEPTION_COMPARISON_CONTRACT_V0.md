# LUNA — YOLO Shadow vs Baseline Perception Comparison Contract v0 (Phase-ModelPerception-003)

## Purpose
Freeze the comparison fields, metrics, and forbidden interpretations for:
- baseline/mock PerceptionEval-001 outputs
vs
- YOLO shadow adapter outputs (ModelPerception-002B).

## Hard boundaries (frozen)
- Comparison does not imply integration.
- Fallback-only YOLO runs must be labeled as fallback-only.
- Do not infer tracking/depth/OCR/dynamic/collision capability from YOLO detection-first outputs.
- No claims of “better navigation”; only signal coverage/differences and boundary integrity.

## Alignment key
- Align by `sample_id` (from FieldBatch sample_matrix).

## Required per-sample comparison record (schema)
Fields:
- `sample_id`
- `fieldbatch_archive_root` (string|optional)
- `baseline_root` (string)
- `yolo_shadow_root` (string)

### Baseline extraction
- `baseline_found` (bool)
- `baseline_file_ref` (string|null)
- `baseline_signal_coverage` (object):
  - `has_object_stability_signal`
  - `has_spatial_passability_signal`
  - `has_risk_field_signal`
  - `has_ocr_navigation_signal`
  - `has_dynamic_event_signal`
  - `coverage_rate` (0..1)
- `baseline_execute_leakage_count` (int)
- `baseline_default_on_leakage_count` (int)

### YOLO shadow extraction
- `yolo_found` (bool)
- `yolo_file_ref` (string|null)
- `yolo_invoked` (bool)
- `yolo_disabled` (bool)
- `fallback_used` (bool)
- `fallback_reason` (string|null)
- `yolo_signal_coverage` (object; same keys as baseline)
- `yolo_object_detection_available` (bool)  # true if invoked and detection_count>0
- `yolo_execute_leakage_count` (int)
- `yolo_default_on_leakage_count` (int)
- `yolo_allows_execute_now_false` (bool)
- `evidence_type_preserved` (bool)
- `controlled_live_stream_false` (bool)

### Artifact integrity (per-sample)
- `yolo_trace_ready` (bool)
- `yolo_replay_ready` (bool)
- `yolo_whitebox_ready` (bool)

### Outcome notes (non-interpretive)
- `notes` (list<string>)

## Required run summary metrics
### Coverage Comparison
- `baseline_signal_coverage_rate`
- `yolo_signal_coverage_rate`
- `yolo_object_detection_available_rate`
- `ocr_not_available_consistency_rate` (YOLO side)
- `dynamic_not_available_consistency_rate` (YOLO side)
- `depth_unavailable_consistency_rate` (YOLO side)

### YOLO Runtime Status
- `yolo_invoked_count`
- `yolo_fallback_count`
- `yolo_disabled_count`
- `yolo_exception_count`
- `yolo_dependency_unavailable_count`

### Boundary Comparison
- `baseline_execute_leakage_count`
- `yolo_execute_leakage_count`
- `baseline_default_on_leakage_count`
- `yolo_default_on_leakage_count`
- `yolo_allows_execute_now_false_rate`
- `evidence_type_preserved_rate`

### Artifact Integrity
- `yolo_replay_ready_rate`
- `yolo_whitebox_ready_rate`
- `yolo_trace_ready_rate`

## Forbidden interpretations (must write explicitly)
- Do NOT claim YOLO improves navigation or safety.
- Do NOT claim YOLO provides depth or collision risk.
- Do NOT claim YOLO has tracking unless a tracking contract exists and is audited.
- Do NOT present fallback outputs as model capability.

