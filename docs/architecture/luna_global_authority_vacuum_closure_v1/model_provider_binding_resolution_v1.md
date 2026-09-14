# Model ↔ Provider Binding Resolution v1

## Resolution

`Model Asset ↔ Provider Family/Adapter/Loader` is a shared contract with one binding lifecycle authority: **Provider Governance** owns the provider-facing compatibility binding record and lifecycle. This does not transfer Model identity, files, checksums or lifecycle to Provider Governance.

## Split responsibilities

- Model Governance owns model-side compatibility declarations, loader metadata, dependency declarations, model version and asset provenance.
- Provider Governance owns Provider identity, Provider Family/Adapter contract, runtime compatibility binding, Provider Admission, invocation and session lifecycle.
- Runtime Admission consumes the binding as evidence of possible execution; it does not create or rewrite the binding.
- Diagnostics supplies observed health; it does not approve compatibility.

## Lifecycle and invalidation

Declaration → compatibility validation → Provider-owned binding version → available/deprecated/superseded. Model version, loader change, Provider adapter change, runtime contract change, retirement or health incompatibility invalidates the binding. Model Governance supplies the model-side cause; Provider Governance records provider-side lifecycle.

## Responsibility

Provider Governance owns wrong binding approval, Provider identity mismatch, adapter/version mismatch and invalid binding lifecycle. Model Governance owns incorrect model declarations. Provider runtime owns invocation failures. No Provider binding may silently create Model identity or mutate the Model Registry.

