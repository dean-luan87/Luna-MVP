# Field Canonical Module Contract v1

## Adjudication

**Disposition: NARROW.** Field remains a canonical source-state boundary, but
its authority is limited to governed environmental/field state and its
deterministic transition lineage. It is not a general world model, truth
arbiter, context owner, or cognition engine.

## Canonical purpose

Field is Luna's governed operational representation of environmental entities,
relations, spatial/accessibility conditions, and location-linked changes after
their source events have passed the applicable admission boundary. Field owns
the versioned state-transition lineage for that representation and preserves
uncertainty, conflict, temporal validity, and provenance.

## Repository evidence

- `capabilities/midplatform/core/field_state_reducer/field_state_reducer_types_v1.py`
  defines Field state status, state types, temporal validity, provenance,
  conflict and supersession fields.
- `field_state_reducer_skeleton_v1.py` declares the reducer as the single
  mutation authority, while explicitly remaining skeleton-only and performing
  no state mutation.
- `field_state_reducer_module_api_v1.py` exposes candidate reduction and
  transition-legality handling, but excludes fact admission, persistence,
  provider/model calls and action execution.
- `field_state_read_model` provides read projections with source state refs,
  versions, stale/insufficient statuses and read-only boundary flags.

## Authority and responsibility

| Decision | Field authority | Responsibility |
|---|---|---|
| Accept an already admitted field event into a reducer transition | Yes, within Field contract | transition legality, temporal ordering, replay lineage |
| Create a candidate/read projection | Yes, structurally | correct state shape and provenance |
| Mutate governed Field state | Reducer only, when a future persistence contract permits it | no bypass or direct mutation |
| Declare World Truth | No | outside Field |
| Decide Need, Hypothesis, Sufficiency or Next-step | No | A |
| Assemble Context | No | Context Foundation |
| Build Current World candidate | No | Current World/State Formation boundary |

The repository's current skeleton cannot yet claim active production state
mutation. The target owner is nevertheless clear: only the Field reducer and
its governed persistence boundary may perform a Field transition.

## Inputs and outputs

Inputs are admitted field events, an existing Field state snapshot, temporal
validity, reducer/policy/version snapshots, conflict and provenance refs.
Raw observation is not a reducer input. The field-event admission contract
produces a reducer input candidate; that candidate is not itself a fact.

Outputs are a Field state candidate/read projection, applied/rejected/ignored
event refs, conflict/unresolved refs, deterministic replay key, state version
lineage and trace. Consumers receive refs/projections; A may interpret their
cognitive consequence, but may not mutate Field.

## State ownership and lifecycle

Field owns the authoritative Field-state lineage when admitted and persisted.
Reducer-local ordering and replay data are local derived/mechanical state.
Evidence, Observation, Current World, Context, Role, Intent and Task remain
external source refs. A Current World payload must not become a second mutable
Field store.

Conceptual lifecycle: admitted event candidate → reducer validation →
deterministic transition candidate → governed Field state/version → read
projection → superseded/expired/revoked state with retained provenance.

## Forbidden boundaries

Field must not perform semantic expansion/folding, A reasoning, Brain global
governance, Context assembly, Current World fusion, Observation acquisition,
Capability/Provider selection, Task/Action planning, Memory mutation, Learning,
or World Truth declaration.

## Current implementation status

`CONTRACT_GAP` and `RUNTIME_GAP`: reducer, event-admission, read-model and
integration contracts exist, but the inspected reducer is explicitly a
controlled skeleton (`runtime_implemented = False`, `state_mutation_executed =
False`). An explicit future persistence/admission handoff remains required.
