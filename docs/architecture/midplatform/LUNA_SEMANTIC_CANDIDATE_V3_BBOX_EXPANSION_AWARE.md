# Luna — Semantic Candidate v3 BBoxExpansionAware

**Phase**：`Phase-Semantic-Candidate-v3-BBoxExpansionAware-001`

## 目的

消费 **Evidence Pack v3 BBoxExpansion**（4 条 expansion strategy），以规则/启发式生成 **Semantic Candidate v3**（bank-like / noisy English / strategy repeat guard），全部为 `candidate_only`，不确认实体、不执行 Source Validation v2、不写事实层。

## 边界

- 不运行 OCR、不调用 LLM/VLM/Vision provider
- bank-like OCR ≠ 银行事实；重复 strategy 输出（如 padding_medium 与 contextual_expand 同文「建银银行」）≠ independent consensus
- noisy English（如 `G QocionBank`）不得自动纠错/补全为 China Construction Bank
- `entity_confirmed` 恒为 false；`write_allowed` 恒为 false

## 实现

- `capabilities/midplatform/semantic_candidate_v3_bbox_expansion_aware.py`
- `tools/evaluation/midplatform/run_semantic_candidate_v3_bbox_expansion_aware.py`
- `tools/evaluation/midplatform/verify_semantic_candidate_v3_bbox_expansion_aware.py`

## 前置

- [LUNA_EVIDENCE_PACK_ADAPTER_V3_BBOX_EXPANSION.md](./LUNA_EVIDENCE_PACK_ADAPTER_V3_BBOX_EXPANSION.md)

## 评测

[LUNA_EVALUATION_SEMANTIC_CANDIDATE_V3_BBOX_EXPANSION_AWARE.md](../evaluation/LUNA_EVALUATION_SEMANTIC_CANDIDATE_V3_BBOX_EXPANSION_AWARE.md)

## 建议下一 phase

- [LUNA_SOURCE_VALIDATION_V2_AFTER_EP_V3.md](./LUNA_SOURCE_VALIDATION_V2_AFTER_EP_V3.md)（Source Validation v2 dry-run）
- `Semantic-Candidate-v3-Review-Policy`
