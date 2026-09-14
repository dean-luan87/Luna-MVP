# Field Kernel Architecture Plan v1

## Position

Field Kernel is Luna's current environment organization layer. It is not a database, knowledge base, Memory, map system, Fact repository, or decision engine. It organizes governed current representation and candidate context into a read-only **Current Field View**.

To preserve existing A2 authority, Current Field View has two non-interchangeable planes:

```text
Admitted Event -> Reducer -> Field State -> derived Field Snapshot
                                         + Context / Primitive / Concept / Field Representation Candidates
                                         -> Current Field View (read-only query composition)
```

The first plane is governed State/Snapshot representation. The second is a candidate overlay. Candidate aggregation may select, group, and expose references for a bounded query; it cannot assert truth, alter Snapshot, or become a State input.

## Responsibilities

Field Kernel may organize Field/Unit/Relation references, governed State/Snapshot query references, Context scope, candidate clusters, temporal awareness, spatial references, attention context, conflicts, unknowns, and task relevance. It may classify material as `current`, `historical`, `possible`, or `unknown` as representation status only—not as fact, prediction, or decision.

It does not determine final Fact, execute Decision/Action, write Memory/Learning, invoke models, or mutate State.

## Candidate aggregation and conflict

Aggregation is reference-preserving: every selected Primitive/Concept/Field Representation Candidate retains provenance, trace, uncertainty, time/spatial scope, and candidate status. Conflicting candidates coexist as `conflicting_candidate_set`; Kernel must surface conflict, limitation, or Information Gap rather than select truth. Unknowns are explicit; historical material is a read-only Temporal Evolution reference; possible material is candidate-only.

## Future consumer boundary

Prediction and Decision layers may later read a bounded Current Field View under their own contracts. They cannot use the view as Decision authority. Any future State-affecting proposal must leave the view as a Field Event Candidate and traverse Admission, Temporal Validity, and Reducer.
