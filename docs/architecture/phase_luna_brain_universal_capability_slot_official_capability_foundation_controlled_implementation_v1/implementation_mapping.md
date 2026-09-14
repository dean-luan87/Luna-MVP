# Implementation Mapping

| Concept | Implementation surface | Ownership |
|---|---|---|
| Universal Slot | `universal_capability_slot_types_v1.py` | Existing Capability Registry / Governance extension |
| Official Module | `CapabilityModuleV1` / `OfficialCapabilityModuleV1` | Capability Registry / Module Admission |
| Admission | `universal_capability_slot_governance_v1.py` | Capability Admission Governance |
| Binding | Compatibility + binding candidate/result helpers | Capability Governance |
| Resolution | `universal_capability_slot_resolution_v1.py` | Capability Registry lookup plus Governance evidence |
| Invocation handoff | `CapabilityInvocationCandidateV1` | Existing execution/provider boundary reference |
| Capability Self | `CapabilitySelfViewV1` | Read-only projection for Cognitive Self |
| Brain Regulation | `CapabilityRegulationCandidateV1` | Reserved Brain candidate boundary only |

Model Manager, Provider Governance, System Maintenance, Resource Governance,
Permission Governance, Safety Constitution, Observation Gateway, and FPO are
referenced boundaries. They are not reimplemented here.

## Direct-file execution compatibility

The Runner and Verifier follow the established B2/B3/B4 entrypoint pattern:
each entrypoint locates the repository root, adds only that root to
`sys.path`, and imports the package through its absolute `capabilities...`
path. Internal implementation modules retain package-relative imports.

The documented direct-file Runner and Verifier execution contract remains
unchanged.
