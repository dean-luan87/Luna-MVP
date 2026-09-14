# Cognitive Constraint Layer Architecture Plan v1

## Purpose and position

Cognitive Constraint Layer is a candidate-only cognitive-resource and behavior-constraint layer. It describes whether a current cognitive path should remain open, be reduced, be paused, accept unresolved information, or require a safer alternative.

Its frozen flow is:

`Survival Constitution -> Current Cognitive Context -> Attention Selection -> Information Value Evaluation -> Cognitive Strategy -> Reasoning / Hypothesis / Belief -> Cognitive Constraint Candidate -> Behavior Boundary Candidate -> Future Behavior Candidate`.

The layer does not decide, execute, permit, or enforce. It produces an explicit `CognitiveConstraintCandidateV1` for future governed consumers.

## Responsibility partition

| Layer | Owns | Does not own |
| --- | --- | --- |
| Survival Constitution | Highest constraint direction | Action selection or execution |
| Cognitive Constraint | Candidate constraints on cognition/exploration/behavior space | Decision, Permission, safety enforcement |
| Behavior Boundary | Current behavior-space expression | Candidate selection or execution |
| Future Behavior Candidate | Possible behavior expression | Decision or Action |
| Reducer | Sole State Mutation Authority | Cognitive constraint evaluation |

## Planning-only boundary

No Runtime, Constraint Engine, Decision Engine, Action Gate, Safety Controller, model/provider call, Agent loop, Field Kernel integration, Reducer integration, State mutation, Memory, Learning, Hive, or Library runtime behavior is authorized.
