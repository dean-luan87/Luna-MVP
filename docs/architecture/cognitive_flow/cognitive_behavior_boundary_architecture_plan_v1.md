# Cognitive Behavior Boundary Architecture Plan v1

## Purpose and position

Behavior Boundary Layer expresses Luna's current candidate behavior space under incomplete information. Its architectural flow is:

`Survival Constraint + Current Cognitive Context + Field Affordance + Belief State + Task Goal -> Behavior Boundary Candidate -> Future Action Candidate`.

It answers what behavior may be considered, restricted, unknown, or evidence-dependent. It does not select an action, grant permission, execute an action, mutate State, or replace future Decision governance.

## Inputs and output

Permitted references are Survival Constraint, Current Cognitive Context, Field, Field Identity/Affordance, Belief, Goal, Risk, required evidence, provenance, and trace. The output is only a `BehaviorBoundaryCandidateV1`; it is candidate-only, non-Fact, non-State, non-Decision, non-Action, and non-Memory.

## Responsibility partition

| Layer | Responsibility | Not responsible for |
| --- | --- | --- |
| Field Identity | Stable Field constraints | Current activity or action permission |
| Field Affordance | Possible behavior patterns under Identity | User intent or current authorization |
| Behavior Boundary | Current safe/restricted/unknown behavior space | Decision or Action execution |
| Future Decision | Selection from an admitted behavior space | Rewriting Boundary evidence |
| Reducer | Sole State mutation authority | Behavior control |

## Planning boundary

This phase defines architecture only. Runtime, Decision, Action, Permission, Field Kernel integration, Reducer integration, model/provider access, Memory, Learning, and Hive behavior are not authorized.
