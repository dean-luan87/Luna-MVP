# Cognitive Process Instance Model v1

## Definition

A Cognitive Process Instance Candidate is an ephemeral, bounded runtime-context description for one potential cognitive activity. It is not persistent State, a State Machine, a task plan, or an executor.

## Example

```text
process_instance_id: airport_navigation_001_candidate
goal_reference: reach_gate_candidate
active_attention: gate_sign_candidate
capability_bundle: visual_text_spatial_candidate
workspace_reference: current_route_workspace_candidate
status: active_candidate
```

## Candidate contents

- process identifier and provenance;
- context, active-goal, and attention references;
- workspace and capability-bundle references;
- budget and lifecycle-status candidates;
- unknown, risk, interruption, and closure references.

## Lifecycle

```text
Formed -> Active Candidate -> Reallocated / Suspended Candidate -> Closed Candidate
```

Lifecycle labels describe a candidate view of an ephemeral process context. They never establish a global runtime state transition and never mutate Reducer-owned State.

## Boundaries

A process instance cannot invoke capabilities, decide, execute, persist memory, or claim an outcome. It is traceable organization context for a future controlled runtime only.

