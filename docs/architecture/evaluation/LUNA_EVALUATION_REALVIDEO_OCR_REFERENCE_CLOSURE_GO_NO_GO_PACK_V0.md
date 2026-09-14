# Luna — RealVideo OCR Reference Closure GO/NO_GO Pack v0

## GO

- RealVideo OCR reference 链完整 closure
- 10 条 evidence lineage 完整；rejected ROI / empty text / case mapping / no-write boundary 完整
- `verifier=GO`（含非空 OCR 文本时）

## CONDITIONAL_GO

- 10 条 evidence 全为 empty text，但 lineage / reference / guard / audit 完整
- 无越界行为；`verifier=CONDITIONAL_GO`

## NO_GO

- 重新运行 OCR；把 `empty_text` 当事实；fusion / Scene Delta candidate
- 写事实层；benchmark 或 provider 比较宣称；改 routing；audit 缺失
