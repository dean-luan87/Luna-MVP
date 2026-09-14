# LUNA Evaluation Tools — Evaluation Report Schema v0 (Phase-EvaluationTools-Foundation-001)

## Purpose

统一所有 Evaluation Tools 输出报告的最小 schema，保证：

- **可审计**（边界字段显式）
- **可对比**（provider/dataset/metrics 结构一致）
- **不可误接入主线**（runtime/whitebox/mainline_side_effect 必须为 false）

## Schema (JSON)

字段：

- `evaluation_id`: string
- `evaluation_type`: `ocr_provider_eval | dataset_quality_gate | provider_ab_test | stress_test | chain_test`
- `module`: string（例如 `"ocr"`）
- `provider`: string|null
- `dataset_ref`: string|null
- `sample_count`: int
- `metrics`: object
- `failure_cases_ref`: string|null
- `human_review_ref`: string|null
- `recommendation`: `pass | weak_pass | repeat | fail | needs_manual_review`
- `runtime_integration`: false（必须）
- `whitebox_integration`: false（必须）
- `mainline_side_effect`: false（必须）
- `created_at`: ISO-8601 UTC（带 `Z`）

对应实现：

- `capabilities/evaluation/common/evaluation_report_schema_v0.py`
- `tools/evaluation/common/verify_evaluation_report_schema_v0.py`

