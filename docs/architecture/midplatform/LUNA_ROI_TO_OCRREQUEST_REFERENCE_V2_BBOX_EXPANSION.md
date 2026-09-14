# Luna — ROI-to-OCRRequest Reference v2 BBoxExpansion

**Phase**：`Phase-ROI-to-OCRRequest-Reference-v2-BBoxExpansion-001`

## 目的

将 4 个 expanded ROI crop artifact 转为 OCRRequest reference v2（`not_submitted`）；保留 expansion_candidate_ref、source/expanded bbox、expansion_strategy 与 source_chain。

## 边界

- Reference v2 ≠ OCR submission ≠ OCR result ≠ Evidence Pack ≠ 事实
- 不调用 OCR provider；`ocrrequest_submitted=false`

## 实现

- `capabilities/midplatform/roi_to_ocrrequest_reference_v2_bbox_expansion.py`
- `tools/evaluation/midplatform/run_roi_to_ocrrequest_reference_v2_bbox_expansion.py`
- `tools/evaluation/midplatform/verify_roi_to_ocrrequest_reference_v2_bbox_expansion.py`

## 前置

- [LUNA_ROI_CROP_EXECUTION_DRYRUN_V2_BBOX_EXPANSION.md](./LUNA_ROI_CROP_EXECUTION_DRYRUN_V2_BBOX_EXPANSION.md)

## 建议下一 phase

- [LUNA_OCRREQUEST_GATED_SUBMISSION_FROM_ROI_V2_BBOX_EXPANSION.md](../ocr/LUNA_OCRREQUEST_GATED_SUBMISSION_FROM_ROI_V2_BBOX_EXPANSION.md)（已完成 smoke：4 gated submission → expanded ROI OCR result v2）
- `Evidence-Pack-Adapter-v3-BBoxExpansion`
