# Capability Registry / Manifest Audit v1

## Capability Registry

`capabilities/registry/luna_capability_registry_v1.json` is a foundation module
registry. It records capability identity, domain, responsibility, lifecycle,
contracts, dependencies, integration evidence, diagnostics/trace support and
explicit authority flags. It states that the registry does not create runtime
loading services.

## Lifecycle Registry

The lifecycle registry distinguishes planned, skeleton, building,
integration-ready, functional-module-ready, degraded, blocked, deprecated and
retired. `functional_module_ready` does not mean production or runtime enabled.

## Universal Slot / Official Catalog

Universal Slot and Official Catalog assets separate module, implementation,
model, Provider, supporting asset, contract, compatibility, health, lifecycle
and provenance. Catalog entries are candidate-only and do not install, activate,
invoke or infer.

## Static vs live state

Registry/Manifest/Baseline/Calibration/quality data define static or governed
metadata. Live dependency, device, runtime and Provider health are evidence
inputs, not static capability identity. Runtime Admission must not silently
rewrite the registry.
