# Cognitive Concept–Field Integration Architecture Plan v1

## Phase position

This is a Planning Only phase for `Phase-A3-Field-Concept-Integration-Architecture-Planning-v1-001`. It defines how a traceable Concept Candidate may be **read and referenced** by a future Field Representation consumer. It creates no runtime, storage, Field Kernel integration, State write, or new admission authority.

## Architectural relationship

```text
Translation -> Primitive Candidate -> Concept Candidate
                                      |
                                      | read-only, governed reference
                                      v
Current Cognitive Context / Field Representation Query Surface
                                      |
                                      v
Field Snapshot remains Reducer-owned-State composition
```

Concept Layer owns meaning, pattern, and situation candidates. Field Kernel owns the organization of current governed world representation. Reducer remains the only Field State mutation authority. A Concept Candidate is not an event, Fact, State, Snapshot, or Decision and cannot become a State input by reference alone.

## Field integration scope

The proposed integration object is a `FieldConceptReferenceBindingCandidate`: a read-only association between a Concept Candidate and an existing Field/Unit/Context/Snapshot reference. It is an optional cognitive-query annotation, outside the authoritative Field State and Snapshot storage paths.

| Concern | Planned binding behavior | Prohibited behavior |
| --- | --- | --- |
| Concept reference | Retain `concept_ref`, primitive and provenance references | Convert the Concept into an Admitted Event, Fact, or State |
| Context binding | Bind only to immutable `context_ref` and `snapshot_ref` scope | Modify Current Cognitive Context or Snapshot |
| Temporal binding | Retain declared source valid-time/history-window references and unknowns | Rewrite State Valid Time, infer missing time, predict evolution |
| Spatial binding | Refer to existing Field/Unit/relation/location references | Create Field Identity, Unit, map state, or location truth |
| Confidence | Display candidate confidence as non-authoritative metadata | Treat confidence as admission, truth, or State confidence |
| Uncertainty | Preserve uncertainty and stale/unknown markers | Suppress uncertainty or force representation completeness |
| Trace | Carry Concept, Primitive, Translation/Evidence, Context, Field/Snapshot trace | Strip, replace, or synthesize lineage |

## Current World Representation effect

Concepts can enrich a future **Cognitive Query View** with optional candidate interpretation context. They do not alter the `Field Snapshot`, `Field State`, temporal history, or Read Model result authority. The authoritative representation remains the existing chain:

```text
Field Event Candidate -> Admission / Temporal Validity -> Admitted Event
-> Reducer -> Field State -> derived Field Snapshot -> Read Model query
```

Any Concept-derived proposal that could eventually motivate a Field Event must follow a separately governed Candidate Event and Admission path. This plan grants no such conversion.

## Concept lifecycle at the Field boundary

```text
Concept Candidate -> Validated Candidate -> Historical Concept Reference
```

- **Concept Candidate**: traceable interpretation candidate; may be referenced only with all declared limitations.
- **Validated Candidate**: schema, provenance, boundary, and consumer validation passed; validation does not mean Fact admission, semantic truth, or State eligibility.
- **Historical Concept Reference**: read-only retained lineage associated with a historical Context/Snapshot scope; it is not Field History, Experience, or Memory.

## Future Language compression boundary

Only a governed Concept reference may later be encoded as a Language expression candidate. Compression must retain the Concept identity, scope, uncertainty, provenance, and trace. It cannot feed back to create a Concept, State, Fact, Field structure, or shared Hive vocabulary in this phase.

## Non-goals

No Field Kernel or Reducer modification, State/Snapshot write, real Concept Runtime, real Evidence, Learning, Hive, language runtime, registry, protocol, or permission-runtime work is authorized.
