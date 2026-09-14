# Luna — MixedVideo OCR Scan LineBox Trace + Source Quality Gate GO/NO_GO Pack v0

## GO

- P0 入选 10 帧均有 linebox trace **或** 完整 `missing_reason`
- Source Quality Gate policy（SQ_A–E）完整
- scan vs pack consistency、full-frame OCR risk、ROI crop requirement、scan observation vs evidence 政策齐全
- no-write boundary `boundary_ok=true`；`verifier=GO`

## CONDITIONAL_GO

- 部分帧无法拿到 linebox，但 `missing_reason` 完整
- 无越界行为（无 fact / WM / routing / benchmark claim）

## NO_GO

- 无 linebox trace 且无 `missing_reason`
- 无 source quality gate
- 继续把 full-frame `ocr_preview` 当主 evidence
- 写事实层 / WorldModel attach / Scene Delta / benchmark 或 provider 比较 claim / 改 routing
- audit 缺失
