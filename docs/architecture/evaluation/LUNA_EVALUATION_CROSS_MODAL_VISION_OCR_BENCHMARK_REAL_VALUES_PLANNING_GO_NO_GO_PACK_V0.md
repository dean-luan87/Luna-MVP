# Benchmark Collector Real Values Planning — GO / NO_GO Pack v0

## GO

- `planning_scope=benchmark_real_values_planning_only`
- T0/T1/T2 指标分层完整；`no_write_boundary_pass_rate` 在 T0
- source map / gate / interpretation / ground truth / simulation binding / output contract 完整
- `real_values_collection_allowed=false`；无 benchmark / provider comparison / model selection 主张
- regression link：`v1_track_closures_status=closed_for_evaluation`，`regression_all_boundary_ok=true`
- audit 全 no-write / no-OCR；verifier **GO**

## CONDITIONAL_GO

- 部分 future source 细节待补，但 T0/T1/T2、gate、non-claims、audit 完整且无越界

## NO_GO

- 运行 OCR / Vision；采集 benchmark values；生成 benchmark claim；比较 provider；写事实层；改 routing

## 下一 phase

**Phase-PublicFacility-Runtime-DryRun-001**（推荐优先于 RealVideo OCRRequest gated submission）。
