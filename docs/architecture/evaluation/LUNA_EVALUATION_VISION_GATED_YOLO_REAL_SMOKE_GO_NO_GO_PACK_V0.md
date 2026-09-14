# Luna Evaluation — Gated YOLO Real Smoke GO / NO_GO Pack v0

## GO

- gate：`eval_only` + `eval_provider_enabled`；`network_request_invoked=false`
- `real_detector_invoked=true`，`fixture_used=false`，`converted_evidence_count>0`
- 全部 evidence：`fact_status=not_fact`；真实路径 `synthetic=false`

## CONDITIONAL_GO

- 本地模型不可用或回退 fixture；probe/gap 完整；无越界

## NO_GO

- 触网下载；改 registry；整帧；标 fact；写事实层；导航；`fixture_used` 却判 GO
