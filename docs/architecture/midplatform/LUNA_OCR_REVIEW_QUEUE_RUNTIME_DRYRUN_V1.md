# Luna — OCR Review Queue Runtime DryRun v1

**Phase**：`Phase-OCR-Review-Queue-Runtime-DryRun-v1-001`

## 目的

将 Review Policy v1 的 **47 个 review_queue_candidate** 接入最小 **Review Queue Runtime** dry-run：

- 模拟入队、分类、优先级排序、状态流转、出队
- 输出 runtime trace 与 decision placeholder
- **不提交** decision、不批准、不写 fact/WM/Scene Delta

## 边界

- 只消费 `review_queue_candidate`；不重新解释 OCR
- 不运行 LLM/VLM；不改 runtime routing

## 实现

- `capabilities/midplatform/ocr_review_queue_runtime_dryrun_v1.py`
- `tools/evaluation/midplatform/run_ocr_review_queue_runtime_dryrun_v1.py`
- `tools/evaluation/midplatform/verify_ocr_review_queue_runtime_dryrun_v1.py`

## 前置

- [LUNA_OCR_SEMANTIC_CANDIDATE_REVIEW_POLICY_V1.md](./LUNA_OCR_SEMANTIC_CANDIDATE_REVIEW_POLICY_V1.md)

## 后续

**TTL Gate v1**（见 [LUNA_OCR_TTL_GATE_V1.md](./LUNA_OCR_TTL_GATE_V1.md)）处理 `ttl_review_queue` 分支。

## 评测

[LUNA_EVALUATION_OCR_REVIEW_QUEUE_RUNTIME_DRYRUN_V1.md](../evaluation/LUNA_EVALUATION_OCR_REVIEW_QUEUE_RUNTIME_DRYRUN_V1.md)
