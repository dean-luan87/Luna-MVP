# Luna — Source Validation v2 after EP v3 GO/NO_GO Pack v0

## GO

- 4 Semantic v3 → 4 validation dry-run；`source_validation_passed_count=0`
- same-frame consensus blocked；strategy repeat 非共识；noisy segment 阻断实体确认
- external support missing 已记录；`boundary_ok=true`；`verifier=GO`

## CONDITIONAL_GO

- candidate 数与输入不一致但 defer/block 原因明确；无越界行为

## NO_GO

- `validation_passed_count>0`；确认实体；调用地图/VSR/LLM/OCR
- 写 fact/WM/SceneDelta；benchmark claim；改 routing
