# Protocol Capability, Model, and Provider Boundary v1

Capability, Model, and Provider contracts may be protocol-governed for
identity/version/compatibility, while their source metadata and runtime
authority remain separate:

- Capability Governance: Capability identity, Slot, Scope, Logical Resolution.
- Model Governance: model identity, asset, loader, mappings, lifecycle.
- Provider Governance: Provider identity, admission, invocation, result.
- Runtime Admission: executable eligibility.

Protocol Manager must not collapse these owners.
