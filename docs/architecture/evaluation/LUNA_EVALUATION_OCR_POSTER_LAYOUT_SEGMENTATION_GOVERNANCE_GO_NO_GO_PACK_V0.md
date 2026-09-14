# Luna — GO/NO_GO: OCR Poster Layout Segmentation Governance v0

**Phase**：`Phase-OCR-Poster-Layout-Segmentation-Governance-001`

## GO

- `full_image_ocr_allowed=false`，`ocr_strategy=segment_first`
- text / non-text / visual-symbol 分流完整；`ocr_region_plan` 仅含 text regions
- logo/qr `ocr_allowed=false`；audit 无 OCR/Vision/写入

## CONDITIONAL_GO

- synthetic fixture 缺非关键装饰区，但 gate/audit 完整；无越界

## NO_GO

- 默认整图 OCR；logo/qr 进普通 OCR；运行真实 OCR；写事实层；缺 gate/audit
