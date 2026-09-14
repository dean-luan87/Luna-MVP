# Luna — Poster Real OCR ReadOnly Consumer GO/NO_GO Pack v0

## GO

- `poster_layout_text_evidence_candidate` 只读消费成功
- 4 region view / matrix / index 完整
- TTL / reading-order / visual separation guard 完整
- `no-write boundary` 通过；`verifier=GO`

## CONDITIONAL_GO

- 部分 region `empty_text=true`，但 consumer / guard / audit 完整
- 无越界行为

## NO_GO

- 重新运行 OCR；semantic join
- 将 visual symbol 当普通 OCR 文本消费
- 写事实层；生成 fusion / Scene Delta candidate
- benchmark 或 provider 比较宣称；改 routing；audit 缺失
