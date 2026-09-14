# Luna — Semantic Candidate v2 ROIAware

**Phase**：`Phase-Semantic-Candidate-v2-ROIAware-001`

## 目的

将 Evidence Pack v2 ROIRef 转为 **risk-aware Semantic Candidate v2**（weak/diagnostic/hold only），消费 `repeated_same_text`、`low_information_text` 等 risk_flags，禁止强语义与实体确认。

## 边界

- 规则/heuristic only；不 OCR、不 LLM/VLM、不写事实
- 单字「行」不得解释为银行/路线/设施；`entity_candidate` 恒为 null

## 实现

- `capabilities/midplatform/semantic_candidate_v2_roiaware.py`
- `tools/evaluation/midplatform/run_semantic_candidate_v2_roiaware.py`
- `tools/evaluation/midplatform/verify_semantic_candidate_v2_roiaware.py`

## 前置

- [LUNA_EVIDENCE_PACK_ADAPTER_V2_ROIREF.md](./LUNA_EVIDENCE_PACK_ADAPTER_V2_ROIREF.md)

## 评测

[LUNA_EVALUATION_SEMANTIC_CANDIDATE_V2_ROIAWARE.md](../evaluation/LUNA_EVALUATION_SEMANTIC_CANDIDATE_V2_ROIAWARE.md)

## 建议下一 phase

- [LUNA_ROI_OCR_QUALITY_DIAGNOSIS_V1.md](./LUNA_ROI_OCR_QUALITY_DIAGNOSIS_V1.md)（已完成 smoke：10 hypotheses，未 confirmed）
- `Crop-Quality-Scoring-v1`
- `ROI-Crop-Diversity-Check-v1`
