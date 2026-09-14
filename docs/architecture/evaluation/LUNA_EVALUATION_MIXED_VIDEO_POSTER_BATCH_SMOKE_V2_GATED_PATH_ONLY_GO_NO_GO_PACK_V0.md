# Luna — Mixed Batch v2 Gated Path Only GO/NO_GO Pack v0

## GO

- capability 不 import RapidOCR；`direct_provider_bypass=false`
- provider 调用均有 `ocr_request_ref`；Evidence Pack 均有 `ocr_request_ref`
- 全帧 scan 非主 evidence；`sq_e_submitted_to_ocr=false`
- no-write boundary 通过；`verifier=GO`

## CONDITIONAL_GO

- gate 较严导致 `provider_call_count` 较少，但路径约束完整
- 部分视频/图片缺失，P0 + 主要 fixtures 仍有效

## NO_GO

- capability 仍直连 RapidOCR
- Pack 无 OCRRequest ref；全帧当主 evidence
- SQ_E 进入 OCR evidence；写 fact/WM/Scene Delta；改 routing
