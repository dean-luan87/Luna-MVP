# Issuance Post-DryRun Review Issue Review v1

Locate breakpoint between `issuance_post_dryrun_review_v1` and its declared direct upstreams. Stop on first non-GO.

Direct upstream order (from issuance post-dryrun review upstream GO checks):
1. `grant_owner_approval_request_issuance_planning_root` → issuance planning
2. `input_output_registry_patch_root` → registry patch
3. `protocol_shared_code_smoke_root` → protocol shared code smoke
4. `grant_owner_approval_request_issuance_dryrun_root` → issuance dryrun

```bash
python3 tools/evaluation/midplatform/run_issuance_post_dryrun_review_issue_review_v1.py
python3 tools/evaluation/midplatform/verify_issuance_post_dryrun_review_issue_review_v1.py
```

Output: `_tmp_eval_out/issuance_post_dryrun_review_issue_review_v1_smoke_v0/`
