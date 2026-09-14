# Cognitive Goal Model v1

## Purpose and boundary

A Goal gives continuity to cognition across fields and time. It is not a
Task, an Action, a Decision, a plan, or an execution command. A Goal records
why a cognitive process exists and the conditions under which it remains
relevant.

The Goal hierarchy is:

```text
Brain Goal (long-term direction)
        ↓
Cognitive Goal (current direction)
        ↓
Task Goal (bounded process)
        ↓
Decision / Action Boundary
```

Brain retains Intent, Value, Goal authority, and final judgment. A Task may
reference a Goal, but cannot create or modify the Brain Goal. A Field provides
context for a Goal; it does not own the Goal.

## Goal layers

- **Long Term Goal**: durable direction such as maintaining health.
- **Current Goal**: a current cognitive direction such as finding a hospital
  entrance.
- **Task Goal**: a bounded objective such as navigating to the hospital.

Each Goal carries a goal_id, parent_goal_reference, origin, scope, priority
candidate, constraints, validity interval, status, provenance, and unknowns.
Goal status is a candidate state and is not an automatic value judgment.

## Continuity rules

Goal continuity survives Field transitions when its validity and constraints
remain applicable. A Field transition may produce a Goal Reassessment
Candidate, never an unreviewed Goal rewrite. New Evidence can invalidate or
pause a Goal, but Reality remains authoritative over historical assumptions.

Goal completion requires an explicit completion condition and a completion
evidence reference. Abandonment requires a Brain/User-authorized candidate.
Suspension preserves the goal reference and unresolved constraints.

## Prohibitions

This architecture does not implement automatic planning, autonomous Goal
creation, Goal mutation by a Provider, Action execution, Emotion, Role, Social
Field, Simulation, B Route, or automatic learning. A Goal does not modify
Reality, Self Identity, Decision, or Action directly.

Goal Reassessment Candidate is the only permitted handoff for a possible
revision. The phase does not permit autonomous Goal creation. A Goal does not
modify Reality and does not modify Self Identity.

Explicit boundary: a Goal does not modify Reality and does not modify Self Identity.
