# Luna — OCR Evidence Pack SpatioTemporal Semantic Contract v0

**Phase**：`Phase-OCR-Evidence-Pack-SpatioTemporal-Semantic-Contract-001`

## 目的

定义统一 **OCR Evidence Pack v0** 三层合同：

```
OCRTextEvidence
  → OCRSemanticCandidate
  → WorldModelAttachCandidate
  → Gate / Review / TTL / Conflict / Source Validation
  → WorldModel Fact
```

OCR 不只输出文字，而是带图像/时空间坐标、来源链、质量标签、语义候选、世界模型挂载候选的结构化证据包。

## 原则

- `raw_ocr_text` 必须保留，不得覆盖
- semantic candidate / attach candidate 均为 **not_fact**
- 缺失坐标显式 `null`，不得伪造
- 本阶段仅 contract/schema/policy/examples，不运行 OCR/语义模型

## 实现

- Capability：`capabilities/midplatform/ocr_evidence_pack_spatiotemporal_semantic_contract_v0.py`
- Runner：`tools/evaluation/midplatform/run_ocr_evidence_pack_spatiotemporal_semantic_contract_v0.py`
- Verifier：`tools/evaluation/midplatform/verify_ocr_evidence_pack_spatiotemporal_semantic_contract_v0.py`

## 评测

[LUNA_EVALUATION_OCR_EVIDENCE_PACK_SPATIOTEMPORAL_SEMANTIC_CONTRACT_V0.md](../evaluation/LUNA_EVALUATION_OCR_EVIDENCE_PACK_SPATIOTEMPORAL_SEMANTIC_CONTRACT_V0.md)

## 相关合同

**WorldModel Unresolved Observation Slot**（见 [LUNA_WORLDMODEL_UNRESOLVED_OBSERVATION_SLOT_CONTRACT_V0.md](./LUNA_WORLDMODEL_UNRESOLVED_OBSERVATION_SLOT_CONTRACT_V0.md)）承接 OCR empty / partial / 未确认区域，预留未来可补全槽位（非 fact）。

## 建议下一跳

**Unresolved Slot dry-run from OCR Evidence Pack** 或继续 ROI / SourceQualityGate 主线。
