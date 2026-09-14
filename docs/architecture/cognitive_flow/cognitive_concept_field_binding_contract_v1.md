# Cognitive Concept–Field Binding Contract v1

## Contract purpose

`FieldConceptReferenceBindingCandidateV1` is a planned, candidate-only read-model annotation contract. It lets an authorized Cognitive Query/Context consumer point at an existing Concept Candidate while preserving Field/Context scope. It is not a Field Kernel write contract.

## Planned fields

| Field | Requirement | Authority boundary |
| --- | --- | --- |
| `binding_id` | Stable, governance-supplied reference | No automatic identity generation |
| `concept_ref` | Existing traceable Concept Candidate reference | Not an assertion of truth |
| `field_ref` | Existing governed Field reference | Cannot create or redefine a Field |
| `field_unit_refs` / `relation_refs` | Optional existing structural references | Cannot create Units, Relations, or causal claims |
| `context_ref` / `snapshot_ref` | Immutable Current Cognitive Context and derived Snapshot scope | Cannot mutate Context or Snapshot |
| `temporal_binding` | Source time, valid-time scope, history window, uncertainty, staleness references | Cannot change State valid time or temporal admission |
| `spatial_binding` | Existing Field/Unit/location/relation references and explicit unknowns | Cannot assert a map/location fact |
| `confidence` / `uncertainty` | Copied candidate metadata; uncertainty mandatory | Cannot affect Fact admission or State confidence |
| `provenance` / `trace_ref` | Full Concept-to-source chain plus binding derivation trace | Cannot be stripped or replaced |
| `binding_status` | `candidate`, `validated_candidate`, or `historical_reference` | Not `admitted`, `fact`, or `active_state` |

## Input and output boundary

Inputs are only a validated Concept Candidate reference, existing Field/Unit/Relation references, Current Cognitive Context reference, derived Snapshot reference, and retained provenance/trace. The sole output is a read-only binding candidate or query annotation.

The binding must not accept raw model/provider payload, Observation, raw Evidence, Field Event Candidate, Admitted Event, State handle, State write target, Fact, Decision, Action, Memory, Learning target, or Hive target.

## Required propagation

1. **Confidence propagation**: output confidence is reference metadata from the Concept; it cannot be aggregated into State confidence or an admission score.
2. **Uncertainty propagation**: all unknown, stale, conflicting, coverage, and temporal limitations remain explicit. A binding with missing scope is not silently completed.
3. **Trace propagation**: Concept trace, Primitive references, Translation/Evidence/source-capability lineage, Context/Snapshot references, and binding derivation trace are retained.
4. **Temporal propagation**: the binding references its source temporal scope only. Temporal Validity stays at the Admission boundary; Field Temporal Evolution remains State-version organization after reduction.

## Authority constraints

`Concept != Fact`; `Concept != State`; `Concept != Decision`; `Concept != Memory`.

Reducer is the only Field State mutation authority. Field Kernel/Read Model may expose a future binding only as a read-only query adjunct. Any result consumer remains subject to L1 Traceability, Permission/Admission, Candidate I/O, and Consumer Governance contracts.
