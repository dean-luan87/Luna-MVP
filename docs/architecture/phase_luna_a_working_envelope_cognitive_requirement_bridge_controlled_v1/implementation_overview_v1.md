# Implementation overview

The implementation is bounded to `capabilities/midplatform/core/cognitive_flow/integration/a_working_envelope_cognitive_requirement_bridge_controlled/`.

It adds only integration candidate types and deterministic synthetic fixtures. The adapter reuses the existing A semantic decision bridge, authority grant status validation, Need → CapabilityRequirement formation, Universal Capability Slot Scope/Resolution, and ObservationCandidateV1. It does not create a new Brain, A Route, Capability, Observation or Loop owner.

