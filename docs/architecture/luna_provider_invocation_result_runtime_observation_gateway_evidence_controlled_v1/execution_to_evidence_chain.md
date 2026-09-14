# Execution-to-evidence chain

Only a completed controlled invocation is eligible for normal observation formation. The adapter preserves provider, capability, binding, grant, allocation, execution-instance, session, invocation, result, lineage, provenance, and trace references through its typed formation result and the envelope provenance/trace fields.

The existing `RuntimeObservationEnvelopeV1` is reused. Its `modality` is the fixed governed transport value `EXTERNAL_PROVIDER`; it is not inferred from Scenario 12 text or capability names. The payload remains an opaque `payload:synthetic:opaque:*` reference.

The existing `ObservationGatewayEngineV1` is reused through `build_gateway_request`. It validates the envelope and produces the existing `ObservationGatewayRuntimeAdmissionV1`, `ObservationCandidateV1`, and `PerceptionEvidenceV1` objects. Gateway admission means ingress accepted, not truth accepted. Evidence remains candidate-only and non-factual.

`FAILED`, `TIMED_OUT`, `STOPPED`, `REVOKED`, malformed, or lineage-inconsistent invocation results stop before normal observation formation. Gateway rejection produces no evidence. Replay uses stable deterministic identities and does not create a second identity.
