# Evaluation: Task Manager Foundation Handoff DryRun v1

The evaluation validates that the Task Manager handoff planning package can be read, checked, referenced, and prepared for downstream planning consumption.

## Inputs

- `task_manager_foundation_handoff_plan_v1.json`
- `task_manager_foundation_handoff_plan_v1.md`
- `task_manager_foundation_boundary_matrix_v1.json`
- `task_manager_candidate_lifecycle_matrix_v1.json`
- `task_manager_downstream_readiness_matrix_v1.json`
- `task_manager_non_execution_constraints_v1.json`
- Planning `summary.json`
- Planning `verifier_report.json`

## Outputs

- `task_manager_foundation_handoff_dryrun_report_v1.json`
- `task_manager_foundation_handoff_dryrun_report_v1.md`
- `task_manager_handoff_package_integrity_matrix_v1.json`
- `task_manager_handoff_evidence_traceability_matrix_v1.json`
- `task_manager_handoff_downstream_consumption_dryrun_matrix_v1.json`
- `task_manager_handoff_non_execution_verification_v1.json`
- `summary.json`
- `verifier_report.json`

## Commands

```bash
python3 tools/evaluation/midplatform/run_midplatform_task_manager_foundation_handoff_dryrun_v1.py
python3 tools/evaluation/midplatform/verify_midplatform_task_manager_foundation_handoff_dryrun_v1.py
```
