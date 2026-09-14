## Evaluation Target

`Phase-Luna-Project-Structure-Consolidation-Planning-v1-001`

## Commands

```bash
python3 tools/evaluation/governance/run_luna_project_structure_consolidation_planning_v1.py
python3 tools/evaluation/governance/verify_luna_project_structure_consolidation_planning_v1.py
```

## Pass Criteria

- `verifier_report.json.passed == true`
- `check_count >= 260`
- 五类 register 齐全，且 `all_plan_rows_have_future_life_system_mapping == true`
- `actual_file_move_executed == false`
- `final_decision == LUNA_PROJECT_STRUCTURE_CONSOLIDATION_PLANNING_READY_FOR_CONSOLIDATION_DRYRUN`
