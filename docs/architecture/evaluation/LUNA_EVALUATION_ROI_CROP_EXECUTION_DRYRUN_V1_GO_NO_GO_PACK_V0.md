# Luna — ROI Crop Execution DryRun v1 GO/NO_GO Pack v0

## GO

- 27 proposal 全部 intake；crop artifact / deferred 记录完整
- `crop_execution_attempted=true`；`ocr_request_generated=false`；`boundary_ok=true`；`verifier=GO`

## CONDITIONAL_GO

- 无实际 PNG（`crop_executed_count=0`），但 defer 原因明确（SQ_E / null bbox / better_frame）
- `crop_executed_count < proposal_count` 且 bbox 校验与 source resolution 完整

## NO_GO

- 调用 OCR / provider；生成 OCRRequest / Evidence Pack；写 fact/WM/Scene Delta
- benchmark/provider comparison claim；改 routing；audit 缺失
