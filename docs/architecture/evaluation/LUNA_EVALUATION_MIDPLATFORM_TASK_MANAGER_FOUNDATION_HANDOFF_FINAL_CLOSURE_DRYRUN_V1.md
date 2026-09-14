# Evaluation: Task Manager Foundation Handoff Final Closure DryRun v1

The evaluation checks whether the final closure planning package is complete and traceable enough to enter final closure post-dryrun review.

## Inputs

- Task Manager foundation handoff final closure planning package.
- Final closure chain evidence map.
- Freeze candidate asset map.
- Governance debt carryover.

## Outputs

- `task_manager_foundation_handoff_final_closure_dryrun_report_v1.json`
- `task_manager_foundation_handoff_final_closure_dryrun_report_v1.md`
- `task_manager_final_closure_plan_integrity_matrix_v1.json`
- `task_manager_final_closure_chain_traceability_matrix_v1.json`
- `task_manager_final_freeze_candidate_validation_v1.json`
- `task_manager_final_closure_boundary_validation_v1.json`
- `task_manager_final_downstream_reference_validation_v1.json`
- `task_manager_final_governance_debt_validation_v1.json`
- `task_manager_final_non_execution_validation_v1.json`
- `task_manager_final_closure_post_review_readiness_v1.json`
- `summary.json`
- `verifier_report.json`

## Commands

```bash
python3 tools/evaluation/midplatform/run_midplatform_task_manager_foundation_handoff_final_closure_dryrun_v1.py
python3 tools/evaluation/midplatform/verify_midplatform_task_manager_foundation_handoff_final_closure_dryrun_v1.py
```
