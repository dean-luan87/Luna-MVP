# Luna — Poster Real OCR Gated Execution GO/NO_GO Pack v0

## GO

- 4 个 text regions 的 gated execution plan 完整
- visual regions 全部排除（guard `all_visual_regions_absent_from_ocr_execution_plan=true`）
- RapidOCR 可用时：real OCR smoke 成功，结果矩阵与 evidence candidate 生成
- `no-write boundary` 通过；`verifier=GO`

## CONDITIONAL_GO

- `provider_unavailable` 但 plan / guard / boundary / audit 完整
- 无 MOCK_TEXT 冒充；无越界行为

## NO_GO

- 整图 OCR；OCR logo/QR/product/background
- QR 解码；品牌确认；VisualSymbolRegistry
- MOCK_TEXT 冒充 real OCR
- semantic join / 写事实层 / benchmark 或 provider 比较宣称
- 改 routing；audit 缺失
