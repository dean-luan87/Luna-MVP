# Luna — OCRRequest Gated Submission from ROI v2 BBoxExpansion

**Phase**：`Phase-OCRRequest-Gated-Submission-from-ROI-v2-BBoxExpansion-001`

## 目的

对 4 条 expanded ROI **OCRRequest reference v2** 做 gated submission；经 **ocr_mainline_bridge** 调用 RapidOCR lightweight，生成 **expanded ROI OCR result collection v2**，并按 `expansion_strategy` 产出 strategy comparison candidate（非 benchmark）。

## 核心原则

1. Reference v2 必须先 gate，再 submission；每次 provider 调用带 `ocrrequest_reference_v2_id`
2. 必须走 `run_ocr_mainline_bridge_v0`；禁止 capability 内 direct RapidOCR/PaddleOCR
3. 禁止 full-frame OCR、mock text、Evidence Pack v3、Semantic Candidate v3、Source Validation v2
4. OCR 结果 ≠ 事实 ≠ Evidence Pack；`non_empty_text` 不代表 accuracy

## 实现

- `capabilities/ocr_runtime/ocrrequest_gated_submission_from_roi_v2_bbox_expansion.py`
- `tools/evaluation/ocr/run_ocrrequest_gated_submission_from_roi_v2_bbox_expansion.py`
- `tools/evaluation/ocr/verify_ocrrequest_gated_submission_from_roi_v2_bbox_expansion.py`

## 前置

- [LUNA_ROI_TO_OCRREQUEST_REFERENCE_V2_BBOX_EXPANSION.md](../midplatform/LUNA_ROI_TO_OCRREQUEST_REFERENCE_V2_BBOX_EXPANSION.md)

## 评测

[LUNA_EVALUATION_OCRREQUEST_GATED_SUBMISSION_FROM_ROI_V2_BBOX_EXPANSION.md](../evaluation/LUNA_EVALUATION_OCRREQUEST_GATED_SUBMISSION_FROM_ROI_V2_BBOX_EXPANSION.md)

## 建议下一 phase

- [LUNA_EVIDENCE_PACK_ADAPTER_V3_BBOX_EXPANSION.md](../midplatform/LUNA_EVIDENCE_PACK_ADAPTER_V3_BBOX_EXPANSION.md)（已完成 smoke：4 EP v3）
- `Semantic-Candidate-v3-BBoxExpansionAware`
- `Semantic-Candidate-v3-BBoxExpansionAware`
