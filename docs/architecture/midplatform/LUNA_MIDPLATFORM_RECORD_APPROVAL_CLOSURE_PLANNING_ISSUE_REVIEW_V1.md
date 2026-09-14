# Record Approval Closure Planning Issue Review v1

Locate breakpoint between `record_approval_closure_planning_v1` and its direct prior request issuance post-review upstream. Stop on first non-GO prior review.

Direct prior review upstream (from planning summary `owner_approval_request_issuance_post_dryrun_review_root`):
- `midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_issuance_post_dryrun_review_v1`

```bash
python3 tools/evaluation/midplatform/run_record_approval_closure_planning_issue_review_v1.py
python3 tools/evaluation/midplatform/verify_record_approval_closure_planning_issue_review_v1.py
```

Output: `_tmp_eval_out/record_approval_closure_planning_issue_review_v1_smoke_v0/`
