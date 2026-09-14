# Luna Evaluation — Midplatform Decision Center Foundation Handoff Planning v1

## Phase

`Phase-Midplatform-Decision-Center-Foundation-Handoff-Planning-v1-001`

## 上游依赖

- `midplatform_decision_center_controlled_skeleton_implementation_post_dryrun_review`（GO）
- `midplatform_decision_center_controlled_skeleton_implementation_dryrun`
- `midplatform_decision_center_mount_dryrun_and_review`
- `midplatform_information_integration_foundation_handoff_dryrun_and_review`

## 执行

```bash
python3 tools/evaluation/midplatform/run_midplatform_decision_center_foundation_handoff_planning_v1.py
python3 tools/evaluation/midplatform/verify_midplatform_decision_center_foundation_handoff_planning_v1.py
```

## 产出目录

`_tmp_eval_out/midplatform_decision_center_foundation_handoff_planning/`

## Verifier

- MIN_CHECKS ≥ 320
- foundation_id / depends_on / version / runtime_status 正确
- 3 skeleton 文件纳入 handoff scope
- primary next phase = Health Watchdog Mount Planning
- blocker_count=0

## Final Decision

`MIDPLATFORM_DECISION_CENTER_FOUNDATION_HANDOFF_PLANNING_READY_FOR_DRYRUN_AND_REVIEW`
