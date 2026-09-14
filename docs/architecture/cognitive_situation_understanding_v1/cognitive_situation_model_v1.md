# Cognitive Situation Model v1

## Purpose

Situation Understanding combines governed reality context with the current
Field and Self context so Luna can represent what the current circumstances
mean for the subject. It stops at a Situation Candidate; it does not choose
what to do. It is not a Decision. It cannot issue an Action.

```text
Reality Evidence / Reality State
        + Cognitive Field State
        + Self State
        + Self Capability State
        + Goal Context
        + Attention Context
        ↓
Situation Candidate
        ↓
A Route input
```

## Situation structure

```text
Situation
├── Environment Context
├── Self Context
├── Goal Context
├── Constraint Context
├── Risk Context
└── Unknown Context
```

Environment Context describes relevant entities, relations, events, and
changes. Self Context describes current State and Capability constraints.
Goal Context is a reference to an existing Brain Intent, not a new Goal.
Constraint Context includes resource, authority, time, and capability limits.
Risk Context and Unknown Context are candidates with support and uncertainty.

## Reality boundary

Reality is an evidence-grounded description of facts. Situation is a
contextual interpretation of those facts relative to Self, Field, and Goal.
Reality is not Situation, and Situation is not Reality. A fact such as
“someone is ahead” may support the Situation Candidate “the person may affect
current passage”; it does not directly create a Decision or Action.

Situation Confidence must include Evidence Support, provenance, uncertainty,
and Unknown. A hypothesis such as “this is a friend” remains a hypothesis
unless separately admitted as evidence. Experience may provide a reference,
but current Reality Evidence has priority.

## Boundaries

Situation Understanding does not own Goal, Value, Decision, Action, Prediction,
Personality, Emotion, or Reality State mutation. It cannot issue a Decision,
recommend an Action, or silently remove Unknown. The Reducer remains the sole
State mutation authority. The Reducer remains the sole State mutation authority.
New evidence produces a Situation Reassessment Candidate rather than a direct
state mutation.
