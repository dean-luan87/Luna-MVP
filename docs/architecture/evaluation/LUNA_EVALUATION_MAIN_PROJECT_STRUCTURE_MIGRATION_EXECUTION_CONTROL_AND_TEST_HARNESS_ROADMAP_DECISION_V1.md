# Luna Evaluation — Execution Control and Test Harness Roadmap Decision v1

**Phase**：`Phase-Main-Project-Structure-Migration-Execution-Control-and-Test-Harness-Roadmap-Decision-v1-001`  
**输出**：`_eval_out/main_project_structure_migration_execution_control_and_test_harness_roadmap_decision_v1_smoke_v0/`

## 运行

```bash
python3 tools/evaluation/governance/run_main_project_structure_migration_execution_control_and_test_harness_roadmap_decision_v1.py
python3 tools/evaluation/governance/verify_main_project_structure_migration_execution_control_and_test_harness_roadmap_decision_v1.py
```

## 通过条件

- Execution Control Closure 上游 GO；`execution_control_test_harness_chain_closed=true`
- `selected_route=Controlled Migration Execution Planning`；`real_migration_execution_trial_blocked=true`
- 全部 execution 禁止 flag 为 false
- `final_decision=MAIN_PROJECT_STRUCTURE_MIGRATION_EXECUTION_CONTROL_AND_TEST_HARNESS_ROADMAP_DECISION_READY_FOR_CONTROLLED_MIGRATION_EXECUTION_PLANNING`
- Verifier ≥ 220 checks（smoke **248**）
