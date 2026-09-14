# Change Manifest

## Created

- `capabilities/midplatform/field_perception_orchestrator/integration/roboflow_provider_poc/rf_detr_declaration_validator_v1.py`
- `docs/architecture/phase_p1_luna_roboflow_rfdet_provider_declaration_and_observation_evidence_seam_implementation_v1/README.md`
- `declaration_binding_contract_v1.md`
- `normalization_evidence_boundary_v1.md`
- `synthetic_fixture_and_verification_v1.md`
- `change_manifest.md`

## Modified

- Existing Model Registry: RF-DETR external model declaration.
- Existing Provider Registry: Roboflow workflow binding and transport
  declaration; replaced `urllib` dependency with `inference-sdk`.
- Existing Capability↔Model binding Registry: object_detection ↔ RF-DETR
  candidate binding.
- Existing Model↔Provider binding Registry: RF-DETR ↔ Roboflow/custom-workflow
  candidate binding.
- Existing Model Contract Repository: external workflow loader, Roboflow
  adapter contract, model asset, deployment/license references.
- Existing Roboflow PoC types, client, fixtures, normalizer, runner, verifier,
  and scenario manifest.
- Observed Serverless envelope is now recorded as
  `response[0].model_output_3.predictions`; normalization fixtures mirror this
  envelope without copying image data.
- Verification is mode-scoped: structural fixture aggregates remain required
  only for structural runs, while real runs validate their actual response
  and handoff fields.
- A real `SUFFICIENT` cognitive result may hand off to `Decision Governance`
  without this Provider PoC fabricating a Decision candidate.

## Not changed

- No canonical owner or enum.
- No Runtime Admission implementation.
- No Provider Admission execution.
- No real SDK/API/network call.
- No model loading or inference.
- No Observation/Action runtime.
- No Current World/Field authoritative mutation.
- No UI/Test Lens implementation.
- No additional workflow integration.
