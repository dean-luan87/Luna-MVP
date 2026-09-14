# Luna — Text Detector DryRun v1

**Phase**：`Text-Detector-DryRun-v1-001`

## 目的

在 30 个 multiframe crop 与 6 个 better frame 上做 **text-like region** dry-run，生成 bbox adjustment candidate；**不**运行 OCR、**不**识别文字内容。

## 边界

- supervision 仅可选工具层（slicing/container/filter），不是 OCR provider
- `detected_text_content=null`；`ocr_text=null`；`fact_status=not_fact`
- Semantic v4 / SV rerun 继续阻断

## 实现

- `capabilities/midplatform/text_detector_dryrun_v1.py`
- `tools/evaluation/midplatform/run_text_detector_dryrun_v1.py`
- `tools/evaluation/midplatform/verify_text_detector_dryrun_v1.py`

## 前置

- [LUNA_CROP_QUALITY_DIAGNOSIS_V2_MULTIFRAME.md](./LUNA_CROP_QUALITY_DIAGNOSIS_V2_MULTIFRAME.md)

## 评测

[LUNA_EVALUATION_TEXT_DETECTOR_DRYRUN_V1.md](../evaluation/LUNA_EVALUATION_TEXT_DETECTOR_DRYRUN_V1.md)

## 建议下一 phase

- `BBox-Adjustment-Proposal-v2-Multiframe`（见 [LUNA_BBOX_ADJUSTMENT_PROPOSAL_V2_MULTIFRAME.md](./LUNA_BBOX_ADJUSTMENT_PROPOSAL_V2_MULTIFRAME.md)）
- 其后：`Multiframe-Crop-Execution-DryRun-v2-TextDetectorAdjusted`
