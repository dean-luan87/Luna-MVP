# Luna — OCR Semantic Candidate Review Policy v1

**Phase**：`Phase-OCR-Semantic-Candidate-Review-Policy-v1-001`

## 目的

消费 **Semantic Candidate v1** 四类产物，定义 **review policy / queue candidate / next-action routing**：

- TTL review、source validation、VisualSymbolRegistry、ROI retry、better source、unresolved slot later、hold

## 边界

- 仅 policy；**不提交** review decision、不批准、不写 fact/WM/Scene Delta
- 不运行 OCR / LLM / VLM；不改 runtime routing

## 实现

- `capabilities/midplatform/ocr_semantic_candidate_review_policy_v1.py`
- `tools/evaluation/midplatform/run_ocr_semantic_candidate_review_policy_v1.py`
- `tools/evaluation/midplatform/verify_ocr_semantic_candidate_review_policy_v1.py`

## 前置

- [LUNA_OCR_SEMANTIC_CANDIDATE_GENERATOR_V1.md](./LUNA_OCR_SEMANTIC_CANDIDATE_GENERATOR_V1.md)

## 后续

**Review Queue Runtime DryRun v1**（见 [LUNA_OCR_REVIEW_QUEUE_RUNTIME_DRYRUN_V1.md](./LUNA_OCR_REVIEW_QUEUE_RUNTIME_DRYRUN_V1.md)）将 queue candidate 接入最小 runtime 模拟。

## 评测

[LUNA_EVALUATION_OCR_SEMANTIC_CANDIDATE_REVIEW_POLICY_V1.md](../evaluation/LUNA_EVALUATION_OCR_SEMANTIC_CANDIDATE_REVIEW_POLICY_V1.md)
