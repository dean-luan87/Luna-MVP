# Field Kernel Authority & Contract Plan v1

## 1. Phase Position

- Phase: `Phase-A2.0-Field-Kernel-Authority-Contract-Planning-v1-001`
- Execution Mode: Planning Only
- Status: architecture contract proposal pending human review
- Constitutional references:
  - `docs/architecture/LUNA_ENGINEERING_ARCHITECTURE_CONSTITUTION_V1.md`
  - `docs/architecture/LUNA_CANONICAL_TERMINOLOGY_REGISTRY_V1.md`
  - `docs/architecture/LUNA_EXISTING_ASSET_ALIGNMENT_PLAN_V1.md`

This document freezes the first Field Kernel contract before implementation. It does not create a runtime, protocol implementation, storage model, runner, verifier, or integration change.

## 2. Position: Current World Representation, Not World Model

Field Kernel is Luna's **World Representation Core**. Its responsibility is to answer:

> What does Luna currently represent this Field as being like?

It is not the External World itself, a general-purpose World Model, a knowledge base, or an understanding engine. The frozen cognitive boundary is:

```text
External World
  -> Evidence
  -> Field Kernel
  -> Current World Representation
  -> Cognitive Analysis
  -> World Understanding
```

Field Kernel represents the currently governed, time-bounded world description. Cognitive Analysis may use that representation to ask *why*, compare explanations, and assess possible futures. It must not turn Field Kernel into an inference or decision owner.

## 3. Frozen Ingress and Representation Chain

```text
External Capability
  -> Observation
  -> Evidence
  -> Cognitive Primitive
  -> Field Event Candidate
  -> Field Event Admission
  -> Admitted Event
  -> Field State Reducer
  -> Field State
  -> Field Snapshot
  -> Cognitive Query
```

Rules for this chain:

- Field Kernel accepts no raw Observation, raw Evidence, Cognitive Primitive, or Field Event Candidate as a state-mutation input.
- `Admitted Event` is the only event form eligible for the existing Field State Reducer.
- Temporal eligibility is assessed before reduction by the existing Field Event Admission / Temporal Validity boundary.
- Evidence, source-chain, trace, and temporal context remain provenance inputs; none independently grants state mutation authority.
- A Field Snapshot is a representation derived from current governed structure and state. It is not a new state store.

## 4. Field Kernel Responsibilities

Field Kernel owns the organization and representation contract for the following current-world structures:

1. Field Identity and its bounded context.
2. Field Units and their declared relationships.
3. The composition of Reducer-owned Field State into a Field Snapshot.
4. A governed query shape for Current World Representation.
5. Preservation of provenance and temporal meaning at the representation boundary.

Field Kernel does **not** own a second reducer, a storage topology, a new admission authority, or an alternate source of Field State.

## 5. Input Contract

| Input | Required source / owner | Field Kernel use | Boundary rule |
| --- | --- | --- | --- |
| Admitted Event | Field Event Admission | Sole event input eligible for state reduction | Must retain its admission result and must not be re-admitted or replaced by raw input. |
| Temporal Metadata | Temporal Validity through Admission | Preserve validity window, ordering, expiry, and evaluation context in representation provenance | Field Kernel does not duplicate temporal eligibility judgment. |
| Evidence Reference | Evidence Chain / admitted-event provenance | Preserve `evidence_refs`, source-chain, and trace lineage for state and snapshot context | Evidence is not Fact and cannot mutate state directly. |
| Structural context | Declared Field Identity, Unit, and Relation contract | Organize representation targets and query scope | No implicit entity, relation, or field creation from a model label. |

The future implementation contract must reject or defer an event that has not reached the admitted-event lifecycle status. It must not silently coerce a Candidate into an admitted input.

## 6. Output Contract

| Output | Meaning | Producing authority | Mutability rule |
| --- | --- | --- | --- |
| Field State | Current effective description of a Field, Unit, or eligible target | **Field State Reducer only** | May change only through a new admitted event reduced by the existing Reducer. |
| Field Snapshot | Minimal, time-stamped composition of a Field's units, relations, and current states | Field Kernel representation composition | Derived query object; must not become an independent authoritative state store. |
| World Representation Query Result | Read-only response describing the requested current representation and its provenance | Read Model / Field Kernel query contract | Must not mutate state, dispatch work, or produce a Hypothesis or Decision Candidate. |

