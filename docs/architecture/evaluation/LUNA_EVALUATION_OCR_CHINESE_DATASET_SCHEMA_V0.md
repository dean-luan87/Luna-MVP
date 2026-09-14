# LUNA Evaluation Tools — OCR Chinese Dataset Schema v0 (Phase-EvaluationTools-OCR-002)

## Manifest schema (JSONL; one sample per line)

字段（v0）：

- `sample_id`: string
- `image_path`: string (absolute path)
- `ground_truth_path`: string (absolute path)
- `ground_truth_text`: string
- `language`: `"zh" | "mixed" | "en"`
- `category`: string
- `font_id`: string
- `font_path`: string (absolute path)
- `font_validation_ref`: string|null
- `sha256`: string
- `width`: int
- `height`: int
- `visible_cjk_passed`: bool
- `tofu_suspected`: bool

约束：

- 必须保证 `ground_truth_text` 与 `ground_truth_path` 文件内容一致
- 中文相关样本必须 `visible_cjk_passed=true` 且 `tofu_suspected=false`
- 本数据集用于 Evaluation Tools；不得成为 runtime 依赖

