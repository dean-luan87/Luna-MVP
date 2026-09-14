# Luna — OCRRequest Gated Submission from ROI v2 BBoxExpansion GO/NO_GO Pack v0

## GO

- 4 reference v2 intake → 4 gated submission；`direct_provider_bypass=false`
- 每次 bridge 调用带 `ocrrequest_reference_v2_id`；`expanded_roi_ocr_result_collection_v2` 生成
- 保留 `expansion_strategy`；strategy comparison `comparison_candidate_only=true`
- 不生成 Evidence Pack v3 / Semantic Candidate v3 / Source Validation v2；`boundary_ok=true`；`verifier=GO`

## CONDITIONAL_GO

- reference 数与 smoke 不一致但 trace/boundary 完整；部分 `provider_error` 无越界

## NO_GO

- direct provider bypass；无 `ocrrequest_reference_v2_id`；full-frame / mock text
- Evidence Pack v3 / Semantic Candidate v3 / Source Validation v2 / 写 fact / WM / SceneDelta
- benchmark 或 provider 优劣 claim；改 routing；audit 缺失
