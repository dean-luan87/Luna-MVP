# Record Approval Closure Post-DryRun Review Issue Review v1

Locate breakpoint between `record_approval_closure_post_dryrun_review_v1` and its direct dryrun upstream. Stop on first non-GO dryrun.

Direct dryrun upstream (from post-dryrun review summary `record_approval_closure_dryrun_root`):
- `midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_dryrun_v1`

```bash
python3 tools/evaluation/midplatform/run_record_approval_closure_post_dryrun_review_issue_review_v1.py
python3 tools/evaluation/midplatform/verify_record_approval_closure_post_dryrun_review_issue_review_v1.py
```

Output: `_tmp_eval_out/record_approval_closure_post_dryrun_review_issue_review_v1_smoke_v0/`
