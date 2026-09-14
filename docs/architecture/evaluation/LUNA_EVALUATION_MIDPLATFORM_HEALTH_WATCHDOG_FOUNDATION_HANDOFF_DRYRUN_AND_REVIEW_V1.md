# Evaluation: Health Watchdog Foundation Handoff DryRunAndReview V1

This evaluation verifies that Health Watchdog foundation handoff planning matches the disk skeleton files and upstream GO chain.

## Output Directory

`/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_health_watchdog_foundation_handoff_dryrun_and_review/`

## Commands

```bash
cd /Users/luanlei/Desktop/Luna-Core
python3 tools/evaluation/midplatform/run_midplatform_health_watchdog_foundation_handoff_dryrun_and_review_v1.py
python3 tools/evaluation/midplatform/verify_midplatform_health_watchdog_foundation_handoff_dryrun_and_review_v1.py
```

## Required Artifacts

- `upstream_go_chain_review_v1.json`
- `foundation_version_tag_review_v1.json`
- `skeleton_file_consistency_review_v1.json`
- `frozen_type_interface_review_v1.json`
- `frozen_function_interface_review_v1.json`
- `frozen_validator_interface_review_v1.json`
- `handoff_contract_dryrun_v1.json`
- `downstream_output_contract_review_v1.json`
- `forbidden_mutation_policy_review_v1.json`
- `change_control_policy_review_v1.json`
- `boundary_freeze_review_v1.json`
- `downstream_readiness_matrix_review_v1.json`
- `non_claims_review_v1.json`
- `route_decision_review_v1.json`
- `issue_register_v1.json`
- `handoff_dryrun_readiness_decision_v1.json`
- `summary.json`
- `verifier_report.json`

## Expected Result

Expected verifier result: `GO`

Minimum checks: `400`

Expected final decision:

`MIDPLATFORM_HEALTH_WATCHDOG_FOUNDATION_HANDOFF_DRYRUN_AND_REVIEW_CLOSED_READY_FOR_TASK_MANAGER_MOUNT_PLANNING`
