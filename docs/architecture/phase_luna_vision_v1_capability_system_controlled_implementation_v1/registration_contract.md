# Dynamic registration contract

`VisualCapabilityManifestV1` and `CapabilityRegistrationCandidateV1` retain:

`capability_id`, domain/version/kind, mandatory-or-optional status, input and
evidence contracts, provider/model references, resources, permissions,
compatibility, provenance, lifecycle state, trace, and `candidate_only`.

Registration does not install, activate, select a provider, invoke a model, or
produce evidence. Safety registration additionally requires approved provider,
baseline, compatibility, provenance/checksum, rollback, degradation, and
resource readiness candidates.
