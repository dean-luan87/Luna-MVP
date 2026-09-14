# Controlled Architecture Alignment Migration Plan

## Inputs

- Dynamic Cognitive System v2 canonical candidate;
- existing asset mapping and duplicate-owner registry;
- active capability module baselines;
- existing interfaces, manifests, traces, and verification evidence.

## Per-asset procedure

1. Resolve the exact old asset and its canonical owner from the baseline.
2. Select one migration type and record the proposed new position.
3. Define compatibility checks for imports, public API, schemas, ownership,
   dependencies, trace/replay, and behavior.
4. Define rollback and legacy-compatibility handling before mutation.
5. Execute only in a separately authorized migration or skeleton phase.
6. Produce a completed migration record with before/after evidence.
7. Submit the record to Migration Integrity Validation.

## Initial alignment matrix

| Asset | Target position | Planned type | Owner rule |
| --- | --- | --- | --- |
| Field State Reducer | Field Context input | adapter | Field System preserved |
| Observation Manager | Environment Understanding | keep | observation/evidence owner preserved |
| Cognitive Attention | Cognitive Projection Support consumer | boundary_update | Attention Governance preserved |
| Memory System | Experience Memory source and historical influence | adapter | Memory System preserved |
| Role System | Role Causal Projection source | boundary_update | Social Self/Role owner preserved |
| Relationship System | Personal network relationship projection | adapter | Relationship owner preserved |
| Intent Architecture | Intent Processing and Gate input | boundary_update | Intent Governance preserved |
| Causality plans | Causal Network contract | boundary_update | Causal Reasoning Governance preserved |
| Task Manager | Task orchestration after decision | keep | no Action execution authority |
| Model Manager | Capability Layer | keep | no cognitive conclusion authority |
| OCR / Vision | Evidence providers | keep | no direct fact authority |
| Protocol Manager | L1 governance | keep | no cognitive/runtime ownership drift |

## Stop conditions

Migration stops when a canonical owner cannot be resolved, compatibility evidence
is incomplete, rollback is missing, a mainline would be duplicated, a source
object would be absorbed by the Personal Cognitive Network, or a regression check
is unavailable. Such an asset remains `blocked`, not “temporarily unassigned.”

