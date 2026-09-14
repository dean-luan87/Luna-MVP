# LUNA — YOLO Baseline Replacement Evidence Matrix v0 (Phase-ModelPerception-011)

本矩阵仅汇总 **005–010** 的可复核证据，支持“是否允许 YOLO shadow 作为离线评测默认 perception candidate source”的复审决策。  
**注意**：全部为 offline/shadow/candidate-only 证据，不代表 runtime 能力。

## Evidence Matrix (005–010)

### 005 — YOLO enabled vs baseline comparison recheck
- inputs:
  - baseline: `logs/perception_eval_option_a_phone_local_001_restore_20260427_1446/`
  - yolo enabled shadow: `logs/yolo_shadow_eval_option_a_phone_local_enabled_smoke_retry_fix002_20260427_1503/`
  - comparison: `logs/yolo_enabled_vs_baseline_compare_005_20260427_1507_v2/`
- runtime:
  - yolo_invoked_count=3
  - fallback_count=0
- detection increment:
  - detection_count_total=39
  - detection_count_per_sample: clear_path=7, minor_obstacle=8, narrow_path=24
  - class_distribution: person=33, bicycle=1, potted plant=5
- boundaries:
  - execute leakage=0; default-on leakage=0
  - allows_execute_now_false_rate=1.0
  - evidence_type_preserved_rate=1.0
- artifacts:
  - trace/replay/whitebox ready rates=1.0

### 006 — YOLO perception replacement trial (offline)
- root (latest): `logs/yolo_perception_replacement_eval_option_a_phone_local_001_20260427_1558/`
- completeness:
  - replacement_result_generated_rate=1.0
  - yolo_invoked_rate=1.0
  - fallback_rate=0.0
  - detection_available_rate=1.0
- Perception-001 five signals:
  - signal_schema_valid_rate=1.0
- unsupported capability honesty:
  - OCR not_available=1.0
  - dynamic not_available=1.0
  - depth_unavailable=1.0
  - collision_risk_not_confirmed=1.0
- boundaries:
  - allows_execute_now_false_rate=1.0
  - leakage totals=0
  - evidence boundary rates=1.0
- critical boundary fix:
  - `pending_real_sidewalk_run` 字段已从 `run_evidence.json` 传递并在该阶段硬断言为 true（用于后续 010 全链路断言）。

### 007 — YOLO replacement → SceneTask bridge evaluation
- root (latest): `logs/yolo_scene_task_bridge_eval_option_a_phone_local_001_20260427_1558/`
- outputs:
  - scene_state_generated_rate=1.0; schema_valid_rate=1.0
  - task_candidate_generated_rate=1.0; schema_valid_rate=1.0
- yolo use + conservatism:
  - yolo_detection_used_rate=1.0
  - unsupported_capabilities_respected_rate=1.0
- boundaries:
  - candidate_only_integrity_rate=1.0
  - leakage totals=0
  - evidence boundary rates=1.0

### 008 — SceneTask → Fusion bridge evaluation
- root (latest): `logs/yolo_fusion_bridge_eval_option_a_phone_local_001_20260427_1558/`
- outputs:
  - fusion_candidate_generated_rate=1.0
  - fusion_candidate_schema_valid_rate=1.0
  - source_attribution_present_rate=1.0
- source traceability:
  - yolo_detection_source_preserved_rate=1.0
  - source_scene_id_present_rate=1.0
  - source_task_candidate_ids_present_rate=1.0
- boundaries:
  - candidate_only_integrity_rate=1.0
  - leakage totals=0
  - evidence boundary rates=1.0

### 009 — Fusion → Output bridge evaluation
- root (latest): `logs/yolo_output_bridge_eval_option_a_phone_local_001_20260427_1558/`
- outputs:
  - output_candidate_generated_rate=1.0
  - output_candidate_schema_valid_rate=1.0
- timing/priority/suppression:
  - validity_window_present_rate=1.0
  - expires_after_generated_rate=1.0
  - priority_valid_rate=1.0
  - suppression_reason_present_rate=1.0
  - repeat_policy_present_rate=1.0
- no-real-TTS:
  - real_tts_invoked_false_rate=1.0
- safety:
  - forbidden_output_semantic_count=0
  - leakage totals=0
- evidence boundary:
  - rates=1.0

### 010 — YOLO end-to-end offline evaluation
- root (latest): `logs/yolo_e2e_offline_eval_option_a_phone_local_001_20260427_1559/`
- chain completeness:
  - sample_chain_complete_rate=1.0
- schema integrity:
  - all stage schema valid rates=1.0
- traceability:
  - yolo_invoked_rate=1.0
  - detection_available_rate=1.0
  - yolo_detection_source_preserved_all_stages_rate=1.0
  - source_attribution_present_all_stages_rate=1.0
- candidate-only / no-TTS:
  - allows_execute_now_false_all_stages_rate=1.0
  - candidate_only_integrity_rate=1.0
  - real_tts_invoked_false_rate=1.0
- safety:
  - leakage totals=0
  - forbidden_output_semantic_count_total=0
- evidence boundary:
  - evidence_type_preserved_all_stages_rate=1.0
  - controlled_live_stream_false_all_stages_rate=1.0
  - phone_local_capture_true_all_stages_rate=1.0
  - pending_real_sidewalk_run_true_rate=1.0

