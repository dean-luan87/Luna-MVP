# Cognitive Memory Architecture Model v1

## Position

Memory is not a database and does not store all history. It organizes
Experience references for the current Field, Time, Self, Goal, Task, and
Context. It supplies relevant past information to Attention and Situation
without becoming Reality, Decision, Goal, or Action.

The governing precedence is:

```text
Reality > Memory
```

Current Reality always overrides Memory. A remembered exit cannot override a
wall or a current closure. Memory is a bounded reference candidate with source,
time, confidence, scope, provenance, Unknown, conflict, and decay metadata.

## Core chain

```text
Experience Candidate
  ↓
Memory Admission
  ↓
Memory Storage
  ↓
Memory Retrieval
  ↓
Current Field Context
  ↓
Attention / Situation Support
```

Memory Admission is selective and evaluates value, stability, reusability, and
risk. Memory Retrieval is Field-driven, not a search of all history. Retrieved
Memory remains supporting context and must be reconciled with current Reality.

## Cross-Field information reuse boundary

Memory and Experience may eventually supply reusable entity/category knowledge
or Field-pattern candidates across Fields. That reuse must not transfer the
previous Field's meaning, ownership, role, function, or relation into the
current Field without current Field/Context/Role/Goal evaluation. The
canonical rule is [Field-Conditioned Entity Semantics & Cross-Field Information Reuse Principle v1](../field_conditioned_entity_semantics_and_cross_field_information_reuse_v1.md).

This is an architectural relation only; it does not implement a Field Cache,
cross-Field resolver, Memory mutation, Experience mutation, or Rumination
Runtime.

## Memory classes

- Working Memory represents the current Cognitive Field and short-lived task
  context.
- Episodic Memory retains bounded events and Outcomes with time and provenance.
- Field Memory retains validated patterns about a Field, such as entrances,
  flow, and recurring constraints; it is not a Field Rule.
- Semantic Memory retains abstract, validated knowledge candidates such as a
  common airport security sequence; it is not current Reality.
- Self Memory retains historical Capability, Self State, and Identity context;
  Identity continuity is immutable by Memory.
- Relationship Memory is a placeholder interface only; Social Runtime is out
  of scope.

## Retrieval contract

```text
Current Field
  + Goal
  + Task
  + Attention
  ↓
Memory Query
  ↓
Relevant Memory
```

Attention supplies relevance and resource candidates. Retrieval returns scoped
items with confidence, recency, provenance, Unknown, and conflict. Memory does
not proactively appear, create a Goal, make a Decision, or execute Action.

## Decay and conflict

Decay combines Time, Confidence, Importance, Reuse, and Contradiction. Decay is
not simple deletion; an old important event may remain archived and retrievable
as a lower-confidence historical candidate. Conflicts follow Current Reality >
Recent Valid Memory > Old Memory. Conflicts are preserved, not silently merged.

## Interfaces and prohibitions

Experience enters through Memory Admission; Memory returns Pattern and Context
Candidates to Attention and Situation. Adaptation may be suggested only after
governed retrieval and current-Reality reconciliation.

No automatic learning, Model Training, model-weight modification, Emotion
Runtime, Role System, Social Runtime, B Route, Prediction, or Action Runtime is
implemented. No database implementation or Memory Runtime is implemented.

Memory does not own Goal, Decision, or Action. Current Reality > Recent Valid
Memory > Old Memory. Conflict is preserved. Emotion Runtime and No Memory
Runtime are out of scope.

Current Reality > Recent Valid Memory > Old Memory. No Memory Runtime.
