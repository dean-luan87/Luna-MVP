# Field-Conditioned Entity Semantics & Cross-Field Information Reuse Principle v1

## Status and scope

This is a documentation-only architectural addendum. It is not a new Phase,
Runtime, schema, contract, owner, resolver, cache, Memory mutation path, or
rumination mechanism.

The canonical principle is:

> Stable Entity Information should be reusable across Fields. Field-conditioned
> meaning must remain independent.

中文：场条件实体语义与跨场信息复用原则。

## Core distinction

```text
Reuse Identity / Knowledge != Reuse Field Meaning
```

Stable object or concept information, category knowledge, and validated
historical experience may be reusable across Fields. Meaning in a particular
Field remains jointly conditioned by:

```text
Field + Relation + Context + Role + Goal / Task
```

Ownership, function, use, value, role, spatial relation, social relation, task
meaning, and Field membership are not permanent intrinsic properties merely
because they were associated with an object in another Field.

## Example

The category knowledge for `cup` may be reused. Its situated interpretation is
not automatically reused:

| Field | Field-conditioned meaning candidate |
|---|---|
| Store | product / sellable object |
| Home | a person's private item / household utensil |
| Office | office supply / company-asset candidate |

These are candidate interpretations formed from the current Field and context,
not permanent properties of `cup`.

Two visually identical cups may share category knowledge while remaining
unresolved as physical instances. They do not thereby share an owner, use,
Field relation, or semantic meaning.

## Canonical relationship

```text
Stable Entity / Concept Knowledge
        +
Field-local Entity / Relation Candidate
        +
Context + Role + Goal / Task
        ↓
Field-Conditioned Meaning Candidate
```

`Field-Conditioned Meaning Candidate` is an interpretation candidate. It is
not an intrinsic Entity property, identity fact, Field Truth, or World Truth.

## Required non-equivalences

```text
Same Class != Same Physical Instance
Same Appearance != Same Entity Identity
Cross-Field Knowledge Reuse != Cross-Field Meaning Reuse
Entity Information Reuse != Field Relation Reuse
Stable Object Knowledge != Field-conditioned Semantic Meaning
```

These rules prohibit the following shortcuts:

- YOLO class → Entity identity;
- detection ID → persistent object identity;
- a Field-local relation → permanent object property;
- Memory retrieval → current Field Truth;
- PCN reference → universal entity ownership;
- Task Target → canonical physical identity.

## Relation to `EntityCandidateV1`

The closed Subject Binding phase established:

```text
Detection / Evidence
  -> EntityCandidateV1
  -> L1 subject_ref_candidate
```

`EntityCandidateV1` remains an observation-linked cognitive candidate with
`identity_resolution_status=UNRESOLVED`. It does not yet provide cross-Field
entity resolution, physical instance identity, persistent object identity, or
Field-conditioned semantic relation resolution.

The L1 candidate can be reused as a reference candidate, but its Field meaning
must be re-evaluated under the current Field, Relation, Context, Role, and
Goal/Task. Reuse of the candidate reference is not reuse of a prior Field
interpretation.

## Relation to Memory, Experience, and future reuse

Future architecture may combine Field information reuse with Memory,
Experience, relation completion, Plan B, and Idle Attention / Cognitive
Rumination to reduce repeated observation and surface useful non-task
information. This remains a future architectural relation only.

This addendum does not implement Rumination Runtime, Field Cache, Memory or
Experience mutation, automatic relation completion, Plan B runtime, or a
cross-Field resolver.

Memory and Experience remain governed candidate/reference systems. Current
Reality and current Field evidence remain authoritative over recalled material.

## Long-term direction, not current metric

Task-time cognition remains:

```text
Goal-driven
  -> Minimum Sufficient Cognition
  -> Stop
```

With familiar Fields and spare cognitive resources, future reuse may support:

```text
Accumulated Field / Entity / Relation / Experience information
  -> reduce repeated observation
  -> selectively observe uncertainty, change, conflict, or low confidence
```

This is a long-term direction. No percentage such as “90% experience reuse” is
implemented or verified.

## Ownership and boundary

This principle does not change ownership of Field Truth, World Truth,
`EntityCandidateV1`, Memory, Experience, Target Binding, Field Reducer, or
Evidence Sufficiency. It does not authorize a candidate to mutate Field,
Memory, Experience, or PCN state.

