# Luna — Evidence Pack Adapter v4 Multiframe

**Phase**：`Evidence-Pack-Adapter-v4-Multiframe-001`

## 目的

将 30 条 `multiframe_ocr_result`（含全 empty）适配为 **Evidence Pack v4 Multiframe**；显式保留 empty OCR 语义，**不**生成 Semantic v4，**不**执行 SV rerun。

## 边界

- 不运行 OCR；`empty_text` 不得解释为 no-text fact
- `semantic_candidate_allowed_later=false`；`source_validation_rerun_allowed_later=false`
- same-frame blocker 仍 active

## 实现

- `capabilities/midplatform/evidence_pack_adapter_v4_multiframe.py`
- `tools/evaluation/midplatform/run_evidence_pack_adapter_v4_multiframe.py`
- `tools/evaluation/midplatform/verify_evidence_pack_adapter_v4_multiframe.py`

## 前置

- [LUNA_OCRREQUEST_GATED_SUBMISSION_FROM_MULTIFRAME_V1.md](../ocr/LUNA_OCRREQUEST_GATED_SUBMISSION_FROM_MULTIFRAME_V1.md)

## 评测

[LUNA_EVALUATION_EVIDENCE_PACK_ADAPTER_V4_MULTIFRAME.md](../evaluation/LUNA_EVALUATION_EVIDENCE_PACK_ADAPTER_V4_MULTIFRAME.md)

## 建议下一 phase

- `Crop-Quality-Diagnosis-v2-Multiframe`（见 [LUNA_CROP_QUALITY_DIAGNOSIS_V2_MULTIFRAME.md](./LUNA_CROP_QUALITY_DIAGNOSIS_V2_MULTIFRAME.md)）
- 其后：`Text-Detector-DryRun-v1` / `BBox-Adjustment-Proposal-v2-Multiframe`
