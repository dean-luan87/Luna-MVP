# Evaluation: Task Manager Mount DryRunAndReview V1

This evaluation validates the Task Manager mount contract against Health Watchdog and Decision Center frozen foundations.

## Output Directory

`/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_task_manager_mount_dryrun_and_review/`

## Commands

```bash
cd /Users/luanlei/Desktop/Luna-Core
python3 tools/evaluation/midplatform/run_midplatform_task_manager_mount_dryrun_and_review_v1.py
python3 tools/evaluation/midplatform/verify_midplatform_task_manager_mount_dryrun_and_review_v1.py
```

## Required Artifacts

- `upstream_mount_contract_consumability_review_v1.json`
- `health_watchdog_frozen_dependency_review_v1.json`
- `decision_center_frozen_dependency_review_v1.json`
- `mount_contract_10_section_review_v1.json`
- `input_contract_dryrun_v1.json`
- `output_contract_dryrun_v1.json`
- `processing_model_dryrun_v1.json`
- `task_state_machine_dryrun_v1.json`
- `model_rule_algorithm_placement_review_v1.json`
- `governance_boundary_dryrun_v1.json`
- `downstream_handoff_matrix_review_v1.json`
- `sample_flow_dryrun_v1.json`
- `failure_route_dryrun_review_v1.json`
- `mount_health_metric_scope_review_v1.json`
- `boundary_matrix_review_v1.json`
- `non_claims_review_v1.json`
- `issue_register_v1.json`
- `mount_dryrun_readiness_decision_v1.json`
- `summary.json`
- `verifier_report.json`

Expected verifier result: `GO`

Minimum checks: `540`
