# Luna Midplatform — Module Governance Closure Gap Review v1

## Scope

Locate the first real breakpoint between `module_governance_closure_v1` and `functional_slice_dryrun_v1`. Stop on first non-GO. Does not rerun handoff, broader roadmap, SLAM, or Scene Graph.

## Run

```bash
python3 tools/evaluation/midplatform/run_task_manager_owner_approval_request_module_governance_closure_gap_review_v1.py
python3 tools/evaluation/midplatform/verify_task_manager_owner_approval_request_module_governance_closure_gap_review_v1.py
```

Output: `_tmp_eval_out/task_manager_owner_approval_request_module_governance_closure_gap_review_v1_smoke_v0/`
