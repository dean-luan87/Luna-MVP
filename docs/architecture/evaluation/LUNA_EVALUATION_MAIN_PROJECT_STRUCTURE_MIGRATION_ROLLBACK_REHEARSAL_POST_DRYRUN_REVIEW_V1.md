# Luna Evaluation — Rollback Rehearsal Post-DryRun Review v1

**Phase**：`Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-Post-DryRun-Review-v1-001`  
**输出**：`_eval_out/main_project_structure_migration_rollback_rehearsal_post_dryrun_review_v1_smoke_v0/`

## 运行

```bash
python3 tools/evaluation/governance/run_main_project_structure_migration_rollback_rehearsal_post_dryrun_review_v1.py
python3 tools/evaluation/governance/verify_main_project_structure_migration_rollback_rehearsal_post_dryrun_review_v1.py
```

## 通过条件

- Rollback Rehearsal DryRun 上游 GO；`ready_for_post_dryrun_review=true`
- 全部 post-review `*_review_pass=true`；`ready_for_closure=true`
- `sandbox_created_now=false`；`evidence_generated_now=false`；`rollback_success_claim_allowed=false`
- Verifier ≥ 360 checks（baseline 300）

## Smoke 结果

- **verifier**: GO
- **checks**: 364/360
- **Next**: `Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-Closure-v1-001`
