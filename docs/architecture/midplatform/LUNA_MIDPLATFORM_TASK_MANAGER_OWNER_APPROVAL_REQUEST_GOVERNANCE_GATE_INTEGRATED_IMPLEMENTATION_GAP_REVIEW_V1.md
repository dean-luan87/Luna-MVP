# Governance Gate Integrated Implementation Gap Review v1

Locate breakpoint between `governance_gate_integrated_implementation_v1` and its declared direct upstreams. Stop on first non-GO.

Direct upstream order (from integrated implementation summary):
1. `record_approval_closure_post_dryrun_review_v1` (`post_review_root`)
2. `final_gate_planning_v1` (`final_gate_planning_root`)

```bash
python3 tools/evaluation/midplatform/run_task_manager_owner_approval_request_governance_gate_integrated_implementation_gap_review_v1.py
python3 tools/evaluation/midplatform/verify_task_manager_owner_approval_request_governance_gate_integrated_implementation_gap_review_v1.py
```

Output: `_tmp_eval_out/task_manager_owner_approval_request_governance_gate_integrated_implementation_gap_review_v1_smoke_v0/`
