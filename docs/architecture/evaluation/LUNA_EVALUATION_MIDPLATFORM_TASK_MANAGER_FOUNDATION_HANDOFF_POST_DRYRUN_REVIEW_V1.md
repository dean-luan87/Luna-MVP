# Evaluation: Task Manager Foundation Handoff Post-DryRun Review v1

The evaluation checks whether the Task Manager foundation handoff dry-run package is clean enough to enter closure / freeze planning.

## Inputs

- Task Manager foundation handoff dry-run report.
- Package integrity matrix.
- Evidence traceability matrix.
- Downstream consumption dry-run matrix.
- Non-execution verification.
- Dry-run summary and verifier report.

## Outputs

- `task_manager_foundation_handoff_post_dryrun_review_v1.json`
- `task_manager_foundation_handoff_post_dryrun_review_v1.md`
- `task_manager_handoff_dryrun_review_matrix_v1.json`
- `task_manager_handoff_boundary_drift_review_v1.json`
- `task_manager_handoff_evidence_chain_review_v1.json`
- `task_manager_handoff_closure_readiness_matrix_v1.json`
- `task_manager_handoff_review_non_execution_constraints_v1.json`
- `summary.json`
- `verifier_report.json`

## Commands

```bash
python3 tools/evaluation/midplatform/run_midplatform_task_manager_foundation_handoff_post_dryrun_review_v1.py
python3 tools/evaluation/midplatform/verify_midplatform_task_manager_foundation_handoff_post_dryrun_review_v1.py
```
