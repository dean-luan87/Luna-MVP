# LUNA — YOLO Shadow End-to-End Offline Eval Contract v0 (Phase-ModelPerception-010)

## Scope
本 contract 仅约束 **YOLO shadow 端到端离线验收产物**，不产生任何 runtime 接入效力。

## Required stage roots (inputs)
评测工具必须读取以下输入根（路径必须可追溯记录在 summary.inputs 中）：
- FieldBatch root（含 `sample_matrix.json`）
- YOLO perception replacement root（Phase-ModelPerception-006）
- YOLO SceneTask bridge root（Phase-ModelPerception-007）
- YOLO Fusion bridge root（Phase-ModelPerception-008）
- YOLO Output bridge root（Phase-ModelPerception-009）

## Per-sample checks (hard)
每条样本必须满足：
- 四段输出均存在（perception/scene_task/fusion/output present）
- 四段 schema 均有效（schema_ok）
- YOLO source traceability 全链路保持：
  - perception: yolo_invoked/detection_count/detected_classes
  - fusion/output: source_attribution.yolo_source 保留上述字段
- candidate-only / no-real-TTS：
  - SceneTask candidates: allows_execute_now=false
  - Fusion candidate: allows_execute_now=false
  - Output candidate: allows_execute_now=false 且 real_tts_invoked=false
- safety leakage totals = 0（execute/default-on/release-retry-reopen/side-effects/forced_action/forbidden semantics）
- evidence boundary 全链路保持：
  - evidence_type == phone_local_controlled_capture
  - controlled_live_stream false
  - phone_local_capture true
  - pending_real_sidewalk_run true（不得被关闭）

## Outputs (required)
输出根必须包含：
- `yolo_e2e_offline_evaluation_summary.json`
- `per_sample_yolo_chain_results.json`
- `yolo_chain_trace_consistency.json`
- `evaluation_notes.md`

## Non-goals (explicit)
- 不证明真实导航能力
- 不进入真实 TTS/Output runtime
- 不执行导航动作、不真实播报

