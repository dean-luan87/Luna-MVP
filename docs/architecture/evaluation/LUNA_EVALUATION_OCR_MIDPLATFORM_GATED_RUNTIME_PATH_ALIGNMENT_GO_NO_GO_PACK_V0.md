# Luna — OCR MidPlatform Gated Runtime Path GO/NO_GO Pack v0

## GO

- `direct_provider_bypass=false`
- 所有 bridge provider 调用有 `ocr_request_ref`
- 所有 Evidence Pack 有 `ocr_request_ref`；无 full-frame 主证据
- SQ gate / readability gate 在 OCRRequest 之前执行
- SQ_E 未提交 OCR；SQ_D 走 visual symbol 路径
- no-write boundary 通过；`verifier=GO`

## CONDITIONAL_GO

- 部分 submission `provider_unavailable`，但路径约束完整
- 无 direct bypass、无 SQ_E 越权

## NO_GO

- harness 仍直接 RapidOCR 作主路径
- Pack 无 OCRRequest ref
- SQ_E 进入 gated OCR evidence
- full-frame 当主证据
- 写 fact / WM / Scene Delta / 改 routing
