# Luna — ROI OCR Quality Diagnosis GO/NO_GO Pack v0

## GO

- 12 链路进入诊断；`repeated_text_ratio=1.0`；`crop_diversity_low=true`；`source_frame_reuse_risk=true`
- `root_cause_confirmed=false`；10 条 hypothesis（high/medium）；`boundary_ok=true`；`verifier=GO`

## CONDITIONAL_GO

- 输入数量与上游一致但不是 12；部分诊断 defer 原因明确

## NO_GO

- 执行 OCR / 新 crop / 新帧；root cause 标 confirmed；provider 失败 claim；写 fact/WM
