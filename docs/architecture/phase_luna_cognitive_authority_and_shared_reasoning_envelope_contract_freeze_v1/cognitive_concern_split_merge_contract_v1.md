# Cognitive Concern Split / Merge Contract

## NewConcernCandidate

A may produce a candidate containing:

- proposed concern ref;
- source concern ref;
- trigger or unresolved gap;
- source state version;
- scope and dependency refs;
- inherited evidence refs;
- reason for split;
- trace/provenance refs;
- candidate_only=true.

A cannot autonomously materialize the concern.

## Brain decision

Brain decides one of:

- ADMIT;
- REJECT;
- DEFER;
- MERGE_WITH_EXISTING.

The decision is global concern governance, not a Loop mechanical transition.

## Split semantics

A split request means that the current reasoning package contains a potentially
independent concern. Until Brain admits it, it remains a candidate reference
and cannot create another Loop, Task, Provider path or B recursive path.

## Merge semantics

Merge means cognitive identity convergence, not physical runtime state-tree
merge. After Brain-governed acceptance:

- one concern continues;
- the other becomes SUPERSEDED_BY_MERGE;
- inherited evidence remains read-only;
- local histories remain traceable;
- no Loop state is silently copied or mutated.

## B boundary

B branch is not a child concern. B may report a branch candidate to A. A may
request a concern split, but only Brain admits it.
