# Luna Midplatform Task Manager Mount Planning V1

Phase: `Phase-Midplatform-Task-Manager-Mount-Planning-v1-001`

This phase plans Task Manager as the downstream task candidate management layer after `midplatform_health_watchdog_foundation_v1` is frozen.

## Position

Task Manager consumes Decision Center and Health Watchdog candidates and organizes task-level candidates. It is not an executor.

Core boundaries:

- `task_candidate ≠ task execution`
- `task_step_candidate ≠ executed step`
- `task_handoff_candidate ≠ direct mount`

## Scope

Allowed outputs are candidate-only:

- `task_candidate`
- `task_readiness_candidate`
- `task_block_candidate`
- `task_plan_candidate`
- `task_step_candidate`
- `task_handoff_candidate`
- `required_observation_handoff_candidate`
- later task pause/resume/abort/output preparation candidates

Forbidden in this phase:

- task execution
- tool call
- model/provider invocation
- Memory / WorldModel write
- user output
- direct mount to Output Gate, Module Adapter, or WorldModel-Memory Bridge

## Next Phase

`Phase-Midplatform-Task-Manager-Mount-DryRunAndReview-v1-001`
