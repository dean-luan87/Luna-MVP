# Luna — OCR Evidence Pack Adapter Update GO/NO_GO Pack v0

## GO

- Poster 4 + RealVideo 10 条 evidence 均适配为 `OCRTextEvidencePack v0`
- 坐标/时空/可读性/`source_chain`/`evidence_status` 字段齐全
- raw OCR preservation 完整；semantic / WM attach 仅 placeholder
- `no-write boundary` 通过；`verifier=GO`

## CONDITIONAL_GO

- 坐标字段存在但大量 `null`，且明确无伪造（`coordinate_fabrication_detected=false`）
- 无越界行为

## NO_GO

- 重新运行 OCR；修改 raw OCR；运行语义模型；执行 WorldModel attach
- 生成 Scene Delta candidate；写事实层；benchmark/provider comparison claim；改 routing；audit 缺失
