# Evaluation: Task Manager Foundation Handoff Final Closure Planning v1

The evaluation checks whether the Task Manager foundation handoff full chain evidence supports a complete final closure planning package.

## Inputs

- Handoff planning, dry-run, and post-dryrun review packages.
- Closure planning, closure dry-run, and closure post-dryrun review packages.
- Task Manager core skeleton files.

## Outputs

- `task_manager_foundation_handoff_final_closure_plan_v1.json`
- `task_manager_foundation_handoff_final_closure_plan_v1.md`
- `task_manager_final_closure_chain_evidence_map_v1.json`
- `task_manager_final_freeze_candidate_asset_map_v1.json`
- `task_manager_final_closure_boundary_contract_v1.json`
- `task_manager_final_candidate_semantics_lock_plan_v1.json`
- `task_manager_final_downstream_reference_contract_v1.json`
- `task_manager_final_governance_debt_carryover_v1.json`
- `task_manager_final_non_execution_constraints_v1.json`
- `task_manager_final_closure_next_phase_readiness_v1.json`
- `summary.json`
- `verifier_report.json`

## Commands

```bash
python3 tools/evaluation/midplatform/run_midplatform_task_manager_foundation_handoff_final_closure_planning_v1.py
python3 tools/evaluation/midplatform/verify_midplatform_task_manager_foundation_handoff_final_closure_planning_v1.py
```
