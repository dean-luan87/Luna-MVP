# Luna — OCR TTL Gate v1

**Phase**：`Phase-OCR-TTL-Gate-v1-001`

## 目的

消费 Review Queue Runtime 中 **`ttl_review_queue`** 项，对商业/促销/时间类 OCR 语义候选执行 **TTL gate dry-run**：

- 输出 `ttl_gate_status` / `hold_reason` / `required_next_action`
- **不批准**、不提交 decision、不写 fact/WM/Scene Delta

## 边界

- 仅 `ttl_review_queue`；不重新运行 OCR
- `ttl_gate_passed_count=0`（本阶段不得放行到事实链）

## 实现

- `capabilities/midplatform/ocr_ttl_gate_v1.py`
- `tools/evaluation/midplatform/run_ocr_ttl_gate_v1.py`
- `tools/evaluation/midplatform/verify_ocr_ttl_gate_v1.py`

## 前置

- [LUNA_OCR_REVIEW_QUEUE_RUNTIME_DRYRUN_V1.md](./LUNA_OCR_REVIEW_QUEUE_RUNTIME_DRYRUN_V1.md)

## 后续

**Source Validation DryRun v1**（见 [LUNA_OCR_SOURCE_VALIDATION_DRYRUN_V1.md](./LUNA_OCR_SOURCE_VALIDATION_DRYRUN_V1.md)）承接 TTL hold 项的来源验证规划。

## 评测

[LUNA_EVALUATION_OCR_TTL_GATE_V1.md](../evaluation/LUNA_EVALUATION_OCR_TTL_GATE_V1.md)
