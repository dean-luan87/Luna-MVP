# Cognitive Field Representation Architecture Plan v1

## Position

`Cognitive Field Representation Candidate` is Luna's dynamic, context-scoped **minimum sufficient cognitive view** of a current environment. It is neither a database, knowledge graph, Memory system, Fact store, Field State, nor an executable Decision surface.

This naming distinguishes two layers that must not collapse:

```text
Admitted Event -> Reducer -> Field State -> derived Field Snapshot
                                      |
                                      | governed, read-only references
                                      v
Current Cognitive Context + Primitive/Concept candidate references
                                      -> Cognitive Field Representation Candidate
```

The existing Field Kernel/Read Model remains the Current World Representation owner for governed State and Snapshot. The new planned Candidate is a downstream, read-only cognitive-query composition. It may describe what is currently relevant and uncertain for bounded understanding, without asserting that its candidate overlays are world truth.

## Field definition

A **Field** is a bounded physical, social, task, temporal, and relationship context in which Luna organizes current information. A Field is not simply a map rectangle, a database row, or a model label. Its identity and structural scope remain governed by the existing Field Kernel contract.

The boundary of a current Field Representation Candidate is declared by an existing `field_ref`, immutable `context_ref`, optional derived `snapshot_ref`, task/goal/attention scope, valid-time scope, spatial scope, and explicit exclusions or unknowns. A candidate must not invent a Field boundary from external output.

## Responsibilities

The planned representation may organize:

- Field identity and bounded Context references;
- selected Entity/Relation/State Primitive Candidate references;
- selected Concept Candidate and Field-Concept Binding references;
- existing structural relation and governed State/Snapshot references;
- temporal and spatial references, attention priority, relevance, uncertainty, provenance, and trace;
- risk and task-relevance **candidates** only.

It does not permanently save knowledge, learn, form Experience, update Memory, admit Facts, mutate State/Snapshot, execute Decisions/Actions, or invoke external capabilities.

## Relevance partition

Every selected or excluded reference is labelled by its current contextual role, not its truth value:

| Relevance class | Meaning | Retention rule |
| --- | --- | --- |
| `primary_now` | Needed for the current Field/Task/Goal/Attention scope | Include with source, reason, uncertainty, and trace |
| `peripheral_now` | In scope but not currently central | Retain as recoverable reference; do not discard or promote |
| `deferred_candidate` | May become relevant under a future Context, not currently selected | Retain an explicit deferral reason and review trigger |
| `excluded_for_current_context_only` | Not selected for this view | Recoverable exclusion only; not deletion or irrelevance claim |

Attention is relevance allocation only. It is not truth confidence, State authority, or an Action command.

## Relationship to Field Kernel and Reducer

The Candidate may read governed Field Snapshot/History query references through the existing Read Model and attach traceable candidate overlays. It never becomes a Reducer input or a Snapshot update command. Environment State Candidates remain references to uncertain Primitive/Concept material; only Reducer output is Field State.

```text
Primitive / Concept Candidate + Context / Temporal / Spatial / Task references
                + governed Field Snapshot reference
  -> Cognitive Field Representation Candidate (read-only, candidate-only)
  -> future Cognitive Analysis read-only input
```

Any later proposal to affect a Field must become a separately governed Field Event Candidate and traverse Admission, Temporal Validity, and the Reducer. This plan creates no conversion path.

## Non-goals

No runtime, schema implementation, provider/model binding, real Evidence ingestion, Field Kernel or Reducer modification, State/Snapshot update, temporal rewrite, Learning, Hive, Memory, Decision, or Action integration is authorized.
