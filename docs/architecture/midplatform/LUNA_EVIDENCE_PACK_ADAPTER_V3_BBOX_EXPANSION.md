# Luna — Evidence Pack Adapter v3 BBoxExpansion

**Phase**：`Phase-Evidence-Pack-Adapter-v3-BBoxExpansion-001`

## 目的

将 `expanded_roi_ocr_result_collection_v2`（4 条，按 `expansion_strategy`）适配为 **Evidence Pack v3 BBoxExpansion**，保留双 bbox、strategy、text_items、provider metadata 与 strategy comparison 风险标记。

## 边界

- 仅 adapter；**不**运行 OCR、不生成 Semantic Candidate v3、不执行 Source Validation v2
- EP v3 ≠ 事实；bank-like OCR text ≠ accuracy；重复 strategy 输出 ≠ independent consensus

## 实现

- `capabilities/midplatform/evidence_pack_adapter_v3_bbox_expansion.py`
- `tools/evaluation/midplatform/run_evidence_pack_adapter_v3_bbox_expansion.py`
- `tools/evaluation/midplatform/verify_evidence_pack_adapter_v3_bbox_expansion.py`

## 前置

- [LUNA_OCRREQUEST_GATED_SUBMISSION_FROM_ROI_V2_BBOX_EXPANSION.md](../ocr/LUNA_OCRREQUEST_GATED_SUBMISSION_FROM_ROI_V2_BBOX_EXPANSION.md)

## 评测

[LUNA_EVALUATION_EVIDENCE_PACK_ADAPTER_V3_BBOX_EXPANSION.md](../evaluation/LUNA_EVALUATION_EVIDENCE_PACK_ADAPTER_V3_BBOX_EXPANSION.md)

## 建议下一 phase

- [LUNA_SEMANTIC_CANDIDATE_V3_BBOX_EXPANSION_AWARE.md](./LUNA_SEMANTIC_CANDIDATE_V3_BBOX_EXPANSION_AWARE.md)（Semantic Candidate v3 BBoxExpansionAware）
- `Source-Validation-v2-after-EP-v3`
