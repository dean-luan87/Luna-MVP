## Phase

- **Phase ID**: `Phase-Main-Project-Structure-Migration-Controlled-Batch-Execution-Authorization-Planning-v1-001`
- **Capability**: `capabilities/governance/main_project_structure_migration_controlled_batch_execution_authorization_planning_v1.py`
- **Status**: controlled-execution-authorization-planning-only（真实执行前最后闸门规划；不执行）

## Intent

把“哪些 batch 可被纳入未来真实执行授权、执行前必须满足哪些条件、失败如何 abort、执行后必须跑哪些测试”一次性写死，避免授权递归链扩张。

本阶段不发授权请求、不授予授权、不 arming、不执行 batch、不做真实 file operation、不 rerun verifier、不执行 rollback rehearsal。

若输入为 `workspace_fallback`，必须记录 `standard_eval_out_write_pending_on_local_repro=true`，避免误读为标准 `_eval_out` 已落盘。

## Final Decision

- `MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_BATCH_EXECUTION_AUTHORIZATION_PLANNING_READY_FOR_DRYRUN`
- **Next**: `Phase-Main-Project-Structure-Migration-Controlled-Batch-Execution-Authorization-DryRun-v1-001`

