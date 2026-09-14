# Capability ↔ Model Binding Boundary v1

`CapabilityModelBindingCandidateV1` is a candidate binding record. Capability
Governance owns its identity, version, lifecycle, invalidation and
supersession. Model Governance supplies the model identity and model-side
Capability declaration refs.

Validation is declaration-only: Capability, Slot, logical resolution,
declaration match, contract version, source versions, lifecycle and
provenance. No file, checksum, dependency or runtime probe is performed.

Valid binding does not imply Runtime Admission, model loading, Provider
Admission or invocation.

