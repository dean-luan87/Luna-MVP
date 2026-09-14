# CrossModal Poster OCR ReferenceOnly — GO / NO-GO Pack v0

## GO

- 全部 reference-only 产物齐全；`reference_scope=reference_only`
- text / visual 各 4 行；`overlap_count=0`；无污染
- simulation `developer_full` + `run_model=false`
- audit 无越界；verifier **GO**

## CONDITIONAL_GO

- simulation context 缺失但 reference/gate/audit 完整
- metrics collector 仅为 bootstrap stub

## NO_GO

- 运行 OCR / QR / 品牌确认；track 混淆；semantic join；写事实层；改 routing
