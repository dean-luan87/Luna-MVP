# Visual Capability Reference Audit

The package audited:

`capabilities/vision/registry/visual_capability_system_controlled/`

No visual files were modified.

| Visual structure | Classification | Mapping finding |
|---|---|---|
| `VisualCapabilityManifestV1` | `NEEDS_FUTURE_MAPPING` | Useful candidate manifest pattern, but visual-specific and not a generic Slot. |
| `CapabilityRegistrationCandidateV1` | `REUSABLE_GENERIC_PATTERN` | Candidate-only registration shape is reusable through a canonical adapter. |
| `CapabilityRegistrationOutcomeV1` | `REUSABLE_GENERIC_PATTERN` | Accepted/reason/candidate-only outcome pattern is reusable, subject to canonical owner mapping. |
| `SafetyRegistrationAssessmentV1` | `VISUAL_SPECIFIC` | Safety admission evidence is useful, but Safety Constitution remains canonical owner. |
| `SafetyCapabilitySlotV1` | `LEGACY_NARROW / DO_NOT_PROMOTE_TO_CANONICAL` | It is explicitly safety-specific and conflicts with the Universal Slot rule if generalized. |
| `CapabilityLifecycleTransitionCandidateV1` | `REUSABLE_GENERIC_PATTERN` | Candidate-only lifecycle request pattern is reusable under Capability Governance. |
| `CapabilityRouteRequestCandidateV1` | `VISUAL_SPECIFIC` | Dual-channel routing is a visual integration pattern, not the Universal Slot contract. |
| `CapabilityRouteResultV1` | `REUSABLE_GENERIC_PATTERN` | Candidate-only route outcomes and negative guards are useful adapter patterns. |
| `build_safety_slots()` | `DO_NOT_PROMOTE_TO_CANONICAL` | It creates domain-specific safety structures. |
| `build_manifests()` | `VISUAL_SPECIFIC` | Reference fixtures only; they must not define generic Module or Slot identity. |
| SNSP/SRSK references | `REFERENCE_ONLY` | Boundary references are useful; no runtime semantics are present. |

## Key audit conclusion

The visual system has a useful candidate-only skeleton and correct separation
from provider execution. Its safety slot type, visual domain names, and
fixture lifecycle should remain narrow until a future Universal Slot
conformance implementation is explicitly approved.