`Field State` is a logical output of the Field Kernel boundary but its mutation is exclusively performed by the existing Field State Reducer. `Field Kernel` composes and exposes representation; it does not claim the Reducer's authority.

## 7. Lifecycle Contract

| Lifecycle point | Owner | Field Kernel role | Forbidden transition |
| --- | --- | --- | --- |
| Observation and Evidence | External Capability / Cognitive Primitive | None beyond provenance preservation | Observation or Evidence directly becoming Field State. |
| Field Event Candidate | Upstream candidate producer | Not accepted for reduction | Candidate directly updating State. |
| Admission and temporal assessment | Field Event Admission / Temporal Validity | Receive only its admitted output | Re-running, bypassing, or weakening admission. |
| State reduction | Field State Reducer | Organize the resulting state in the Field representation | Creating a competing mutation path. |
| Snapshot composition | Field Kernel / Read Model boundary | Build current, minimal representation for a query | Persisting Snapshot as a second active state authority. |
| Cognitive query | Read Model | Serve read-only representation to downstream cognition | Query result directly becoming Hypothesis, Decision, or Action. |

Revision, expiry, retraction, and ordering remain governed by the existing admission, temporal, reducer, and Read Model contracts. A2 implementation must map to those contracts rather than redefine them.

## 8. Unique Mutation Authority

The following authority is frozen:

```text
Admitted Event
  -> Field State Reducer
  -> Field State
```

Only the existing **Field State Reducer** may modify Field State. The following must not directly write Field State:

- Cognitive Analysis;
- Hypothesis or Information Gap processing;
- Experience System or Hive Experience Field;
- External Capability, model, OCR, SLAM, LLM, VLM, or other organ;
- Cognitive Primitive Layer;
- Field Kernel orchestration or snapshot composition;
- Read Model or Cognitive Query consumer.

## 9. Existing Module Contract Relationship

```text
Field Event Admission + Temporal Validity
  -> eligible Admitted Event
  -> Field State Reducer (unique mutation authority)
  -> Field Kernel organization and Snapshot contract
  -> Field State Read Model (World Representation Query Layer)
  -> Cognitive Analysis (read-only consumer)
```

| Existing module | Frozen relationship to Field Kernel |
| --- | --- |
| Field Event Admission | Cognitive Admission Boundary. It owns candidate eligibility and supplies the only event form that may reach the Reducer. |
| Temporal Validity | Admission-side temporal authority. Its time decision is preserved, not duplicated inside Field Kernel. |
| Field State Reducer | Field Kernel Mutation Authority. It remains the singular Field State modifier. |
| Field State Read Model | World Representation Query Layer. It exposes a read-only, compatible surface for State, Snapshot, and query results. |
| Evidence Chain | Provenance substrate. It supplies non-substitution, source-chain, evidence-reference, and trace semantics. |
| Cognitive Primitive Layer | Upstream candidate organizer only. Its objects do not establish Field State. |
| Cognitive Analysis | Downstream read-only consumer. It may form Hypotheses but has no representation mutation right. |

## 10. Future Reservations and Present Non-Goals

The contract may reserve names and compatibility points for:

- Temporal Evolution;
- Field History;
- State Confidence;
- Attention Context.

This phase and the first Field Kernel implementation must not implement or assign authority for:

- Hypothesis, causal explanation, or prediction;
- Experience Episode, Experience Kernel, or Hive behavior;
- Decision Candidate or Action;
- databases, storage integration, external data ingestion, or model integration;
- a replacement Reducer, Read Model, Admission module, Temporal Validity module, Manifest, Baseline, Registry, Protocol, or Lifecycle.

## 11. Human Review Questions

1. Confirm that Field Kernel is the Current World Representation layer, not Luna's World Model or World Understanding owner.
2. Confirm that Field Snapshot remains a derived query object and never becomes a parallel state store.
3. Confirm that A2 implementation must adapt to the existing Reducer and Read Model rather than create replacements.

## 12. Phase Stop Boundary

This planning artifact freezes no runtime behavior and grants no implementation or production authority. Human review is required before `Phase-A2-Field-Kernel-Implementation-v1-001` is entered.
