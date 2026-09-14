## Evaluation Target

`Phase-Luna-Project-Structure-Consolidation-DryRun-v1-001`

## Commands

```bash
python3 tools/evaluation/governance/run_luna_project_structure_consolidation_dryrun_v1.py
python3 tools/evaluation/governance/verify_luna_project_structure_consolidation_dryrun_v1.py
```

## Pass Criteria

- `verifier_report.json.passed == true` 且 `check_count >= 320`
- `batch_count >= 7`，`merge_plan_rows > 0`，`archive_plan_rows > 0`
- `human_review_required_register_count >= 1`
- `do_not_auto_execute_register_count >= 10`
- `missing_life_system_mapping_count == 0`
- 全部 no-execute / no-modify 边界为 false
- `final_decision == LUNA_PROJECT_STRUCTURE_CONSOLIDATION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW`
