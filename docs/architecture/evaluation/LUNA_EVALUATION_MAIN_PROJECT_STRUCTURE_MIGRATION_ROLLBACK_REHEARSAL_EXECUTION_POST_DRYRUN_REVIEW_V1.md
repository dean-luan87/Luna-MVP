# Luna Evaluation — Rollback Rehearsal Execution Post-DryRun Review v1

**Phase**：`Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-Execution-Post-DryRun-Review-v1-001`  
**输出**：`_eval_out/main_project_structure_migration_rollback_rehearsal_execution_post_dryrun_review_v1_smoke_v0/`

## 运行

```bash
python3 tools/evaluation/governance/run_main_project_structure_migration_rollback_rehearsal_execution_post_dryrun_review_v1.py
python3 tools/evaluation/governance/verify_main_project_structure_migration_rollback_rehearsal_execution_post_dryrun_review_v1.py
```

## 通过条件

- Execution DryRun 上游 GO；9 类 review 对象已生成
- 全部权限仍 false；success claim blocked；`ready_for_roadmap_decision=true`
- Verifier ≥ 360 checks（baseline 300）

## Smoke 结果

- **verifier**: GO
- **checks**: 364/360
- **Next**: `Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-Execution-Roadmap-Decision-v1-001`

## 下游（已完成）

- Execution Roadmap Decision v1：`Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-Execution-Roadmap-Decision-v1-001`（GO；356/260；选中 Route A，下一阶段为 Real Rollback Rehearsal Pre-Authorization Planning）
