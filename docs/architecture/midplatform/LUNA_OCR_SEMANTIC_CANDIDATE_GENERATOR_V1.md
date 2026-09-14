# Luna — OCR Semantic Candidate Generator v1

**Phase**：`Phase-OCR-Semantic-Candidate-Generator-v1-001`

## 目的

基于 **Evidence Pack Adapter v1** 的 `evidence_tier` 生成 **OCRSemanticCandidate v1**，按 tier 分流：

| evidence_tier | 输出 |
|---------------|------|
| `gated_ocr_primary` | 主 OCRSemanticCandidate v1 |
| `scan_observation_only` | `scan_observation_semantic_hint`（非主候选） |
| `visual_symbol_route` | VisualSymbol / BrandSymbol 路由（非普通文字） |
| `sq_e_blocked` | `blocked_unreadable_or_low_quality`（无强语义） |

## 边界

- 不运行 OCR / RapidOCR / PaddleOCR
- 不运行 LLM / VLM / 语义模型
- 不执行 WorldModel attach；不写 fact / WM / Scene Delta
- 不改 runtime routing

## 实现

- `capabilities/midplatform/ocr_semantic_candidate_generator_v1.py`
- `tools/evaluation/midplatform/run_ocr_semantic_candidate_generator_v1.py`
- `tools/evaluation/midplatform/verify_ocr_semantic_candidate_generator_v1.py`

## 前置

- [LUNA_OCR_EVIDENCE_PACK_ADAPTER_V1_SCAN_OBSERVATION_ALIGNMENT_V0.md](./LUNA_OCR_EVIDENCE_PACK_ADAPTER_V1_SCAN_OBSERVATION_ALIGNMENT_V0.md)
- Mixed Batch v2 gated-only smoke

## 后续

**Review Policy v1**（见 [LUNA_OCR_SEMANTIC_CANDIDATE_REVIEW_POLICY_V1.md](./LUNA_OCR_SEMANTIC_CANDIDATE_REVIEW_POLICY_V1.md)）定义 TTL / validation / registry / retry 等 next-action，不提交 decision。

## 评测

[LUNA_EVALUATION_OCR_SEMANTIC_CANDIDATE_GENERATOR_V1.md](../evaluation/LUNA_EVALUATION_OCR_SEMANTIC_CANDIDATE_GENERATOR_V1.md)
