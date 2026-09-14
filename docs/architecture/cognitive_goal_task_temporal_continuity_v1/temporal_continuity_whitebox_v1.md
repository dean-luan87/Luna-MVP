# Temporal Continuity Whitebox v1

## Complete trace

```text
Brain Intent / Goal
        ↓
Goal Hierarchy
        ↓
Field-bound Task Process
        ↓
Task Lifecycle State
        ↓
Attention / Situation / Decision
        ↓
Action Boundary
        ↓
Outcome Evidence
        ↓
Experience Candidate
        ↓
Suspend / Resume / Complete Candidate
```

Each trace preserves goal_reference, task_id, field_reference, lifecycle
state, constraints, progress, pending_information, next_requirement,
completion_condition, interruption context, resume evidence, provenance,
confidence, and unknowns.

## Boundary assertions

Reality is updated only through Evidence and the Reducer. The Reducer remains
the sole State mutation authority. Goal and Task are not Action Commands.
Task continuity is not a Scheduler, not automatic planning, not automatic
execution, and not a second cognitive subject.

No Runtime, no Action Runtime, no hardware control, no external system
operation, no Emotion Runtime, no Role Runtime, no Social Runtime, no B Route,
no Simulation, and no online learning are implemented.

The lifecycle state is explicit. This is not automatic execution. No hardware
control, No external system operation, No B Route, and No online learning are
enabled.

No hardware control is enabled.
