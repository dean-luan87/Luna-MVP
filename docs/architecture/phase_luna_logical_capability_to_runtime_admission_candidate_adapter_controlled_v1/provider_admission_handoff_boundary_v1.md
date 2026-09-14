# Provider Admission Handoff Boundary

The adapter may emit `ProviderAdmissionInputCandidateV1` after an executable
candidate exists. Its `provider_invocation_authorized` field remains false.

Provider Governance/FPO retains authority to create and validate the existing
Provider admission candidate. This phase does not select a Provider, load a
model, create evidence, or invoke Provider execution.

