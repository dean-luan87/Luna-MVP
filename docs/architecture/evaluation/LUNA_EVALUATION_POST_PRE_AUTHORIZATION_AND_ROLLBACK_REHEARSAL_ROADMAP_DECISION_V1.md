# Luna Evaluation — Post Pre-Authorization and Rollback Rehearsal Roadmap Decision v1

**Phase**：`Phase-Post-Pre-Authorization-and-Rollback-Rehearsal-Roadmap-Decision-v1-001`  
**输出**：`_eval_out/post_pre_authorization_and_rollback_rehearsal_roadmap_decision_v1_smoke_v0/`

## 运行

```bash
python3 tools/evaluation/governance/run_post_pre_authorization_and_rollback_rehearsal_roadmap_decision_v1.py
python3 tools/evaluation/governance/verify_post_pre_authorization_and_rollback_rehearsal_roadmap_decision_v1.py
```

## 通过条件

- Pre-Authorization Closure 上游 GO；`pre_authorization_rollback_rehearsal_chain_closed=true`
- `selected_route=Rollback Rehearsal DryRun Planning`
- `real_migration_execution_trial_blocked=true`；`rollback_rehearsal_execution_blocked=true`；`controlled_batch_arming_planning_deferred=true`
- `missing_rollback_rehearsal_blocks_real_migration=true`；`missing_rollback_rehearsal_blocks_batch_arming=true`
- Verifier ≥ 220 checks（baseline 180）

## Smoke 结果

- **verifier**: GO
- **checks**: 293/220
- **boundary_ok**: true
- **Next**: `Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-DryRun-Planning-v1-001`
