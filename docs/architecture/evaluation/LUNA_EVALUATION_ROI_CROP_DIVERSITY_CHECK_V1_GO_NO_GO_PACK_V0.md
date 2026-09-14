# Luna — ROI Crop Diversity Check GO/NO_GO Pack v0

## GO

- 12 链路进入 diversity intake；`unique_bbox_count=1`；`unique_frame_count=1`；`crop_diversity_low=true`
- `linebox_reuse_risk=true`；`many_proposals_to_one_bbox/frame=true`；combined duplicate group 存在
- `quality_claim_allowed=false`；`blocked_source_validation_v2=true`；`root_cause_confirmed=false`
- `boundary_ok=true`；`verifier=GO`

## CONDITIONAL_GO

- 输入数量与上游一致但不是 12；部分 diversity 字段缺失但 defer 原因明确

## NO_GO

- 执行 OCR / 新 crop / 新帧；Source Validation v2 被执行；quality claim 或 fact 写入
- WorldModel attach / SceneDelta；benchmark/provider comparison claim；改 routing
