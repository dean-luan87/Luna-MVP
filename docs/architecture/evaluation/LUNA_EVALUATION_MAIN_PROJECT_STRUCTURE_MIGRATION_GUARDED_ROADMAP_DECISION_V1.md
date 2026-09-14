# Luna Evaluation — Main Project Structure Migration Guarded Roadmap Decision v1

**Phase**：`Phase-Main-Project-Structure-Migration-Guarded-Roadmap-Decision-v1-001`  
**性质**：roadmap-decision-only  
**输出目录**：`_eval_out/main_project_structure_migration_guarded_roadmap_decision_v1_smoke_v0/`

## 运行

```bash
python3 tools/evaluation/governance/run_main_project_structure_migration_guarded_roadmap_decision_v1.py
python3 tools/evaluation/governance/verify_main_project_structure_migration_guarded_roadmap_decision_v1.py
```

## 通过条件

- `selected_route=Migration Execution Control and Test Harness Planning`
- `guarded_migration_chain_closed=true`；`real_migration_allowed=false`
- `migration_execution_control_required=true`；`post_migration_test_harness_required=true`
- Route E 真实迁移 blocked；Route F/G 白盒/后台 deferred
- `final_decision=MAIN_PROJECT_STRUCTURE_MIGRATION_GUARDED_ROADMAP_DECISION_READY_FOR_EXECUTION_CONTROL_AND_TEST_HARNESS_PLANNING`
- `recommended_next_phase=Phase-Main-Project-Structure-Migration-Execution-Control-and-Test-Harness-Planning-v1-001`
- Verifier ≥ 220 checks（smoke 262）
