# Evaluation: Task Manager Foundation Handoff Closure Planning v1

The evaluation verifies that the three prior GO stages can support a closure planning package without executing closure or freezing the foundation.

## Inputs

- Foundation handoff planning package (GO)
- Foundation handoff dry-run package (GO)
- Foundation handoff post-dryrun review package (GO)
- Task Manager core skeleton files

## Outputs

- `task_manager_foundation_handoff_closure_plan_v1.json`
- `task_manager_foundation_handoff_closure_plan_v1.md`
- `task_manager_foundation_asset_inventory_v1.json`
- `task_manager_handoff_closure_evidence_chain_v1.json`
- `task_manager_handoff_freeze_candidate_boundary_v1.json`
- `task_manager_handoff_candidate_semantics_lock_plan_v1.json`
- `task_manager_handoff_downstream_planning_map_v1.json`
- `task_manager_handoff_future_l1_protocol_dependency_map_v1.json`
- `task_manager_handoff_closure_non_execution_constraints_v1.json`
- `summary.json`
- `verifier_report.json`

## Commands

```bash
python3 tools/evaluation/midplatform/run_midplatform_task_manager_foundation_handoff_closure_planning_v1.py
python3 tools/evaluation/midplatform/verify_midplatform_task_manager_foundation_handoff_closure_planning_v1.py
```
