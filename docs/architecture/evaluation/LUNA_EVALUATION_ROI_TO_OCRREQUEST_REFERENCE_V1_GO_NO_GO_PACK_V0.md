# Luna — ROI to OCRRequest Reference GO/NO_GO Pack v0

## GO

- 12 generated crop → 12 OCRRequest reference；`ocrrequest_submitted=false`；`provider_invoked=false`
- excluded report 记录 `future_detector_deferred_count=8`、`multiframe_deferred_count=7`
- `boundary_ok=true`；`verifier=GO`

## CONDITIONAL_GO

- generated crop 数量与 smoke 不一致，但 reference 数与 eligible crop 一致；无越界行为

## NO_GO

- 提交 OCRRequest；调用 OCR provider；生成 Evidence Pack / Semantic Candidate
- 写 fact / WorldModel attach / Scene Delta；benchmark 或 provider 优劣 claim
- 改 routing；audit 缺失
