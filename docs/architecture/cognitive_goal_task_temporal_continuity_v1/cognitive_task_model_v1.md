# Cognitive Task Model v1

## Task as a cognitive process

A Task is a bounded, persistent Cognitive Process within a Field context. It
is not a Todo List item, an Action Command, an execution thread, or a second
cognitive subject. A Task explains what remains to be carried through time;
Decision and Action Boundary still govern what may be requested.

```text
Field
  ↓
Goal
  ↓
Task Process
  ↓
Situation / Option / Decision
  ↓
Action Boundary
  ↓
Outcome / Experience
```

## Task contract

Every Task contains:

- task_id and origin_field_reference;
- goal_reference and intent_reference;
- lifecycle_state;
- constraints and resource context;
- progress evidence and completion condition;
- pending_information and next_requirement_candidate;
- interruption context and resume conditions;
- provenance, confidence, and unknowns.

The Task state is a candidate state maintained through the approved State
Reducer. The Reducer remains the sole State mutation authority. Task state does
not directly mutate Reality, Goal, Self, Decision, Attention, or Action.

## Field binding

A Task may remain bound to its origin Field, follow a governed Field
transition, or become Background when its origin Field is suspended. A Field
transition creates a Task Context Update Candidate. It does not delete a task,
invent a task, or transfer confidential information without a boundary check.

## Task lifecycle

```text
Created → Active → Background → Suspended → Resumed → Completed
                                      ↘ Abandoned / Expired
```

`Resumed` requires preserved task identity, constraints, and pending
information. `Completed` requires completion evidence. `Abandoned` requires a
reviewed candidate; it is not inferred from one failed Action.

## Prohibitions

No automatic planning, no automatic execution, no Task-as-Brain, no Provider
Goal mutation, no Emotion, no Role, no Social Field, no B Route, and no
Simulation Runtime are implemented here.

Task is not a second cognitive subject. Task state does not directly mutate
Reality. Provider Goal mutation is prohibited.

Explicit boundary: Task state does not directly mutate Reality.
