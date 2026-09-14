# LUNA — YOLO Shadow End-to-End Offline Evaluation Matrix v0 (Phase-ModelPerception-010)

## Inputs (this run)
- FieldBatch root: `logs/phone_local_field_batch_002_20260427_111431/`
- YOLO perception replacement root: `logs/yolo_perception_replacement_eval_option_a_phone_local_001_20260427_1558/`
- YOLO SceneTask bridge root: `logs/yolo_scene_task_bridge_eval_option_a_phone_local_001_20260427_1558/`
- YOLO Fusion bridge root: `logs/yolo_fusion_bridge_eval_option_a_phone_local_001_20260427_1558/`
- YOLO Output bridge root: `logs/yolo_output_bridge_eval_option_a_phone_local_001_20260427_1558/`

## Output (this run)
- E2E output root: `logs/yolo_e2e_offline_eval_option_a_phone_local_001_20260427_1559/`

## Per-sample matrix (3 samples)

### phone_local_001_clear_path
- chain completeness: perception/scene_task/fusion/output present = true
- schema: perception/scene_task/fusion/output schema_ok = true
- yolo source traceability: preserved all stages = true
- candidate-only: allows_execute_now false all stages = true
- no-real-TTS: real_tts_invoked false = true
- safety leakage totals: 0
- evidence boundary:
  - evidence_type preserved = true
  - controlled_live_stream false = true
  - phone_local_capture true = true
  - pending_real_sidewalk_run true = true

### phone_local_002_minor_obstacle
- chain completeness: true
- schema integrity: true
- yolo source traceability: true
- candidate-only/no-TTS: true
- safety leakage totals: 0
- evidence boundary: all true (including pending_real_sidewalk_run)

### phone_local_003_narrow_path
- chain completeness: true
- schema integrity: true
- yolo source traceability: true
- candidate-only/no-TTS: true
- safety leakage totals: 0
- evidence boundary: all true (including pending_real_sidewalk_run)

