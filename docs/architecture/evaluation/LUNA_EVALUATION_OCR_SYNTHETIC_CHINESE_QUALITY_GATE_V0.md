# LUNA Evaluation Tools — OCR Synthetic Chinese Quality Gate v0 (Phase-EvaluationTools-OCR-002)

## Goal

在不调用 OCR provider 的前提下，对中文 synthetic 子集执行数据集质量门控：

- 中文字体 **可见性通过**
- ground truth 与 manifest **一致**
- 样本资产（图片/gt/sha256/尺寸）**完整**

## Hard boundaries

- Evaluation Tools only；不接入 runtime / whitebox。
- 不调用 OCR provider。
- 不进入 MidPlatform / SceneDelta / WorldContextEvidence / semantic / 语音链路。

## Dataset (quality gate subset)

建议固定小规模子集（默认 50）：

- `zh_plain_text_quality_gate`：20
- `mixed_zh_en_digit_quality_gate`：20
- `digits_with_chinese_context`：10

## Verifier

`tools/evaluation/ocr/verify_ocr_chinese_font_quality_gate_dataset_v0.py`：

- 样本数量与类别覆盖
- 每行 manifest 的 `image_path` / `ground_truth_path` 存在
- `ground_truth_text` 与 gt 文件内容一致
- `sha256` / `font_id` / `font_path` 存在
- `visible_cjk_passed=true` 且 `tofu_suspected=false`

## Output artifacts

Dataset root（`--output-root`）：

- `manifest.jsonl`
- `dataset_summary.json`
- `font_registry.json`（可选）
- `font_selection_report.json`（可选）
- `font_visibility_report.json`
- `images/`
- `ground_truth/`
- `font_probe/`
- `quality_gate_notes.md`
- `verifier_report.json`

