# Evaluation: Task Manager Foundation Handoff Final Closure Post-DryRun Review v1

The evaluation checks whether the final closure dry-run package is clean enough to enter freeze authorization planning.

## Inputs

- Task Manager foundation handoff final closure dry-run report.
- Final closure chain traceability matrix.
- Freeze candidate validation.
- Governance debt validation.
- Dry-run summary and verifier report.

## Outputs

- `task_manager_foundation_handoff_final_closure_post_dryrun_review_v1.json`
- `task_manager_foundation_handoff_final_closure_post_dryrun_review_v1.md`
- `task_manager_final_closure_dryrun_review_matrix_v1.json`
- `task_manager_final_closure_boundary_drift_review_v1.json`
- `task_manager_final_closure_chain_evidence_review_v1.json`
- `task_manager_final_freeze_candidate_review_v1.json`
- `task_manager_final_downstream_reference_review_v1.json`
- `task_manager_final_governance_debt_review_v1.json`
- `task_manager_final_authorization_planning_readiness_v1.json`
- `task_manager_final_review_non_execution_constraints_v1.json`
- `summary.json`
- `verifier_report.json`

## Commands

```bash
python3 tools/evaluation/midplatform/run_midplatform_task_manager_foundation_handoff_final_closure_post_dryrun_review_v1.py
python3 tools/evaluation/midplatform/verify_midplatform_task_manager_foundation_handoff_final_closure_post_dryrun_review_v1.py
```
