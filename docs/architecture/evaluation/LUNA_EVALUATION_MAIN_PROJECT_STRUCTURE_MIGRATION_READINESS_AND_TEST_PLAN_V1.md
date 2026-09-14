## Evaluation Target

`Phase-Main-Project-Structure-Migration-Readiness-and-Test-Plan-v1-001`

## Commands

```bash
python3 tools/evaluation/governance/run_main_project_structure_migration_readiness_and_test_plan_v1.py
python3 tools/evaluation/governance/verify_main_project_structure_migration_readiness_and_test_plan_v1.py
```

## Pass Criteria

- `verifier_report.json.passed == true`
- `check_count >= 260`
- 13 intake roots loaded；必选 upstream artifacts present
- `post_migration_test_group_count >= 5`（A–E）
- `pre_migration_check_count >= 10`；`forbidden_scope_count >= 10`；`future_reserved_module_count >= 10`
- `protected_assets_excluded_from_migration` / `permanent_blocks_excluded_from_migration` / `human_review_items_excluded_or_manual_only`
- `rollback_required` / `post_migration_test_required`
- whitebox deferred + `developer_backend_overall_structure_deferred`
- `ready_for_migration_guarded_planning == true`；`ready_for_real_migration == false`
- 无副作用：`actual_file_move/delete/rename/merge == false`；`docs/readme/verdict_table_modified_by_planning == false`
- `final_decision == MAIN_PROJECT_STRUCTURE_MIGRATION_READINESS_AND_TEST_PLAN_READY_FOR_GUARDED_MIGRATION_PLANNING`
- `recommended_next_phase == Phase-Main-Project-Structure-Migration-Guarded-Planning-v1-001`
