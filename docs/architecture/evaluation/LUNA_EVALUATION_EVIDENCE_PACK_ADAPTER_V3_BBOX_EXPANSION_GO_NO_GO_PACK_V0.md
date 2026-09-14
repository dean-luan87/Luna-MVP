# Luna — Evidence Pack Adapter v3 BBoxExpansion GO/NO_GO Pack v0

## GO

- 4 expanded ROI OCR result v2 → 4 EP v3；`one_to_one_mapping=true`
- `raw_ocr_text` / `text_items` / v2 refs / strategy / 双 bbox / provider metadata 全保留
- `strategy_comparison_candidate_only=true`；`padding_medium` 与 `contextual_expand` 重复标记 `repeated_with_other_strategy`
- 不生成 Semantic Candidate；不执行 Source Validation v2；`boundary_ok=true`；`verifier=GO`

## CONDITIONAL_GO

- result 数与 smoke 不一致但 alignment/boundary 完整；部分 text_items 缺字段但已记录 `missing_fields`

## NO_GO

- raw OCR 被覆盖；strategy 或 bbox ref 丢失；生成 Semantic / 执行 SV v2 / 写事实层；benchmark 或 provider 优劣 claim；改 routing；audit 缺失
