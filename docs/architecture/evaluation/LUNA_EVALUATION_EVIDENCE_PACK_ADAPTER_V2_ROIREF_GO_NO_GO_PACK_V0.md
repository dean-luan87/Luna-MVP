# Luna — Evidence Pack Adapter v2 ROIRef GO/NO_GO Pack v0

## GO

- 12 ROI OCR result → 12 Evidence Pack v2；refs/bbox/confidence/provider metadata 全保留
- `repeated_same_text` / `low_information_text` 风险已标记；`boundary_ok=true`；`verifier=GO`

## CONDITIONAL_GO

- result 数与 smoke 不一致但 pack 与 eligible 对齐；text_items 缺字段但 `missing_fields` 已记录

## NO_GO

- raw OCR 被覆盖；ocrrequest/crop ref 丢失；重复/低信息未标风险
- 生成 Semantic Candidate；写 fact/WM；benchmark/provider claim；改 routing
