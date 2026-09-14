# Luna — GO/NO_GO: CrossModal Vision OCR TestBoard Metrics Schema v0

**Phase**：`Phase-CrossModal-Vision-OCR-TestBoard-Metrics-Schema-001`

## GO

- `metrics_scope=schema_only`；七组指标完整；definition matrix / source map / gate / non-claims / collector stub 完整
- poster governance 已映射；`benchmark_claim_allowed=false`；audit 无 OCR/写入

## CONDITIONAL_GO

- 非关键指标定义缺失，但 boundary / gate / source map 完整；无越界

## NO_GO

- 运行 OCR/Vision；生成 benchmark 结论；指标用于自动批准；缺 Poster/Boundary 组；缺 audit
