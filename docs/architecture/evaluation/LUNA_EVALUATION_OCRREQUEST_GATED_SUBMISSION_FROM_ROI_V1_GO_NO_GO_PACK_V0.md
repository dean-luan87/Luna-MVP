# Luna — OCRRequest Gated Submission from ROI GO/NO_GO Pack v0

## GO

- 12 reference intake → 12 gated submission；`direct_provider_bypass=false`
- 每次 bridge 调用带 `ocrrequest_reference_id`；`roi_ocr_result_collection` 生成
- 不生成 Evidence Pack / Semantic Candidate；`boundary_ok=true`；`verifier=GO`

## CONDITIONAL_GO

- reference 数与 smoke 不一致但 trace/boundary 完整；部分 `provider_error` 无越界

## NO_GO

- direct provider bypass；无 ocrrequest_ref；full-frame / mock text
- Evidence Pack / Semantic Candidate / 写 fact / WM / SceneDelta
- benchmark 或 provider 优劣 claim；改 routing；audit 缺失
