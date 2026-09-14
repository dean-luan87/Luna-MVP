# Capability ↔ Model Binding Contract v1

## Authority

Capability Governance owns the binding record and lifecycle. Model Governance owns Model identity, asset/version and model-side capability declaration. Runtime Admission consumes the binding; it does not create or rewrite it.

## Minimal contract surface

| Field | Meaning / owner |
|---|---|
| `binding_ref`, `binding_version` | Capability-owned binding identity/version |
| `capability_ref`, `capability_slot_ref`, `capability_contract_version` | Capability source refs |
| `model_asset_ref`, `model_version_ref`, `weights_version_ref` | Model source refs |
| `model_capability_declaration_ref` | Model Governance declaration |
| `compatibility_status`, `compatibility_constraints` | Capability binding assessment |
| `source_versions` | source-owner version map |
| `lifecycle_status`, `invalidation_refs` | Capability binding lifecycle |
| `provenance_refs`, `trace_ref` | reverse lineage |
| `candidate_only` / binding status | distinguishes declaration/candidate from active binding |

## Contract phases

Model declaration `FORMATION`; structural/version check `VALIDATION`; Capability-owned record `BINDING`; governed availability `ADMISSION`; Runtime Admission `ADOPTION` of the binding as evidence. Binding never implies executable readiness, Provider selection, invocation or evidence quality.

## Failure and bypass

Capability Governance owns wrong binding approval, scope contamination, version loss and lifecycle errors. Model Governance owns incorrect declarations. Runtime Admission owns executable eligibility. Model Governance cannot mutate Capability metadata; Capability Governance cannot mutate Model metadata.

