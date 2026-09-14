# Luna Evaluation — Pre-Authorization and Rollback Rehearsal Planning v1

**Phase**：`Phase-Main-Project-Structure-Migration-Pre-Authorization-and-Rollback-Rehearsal-Planning-v1-001`  
**输出**：`_eval_out/main_project_structure_migration_pre_authorization_and_rollback_rehearsal_planning_v1_smoke_v0/`

## 运行

```bash
python3 tools/evaluation/governance/run_main_project_structure_migration_pre_authorization_and_rollback_rehearsal_planning_v1.py
python3 tools/evaluation/governance/verify_main_project_structure_migration_pre_authorization_and_rollback_rehearsal_planning_v1.py
```

## 通过条件

- 12 个上游 `_eval_out` 输入根已加载（roadmap + controlled execution 链 + execution control + guarded + readiness + PAHR + structure map + gate taxonomy）
- 10 类核心规划产物已生成（policy / owner plan / operator ack / package / rehearsal scope-plan-evidence / arming record / blockers / readiness）
- `owner_authorization_type_count=7`；`rollback_rehearsal_step_count>=10`；`authorization_blocker_count>=14`；`batch_arming_record_count=8`
- `owner_confirmed_now=false`；`rollback_rehearsal_executed_now=false`；`armed_batch_count=0`
- `ready_for_pre_authorization_dryrun=true`；`ready_for_real_migration=false`
- Verifier ≥ 320 checks；`boundary_ok=true`

## 下一 phase

`Phase-Main-Project-Structure-Migration-Pre-Authorization-and-Rollback-Rehearsal-DryRun-v1-001` — 仍不迁移，模拟 owner/ack/rehearsal 缺失能否阻断真实执行。
