## Evaluation Target

`Phase-Luna-Project-Structure-Consolidation-Roadmap-Decision-v1-001`

## Commands

```bash
python3 tools/evaluation/governance/run_luna_project_structure_consolidation_roadmap_decision_v1.py
python3 tools/evaluation/governance/verify_luna_project_structure_consolidation_roadmap_decision_v1.py
```

## Pass Criteria

- `verifier_report.json.passed == true` 且 `check_count >= 200`
- 七路输入 root 全部 `loaded=true`
- `route_option_count >= 8`（实际 10 条 A–J）
- `selected_route == Protected Asset and Human Review Resolution Planning`
- `consolidation_closed == true`
- `plan_revision_required == 0`，`human_review_required == 240`，`permanent_do_not_auto_execute == 914`
- 全部 deferred flags true（developer backend / docs / midplatform / real migration / mainline return）
- `real_migration_allowed == false`；全部 ready_for_* migration flags false
- `final_decision == LUNA_PROJECT_STRUCTURE_CONSOLIDATION_ROADMAP_DECISION_READY_FOR_PROTECTED_ASSET_AND_HUMAN_REVIEW_RESOLUTION_PLANNING`
- `recommended_next_phase == Phase-Protected-Asset-and-Human-Review-Resolution-Planning-v1-001`

## Explicit Non-Selection

- Route G（Real Structure Migration Guarded Planning）必须为 blocked / deferred
- Route F（Human Review Execution Trial）不得 selected_now（须先 resolution planning）
