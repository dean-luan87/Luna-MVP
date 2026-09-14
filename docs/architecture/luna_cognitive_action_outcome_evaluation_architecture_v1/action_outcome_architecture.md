# Luna Action Outcome Evaluation Architecture v1

## Position

Outcome Evaluation closes the A-route loop after an Action has been admitted
by a future Action Runtime. It separates the execution fact from the
interpretation of that fact:

```text
Decision
   ↓
Action Execution (future)
   ↓
Outcome Observation
   ↓
Outcome Evaluation Candidate
   ↓
Experience Candidate
   ↓
Memory / Schema Candidate
```

Action is an attempt or execution request; Outcome is what Reality returned.
Outcome Evaluation asks how the result relates to the Goal, expected outcome,
safety, resources, prediction accuracy, and user impact. It cannot rewrite
Reality or directly mutate Memory, Schema, Belief, Self, or Personality.

## Closed-loop boundary

Expected Outcome comes from the Decision Candidate. Actual Outcome and
Evidence come from Reality Validation or a future Action Runtime result. The
difference is retained, including unknowns and provenance. Evaluation emits
Learning Signal, Experience, Memory, Schema, Belief, and Self adjustment
candidates only. Consolidation and governance remain separate authorities.

## Phase limits

This directory defines contracts only. It does not implement Action Runtime,
Outcome Collector, Learning Runtime, automatic Memory writes, automatic Schema
updates, Emotion, B Route, or hardware/provider calls.
