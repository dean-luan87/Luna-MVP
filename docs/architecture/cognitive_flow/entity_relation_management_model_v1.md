# Entity and Relation Management Model v1

## Fact-layer objects

Entity Management tracks an identity candidate, attributes, location reference,
validity, confidence, and provenance. Relation Management tracks a bounded
subject–predicate–object relation candidate, time window, confidence, and source.
Event and Change references may update either object through the Reducer.

```text
Evidence Fragments
      ↓
Entity / Relation Candidate
      ↓
Conflict and temporal alignment
      ↓
Current Entity / Relation State
```

## Boundary

Entity and Relation State describes what is observed and how observed objects are
associated. It does not infer social meaning, intent, risk value, action, or
Decision. Semantic interpretation remains in A Route and Brain.
