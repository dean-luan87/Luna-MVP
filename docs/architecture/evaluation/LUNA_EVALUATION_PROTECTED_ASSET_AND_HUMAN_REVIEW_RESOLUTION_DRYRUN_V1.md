## Evaluation Target

`Phase-Protected-Asset-and-Human-Review-Resolution-DryRun-v1-001`

## Commands

```bash
python3 tools/evaluation/governance/run_protected_asset_and_human_review_resolution_dryrun_v1.py
python3 tools/evaluation/governance/verify_protected_asset_and_human_review_resolution_dryrun_v1.py
```

## Pass Criteria

- `verifier_report.json.passed == true` 且 `check_count >= 320`
- planning + upstream registers loaded
- `human_review_case_count == 240`；`permanent_dnae_case_count == 914`
- `high_risk_merge == 5`；`future_placeholder == 35`；`target_module_unclear == 200`
- `protected_conflict == 448`；`static_dnae == 466`
- `audit_trace_generated_count >= 1154`；`rollback_ref_generated_count >= 1154`
- 全部 forbidden decision blocked；forbidden states absent
- `actual_human_review_executed == false`；`protected_assets_modified == false`
- `ready_for_post_dryrun_review == true`
- `final_decision == PROTECTED_ASSET_AND_HUMAN_REVIEW_RESOLUTION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW`

## Post-DryRun Focus

重点审查三项：240 条是否全部进入安全终态、914 条是否全部保持 permanent block、禁止决策/禁止状态是否全部被阻断。
