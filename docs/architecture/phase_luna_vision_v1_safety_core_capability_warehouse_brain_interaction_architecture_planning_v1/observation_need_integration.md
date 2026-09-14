# Observation Need integration

Reuse `ObservationDemandCandidateV1`, `ObservationRequestCandidateV1`,
`CapabilityRequirementCandidateV1`, `EvidenceSufficiencyCandidateV1`, and
`ObservationControlDecisionV1` in Active Observation Control/FPO.

Task Observation may continue, redirect, switch provider, add a capability,
reconsider, defer, or stop according to existing sufficiency semantics.
Safety Perception may use the existing safety-critical exception path and
must not wait for ordinary task demand. Neither channel invokes a provider
from the Brain/Gateway boundary in this planning phase.

The sufficiency used by this control surface is Evidence Sufficiency. Future
Semantic Sufficiency belongs to SRSK and must not be folded into FPO's
acquisition decision.
