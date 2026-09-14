## Evaluation Target

`Phase-Main-Project-Structure-Migration-Guarded-DryRun-v1-001`

## Commands

```bash
python3 tools/evaluation/governance/run_main_project_structure_migration_guarded_dryrun_v1.py
python3 tools/evaluation/governance/verify_main_project_structure_migration_guarded_dryrun_v1.py
```

## Pass Criteria

- `verifier_report.json.passed == true`
- `check_count >= 320`
- `batch_count == 8`；`gate_sequence_count == 10`
- `bound_test_count == 31`；`unbound_test_count == 0`；`executed_test_count == 0`
- `rollback_checkpoint_count >= 8`；`rollback_executed == false`
- 全部排除范围 flag 为 true
- `ready_for_post_dryrun_review == true`；`ready_for_real_migration == false`
- `final_decision == MAIN_PROJECT_STRUCTURE_MIGRATION_GUARDED_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW`
