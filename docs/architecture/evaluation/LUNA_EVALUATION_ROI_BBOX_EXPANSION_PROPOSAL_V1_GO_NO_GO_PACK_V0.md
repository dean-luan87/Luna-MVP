# Luna — ROI BBox Expansion Proposal GO/NO_GO Pack v0

## GO

- 12 链路进入 expansion planning；1 个 canonical source bbox group（member_count=12）
- 至少 4 类 expansion candidates；原 bbox 保留；bounds check 完整
- `new_crop_generated=false`；`new_ocr_invoked=false`；`boundary_ok=true`；`verifier=GO`

## CONDITIONAL_GO

- frame bounds 缺失导致部分 candidate deferred；候选数少于预期但原因明确

## NO_GO

- 覆盖原 bbox；生成新 crop；执行 OCR；写 fact/WM；改 routing
