# Model ↔ Provider Binding Contract v1

## Authority

Provider Governance owns the provider-facing compatibility binding and lifecycle. Model Governance owns Model identity, loader, dependency and runtime declarations. Provider Admission and invocation remain separate.

## Minimal contract surface

| Field | Meaning / owner |
|---|---|
| `binding_ref`, `binding_version` | Provider-owned binding identity/version |
| `model_asset_ref`, `model_version_ref` | Model source refs |
| `loader_contract_ref` | Model-declared loader contract |
| `provider_family_ref`, `provider_adapter_ref`, `provider_contract_version` | Provider source refs |
| `runtime_compatibility_refs`, `dependency_compatibility_refs` | declaration/evidence refs |
| `compatibility_status`, `constraints` | Provider binding assessment |
| `source_versions`, `lifecycle_status`, `invalidation_refs` | binding lineage |
| `provenance_refs`, `trace_ref` | reverse lineage |

## Contract phases

Declarations `FORMATION`; compatibility check `VALIDATION`; Provider-owned record `BINDING`; Provider Admission `ADMISSION`; runtime invocation `EXECUTION`. Compatibility does not imply health, permission, resource availability, Model registration, or invocation.

## Failure and bypass

Provider Governance owns wrong Provider binding, adapter/version mismatch and binding lifecycle. Model Governance owns wrong Model declarations. Diagnostics supplies health evidence. Provider owns invocation failure. Provider Governance cannot mutate the Model Registry; Model Governance cannot create Provider Admission.

