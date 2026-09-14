# Luna Evaluation — Controlled Execution Roadmap Decision v1

**Phase**：`Phase-Main-Project-Structure-Migration-Controlled-Execution-Roadmap-Decision-v1-001`  
**输出**：`_eval_out/main_project_structure_migration_controlled_execution_roadmap_decision_v1_smoke_v0/`

## 运行

```bash
python3 tools/evaluation/governance/run_main_project_structure_migration_controlled_execution_roadmap_decision_v1.py
python3 tools/evaluation/governance/verify_main_project_structure_migration_controlled_execution_roadmap_decision_v1.py
```

## 通过条件

- Controlled Execution Closure 上游 GO；`controlled_execution_chain_closed=true`
- `selected_route=Real Migration Pre-Authorization and Rollback Rehearsal Planning`
- `real_migration_execution_trial_blocked=true`；`batch_arming_trial_blocked=true`
- Verifier ≥ 220 checks
