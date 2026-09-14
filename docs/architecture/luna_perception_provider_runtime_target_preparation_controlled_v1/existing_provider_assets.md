# Existing provider assets and compatibility decision

Reconnaissance found:

- `provider_runtime_governance_types_v1.py`: Provider Governance manager, registry entry, health snapshot, fallback route and admission-check planning contracts. These are candidate/planning contracts and keep runtime activation disabled.
- `provider_registry_loader_v1.py` and `provider_registry_v1.json`: Model Manager Provider Registry view. The registry uses `model_id` as its provider record key and declares provider type, lifecycle, admission status and capabilities; this historical shape is not treated as a new model/provider binding contract here.
- `multi_provider_selection_v1.py`: existing candidate-producing provider selection with score/rank/selected fields. It is deliberately not reused because this phase must retain all explicit candidates without ranking or a winner.
- `provider_runtime_to_observation_ingress/types_v1.py`: downstream `ProviderRuntimeRequestV1` and result contracts. They require `execution_instance_ref` and are provider/runtime-facing; they are not preparation candidates.
- `capability_model_provider_binding_controlled/types_v1.py`: existing Capability→Model and Model→Provider binding candidates. They belong to the later binding boundary and require model/provider declarations.
- `field_understanding/spatial_evidence_provider_admission`: domain-specific provider admission/planning, not a generic cross-demand target contract.

Conclusion: no existing generic Provider Runtime Target Preparation Candidate was found. The new contract is a thin Provider Governance-side candidate projection over an explicit mapping snapshot; it does not call registry selection, binding, activation or runtime ingress APIs.
