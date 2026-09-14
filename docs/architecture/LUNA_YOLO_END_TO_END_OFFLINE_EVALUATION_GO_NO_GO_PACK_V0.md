# LUNA — YOLO Shadow End-to-End Offline Evaluation Go/No-Go Pack v0 (Phase-ModelPerception-010)

## Inputs (this run)
- FieldBatch root: `logs/phone_local_field_batch_002_20260427_111431/`
- YOLO perception replacement root: `logs/yolo_perception_replacement_eval_option_a_phone_local_001_20260427_1558/`
- YOLO SceneTask bridge root: `logs/yolo_scene_task_bridge_eval_option_a_phone_local_001_20260427_1558/`
- YOLO Fusion bridge root: `logs/yolo_fusion_bridge_eval_option_a_phone_local_001_20260427_1558/`
- YOLO Output bridge root: `logs/yolo_output_bridge_eval_option_a_phone_local_001_20260427_1558/`

## Outputs
- E2E output root: `logs/yolo_e2e_offline_eval_option_a_phone_local_001_20260427_1559/`

Docs:
- `docs/architecture/LUNA_YOLO_END_TO_END_OFFLINE_EVALUATION_DEFINITION_V0.md`
- `docs/architecture/LUNA_YOLO_END_TO_END_OFFLINE_EVAL_CONTRACT_V0.md`
- `docs/architecture/LUNA_YOLO_END_TO_END_OFFLINE_EVALUATION_MATRIX_V0.md`

## Decision
### Result
**GO**

## Evidence (from E2E summary)
Chain completeness:
- sample_chain_complete_rate: **1.0**
- stage complete rates (perception/scene_task/fusion/output): **1.0**

Schema integrity:
- yolo_perception_schema_valid_rate: **1.0**
- yolo_scene_task_schema_valid_rate: **1.0**
- yolo_fusion_schema_valid_rate: **1.0**
- yolo_output_schema_valid_rate: **1.0**

YOLO source traceability:
- yolo_invoked_rate: **1.0**
- detection_available_rate: **1.0**
- yolo_detection_source_preserved_all_stages_rate: **1.0**
- source_attribution_present_all_stages_rate: **1.0**

Candidate-only / no-real-TTS:
- allows_execute_now_false_all_stages_rate: **1.0**
- candidate_only_integrity_rate: **1.0**
- real_tts_invoked_false_rate: **1.0**

Safety boundary totals:
- execute/default-on/release-retry-reopen/side-effects/forced_action/forbidden semantics totals: **0**

Evidence boundary:
- evidence_type_preserved_all_stages_rate: **1.0**
- controlled_live_stream_false_all_stages_rate: **1.0**
- phone_local_capture_true_all_stages_rate: **1.0**
- pending_real_sidewalk_run_true_rate: **1.0**

## Hard blockers
- `[]`

## Soft follow-ups
- 本阶段仅验证“离线候选链路机制闭合”，不等价于真实导航能力验证。
- Output/Fusion/SceneTask policy 仍为最小规则 v0；需要更多样本与更严格策略后再谈性能或可用性。

## Recommended next phase (do not auto-enter)
- **Phase-ModelPerception-011：YOLO Shadow Baseline Replacement Review v0**

## Explicit boundary re-statement
- 默认路径仍未开启
- 未进入 full controlled trial
- 未扩大真实 side effects 面
- 未执行 controlled_live_stream
- 未扩 Option A
- 未执行导航动作
- 未真实播报
- YOLO shadow 仍未进入真实 runtime
- 本阶段只做 YOLO shadow 端到端离线机制验收

