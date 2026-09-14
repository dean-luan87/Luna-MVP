# A Route Field / Task Integration Validation v1

## Field-bound process rule

A Task is a Field-bound Cognitive Process. It is not a global task list and
not a simple queue. The Task follows governed context transitions while
preserving its task_id, Goal reference, constraints, pending information, and
unknowns.

```text
Office Field + Work Task
          ↓ leave office
Office Task → Background / Suspended
          ↓ enter home
Home Field + Home Task Active Candidate
          ↓ return next day
Office Field + Work Task Resume Candidate
```

## Validation cases

- Same Reality and different Goal create different Task/Field context.
- Office departure backgrounds an unfinished Work Task instead of deleting it.
- A home task does not inherit confidential office context.
- A high-risk event suspends a current Task and preserves resume conditions.
- Resume confirms current Reality, Field, Self State, and Attention allocation.
- Completion requires outcome evidence; interruption alone is not failure.

Field does not modify Goal. Task does not modify Reality. Task lifecycle state
is maintained by the Reducer, the sole State mutation authority.

## Long-term boundary

24-hour, 7-day, and 30-day fixtures may show Field transitions and Task
continuity. They do not implement Multi-A, Role, Social Field, automatic
planning, or execution.

Completion evidence is required. No automatic planning and No execution are
included in this architecture validation.

Completion evidence is required before a Task is Completed.

The completion evidence reference is retained for continuity.
