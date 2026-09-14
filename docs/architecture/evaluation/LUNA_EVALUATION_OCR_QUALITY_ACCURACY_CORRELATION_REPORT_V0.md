# LUNA Evaluation Tools — OCR Quality × Accuracy Correlation Report v0 (Phase-EvaluationTools-OCR-005)

## Purpose

在不重新调用 OCR provider 的前提下，把：

- OCR-003（识别效果：CER/中文召回/空串率/乱码率/失败分类）
- OCR-004（输入质量：分辨率/模糊/对比度/曝光/文字尺度/倾斜/文本占比…）

按 `sample_id` 对齐合并，输出 **可解释** 的相关性与分桶报告，用于回答工程问题：

- 输入质量差时 CER 是否变差？
- 哪些样本是 input_quality_risk 但 OCR 仍好？
- 哪些是 good_input 但 OCR 坏（可能是 provider/模型/布局问题）？

## Hard boundaries

- Evaluation Tools only；不接入 runtime / whitebox
- 不调用 OCR provider（merge-only）
- 不修改 ground truth
- 不影响主线 provider 决策

## Inputs

- `--accuracy-root`：OCR-003 输出根（含 `rapidocr_chinese_sample_eval_matrix.json`）
- `--quality-root`：OCR-004 输出根（含 `ocr_input_quality_image_matrix.jsonl`）

## Outputs

- `ocr_quality_accuracy_merge_summary.json`
- `ocr_quality_accuracy_sample_matrix.json`
- `ocr_quality_bucket_report.json`
- `ocr_quality_metric_correlation_report.json`
- `ocr_provider_vs_input_failure_report.json`
- `ocr_quality_accuracy_trace.jsonl`
- `ocr_quality_accuracy_replay.jsonl`
- `merge_notes.md`

