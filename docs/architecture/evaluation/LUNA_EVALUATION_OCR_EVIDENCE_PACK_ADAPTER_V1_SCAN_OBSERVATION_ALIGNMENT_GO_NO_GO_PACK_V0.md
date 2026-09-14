# Luna — Evidence Pack Adapter v1 Scan Observation Alignment GO/NO_GO Pack v0

## GO

- v2 gated packs 升级为 `ocr_text_evidence_pack_v1`
- 全部 gated pack 含 `ocr_request_ref` + `gated_path_ref` + SQ/readability refs
- scan sidecar 明确非主 evidence；hierarchy / semantic readiness 完整
- no-write boundary；`verifier=GO`

## CONDITIONAL_GO

- gated pack 数量少但字段覆盖完整

## NO_GO

- gated pack 缺 `ocr_request_ref`
- scan sidecar 被标为主 OCRTextEvidence
- 运行 OCR / 写 fact / WM
