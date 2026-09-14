# Legacy Middleware Boundary Review v2

## `runtime/main_loop.py`

Observed as a legacy fixed-loop runtime with decision/execution behavior. It is incompatible with the event-driven, candidate-only A-route boundary and must remain isolated.

**Disposition:** `DEPRECATE from A-route`; retain untouched as a parallel legacy asset pending separately authorized Decision–Execution migration.

## Legacy Task Manager

The Task Manager provides useful lifecycle, decomposition, dependency, interruption/recovery, result aggregation, and diagnostics assets. Its `task_goal`, `task_plan`, and execution-request vocabulary cannot remain upstream of Brain/Neural CWO.

**Disposition:** `MIGRATE` as a CWO-scoped Middleware execution-organization adapter only.

## Legacy Model Manager

Model Manager provides strong reusable Provider Management components: capability matching, admission, resource/ownership evaluation, routing candidates, lifecycle plans, fallback, diagnostics, and trace/replay.

**Disposition:** `MIGRATE` as Provider Management support; prohibit Goal, Attention, task-decision, direct Brain, truth, and action authority.

## Capability Registry

Registry/manifests/lifecycle/baseline assets are canonical Capability Governance assets. They are already designed as governance metadata, not a runtime loader.

**Disposition:** `KEEP`; Brain must not access Registry directly, and baselines remain restricted to engineering governance/diagnostics/calibration.

## Boundary rule

No legacy asset may regain Goal, Decision, Action, Truth, or Reducer State Mutation authority by joining the Cognitive Middleware. All legacy ingress must be normalized through CWO-derived capability requirements and all outputs through Evidence Gateway/Middleware Report/Neural Feedback.
