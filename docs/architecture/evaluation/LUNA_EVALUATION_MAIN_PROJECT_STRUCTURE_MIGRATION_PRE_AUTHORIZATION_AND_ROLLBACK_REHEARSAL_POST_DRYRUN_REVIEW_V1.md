# Luna Evaluation — Pre-Authorization and Rollback Rehearsal Post-DryRun Review v1

**Phase**：`Phase-Main-Project-Structure-Migration-Pre-Authorization-and-Rollback-Rehearsal-Post-DryRun-Review-v1-001`  
**输出**：`_eval_out/main_project_structure_migration_pre_authorization_and_rollback_rehearsal_post_dryrun_review_v1_smoke_v0/`

## 运行

```bash
python3 tools/evaluation/governance/run_main_project_structure_migration_pre_authorization_and_rollback_rehearsal_post_dryrun_review_v1.py
python3 tools/evaluation/governance/verify_main_project_structure_migration_pre_authorization_and_rollback_rehearsal_post_dryrun_review_v1.py
```

## 通过条件

- DryRun + Planning 上游 GO；12 类 post-review 产物已生成
- `gap_hard_block_post_review.gap_hard_block_review_pass=true`
- `ready_for_closure=true`；`armed_batch_count=0`
- Verifier ≥ 340 checks；`boundary_ok=true`

## 下一 phase

`Phase-Main-Project-Structure-Migration-Pre-Authorization-and-Rollback-Rehearsal-Closure-v1-001` — 仍不授权真实迁移，仅冻结 pre-authorization 治理链。
