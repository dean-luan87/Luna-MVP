# Change manifest

Added:

- `capabilities/midplatform/core/provider_runtime_to_observation_ingress/provider_invocation_result_adapter_v1.py`
- `capabilities/evaluation/provider_invocation_result_runtime_observation_gateway_evidence_controlled/`
- this architecture documentation directory.

Reused without semantic changes:

- `RuntimeObservationEnvelopeV1`;
- `ObservationGatewayEngineV1` and its existing admission/evidence contracts;
- `ProviderInvocationResultV1`;
- Governance Backbone profile, registry, resolver, preflight, postflight, and unified final-decision helper.

The existing Gateway static guard received one generic compatibility extension: a
controlled synthetic envelope may use the canonical `LIVE_RUNTIME` envelope
validation path when `controlled_integration_only=true`. Admission and evidence
semantics are unchanged. No Gateway core type, Evidence type, Governance
Backbone, FPO implementation, or upstream cognition contract was modified.
