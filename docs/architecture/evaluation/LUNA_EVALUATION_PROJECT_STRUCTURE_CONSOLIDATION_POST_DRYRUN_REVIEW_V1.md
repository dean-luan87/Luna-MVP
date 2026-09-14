## Evaluation Target

`Phase-Luna-Project-Structure-Consolidation-Post-DryRun-Review-v1-001`

## Commands

```bash
python3 tools/evaluation/governance/run_luna_project_structure_consolidation_post_dryrun_review_v1.py
python3 tools/evaluation/governance/verify_luna_project_structure_consolidation_post_dryrun_review_v1.py
```

## Pass Criteria

- `verifier_report.json.passed == true` 且 `check_count >= 320`
- 五路输入 root 全部 `loaded=true`
- 全部 review 产物 `*_generated=true`
- `total_conflict_count == 1830`，`human_review_required_count == 240`，`do_not_auto_execute_count == 466`
- `batch_count >= 7`，`missing_life_system_mapping_count == 0`
- `rollback_plan_review_pass == true`
- 全部 no-execute / no-modify / no-runtime 边界为 false
- `ready_for_closure == true`（或 plan-revision 分支：`requires_consolidation_plan_revision == true`）
- `ready_for_real_migration / file_move / file_delete / module_merge == false`
- `final_decision` 为以下之一：
  - `LUNA_PROJECT_STRUCTURE_CONSOLIDATION_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE`
  - `LUNA_PROJECT_STRUCTURE_CONSOLIDATION_POST_DRYRUN_REVIEW_REQUIRES_PLAN_REVISION`

## Review Focus

跑完后重点检查 `plan_revision_required_conflicts_register.json`：

- 若 `item_count` 很大（>150），应走 plan-revision 分支，不得 closure
- 若为空或很小且高风险项已被 dry-run 阻断，可 conditional closure
