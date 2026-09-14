# Implementation Overview v1

The narrow package under `capabilities/midplatform/core/cognitive_flow/integration/capability_model_provider_binding_controlled/` contains:

- local input and candidate records;
- Capability/Model and Model/Provider declaration validators;
- cross-binding consistency validation;
- synthetic fixtures, Runner and Verifier.

The implementation reuses `CapabilityResolutionCandidateV1`,
`ModelAssetContractV1`, and `EdgeObservabilityCandidateV1` as existing
contract families. It does not alter those canonical definitions.

