# RealVideo ROI-to-OCR Reference — GO / NO_GO Pack v0

## GO

- `reference_scope=reference_only`；frame-to-ROI ≥1 行；OCRRequest 矩阵全部 `submission_status=not_submitted`
- case mapping 全部 `reference_mapping_only`；`should_write_fact=false`
- poster_track_b_closed；no-write boundary 通过；verifier **GO**

## CONDITIONAL_GO

- facility case 无 sample mapping，但 governance/boundary/audit 完整

## NO_GO

- 提交 OCRRequest 或运行 OCR/Vision
- 生成 evidence / fusion / Scene Delta
- 写事实或改 routing

## 下一 phase

`Phase-CrossModal-Vision-OCR-TestBoard-v1-Regression-Comparison-001`
