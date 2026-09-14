# Luna — OCRRequest Gated Submission from Multiframe v1

**Phase**：`OCRRequest-Gated-Submission-from-Multiframe-v1-001`

## 目的

对 30 个 multiframe projection crop 执行 **gated OCRRequest submission**（经 `ocr_mainline_bridge`），生成 `multiframe_ocr_result_collection_v1`；**不**生成 EP v4 / Semantic v4 / SV rerun。

## 边界

- 禁止 capability 内直接 import RapidOCR/PaddleOCR
- `detected_region=false`；`same_frame_blocker` 不得解除
- OCR result **不是** fact / evidence pack

## 实现

- `capabilities/ocr_runtime/ocrrequest_gated_submission_from_multiframe_v1.py`
- `tools/evaluation/ocr/run_ocrrequest_gated_submission_from_multiframe_v1.py`
- `tools/evaluation/ocr/verify_ocrrequest_gated_submission_from_multiframe_v1.py`

## 前置

- [LUNA_MULTIFRAME_CROP_EXECUTION_DRYRUN_V1.md](../midplatform/LUNA_MULTIFRAME_CROP_EXECUTION_DRYRUN_V1.md)

## 评测

[LUNA_EVALUATION_OCRREQUEST_GATED_SUBMISSION_FROM_MULTIFRAME_V1.md](../evaluation/LUNA_EVALUATION_OCRREQUEST_GATED_SUBMISSION_FROM_MULTIFRAME_V1.md)

## 建议下一 phase

- `Crop-Quality-Diagnosis-v2-Multiframe`（EP v4 见 [LUNA_EVIDENCE_PACK_ADAPTER_V4_MULTIFRAME.md](../midplatform/LUNA_EVIDENCE_PACK_ADAPTER_V4_MULTIFRAME.md)）
