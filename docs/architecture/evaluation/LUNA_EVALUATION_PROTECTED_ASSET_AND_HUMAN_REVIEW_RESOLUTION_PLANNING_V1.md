## Evaluation Target

`Phase-Protected-Asset-and-Human-Review-Resolution-Planning-v1-001`

## Commands

```bash
python3 tools/evaluation/governance/run_protected_asset_and_human_review_resolution_planning_v1.py
python3 tools/evaluation/governance/verify_protected_asset_and_human_review_resolution_planning_v1.py
```

## Pass Criteria

- `verifier_report.json.passed == true` 且 `check_count >= 260`
- roadmap + closure + post-review + carryover registers loaded
- 全部 policy/schema/state machine 产物 generated
- `protected_asset_type_count >= 10`，`human_review_category_count >= 8`，`permanent_block_rule_count >= 8`
- `human_review_required_count == 240`，`permanent_do_not_auto_execute_count == 914`
- `protected_conflict_count == 448`，`static_dnae_rule_count == 466`
- 全部 auto-delete/archive/move/merge = false；human_review_execution = false
- 全部 forbidden decision flags = true
- `ready_for_human_review_resolution_dryrun == true`
- `ready_for_real_migration / file_move / file_delete / module_merge == false`
- `final_decision == PROTECTED_ASSET_AND_HUMAN_REVIEW_RESOLUTION_PLANNING_READY_FOR_DRYRUN`
- `recommended_next_phase == Phase-Protected-Asset-and-Human-Review-Resolution-DryRun-v1-001`

## Next Phase Focus

DryRun 只模拟 240 条 review 和 914 条 permanent block 的处理流程，不做真实人工处理。
