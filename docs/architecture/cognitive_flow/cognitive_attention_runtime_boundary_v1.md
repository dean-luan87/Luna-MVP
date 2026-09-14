# Cognitive Attention Runtime Boundary v1

## Boundary

Attention Governance determines what deserves cognitive resource consideration. It does not schedule software processes or execute cognitive modules.

```text
Attention Candidate Pool
  -> Attention Controller
  -> Cognitive Allocation Candidate
  -> Future Runtime Executor
  -> Outcome / Feedback Candidate
```

## Attention Controller responsibilities

- aggregate and arbitrate attention candidates;
- propose scope, depth, duration, direction, and budget allocation;
- propose deferral, suppression, continuation, or reallocation;
- preserve stability and inertia constraints.

## Explicit exclusions

The Attention Controller cannot:

- invoke Perception, Context, Workspace, Simulation, Operation, or Evaluation modules;
- schedule a process or allocate actual CPU/GPU/device resources;
- invoke an external model or sensor;
- determine facts, decisions, permissions, or actions;
- mutate Reducer-owned State.

## Future runtime handoff

A future Runtime Executor may consume an admitted allocation candidate as a bounded input. Runtime admission remains separately governed. Runtime execution cannot retroactively convert attention priority into truth, authority, or action permission.

