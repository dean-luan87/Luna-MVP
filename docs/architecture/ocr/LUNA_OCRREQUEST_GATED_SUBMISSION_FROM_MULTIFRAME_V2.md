# Luna — OCRRequest Gated Submission from Multiframe v2

**Phase**：`OCRRequest-Gated-Submission-from-Multiframe-v2-001`

## 目的

对 **5** 个 TextDetectorAdjusted multiframe crop 执行 **gated OCRRequest submission v2**（经 `ocr_mainline_bridge`），生成 `multiframe_ocr_result_v2_collection` 并与 v1（30 条 empty）做只读对比；**不**生成 EP / Semantic / SV rerun。

## 架构原则

本 phase 受 [LUNA_OCR_TASK_ORIENTED_CAPABILITY_PRINCIPLE_V0.md](./LUNA_OCR_TASK_ORIENTED_CAPABILITY_PRINCIPLE_V0.md) 约束：v2 为 **任务型受控 OCR 验证**，非世界建模主通道；empty 结果推荐 **User-Guidance-Recovery**，不无限 internal re-crop。

## 边界

- 禁止 capability 内直接 import RapidOCR/PaddleOCR
- 保留 `same_bbox_or_near_same_bbox_risk`；`same_frame_blocker` 不得解除
- v2 全 empty / 低置信时推荐 `User-Guidance-Recovery-Policy-v1`（本阶段不执行 TTS / runtime action）
- OCR result v2 **不是** fact / evidence pack

## 实现

- `capabilities/ocr_runtime/ocrrequest_gated_submission_from_multiframe_v2.py`
- `tools/evaluation/ocr/run_ocrrequest_gated_submission_from_multiframe_v2.py`
- `tools/evaluation/ocr/verify_ocrrequest_gated_submission_from_multiframe_v2.py`

## 前置

- [LUNA_MULTIFRAME_CROP_EXECUTION_DRYRUN_V2_TEXTDETECTOR_ADJUSTED.md](../midplatform/LUNA_MULTIFRAME_CROP_EXECUTION_DRYRUN_V2_TEXTDETECTOR_ADJUSTED.md)
- [LUNA_OCRREQUEST_GATED_SUBMISSION_FROM_MULTIFRAME_V1.md](./LUNA_OCRREQUEST_GATED_SUBMISSION_FROM_MULTIFRAME_V1.md)（v1/v2 对比）

## 评测

[LUNA_EVALUATION_OCRREQUEST_GATED_SUBMISSION_FROM_MULTIFRAME_V2.md](../evaluation/LUNA_EVALUATION_OCRREQUEST_GATED_SUBMISSION_FROM_MULTIFRAME_V2.md)

## 建议下一 phase

- [LUNA_USER_GUIDANCE_RECOVERY_POLICY_V1.md](../midplatform/LUNA_USER_GUIDANCE_RECOVERY_POLICY_V1.md)（已完成 policy v1 smoke）
- `STC-Sampling-Guidance-Policy-v1`
- `Evidence-Pack-Adapter-v4-Multiframe-Rerun`（v2 出现非空候选时）
