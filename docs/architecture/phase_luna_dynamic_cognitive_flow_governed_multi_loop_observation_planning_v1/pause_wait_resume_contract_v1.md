# Pause, waiting, and resume contract

Pause and waiting preserve the minimum state required for future assessment,
not a full runtime resource reservation.

## Pause

`PAUSED` is an active governance decision to stop progressing a loop for a
reason such as Brain control, Safety / Survival preemption, Resource pressure,
or User control. A pause candidate preserves, at minimum:

- `loop_id` and `goal_ref`
- `intent_refs`
- latest `current_state_version_ref`
- `current_need_ref`
- `provisional_plan_ref`
- `pending_candidate_refs`
- Requirement, Observation, Context, Field, Current World, priority, resource,
  trace, and provenance references
- the last cognitive disposition and the pause reason
- continuity refs for Intent, Task/Behavior, Temporal, Spatial, Field, and
  Role/Perspective assessment

Pause never deletes a goal, recreates an Intent, turns pending candidates into
failures, releases or reallocates all capability history automatically, or
declares Task failure. It may relinquish runtime resource reservations when a
separate Resource owner proposes that change; the Loop keeps the resource
envelope reference and must be reassessed on resume.

## Waiting

`WAITING` means the loop has no currently admitted next step because it needs a
user response, external information, capability recovery, permission, or a
dependency. It is not the same as `PAUSED`:

- `PAUSED` is an intentional control decision.
- `WAITING` is a dependency state with no executable next step.

Both preserve the loop snapshot and remain candidate-only. Waiting for
capability recovery does not authorize a retry; waiting for user input does not
turn the user response into World Truth without normal admission.

## Resume assessment

Resume is never “continue the old queue”. The controlled sequence is:

```text
PAUSED / WAITING
  -> Resume Assessment
  -> compare Intent / Task-Behavior / Temporal / Spatial / Field / Role-Perspective continuity
  -> compare Context / Field / Current World / Cognitive State version
  -> reassess old Need and Requirement
  -> KEEP | SUPERSEDE | REPLAN | COMPLETE | remain WAITING
```

The assessment outcomes mean:

- `KEEP`: the Need remains the minimum necessary Need and the Requirement is
  still current for the observed state version. It may produce a new candidate
  assessment, not an invocation.
- `SUPERSEDE`: the old Requirement is stale or invalidated by the newer state;
  it cannot force invocation.
- `REPLAN`: changed evidence or hypothesis changes the candidate path.
- `COMPLETE`: the loop's own goal is sufficient; remaining candidates stop
  locally.
- `remain WAITING`: the dependency is still unresolved.

Only after this assessment may the current minimum Need form a new bounded
Capability Requirement, followed by Scope, Resolution, Permission, Resource,
and Observation admission.

Brain remains the authority for materialization and resume governance. A Loop
does not independently resume itself, and Brain must not independently solve a
materialized local concern in parallel.
