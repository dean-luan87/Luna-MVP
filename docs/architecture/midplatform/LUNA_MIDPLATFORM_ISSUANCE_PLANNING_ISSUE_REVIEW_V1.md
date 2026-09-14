# Issuance Planning Issue Review v1

Locate breakpoint between `issuance_planning_v1` and its declared prior upstreams. Stop on first non-GO.

Direct prior upstream order (from issuance planning upstream GO checks):
1. `grant_owner_approval_request_post_dryrun_review_root`
2. `grant_owner_approval_request_planning_root`
3. `grant_owner_approval_request_dryrun_root`
4. `input_output_registry_patch_root`

```bash
python3 tools/evaluation/midplatform/run_issuance_planning_issue_review_v1.py
python3 tools/evaluation/midplatform/verify_issuance_planning_issue_review_v1.py
```

Output: `_tmp_eval_out/issuance_planning_issue_review_v1_smoke_v0/`
