# LUNA — YOLO Shadow Output Bridge Evaluation Matrix v0 (Phase-ModelPerception-009)

## Inputs
- YOLO Fusion bridge root:
  - `logs/yolo_fusion_bridge_eval_option_a_phone_local_001_20260427_1531/`

## Outputs
- YOLO Output bridge eval root:
  - `logs/yolo_output_bridge_eval_option_a_phone_local_001_20260427_1539/`

## Per-sample matrix (3 samples)

### phone_local_001_clear_path
- navigation_output_candidate: generated; schema_valid=true
- timing: validity_window/expires_at present; expires_after_generated=true
- priority/suppression/repeat_policy: present; priority valid
- source attribution: present; yolo_source preserved
- candidate-only: allows_execute_now=false
- no-real-TTS: real_tts_invoked=false
- safety: leakage=0; forbidden_output_semantic_count=0
- evidence boundary: preserved

### phone_local_002_minor_obstacle
- navigation_output_candidate: generated; schema_valid=true
- timing/priority/suppression: present & valid
- source attribution: present; yolo_source preserved
- candidate-only: allows_execute_now=false
- no-real-TTS: real_tts_invoked=false
- safety: leakage=0; forbidden_output_semantic_count=0
- evidence boundary: preserved

### phone_local_003_narrow_path
- navigation_output_candidate: generated; schema_valid=true
- timing/priority/suppression: present & valid
- source attribution: present; yolo_source preserved
- candidate-only: allows_execute_now=false
- no-real-TTS: real_tts_invoked=false
- safety: leakage=0; forbidden_output_semantic_count=0
- evidence boundary: preserved

