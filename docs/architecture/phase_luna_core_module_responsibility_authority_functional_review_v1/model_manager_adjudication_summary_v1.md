# Model Manager Adjudication Summary v1

## Final decision

**KEEP / NARROW** Model Manager / Model Governance as the authority for model
identity, assets, versions, declared paths/checksums, loader/dependency
declarations, provisioning, lifecycle, and model-side mappings.

## Target flow

```text
External/governed source
        → provisioning candidate
        → Model Governance
        → Registered Model Asset / Manifest
        ├→ Capability mapping
        ├→ Provider compatibility
        ├→ Loader/dependency declarations
        └→ lifecycle/baseline refs
Diagnostics observed state + Capability resolution + global constraints
        → Runtime Admission
        → Executable Capability Candidate
        → Provider Admission / runtime / result
```

Model Governance stops before executable admission and runtime execution.

## Current status

Repository contracts, registry, lifecycle, YOLO11n readiness/provisioning,
loader/dependency and mapping assets exist, but the unified runtime contract
and adapters remain incomplete. No runtime or model operation was performed.
