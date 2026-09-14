# LUNA — YOLO Shadow PerceptionEval Replacement Trial Go/No-Go Pack v0 (Phase-ModelPerception-006)

## Inputs
- sample_matrix: `logs/phone_local_field_batch_002_20260427_111431/sample_matrix.json`
- yolo shadow root: `logs/yolo_shadow_eval_option_a_phone_local_enabled_smoke_retry_fix002_20260427_1503/`
- replacement output root:
  - `logs/yolo_perception_replacement_eval_option_a_phone_local_001_20260427_1513/`

Docs:
- `docs/architecture/LUNA_YOLO_PERCEPTION_REPLACEMENT_TRIAL_DEFINITION_V0.md`
- `docs/architecture/LUNA_YOLO_PERCEPTION_REPLACEMENT_TRIAL_CONTRACT_V0.md`
- `docs/architecture/LUNA_YOLO_PERCEPTION_REPLACEMENT_TRIAL_MATRIX_V0.md`

## Decision
### Result
**GO**

## Evidence (from replacement summary)
Key metrics:
- replacement_result_generated_rate: **1.0**
- yolo_invoked_rate: **1.0**
- fallback_rate: **0.0**
- detection_available_rate: **1.0**
- signal_schema_valid_rate: **1.0**
- unsupported honesty:
  - ocr_not_available_rate: **1.0**
  - dynamic_not_available_rate: **1.0**
  - depth_unavailable_rate: **1.0**
  - collision_risk_not_confirmed_rate: **1.0**
- candidate-only/safety:
  - allows_execute_now_false_rate: **1.0**
  - execute/default-on/release-retry-reopen/side-effects leakage: **0**
- evidence boundary:
  - evidence_type_preserved_rate: **1.0**
  - controlled_live_stream_false_rate: **1.0**
  - phone_local_capture_true_rate: **1.0**

## Hard boundaries (re-affirmed)
- 本阶段是 offline replacement trial，不是正式替换
- 不进入 SceneTask/Fusion/Output
- 不执行导航动作、不真实播报
- 不开启默认路径、不扩大 side effects 面
- 不宣称 depth/OCR/dynamic/collision risk 能力
- replacement 结果仅用于离线复核与后续离线桥接评测准备

## Hard blockers
- `[]`

## Soft follow-ups
- torch.hub 仍是可复现性风险（后续需 pinned local weights + pinned deps），不作为 v0 阻断。

## Recommended next phase (do not auto-enter)
- **Phase-ModelPerception-007：YOLO Shadow SceneTask Bridge Evaluation v0**

## Explicit boundary re-statement
- 默认路径仍未开启
- 未进入 full controlled trial
- 未扩大真实 side effects 面
- 未执行 controlled_live_stream
- 未扩 Option A
- 未执行导航动作
- 未真实播报
- YOLO replacement 不进入 SceneTask/Fusion/Output
- 本阶段只做 YOLO perception replacement offline trial

