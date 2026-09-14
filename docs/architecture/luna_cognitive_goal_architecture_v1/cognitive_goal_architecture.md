# Luna Cognitive Goal Architecture v1

## Purpose

The Goal Layer gives Luna a stable direction between understanding a Field and
forming a Decision Candidate. A goal describes a state that the主体 should
maintain, improve, or reach over time. It is not a task, desire, plan, action,
or execution command.

```text
Self / Constitution constraints
              ↓
        Goal Candidate
              ↓
       Self Goal Governance
              ↓
          Approved Goal
              ↓
          Task Manager
              ↓
       Brain Decision Candidate
              ↓
         Action Boundary
```

## Boundary

Task is an external or bounded work request, such as navigating to a location.
Goal is the direction that gives the task meaning, such as helping the user
arrive safely. Goal does not execute Action and does not become a desire or an
emotion. Brain remains the cognitive authority for a decision candidate;
Runtime is a future execution boundary.

Goals are candidates until Self Goal Governance evaluates them. No automatic
goal generation, automatic goal adjustment, Goal Runtime, Action Runtime,
Emotion Runtime, B Route, or model/provider call is part of this phase.

## Context and constraints

Field supplies current reality context. Memory and Schema supply historical and
pattern context but cannot create a goal automatically. Value is a reserved
future preference interface. Self reviews reasonability, capability, resource
cost, stability, and Constitution compliance. Unknowns remain explicit.

## Canonical flow

```text
Field + Intent + Drive + Memory/Schema context
                    ↓
             Goal Candidate
                    ↓
            Self Governance Review
                    ↓
       Approved / Rejected / Deferred Candidate
                    ↓
                Task reference
                    ↓
             Brain Decision Candidate
```

The phase is architecture-only. The contracts in this directory define
interfaces and negative guards for a later implementation; they do not mutate
state, schedule work, execute actions, or alter identity, value, or
Constitution.
