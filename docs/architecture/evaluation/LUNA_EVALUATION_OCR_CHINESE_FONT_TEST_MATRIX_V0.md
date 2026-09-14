# LUNA Evaluation Tools — OCR Chinese Font Test Matrix v0 (Phase-EvaluationTools-OCR-002)

## Probe

- `probe_text`: `上海地铁9号线防范电信网络诈骗`
- glyph diversity probe: `"中"` vs `"海"`

## Pass criteria (v0)

- Pillow 可加载（truetype 不报错）
- `"中"` 与 `"海"` 渲染 mask **不完全相同**
- `ink_ratio >= 0.002`

## Expected outputs

- `chinese_font_visibility_report.json` 记录 `ink_ratio`、`tofu_suspected`、`validation_result`
- `chinese_font_probe_images/probe_text.png` 用于人工抽查

