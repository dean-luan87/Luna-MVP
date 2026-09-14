# Cognitive Runtime Instance Model v1

## Runtime Instance Candidate

Fields: `runtime_id`, trigger reference, input reference, context reference, resource-boundary reference, lifecycle-status candidate, provenance, and trace.

## Lifecycle

`Created -> Running -> Suspended -> Completed -> Terminated`.

Lifecycle labels describe resource use for one cognitive process. They are not a persistent State Machine and cannot write Field, Reducer, Memory, Experience, Decision, Action, or Permission state.
