# Capability Model Mapping v1

The mapping is potentially many-to-many:

- one Capability/Slot → multiple models/providers;
- one Model Asset → multiple Capability contracts;
- one Provider family → multiple compatible slots.

Mapping records should preserve:

- capability/module and slot version;
- model asset and model version;
- Provider family/adapter contract;
- input/output/evidence contract;
- compatibility refs;
- performance/quality baseline refs;
- deployment/resource constraints;
- integrity/provisioning refs and provenance.

No ranking policy is introduced here. Runtime Admission may eliminate
unavailable candidates, while Provider Governance handles execution choice under
its contract.

The official catalog types already separate capability modules, model refs,
Provider refs, slot compatibility, health, lifecycle and provenance, and mark
the catalog candidate-only with no runtime execution.
