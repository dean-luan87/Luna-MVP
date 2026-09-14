# LUNA Evaluation Tools — Human Review Package v0 (Phase-EvaluationTools-Foundation-001)

## Purpose

为人工快速复核提供统一产物格式：

- contact sheet（样本缩略图 + sample_id + ground truth）
- review index（JSON，便于检索与对照）
- annotations template（标注模板，便于回写人工判断）

## Outputs

`capabilities/evaluation/ocr/ocr_human_review_package_v0.py` 生成：

- `human_review_contact_sheet.png`
- `human_review_index.json`
- `review_annotations_template.json`

## Non-goals / boundary

- 不执行 OCR provider
- 不接 runtime / whitebox
- 不自动写主线决策

