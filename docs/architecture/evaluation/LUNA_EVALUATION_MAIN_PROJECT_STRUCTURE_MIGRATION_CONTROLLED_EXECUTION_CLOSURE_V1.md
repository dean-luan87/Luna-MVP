# Luna Evaluation — Controlled Execution Closure v1

**Phase**：`Phase-Main-Project-Structure-Migration-Controlled-Execution-Closure-v1-001`  
**输出**：`_eval_out/main_project_structure_migration_controlled_execution_closure_v1_smoke_v0/`

## 运行

```bash
python3 tools/evaluation/governance/run_main_project_structure_migration_controlled_execution_closure_v1.py
python3 tools/evaluation/governance/verify_main_project_structure_migration_controlled_execution_closure_v1.py
```

## 通过条件

- Post-Review / DryRun / Planning 上游 GO；`completed_phase_count>=3`
- `controlled_execution_chain_closed=true`；`armed_batch_count=0`
- Correction A 记录且 `correction_semantic_impact=no_permission_granted`
- `final_decision=MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_EXECUTION_CLOSED_FOR_CURRENT_MAINLINE`
- Verifier ≥ 260 checks
