# Evaluation: Task Manager Foundation Handoff Closure Post-DryRun Review v1

The evaluation checks whether the Task Manager foundation handoff closure dry-run package is clean enough to enter final closure / freeze planning.

## Inputs

- Task Manager foundation handoff closure dry-run report.
- Closure plan integrity matrix.
- Closure evidence traceability matrix.
- Freeze candidate validation.
- Candidate semantics validation.
- Downstream scope validation.
- Non-execution validation.
- Closure governance debt register.
- Dry-run summary and verifier report.

## Outputs

- `task_manager_foundation_handoff_closure_post_dryrun_review_v1.json`
- `task_manager_foundation_handoff_closure_post_dryrun_review_v1.md`
- `task_manager_closure_dryrun_review_matrix_v1.json`
- `task_manager_closure_boundary_drift_review_v1.json`
- `task_manager_closure_evidence_chain_review_v1.json`
- `task_manager_closure_governance_debt_review_v1.json`
- `task_manager_closure_final_planning_readiness_matrix_v1.json`
- `task_manager_closure_review_non_execution_constraints_v1.json`
- `summary.json`
- `verifier_report.json`

## Commands

```bash
python3 tools/evaluation/midplatform/run_midplatform_task_manager_foundation_handoff_closure_post_dryrun_review_v1.py
python3 tools/evaluation/midplatform/verify_midplatform_task_manager_foundation_handoff_closure_post_dryrun_review_v1.py
```
