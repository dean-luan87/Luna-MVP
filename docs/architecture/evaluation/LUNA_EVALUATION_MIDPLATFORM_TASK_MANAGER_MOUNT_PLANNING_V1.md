# Evaluation: Task Manager Mount Planning V1

This evaluation verifies Task Manager mount planning after Health Watchdog is frozen as `midplatform_health_watchdog_foundation_v1`.

## Output Directory

`/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_task_manager_mount_planning/`

## Commands

```bash
cd /Users/luanlei/Desktop/Luna-Core
python3 tools/evaluation/midplatform/run_midplatform_task_manager_mount_planning_v1.py
python3 tools/evaluation/midplatform/verify_midplatform_task_manager_mount_planning_v1.py
```

## Required Artifacts

- `task_manager_mount_scope_v1.json`
- `task_manager_mount_contract_v1.json`
- `task_manager_input_contract_v1.json`
- `task_manager_output_contract_v1.json`
- `task_manager_processing_model_v1.json`
- `task_manager_task_state_machine_v1.json`
- `task_manager_model_rule_algorithm_placement_v1.json`
- `task_manager_governance_boundary_v1.json`
- `task_manager_health_watchdog_dependency_boundary_v1.json`
- `task_manager_decision_center_dependency_boundary_v1.json`
- `task_manager_downstream_handoff_matrix_v1.json`
- `task_manager_sample_flow_plan_v1.json`
- `task_manager_failure_route_matrix_v1.json`
- `task_manager_mount_health_metric_scope_v1.json`
- `task_manager_boundary_matrix_v1.json`
- `task_manager_mount_non_claims_v1.json`
- `task_manager_mount_readiness_decision_v1.json`
- `summary.json`
- `verifier_report.json`

Expected verifier result: `GO`

Minimum checks: `460`
