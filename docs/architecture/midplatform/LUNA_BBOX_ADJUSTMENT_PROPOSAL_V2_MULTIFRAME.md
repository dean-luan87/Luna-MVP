# Luna — BBox Adjustment Proposal v2 Multiframe

**Phase**：`BBox-Adjustment-Proposal-v2-Multiframe-001`

## 目的

将 Text Detector DryRun 的 5 条 bbox adjustment candidate 正式治理为 **BBox Adjustment Proposal v2**（bounds check、clip、去重）；**不**生成新 crop、**不**运行 OCR。

## 边界

- proposal 不是 detected text region；heuristic 不是事实
- `proposal_ready_for_future_recrop` 不等于 OCR-ready fact

## 实现

- `capabilities/midplatform/bbox_adjustment_proposal_v2_multiframe.py`
- `tools/evaluation/midplatform/run_bbox_adjustment_proposal_v2_multiframe.py`
- `tools/evaluation/midplatform/verify_bbox_adjustment_proposal_v2_multiframe.py`

## 前置

- [LUNA_TEXT_DETECTOR_DRYRUN_V1.md](./LUNA_TEXT_DETECTOR_DRYRUN_V1.md)

## 评测

[LUNA_EVALUATION_BBOX_ADJUSTMENT_PROPOSAL_V2_MULTIFRAME.md](../evaluation/LUNA_EVALUATION_BBOX_ADJUSTMENT_PROPOSAL_V2_MULTIFRAME.md)

## 建议下一 phase

- `Multiframe-Crop-Execution-DryRun-v2-TextDetectorAdjusted`（见 [LUNA_MULTIFRAME_CROP_EXECUTION_DRYRUN_V2_TEXTDETECTOR_ADJUSTED.md](./LUNA_MULTIFRAME_CROP_EXECUTION_DRYRUN_V2_TEXTDETECTOR_ADJUSTED.md)）
