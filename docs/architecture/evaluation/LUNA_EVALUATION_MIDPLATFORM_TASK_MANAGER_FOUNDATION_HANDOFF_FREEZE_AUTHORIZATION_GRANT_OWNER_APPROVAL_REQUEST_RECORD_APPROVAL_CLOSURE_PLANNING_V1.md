# Luna Evaluation — Midplatform Task Manager Record Approval Closure Planning v1

## Runner

```bash
python3 tools/evaluation/midplatform/run_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_planning_v1.py
```

## Verifier

```bash
python3 tools/evaluation/midplatform/verify_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_planning_v1.py
```

## Output

`_tmp_eval_out/midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_planning_v1_smoke_v0/`

## Upstream

Owner Approval Request Issuance Post-DryRun Review smoke output must be GO with `timeout_event_review_ok`, `validate_once_reference_review_ok`, and `issuance_dryrun_result_accepted`.

## GO Threshold

- `verifier=GO`
- `passed_checks>=420`
- `failed_checks=0`
- `file_size_governance_review_exists=true`
