# Field Kernel Integration Contract v1

## 1. Phase Position

- Phase: `Phase-A2.3-Field-Kernel-Contract-Integration-Planning-v1-001`
- Execution Mode: Planning Only
- Module: L1 Cognitive Flow / Field Kernel
- Status: system-composition contract pending human review

This document freezes the internal composition contract for Field Kernel. It creates no code, runtime, runner, verifier, database, model connection, or real-data integration.

## 2. Field Kernel Position

Field Kernel is Luna's **Current World Representation Core**. It organizes governed world change into a current Field representation and answers:

> What does Luna currently represent this Field as being like?

It does not answer why the state exists, what action should be taken, or what may happen in the future. It is not a World Model, Knowledge Base, Database, Cognitive Analysis module, or Decision module.

## 3. Frozen End-to-End Data Flow

```text
Cognitive Primitive
  -> Field Event Candidate
  -> Field Event Admission
  -> Admitted Event
  -> Field State Reducer
  -> Field State
  -> Temporal Evolution
  -> Field Snapshot
  -> Read Model Query
```

Each arrow is unidirectional. A downstream module may not mutate, re-admit, reinterpret, or feed a write command back into an upstream module. In particular:

- Field Kernel does not accept raw Cognitive Primitive objects or Field Event Candidates for State mutation.
- Field Event Admission is the sole Candidate Event to Admitted Event gate.
- Field State Reducer is the sole Field State mutation authority.
- Temporal Evolution represents State versioning and history after reduction; it does not produce State.
- Snapshot is derived and read-only; it cannot become a State source.
- Read Model performs governed queries; it cannot read raw events or write Field Kernel objects.

## 4. Field Kernel Composition

```text
                         Field Kernel
                              |
              +---------------+---------------+
              |                               |
       Field Structure                 Field Evolution
              |                               |
    Field Identity / Unit / Relation   State Version / Transition / History
              \                               /
               \                             /
                +------ governed Field State -+
                              |
                       Field Snapshot
                              |
                    Read Model Query Layer
```

`Field State` is the common governed anchor, not a shared mutable object. Field Structure provides representation scope; Field Evolution provides version and temporal context. Both consume or describe Reducer-owned State under declared boundaries.

## 5. Internal Input / Output Contracts

| Component | Accepted inputs | Outputs | Cannot accept or emit |
| --- | --- | --- | --- |
| Field Identity | Governed Field Reference and identity provenance | Field Identity | State value, causal conclusion, direct State mutation |
| Field Unit | Field Identity, bounded structural attributes, provenance | Field Unit | final Entity truth, State mutation |
| Field Relation | Field / Unit references, structural provenance | Field Relation | causal relation, value judgement, State mutation |
| Field State | Existing Reducer Output only | Reducer-owned current State representation | raw event, model output, Cognitive Analysis/Experience/Hive output |
| Temporal Evolution | Reducer-originated State Version, transition source, valid-time and provenance | Transition Record, History Projection | new State, causal explanation, prediction |
| Field Snapshot | Identity, Units, Relations, current Field State, Temporal Context | derived Snapshot | persistent State, mutation command |
| Read Model Query | Snapshot and declared query scope | Current or future Historical View result | raw Event query, direct store bypass, State write |

## 6. Field Identity Contract

### Input

- Field Reference;
- declared physical, social, task, and relationship context;
- evidence / source / trace provenance compatible with Field Kernel boundaries.

### Output

- Field Identity that establishes **what this Field is** and its representation scope.

### Forbidden behavior

- defining what the Field's current State is;
- using a map label or model classification as final identity without governed provenance;
- modifying Field State;
- generating a Hypothesis, Experience, or Decision.

## 7. Field Unit and Relation Contract

Field Unit describes a manageable part of a Field. Field Relation describes structural association between scoped Field/Unit references.

```text
Allowed: shop belongs_to shopping_mall
Forbidden: shop closure causes shopping_mall failure
```

The first is a structural relationship. The second is a causal explanation and belongs outside Field Kernel, under a future Cognitive Analysis contract.

## 8. Field State Contract

Field State has one production source:

```text
Admitted Event -> Field State Reducer Output -> Field State
```

A Field State representation must retain at least:

- State value;
- State Valid Time;
- Evidence References;
- source-chain and trace provenance;
- Reducer / reduction provenance;
- compatible State Version reference when Temporal Evolution is present.

The following must not generate or write Field State: Cognitive Analysis, external model/capability, Experience System, Hive Experience Field, Field Snapshot, Read Model, or Temporal Evolution.

## 9. Temporal Evolution Contract

Temporal Evolution receives Reducer-originated State Version representations and produces descriptive Transition Records and read-only History Projections.

It may organize:

- predecessor / successor version links;
- State Valid Time and explicit time uncertainty;
- governed transition sources;
- expiry and archival representation;
- history projection.

It must not generate a new State, mutate a State, explain why a State changed, predict future State, infer Experience, or decide an action.

## 10. Snapshot Generation Contract

```text
Field Identity + Field Unit + Field Relation + current Field State + Temporal Context
  -> Field Snapshot
```

The Snapshot is a derived, read-only Current World Representation view. Its provenance must identify its structural, State, and temporal sources and its snapshot time. It must not become:

- a State mutation authority;
- a second State store;
- an event log;
- a Hypothesis, Decision, or Experience object;
- a source that bypasses the Reducer on later reads.

## 11. Read Model Contract

Read Model is the **World Representation Query Layer**. Its planned query surfaces are:

| View | Input boundary | Result boundary |
| --- | --- | --- |
| Current View | Field Snapshot and declared query scope | read-only current representation with provenance |
| Historical View (future) | Field History Projection and declared temporal scope | read-only version/transition view with uncertainty retained |

Read Model must not query underlying raw Events directly, bypass Field Kernel to inspect State internals, mutate State, alter History chronology, or dispatch work.

## 12. Field Kernel Lifecycle

```text
Create Field
  -> Receive governed Event
  -> Reducer updates Field State
  -> Temporal Evolution organizes State version context
  -> Generate derived Snapshot
  -> Read Model Query
  -> read-only Historical Evolution projection
```

“Create Field” here means creation under a future governed Field Identity lifecycle; it does not authorize a model, primitive, or query consumer to invent a Field. “Receive governed Event” means an Admitted Event only.

## 13. Integration Guards

- No cyclic dependency: Snapshot and Read Model cannot write to Structure, State, Evolution, Admission, or Reducer.
- No raw ingress: Field Kernel State path never accepts raw Observation, Evidence, Primitive, or Candidate Event.
- No parallel state: Snapshot, History Projection, and Read Model results are derived views, not State owners.
- No semantic escalation: structural Relation is not causal relation; temporal sequence is not causal explanation; History is not Experience.
- No action escalation: read results may later be inputs to Cognitive Analysis only through a separate read-only interface.

## 14. Phase Boundary

This contract does not implement integration, change existing module behavior, or activate any interface. It awaits human architecture review before a later contract-integration implementation or DryRun phase.
