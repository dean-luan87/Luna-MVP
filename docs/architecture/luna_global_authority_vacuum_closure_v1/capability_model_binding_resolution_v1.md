# Capability ↔ Model Binding Resolution v1

## Resolution

`Capability ↔ Model` is a shared contract with one binding lifecycle authority: **Capability Governance** owns the canonical compatibility binding record and its lifecycle. This does not transfer Model identity or asset ownership.

## Split responsibilities

- Capability Governance owns Capability identity, Slot, capability-side input/output/evidence contract, scope and logical resolution.
- Model Governance owns Model identity, asset/version, declared capabilities, loader/dependency declarations, integrity/provisioning refs and model-side compatibility declaration.
- Capability Governance binds those declarations into a versioned mapping record.
- Runtime Admission validates current executability using the binding plus Diagnostics, integrity, Provider, Safety, Permission and Resource evidence.

## Binding fields conceptually preserved

Capability/Slot version, Model asset/version, input/output/evidence contract, compatibility refs, baseline/quality refs, deployment/resource constraints, integrity/provisioning refs and provenance.

## Lifecycle and invalidation

Candidate declaration → compatibility validation → Capability-owned binding version → active/deprecated/superseded mapping. Capability or Model version changes, Model retirement, contract change, integrity change or Provider incompatibility invalidates the binding. Model Governance may submit an invalidation cause but cannot mutate the Capability-owned binding record.

## Responsibility

Capability Governance is responsible for incorrect binding approval, scope contamination, version loss and invalid mapping lifecycle. Model Governance is responsible for incorrect model declarations. Runtime Admission is responsible for wrong executable eligibility. No direct mapping-to-execution bypass is allowed.

