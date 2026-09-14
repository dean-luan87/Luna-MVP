# Field Kernel Object Relationship v1

## 1. Scope

This document defines the first-version conceptual object graph for Field Kernel. It is a planning contract, not a schema, runtime object model, database design, or protocol implementation.

The graph represents the **current world representation** available to Luna. It does not define causal understanding, predictive simulation, or final facts outside the governed Field State lifecycle.

## 2. Object Graph

```text
Field Identity
  ├─ organizes -> Field Unit [0..n]
  ├─ has context -> physical / social / task / relational
  ├─ is described by -> Field State [0..n]
  └─ is represented by -> Field Snapshot [0..n over time]

Field Unit
  ├─ belongs to -> Field Identity
  ├─ participates in -> Field Relation [0..n]
  ├─ may reference -> Entity Candidate [0..n]
  └─ is described by -> Field State [0..n]

Field Relation
  └─ links -> Field Identity and/or Field Unit references

Field State
  └─ describes -> Field Identity, Field Unit, or an eligible relation target

Field Snapshot
  └─ composes -> one Field Identity + relevant Units + Relations + current States
```

`Entity Candidate` remains a Cognitive Primitive / future Field Identity concern. In A2.0 it can be referenced by a Unit but is not promoted into a final entity, nor does it create a Field or Field State by itself.

## 3. Field Identity

### Definition

Field Identity describes one cognitive Field: the bounded environment against which Luna organizes its current representation.

### Minimum planned attributes

| Attribute | Meaning | Boundary |
| --- | --- | --- |
| `field_id` | Stable Field identifier within its declared contract | Must not be inferred as a fact merely from a map/model label. |
| `field_type` | Declared candidate category of Field | Requires canonical vocabulary and provenance. |
| `parent_field` | Optional enclosing Field reference | Represents structure, not automatic spatial containment truth. |
| `identity_refs` | Evidence, admission, or governed identity references | Preserve provenance; do not substitute references with confidence alone. |
| `semantic_context` | Physical, social, task, and relational context descriptors | Context supports representation scope; it is not causal reasoning. |

### Frozen meaning

Field Identity is **not** merely a map region, database partition, model classification, or list of entities. A Field may contain physical location, social setting, task framing, and relationships together. It organizes representation without claiming to explain it.

## 4. Field Unit

### Definition

Field Unit is a manageable internal component of a Field.

Examples: a shopping-centre entrance, shop, service desk, parking area, airport gate, or street crossing.

### Minimum planned attributes

| Attribute | Meaning | Boundary |
| --- | --- | --- |
| `unit_id` | Stable unit identifier within its parent Field contract | Does not independently confer final entity identity. |
| `unit_type` | Declared unit category | Must retain compatible provenance when derived from candidate inputs. |
| `parent_field` | Required Field Identity reference | A Unit cannot be queried outside declared Field scope without a governed cross-field contract. |
| `relation_refs` | References to declared Field Relations | References do not assert causality or permanent topology. |

A Field therefore is not one monolithic object: it is an organizing structure that contains manageable Units. Entity Candidates may be associated with Units, while Entity identity remains a distinct lifecycle concern.

## 5. Field Relation

### Definition

Field Relation describes a current, scoped relationship between Field-representation references.

Examples: `contains`, `belongs_to`, `connected_to`, and `near`.

### Minimum planned attributes

| Attribute | Meaning | Boundary |
| --- | --- | --- |
| `subject` | Source Field or Unit reference | Must resolve within the declared representation scope. |
| `relation` | Canonical relationship predicate | Does not express causality, preference, or decision. |
| `object` | Target Field or Unit reference | Must retain compatible provenance and scope. |

Relationship validity, evidence, and time context must be carried by the applicable state/provenance contract. A graph edge is not automatically a permanent fact.

## 6. Field State

### Definition

Field State is the current effective description of one Field, Field Unit, or eligible relation target within a defined validity window.

### Minimum planned attributes

| Attribute | Meaning | Boundary |
| --- | --- | --- |
| `state_id` | Stable State record identity | State is not an event or evidence reference. |
| `target_ref` | Field, Unit, or eligible relation target described | Does not authorize arbitrary target creation. |
| `state_type` | Governed type of effective description | Must not encode a Hypothesis or Decision. |
| `value` | Current described value | Not a causal explanation or value judgement. |
| `valid_time` | Time window in which the State is effective | Temporal eligibility remains admission-side authority. |
| `evidence_refs` | Supporting provenance references | Evidence does not independently establish State. |
| `provenance` | Admission, source-chain, trace, and reduction lineage | Must survive read and snapshot composition. |

Field State is not a facts database. It is Luna's current, governed world description produced from an Admitted Event through the sole Field State Reducer.

## 7. Field Snapshot

### Definition

Field Snapshot is the complete minimum representation of one Field at a stated generation time for a read/query purpose.

### Minimum planned attributes

| Attribute | Meaning | Boundary |
| --- | --- | --- |
| `snapshot_id` | Identity of this generated representation | It does not create independent state authority. |
| `field_ref` | Field Identity represented | Query scope must be explicit. |
| `units` | Relevant Field Units | Read composition only. |
| `relations` | Relevant Field Relations | Read composition only. |
| `states` | Current Field States in scope | Derived from Reducer-owned state. |
| `generated_at` | Representation generation time | Does not revise State validity. |
| `provenance` | Composition, state, evidence, admission, and trace lineage | Must not be dropped for convenience. |

### State and Snapshot boundary

| Field State | Field Snapshot |
| --- | --- |
| Describes one effective condition of one target. | Composes multiple relevant Units, Relations, and current States for one Field. |
| Example: `entrance = closed` in a valid time window. | Example: an airport representation containing entrance closure, higher foot traffic, and restricted-area access. |
| Mutated only by the Field State Reducer from Admitted Events. | Generated as a read/query object; never a separate active state store. |
| May be consumed by snapshot composition. | May be consumed by Cognitive Query and later Cognitive Analysis, read-only. |

## 8. Ownership and Mutability Matrix

| Object | Principal contractual owner | May be created/updated by | Must not be changed by |
| --- | --- | --- | --- |
| Field Identity | Field Kernel representation contract | Future governed Field identity lifecycle; no authority is granted in A2.0 | external model output, Cognitive Analysis, Hive, Read Model query |
| Field Unit | Field Kernel representation contract | Future governed structural lifecycle; no authority is granted in A2.0 | raw Observation, model label, Cognitive Analysis |
| Field Relation | Field Kernel representation contract | Future governed structural lifecycle; no authority is granted in A2.0 | causal reasoning, Experience, Hive, Read Model |
| Field State | Field State Reducer | **Existing Reducer only**, from an Admitted Event | all other modules, including Field Kernel composition |
| Field Snapshot | Field Kernel / Read Model query contract | Read-only composition from current governed structures | Snapshot consumer, model, Cognitive Analysis, Hive |

## 9. Explicit Object Non-Equivalences

- `Field Identity` is not a map polygon, storage key, or model-detected scene label.
- `Field Unit` is not automatically an `Entity`.
- `Field Relation` is not a causal explanation.
- `Field State` is not an Event, Observation, Evidence item, or Fact database.
- `Field Snapshot` is not a State store, event log, hypothesis graph, or action plan.
- A collection of Snapshot fields is not World Understanding.

## 10. Deferred Model Detail

The following are expressly deferred to later authorized contracts: stable Field identity admission, structural relation lifecycle, cross-Field composition, history retention, temporal evolution, confidence representation, attention context, and entity identity resolution. They must not be silently introduced by A2 implementation.
