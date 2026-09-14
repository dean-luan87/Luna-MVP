# GO / NO-GO Pack — OCR Regression Route Compliance v1

## GO

- 五条路线均已 checked（RealVideo / Poster / StaticReading / Memory / Hardware）
- `blocked_ocrrequest_candidate_count=34`，`capture_status=not_captured`
- 无 provider bypass；无 WM/SceneDelta 写入；`boundary_ok=true`
- `regression_runtime_executed=false`
- Verifier `verdict=GO`（允许 `REGRESSION_ROUTE_COMPLIANCE_PASS` 或 `CONDITIONAL_PASS`）

## CONDITIONAL_GO

- 可选 root 缺失（如 `cross_modal_vision_ocr_testboard_metrics_schema_v0`）
- `final_decision=REGRESSION_ROUTE_COMPLIANCE_CONDITIONAL_PASS`
- 关键 closure / staticreading / memory / hardware root 必须完整

## NO_GO

- 关键 root 缺失；或 OCR/provider 被调用；或 OCRRequest 提交；或 EP v5 / Memory / WM 写入
- StaticReading gate 被绕过；Poster full-image OCR 放行

## 非宣称

- 回归通过 ≠ production ready；路线合规 ≠ 识别准确率
