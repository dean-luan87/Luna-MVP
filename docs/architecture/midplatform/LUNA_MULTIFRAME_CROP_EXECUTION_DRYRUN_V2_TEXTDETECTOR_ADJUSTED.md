# Luna — Multiframe Crop Execution DryRun v2 TextDetectorAdjusted

**Phase**：`Multiframe-Crop-Execution-DryRun-v2-TextDetectorAdjusted-001`

## 目的

消费 5 条 BBox Adjustment Proposal v2，基于 `clipped_adjusted_bbox_xyxy` 生成 **TextDetectorAdjusted** multiframe crop PNG；验证 proposal → re-crop → future OCR v2 链路可执行。

## 边界

- 不运行 OCR；不生成 OCRRequest；same-frame blocker 未解除
- 若后续 re-OCR 仍 empty：**不得**无限内部扩框重试 → 进入 User Guidance Recovery / STC Sampling Guidance（本阶段仅 follow-up）

## 实现

- `capabilities/midplatform/multiframe_crop_execution_dryrun_v2_textdetector_adjusted.py`
- `tools/evaluation/midplatform/run_multiframe_crop_execution_dryrun_v2_textdetector_adjusted.py`
- `tools/evaluation/midplatform/verify_multiframe_crop_execution_dryrun_v2_textdetector_adjusted.py`

## 前置

- [LUNA_BBOX_ADJUSTMENT_PROPOSAL_V2_MULTIFRAME.md](./LUNA_BBOX_ADJUSTMENT_PROPOSAL_V2_MULTIFRAME.md)

## 评测

[LUNA_EVALUATION_MULTIFRAME_CROP_EXECUTION_DRYRUN_V2_TEXTDETECTOR_ADJUSTED.md](../evaluation/LUNA_EVALUATION_MULTIFRAME_CROP_EXECUTION_DRYRUN_V2_TEXTDETECTOR_ADJUSTED.md)

## 建议下一 phase

- [LUNA_OCRREQUEST_GATED_SUBMISSION_FROM_MULTIFRAME_V2.md](../ocr/LUNA_OCRREQUEST_GATED_SUBMISSION_FROM_MULTIFRAME_V2.md)（已完成 smoke：5/5 OCR v2 empty → User Guidance Recovery）
