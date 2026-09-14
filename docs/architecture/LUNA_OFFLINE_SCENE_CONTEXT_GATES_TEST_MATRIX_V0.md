# LUNA — Offline SceneContext Gates Test Matrix v0 (Phase-EngineeringFlow-003)

## Inputs / artifacts
- PerceptionEval input_root（YOLO selected run）：
  - `logs/perception_eval_yolo_default_source_policy_ef002_20260428_102332`
- SceneContext gates evaluation output_root：
  - `logs/scene_context_gates_offline_ef003_20260428_103623`
- Verifier report：
  - `logs/offline_scene_context_gates_verify_002_20260428_1038.json`

## Verifier matrix（A–I）
- A 正常输入 → gate result 生成：pass
- B screen/poster/ad 等 depicted hint → transition blocked：pass
- C depth unavailable → physics 不确认：pass
- D unsupported OCR/dynamic/depth/collision → 保守处理：pass（v0 不升级）
- E zone candidate only：pass
- F conflict/degraded：pass（v0 degraded_or_uncertain=true）
- G forbidden execute probe → blocked：pass
- H evidence boundary 保持：pass
- I pending_real_sidewalk_run=true：pass

## 实际样本 gate 结果（来自 gate_summary.json）
- gate_result_generated_rate=1.0
- visual_medium_gate_result_rate=1.0
- physics_gate_result_rate=1.0
- scene_continuity_gate_result_rate=1.0
- overall_gate_result_rate=1.0
- depicted_scene_block_rate=0.0（真实样本未注入 depicted fixture）
- degraded_or_uncertain_present_rate=1.0（v0 保守默认）
- safety leakage=0（execute/default-on/side-effects）
- evidence boundary rates=1.0（evidence_type/controlled_live/phone_local/pending）

