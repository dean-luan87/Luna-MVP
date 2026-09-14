# Cognitive Field Representation Boundary Contract v1

## Accepted input references

Only the following reference forms may enter a future `CognitiveFieldRepresentationCandidateV1`:

- traceable Primitive Candidate;
- traceable Concept Candidate / validated Field-Concept Binding Candidate;
- immutable Current Cognitive Context reference;
- governed Field identity, Unit, Relation, State/Snapshot, Temporal Evolution query references;
- Temporal Reference and Spatial Reference with explicit uncertainty;
- authorized Task, Goal, and Attention context references;
- retained provenance, Evidence, source-capability, and trace references.

Raw Model Output, Provider Identity, raw Observation/Evidence payload, Memory, Fact Store, Decision, Action, State write target, database handle, and external service handle are prohibited inputs.

## Output

The only planned output is a candidate-only, read-only Cognitive Field Representation. It may be read by an authorized future Cognitive Analysis/Context consumer under L1 Candidate I/O, Traceability, Permission/Admission, and Consumer Governance. It cannot be written to Field Kernel, Reducer, Read Model, Memory, Learning, Hive, or Action systems.

## State and snapshot boundary

`Field Representation Candidate != Field State` and `Field Representation Candidate != Field Snapshot`.

Field State may be changed only through:

```text
Field Event Candidate -> Admission + Temporal Validity -> Admitted Event
-> Field State Reducer -> Field State
```

The planned Candidate cannot update a State, create a State Version, alter State Valid Time, update a Snapshot, rewrite temporal history, or become an alternate state store.

## Temporal and spatial boundary

Event Time, Observation Time, Admission Time, State Valid Time, Snapshot Time, and Context current-time reference retain their existing separate meanings. Missing, stale, ambiguous, or estimated time/location remains explicit. A temporal/spatial reference does not establish a Field boundary, State, map fact, causal explanation, prediction, or action.

## Permanent negative guards

1. Concept is not Field State.
2. Field Representation is not Fact.
3. Field Representation is not Memory.
4. Field Representation is not Decision.
5. Attention is not Action.
6. External Model Output cannot directly enter Field Representation.
7. Reducer remains the unique Field State authority.
8. Candidate confidence, relevance, and risk cannot grant admission or permission.
9. Unknowns/exclusions cannot be silently completed or treated as deletion.
