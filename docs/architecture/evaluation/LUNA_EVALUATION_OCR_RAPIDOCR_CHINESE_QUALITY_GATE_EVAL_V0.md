# LUNA Evaluation Tools — RapidOCR Chinese Quality Gate Evaluation v0 (Phase-EvaluationTools-OCR-003)

## Purpose

在 **已通过中文字体可见性/数据集质量门控** 的前提下，离线评估 RapidOCR 对中文样本的真实识别表现：

- CER
- 中文字符召回率
- 空串率
- 乱码率
- failure cases 分类与归档

## Hard boundaries

- Evaluation Tools only；不接入 runtime / whitebox
- 不修改 ground truth
- 不影响主线 OCR provider 决策
- 不进入 MidPlatform / SceneDelta / WorldContextEvidence / semantic / 语音链路

## Inputs

- `--dataset-root`: 中文质量门控数据集（manifest.jsonl）
- `--cross-validation-root`:（可选）OCR-002 cross validation 输出，仅作为引用

## Outputs (v0)

写入 `--output-root`：

- `rapidocr_chinese_quality_eval_summary.json`
- `rapidocr_chinese_sample_eval_matrix.json`
- `rapidocr_chinese_cer_summary.json`
- `rapidocr_chinese_recall_summary.json`
- `rapidocr_chinese_empty_output_report.json`
- `rapidocr_chinese_garbled_report.json`
- `rapidocr_chinese_failure_cases.json`
- `rapidocr_chinese_eval_trace.jsonl`
- `rapidocr_chinese_eval_replay.jsonl`
- `rapidocr_chinese_eval_whitebox.jsonl`（evaluation-only 审计）
- `rapidocr_chinese_eval_notes.md`

## Case taxonomy (v0)

- `provider_fail`
- `font_visible_but_ocr_empty`
- `low_recall`
- `garbled_output`
- `acceptable_output`

