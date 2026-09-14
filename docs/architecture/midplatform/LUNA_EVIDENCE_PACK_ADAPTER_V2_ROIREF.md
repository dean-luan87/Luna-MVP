# Luna — Evidence Pack Adapter v2 ROIRef

**Phase**：`Phase-Evidence-Pack-Adapter-v2-ROIRef-001`

## 目的

将 ROI OCR gated submission 产出的 `roi_ocr_result_collection` 适配为 **Evidence Pack v2（ROIRef）**，保留 ocrrequest/crop/text_items/provider metadata，并标记 repeated/low-information 风险。

## 边界

- 仅 adapter；不运行 OCR、不生成 Semantic Candidate、不写事实
- `non_empty_text` ≠ accuracy；12 条同为「行」须标 `repeated_same_text`

## 实现

- `capabilities/midplatform/evidence_pack_adapter_v2_roiref.py`
- `tools/evaluation/midplatform/run_evidence_pack_adapter_v2_roiref.py`
- `tools/evaluation/midplatform/verify_evidence_pack_adapter_v2_roiref.py`

## 前置

- [LUNA_OCRREQUEST_GATED_SUBMISSION_FROM_ROI_V1.md](../ocr/LUNA_OCRREQUEST_GATED_SUBMISSION_FROM_ROI_V1.md)

## 评测

[LUNA_EVALUATION_EVIDENCE_PACK_ADAPTER_V2_ROIREF.md](../evaluation/LUNA_EVALUATION_EVIDENCE_PACK_ADAPTER_V2_ROIREF.md)

## 建议下一 phase

- [LUNA_SEMANTIC_CANDIDATE_V2_ROIAWARE.md](./LUNA_SEMANTIC_CANDIDATE_V2_ROIAWARE.md)（已完成 smoke：12 diagnostic semantic）
- `ROI-OCR-Quality-Diagnosis-v1`
