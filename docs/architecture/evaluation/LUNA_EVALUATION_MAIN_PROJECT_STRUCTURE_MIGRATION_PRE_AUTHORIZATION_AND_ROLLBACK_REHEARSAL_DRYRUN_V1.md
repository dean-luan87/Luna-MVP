# Luna Evaluation — Pre-Authorization and Rollback Rehearsal DryRun v1

**Phase**：`Phase-Main-Project-Structure-Migration-Pre-Authorization-and-Rollback-Rehearsal-DryRun-v1-001`  
**输出**：`_eval_out/main_project_structure_migration_pre_authorization_and_rollback_rehearsal_dryrun_v1_smoke_v0/`

## 运行

```bash
python3 tools/evaluation/governance/run_main_project_structure_migration_pre_authorization_and_rollback_rehearsal_dryrun_v1.py
python3 tools/evaluation/governance/verify_main_project_structure_migration_pre_authorization_and_rollback_rehearsal_dryrun_v1.py
```

## 通过条件

- Planning 上游 GO；10 类 dry-run 产物已生成
- 三类缺口模拟：`owner_confirmed_now=false` · `operator_ack_executed_now=false` · `rehearsal_executed_now=false`
- `gap_hard_block_matrix` 三类缺口均阻断 migration 与 arming
- `armed_batch_count=0`；`all_batches_not_armed=true`
- `ready_for_post_dryrun_review=true`；`ready_for_real_migration=false`
- Verifier ≥ 360 checks；`boundary_ok=true`

## 下一 phase

`Phase-Main-Project-Structure-Migration-Pre-Authorization-and-Rollback-Rehearsal-Post-DryRun-Review-v1-001`
