# Luna — OCR Evidence Pack Adapter v1 Scan Observation Alignment v0

**Phase**：`Phase-OCR-Evidence-Pack-Adapter-v1-ScanObservation-Alignment-001`

## 目的

将 **Mixed Batch v2** gated-only 产物升级为 **`ocr_text_evidence_pack_v1`**，补齐：

- `scan_observation_ref`
- `source_quality_grade`
- `readability_gate_ref`
- `ocr_request_ref`
- `gated_path_ref`
- `evidence_tier`（gated_ocr_primary vs scan_observation_only）

明确 **scan observation 不是主 evidence**；为 Semantic Candidate v1 提供分层依据。

## 边界

- 不运行 OCR；不写 fact / WM；不改 routing

## 实现

- `capabilities/midplatform/ocr_evidence_pack_adapter_v1_scan_observation_alignment_v0.py`
- `tools/evaluation/midplatform/run_ocr_evidence_pack_adapter_v1_scan_observation_alignment_v0.py`
- `tools/evaluation/midplatform/verify_ocr_evidence_pack_adapter_v1_scan_observation_alignment_v0.py`

## 后续

**Semantic Candidate Generator v1**（见 [LUNA_OCR_SEMANTIC_CANDIDATE_GENERATOR_V1.md](./LUNA_OCR_SEMANTIC_CANDIDATE_GENERATOR_V1.md)）消费本阶段 Evidence Pack v1 的 `evidence_tier`。

## 评测

[LUNA_EVALUATION_OCR_EVIDENCE_PACK_ADAPTER_V1_SCAN_OBSERVATION_ALIGNMENT_V0.md](../evaluation/LUNA_EVALUATION_OCR_EVIDENCE_PACK_ADAPTER_V1_SCAN_OBSERVATION_ALIGNMENT_V0.md)
