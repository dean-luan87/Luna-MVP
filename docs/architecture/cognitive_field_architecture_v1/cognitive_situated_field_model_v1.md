# Cognitive Situated Field Model v1

## Purpose

Situated Cognitive Field is the current local information environment for one
bounded cognitive context. It does not form Situation; it supplies the organized
inputs from which A Route may form Situation Candidate.

## Inputs

- Reality State;
- Self State;
- Goal Context;
- Rule Reference;
- Social Context;
- Emotion Influence Candidate.

## Output

Field State contains Relevant Reality, Self State, Goal Context, Rule Reference,
Social Reference, Emotion Influence Candidate, Unknown, validity, and Provenance.
It contains no Recommendation, Decision, Plan, Prediction, Outcome Evaluation, or
Action. It has no Decision output.

## Field-conditioned entity semantics

Stable entity or concept knowledge may be reused across Fields, but meaning is
conditioned by the current Field, Relation, Context, Role, and Goal/Task. A
Field-conditioned meaning is an interpretation candidate, not an intrinsic
Entity property or Field Truth. The canonical principle is recorded in
[Field-Conditioned Entity Semantics & Cross-Field Information Reuse Principle v1](../field_conditioned_entity_semantics_and_cross_field_information_reuse_v1.md).

Field context must not inherit ownership, function, value, role, or relation
from another Field merely because the class or appearance is the same.

## Emotion and social boundaries

Emotion may enter only as Attention Bias Candidate, Priority Influence Candidate,
or Relationship Weight Candidate. Social data may enter as Role Reference,
Relationship State, or Permission Context. Neither layer may modify Reality or
directly create a Decision. Role and relationship reasoning remain future Brain or
Emotional Engine work.
