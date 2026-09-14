# Luna Midplatform 1.0 - Health Watchdog Mount Planning v1

**Phase**: `Phase-Midplatform-Health-Watchdog-Mount-Planning-v1-001`

This phase plans Health Watchdog as the primary downstream consumer of `midplatform_decision_center_foundation_v1`.

## Boundary

Health Watchdog may consume Decision Center health/block/hold/safety refs and produce health supervision candidates. It must not execute recovery, restart modules, control processes, run tasks, invoke model/provider, write Memory/WorldModel, or produce user output.

## Candidate Outputs

- `health_signal_candidate`
- `degradation_candidate`
- `recovery_recommendation_candidate`
- `required_observation_candidate`
- `module_health_review_candidate`
- `watchdog_handoff_candidate`
- `hold_candidate`
- `safety_block_candidate`
- `governance_review_candidate`

## Run

```bash
cd /Users/luanlei/Desktop/Luna-Core
python3 tools/evaluation/midplatform/run_midplatform_health_watchdog_mount_planning_v1.py
python3 tools/evaluation/midplatform/verify_midplatform_health_watchdog_mount_planning_v1.py
```

## Final Decision

```text
MIDPLATFORM_HEALTH_WATCHDOG_MOUNT_PLANNING_READY_FOR_DRYRUN_AND_REVIEW
```

## Next Phase

```text
Phase-Midplatform-Health-Watchdog-Mount-DryRunAndReview-v1-001
```
