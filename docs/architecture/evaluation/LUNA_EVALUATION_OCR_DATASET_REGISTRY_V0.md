# LUNA Evaluation Tools — OCR Dataset Registry v0 (Phase-EvaluationTools-Foundation-001)

## Purpose

登记 synthetic / real-world / human-reviewed 数据集的 **evaluation-only** 元信息：

- 统一 dataset_id 与类型
- 说明 gt 质量与语言覆盖
- 标记 intended_use（provider_eval/layout_eval/stress/regression/quality_gate）
- 明确 `runtime_allowed=false`（硬边界）

## Schema (entry)

参见 `capabilities/evaluation/ocr/ocr_dataset_registry_v0.py`：

- `dataset_id`
- `dataset_type`
- `root`
- `sample_count`
- `has_ground_truth`
- `ground_truth_quality`
- `language_coverage`
- `sample_categories`
- `intended_use`
- `runtime_allowed`（必须为 false）

