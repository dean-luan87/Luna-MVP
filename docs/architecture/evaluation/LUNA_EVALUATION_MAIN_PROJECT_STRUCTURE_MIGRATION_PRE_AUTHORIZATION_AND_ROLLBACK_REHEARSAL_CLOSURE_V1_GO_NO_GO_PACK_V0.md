## GO

- 三阶段链闭环；gap_hard_block 已冻结；Semantic Clarification A 已记录
- `armed_batch_count=0`；无权限释放

## NO-GO

- Post-Review 未 GO 或 `armed_batch_count>0` / `rollback_success_claim_allowed=true`
- `pre_authorization_rollback_rehearsal_chain_closed=false`

## Smoke

- **Output**: `_eval_out/main_project_structure_migration_pre_authorization_and_rollback_rehearsal_closure_v1_smoke_v0/`
- **Next**: `Phase-Post-Pre-Authorization-and-Rollback-Rehearsal-Roadmap-Decision-v1-001`
