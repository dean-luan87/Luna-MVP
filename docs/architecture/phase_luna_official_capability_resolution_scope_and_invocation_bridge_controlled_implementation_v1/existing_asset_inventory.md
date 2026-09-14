# Existing asset inventory

The existing `CapabilityRequirementV1`, `CapabilityResolutionCandidateV1`,
`CapabilityInvocationCandidateV1`, Universal Slot governance, Catalog/CSA, and
Capability Self projection are reused. Resolution remains in
`universal_capability_slot_resolution_v1.py`; no parallel Resolver, Router, or
Registry was created.

Capability Registry/Governance owns Module identity and admission. Model
Manager and Provider Governance expose dependency references. Observation
Gateway/FPO remain the visual execution boundary. OCR Manager and spatial
mapping adapters remain implementation boundaries. Self is read-only.
