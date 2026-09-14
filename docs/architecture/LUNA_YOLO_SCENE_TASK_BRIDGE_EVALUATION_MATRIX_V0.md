# LUNA — YOLO Shadow SceneTask Bridge Evaluation Matrix v0 (Phase-ModelPerception-007)

## Inputs
- YOLO perception replacement root:
  - `logs/yolo_perception_replacement_eval_option_a_phone_local_001_20260427_1513/`

## Outputs
- SceneTask bridge eval root:
  - `logs/yolo_scene_task_bridge_eval_option_a_phone_local_001_20260427_1522/`

## Per-sample matrix (3 samples)

### phone_local_001_clear_path
- perception_runtime_mode: yolo_shadow_replacement
- scene_task_runtime_mode: yolo_replacement_downstream
- yolo_invoked: true
- detection_count: 7; detected_classes: [person]
- scene_state: generated; schema_valid=true
  - scene_type: uncertain_scene
  - scene_phase: sidewalk_obstacle_candidate
  - scene_confidence: 0.30 (conservative)
- task_candidates: generated; schema_valid=true
- yolo_detection_used: true
- unsupported_capabilities_respected: true
- candidate-only: allows_execute_now=false
- leakage: execute/default-on/release-retry-reopen/forced_action = 0
- evidence boundary: preserved; controlled_live_stream=false; phone_local_capture=true

### phone_local_002_minor_obstacle
- perception_runtime_mode: yolo_shadow_replacement
- scene_task_runtime_mode: yolo_replacement_downstream
- yolo_invoked: true
- detection_count: 8; detected_classes: [bicycle, person]
- scene_state: generated; schema_valid=true
  - scene_type: uncertain_scene
  - scene_phase: sidewalk_obstacle_candidate
  - scene_confidence: 0.30 (conservative)
- task_candidates: generated; schema_valid=true
- yolo_detection_used: true
- unsupported_capabilities_respected: true
- candidate-only: allows_execute_now=false
- leakage: execute/default-on/release-retry-reopen/forced_action = 0
- evidence boundary: preserved; controlled_live_stream=false; phone_local_capture=true

### phone_local_003_narrow_path
- perception_runtime_mode: yolo_shadow_replacement
- scene_task_runtime_mode: yolo_replacement_downstream
- yolo_invoked: true
- detection_count: 24; detected_classes: [person, potted plant]
- scene_state: generated; schema_valid=true
  - scene_type: uncertain_scene
  - scene_phase: sidewalk_obstacle_candidate (person presence => conservative obstacle candidate)
  - scene_confidence: 0.30 (conservative)
- task_candidates: generated; schema_valid=true
- yolo_detection_used: true
- unsupported_capabilities_respected: true
- candidate-only: allows_execute_now=false
- leakage: execute/default-on/release-retry-reopen/forced_action = 0
- evidence boundary: preserved; controlled_live_stream=false; phone_local_capture=true

