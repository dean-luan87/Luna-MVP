# LUNA Evaluation Tools — OCR Distortion Prevention Rules v0 (Phase-EvaluationTools-OCR-007)

## 报告文件

- `ocr_distortion_prevention_report.json`

## `rules_checked`（v0）

| 规则 id | v0 检查内容 |
|---------|-------------|
| `non_ocr_not_fact_text` | `non_ocr_content_types` 不得出现在 `eligible_text_evidence` |
| `symbol_glyph_not_raw_text_fact` | 符号/艺术字/混排等 symbol-glyph-like 类型不得进入 `eligible_text_evidence` |
| `reading_order_uncertain_not_global_fact` | 若 sample 提供 `reading_order_uncertain=true`，该 `case_id` 不得进入 `eligible_text_evidence` |
| `multi_panel_not_cross_joined` | `multi_panel_layout` 不得进入 `eligible_text_evidence` |
| `low_quality_requires_uncertainty` | `input_quality_gate=NO_GO` 不得进入 eligible；`CONDITIONAL_GO` 且路由为 eligible 时必须带 `eligible_but_quality_conditional` 等不确定性说明 |

## `distortion_prevention_passed`

- `violations` 为空时为 `true`。
