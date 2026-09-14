# LUNA — YOLO Shadow Fusion Bridge Evaluation Matrix v0 (Phase-ModelPerception-008)

## Inputs
- YOLO SceneTask bridge root:
  - `logs/yolo_scene_task_bridge_eval_option_a_phone_local_001_20260427_1522/`

## Outputs
- YOLO Fusion bridge eval root:
  - `logs/yolo_fusion_bridge_eval_option_a_phone_local_001_20260427_1531/`

## Per-sample matrix (3 samples)

### phone_local_001_clear_path
- fusion_decision_candidate: generated; schema_valid=true
- fusion_candidate_type: (selected from SceneTask candidates; conservative)
- source attribution:
  - source_scene_id: present
  - source_task_candidate_ids: present
  - yolo_source: present (yolo_invoked/detection_count/detected_classes)
- conflict handling: present (conflict_detected may be false)
- degraded/uncertain handling: present
- candidate-only: allows_execute_now=false
- leakage: execute/default-on/release-retry-reopen/side-effects/forced_action = 0
- evidence boundary: preserved; controlled_live_stream=false; phone_local_capture=true

### phone_local_002_minor_obstacle
- fusion_decision_candidate: generated; schema_valid=true
- fusion_candidate_type: (selected from SceneTask candidates; conservative)
- source attribution:
  - source_scene_id: present
  - source_task_candidate_ids: present
  - yolo_source: present
- conflict handling: present
- degraded/uncertain handling: present
- candidate-only: allows_execute_now=false
- leakage: 0
- evidence boundary: preserved

### phone_local_003_narrow_path
- fusion_decision_candidate: generated; schema_valid=true
- fusion_candidate_type: (selected from SceneTask candidates; conservative)
- source attribution:
  - source_scene_id: present
  - source_task_candidate_ids: present
  - yolo_source: present
- conflict handling: present
- degraded/uncertain handling: present
- candidate-only: allows_execute_now=false
- leakage: 0
- evidence boundary: preserved

