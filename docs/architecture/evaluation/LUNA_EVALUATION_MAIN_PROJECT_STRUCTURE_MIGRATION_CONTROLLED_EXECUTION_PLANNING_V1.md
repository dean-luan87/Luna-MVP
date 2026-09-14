# Luna Evaluation — Controlled Execution Planning v1

**Phase**：`Phase-Main-Project-Structure-Migration-Controlled-Execution-Planning-v1-001`  
**输出**：`_eval_out/main_project_structure_migration_controlled_execution_planning_v1_smoke_v0/`

## 运行

```bash
python3 tools/evaluation/governance/run_main_project_structure_migration_controlled_execution_planning_v1.py
python3 tools/evaluation/governance/verify_main_project_structure_migration_controlled_execution_planning_v1.py
```

## 通过条件

- Roadmap / Execution Control Closure 上游 GO
- `batch_count=8`；`owner_authorization_gate_count>=7`；`post_batch_test_count=31`；`verifier_suite_count>=12`
- `rollback_rehearsal_mandatory=true`；`one_batch_at_a_time_required=true`；`pass_required_before_next_batch=true`
- 全部 execution 禁止 flag 为 false；`evidence_pack_generated_now=false`
- `final_decision=MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_EXECUTION_PLANNING_READY_FOR_DRYRUN`
- Verifier ≥ 320 checks（smoke **337**）
