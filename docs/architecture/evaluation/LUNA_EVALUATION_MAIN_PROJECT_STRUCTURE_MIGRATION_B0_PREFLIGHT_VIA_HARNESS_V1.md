# Luna Evaluation — Main Project Structure Migration B0 Preflight Via Harness v1

## 目标

- 使用已固化的 reusable Batch Preflight Harness contract，对 B0 `batch_config` 执行一次 **实际 preflight**
- 输出 `preflight_result` 与全部 fixed check results
- 同步输出 Migration Refactor Opportunity Scan（仅候选，不 runtime refactor）

## 成功条件（GO）

- reusable contract closure 上游 GO 且 `boundary_ok=true`
- B0 batch_config instance 合法（scope / domain / guards / ops / manifest / rollback / rerun / tests / abort / workspace_fallback / non_claims）
- 全部 fixed checks pass
- `migration_refactor_opportunity_scan` pass 且 `extract_now_allowed=false`、`runtime_refactor_executed_now=false`
- B1–B7 未进入 preflight / adoption / execution
- 所有 file-op / arming / execution 边界为 false

## 输出目录

- `_eval_out/main_project_structure_migration_b0_preflight_via_harness_v1_smoke_v0/`
