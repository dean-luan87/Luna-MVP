# Luna Midplatform Health Watchdog Controlled Skeleton Implementation Planning V1

Phase: `Phase-Midplatform-Health-Watchdog-Controlled-Skeleton-Implementation-Planning-v1-001`

This phase plans the minimum Health Watchdog skeleton after Health Watchdog Mount DryRunAndReview is GO. It does not create the three Health Watchdog skeleton files and does not enable any runtime.

## Scope

Allowed planning targets:

- `enum`
- `dataclass`
- `pure_function`
- `static_validator`
- `candidate_generator`

Recommended skeleton files for the next Implementation DryRun:

- `capabilities/midplatform/core/health_watchdog_types_v1.py`
- `capabilities/midplatform/core/health_watchdog_skeleton_v1.py`
- `capabilities/midplatform/core/health_watchdog_static_validators_v1.py`

In this phase, `health_watchdog_files_created_now=false`.

## Contracts

The planning artifact defines:

- `HealthWatchdogState`
- `HealthSeverity`
- `HealthSignalCandidate`
- `DegradationCandidate`
- `RecoveryRecommendationCandidate`
- `RequiredObservationCandidate`
- `ModuleHealthReviewCandidate`
- `WatchdogHandoffCandidate`
- 10 pure function contracts
- 11 static validator contracts
- processing chain contract
- governance guard plan
- recovery guard plan
- Decision Center dependency guard plan
- sample plan
- test plan
- skeleton boundary matrix
- non-claims

All candidates require `candidate_id`, `trace_ref`, and `fact_status=not_fact`.

## Hard Boundaries

- `recovery_recommendation_candidate ≠ recovery execution`
- `degradation_candidate ≠ real degradation`
- `watchdog_handoff_candidate ≠ direct mount`
- `RecoveryRecommendationCandidate.recovery_execution=false`
- `RecoveryRecommendationCandidate.restart_allowed=false`
- `RecoveryRecommendationCandidate.process_control_allowed=false`
- `DegradationCandidate.real_degradation=false`
- `WatchdogHandoffCandidate.direct_mount=false`

No Health Watchdog runtime, recovery execution, module restart, process control, model/provider invocation, task execution, Memory/WorldModel write, user output, Output Gate mount, or Task Manager mount is enabled.

## Readiness

Expected final decision:

`MIDPLATFORM_HEALTH_WATCHDOG_CONTROLLED_SKELETON_IMPLEMENTATION_PLANNING_READY_FOR_IMPLEMENTATION_DRYRUN`

Recommended next phase:

`Phase-Midplatform-Health-Watchdog-Controlled-Skeleton-Implementation-DryRun-v1-001`
