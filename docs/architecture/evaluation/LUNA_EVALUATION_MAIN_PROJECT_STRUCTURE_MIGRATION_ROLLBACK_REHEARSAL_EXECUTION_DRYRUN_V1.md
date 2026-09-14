# Luna Evaluation — Rollback Rehearsal Execution DryRun v1

**Phase**：`Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-Execution-DryRun-v1-001`  
**输出**：`_eval_out/main_project_structure_migration_rollback_rehearsal_execution_dryrun_v1_smoke_v0/`

## 运行

```bash
python3 tools/evaluation/governance/run_main_project_structure_migration_rollback_rehearsal_execution_dryrun_v1.py
python3 tools/evaluation/governance/verify_main_project_structure_migration_rollback_rehearsal_execution_dryrun_v1.py
```

## 通过条件

- Execution Planning 上游 GO；12 个 planning 对象已消费
- 10 类 dry-run 核心对象已生成；`dryrun_only=true`；`execution_released=false`（全 gate）
- `ready_for_post_dryrun_review=true`；`ready_for_rollback_rehearsal_execution=false`
- Verifier ≥ 380 checks（baseline 320）

## Smoke 结果

- **verifier**: GO
- **checks**: 426/380
- **Next**: `Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-Execution-Post-DryRun-Review-v1-001`

## 下游（已完成）

- Execution Post-DryRun Review v1：GO（364/360）
- Execution Roadmap Decision v1：GO（356/260；选中 Route A `Real Rollback Rehearsal Pre-Authorization Planning`）
