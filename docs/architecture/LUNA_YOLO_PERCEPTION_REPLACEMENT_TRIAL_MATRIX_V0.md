# LUNA — YOLO Shadow PerceptionEval Replacement Trial Matrix v0 (Phase-ModelPerception-006)

## Inputs
- sample_matrix: `logs/phone_local_field_batch_002_20260427_111431/sample_matrix.json`
- yolo shadow root: `logs/yolo_shadow_eval_option_a_phone_local_enabled_smoke_retry_fix002_20260427_1503/`
- replacement output root: `logs/yolo_perception_replacement_eval_option_a_phone_local_001_20260427_1513/`

## Per-sample matrix (3 samples)

### phone_local_001_clear_path
- replacement_generated: true
- yolo_invoked: true; fallback_used: false
- detection_count: 7; detected_classes: [person]
- signals present: object/ocr/passability/dynamic/risk = 5/5
- unsupported honesty:
  - ocr_status=not_available
  - dynamic_status=not_available
  - depth_unavailable=true
  - collision_risk_not_confirmed=true
- candidate-only: allows_execute_now=false
- leakage: execute/default-on/release-retry-reopen/side-effects = 0
- evidence boundary: evidence_type preserved; controlled_live_stream=false; phone_local_capture=true

### phone_local_002_minor_obstacle
- replacement_generated: true
- yolo_invoked: true; fallback_used: false
- detection_count: 8; detected_classes: [bicycle, person]
- signals present: object/ocr/passability/dynamic/risk = 5/5
- unsupported honesty:
  - ocr_status=not_available
  - dynamic_status=not_available
  - depth_unavailable=true
  - collision_risk_not_confirmed=true
- candidate-only: allows_execute_now=false
- leakage: execute/default-on/release-retry-reopen/side-effects = 0
- evidence boundary: evidence_type preserved; controlled_live_stream=false; phone_local_capture=true

### phone_local_003_narrow_path
- replacement_generated: true
- yolo_invoked: true; fallback_used: false
- detection_count: 24; detected_classes: [person, potted plant]
- signals present: object/ocr/passability/dynamic/risk = 5/5
- unsupported honesty:
  - ocr_status=not_available
  - dynamic_status=not_available
  - depth_unavailable=true
  - collision_risk_not_confirmed=true
- candidate-only: allows_execute_now=false
- leakage: execute/default-on/release-retry-reopen/side-effects = 0
- evidence boundary: evidence_type preserved; controlled_live_stream=false; phone_local_capture=true

