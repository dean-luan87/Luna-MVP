# Luna — OCRRequest Gated Submission from ROI v1

**Phase**：`Phase-OCRRequest-Gated-Submission-from-ROI-v1-001`

## 目的

消费 ROI-to-OCRRequest Reference v1 产出的 12 条 reference，经 gate 后通过 **ocr_mainline_bridge** 提交 OCRRequest，生成 ROI OCR result collection 与 bridge invocation trace。

## 核心原则

1. 所有 provider 调用必须带 `ocrrequest_reference_id`
2. 必须走 `run_ocr_mainline_bridge_v0`；禁止 capability 内 direct RapidOCR/PaddleOCR
3. 禁止 full-frame OCR、mock text、Evidence Pack v2、Semantic Candidate v2
4. OCR 结果 ≠ 事实 ≠ Evidence Pack

## 实现

- `capabilities/ocr_runtime/ocrrequest_gated_submission_from_roi_v1.py`
- `tools/evaluation/ocr/run_ocrrequest_gated_submission_from_roi_v1.py`
- `tools/evaluation/ocr/verify_ocrrequest_gated_submission_from_roi_v1.py`

## 前置

- [LUNA_ROI_TO_OCRREQUEST_REFERENCE_V1.md](../midplatform/LUNA_ROI_TO_OCRREQUEST_REFERENCE_V1.md)

## 评测

[LUNA_EVALUATION_OCRREQUEST_GATED_SUBMISSION_FROM_ROI_V1.md](../evaluation/LUNA_EVALUATION_OCRREQUEST_GATED_SUBMISSION_FROM_ROI_V1.md)

## 建议下一 phase

- [LUNA_EVIDENCE_PACK_ADAPTER_V2_ROIREF.md](../midplatform/LUNA_EVIDENCE_PACK_ADAPTER_V2_ROIREF.md)（已完成 smoke：12 EP v2）
- `Semantic-Candidate-v2-ROIAware`
