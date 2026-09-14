# Repository Asset Inventory

## Reusable

- `CapabilityResolutionCandidateV1` and Universal Capability Slot resolution
  exist under `model_manager/registries/universal_capability_slot/`.
- `CapabilityModelBindingCandidateV1` and `ModelProviderBindingCandidateV1`
  exist in the controlled binding package.
- `RuntimeAdmissionAssessmentCandidateV1` and
  `ExecutableCapabilityCandidateV1` exist in the controlled Runtime Admission
  integration package.
- `ModelAssetContractV1`, `LoaderContractV1`, `CapabilityContractV1`, and
  `ProviderAdapterContractV1` exist in the Model Contract Repository.
- YOLO11n model, loader, capability, evidence, and adapter candidate
  declarations exist in `model_contract_repository_registry_v1.py`.

## Candidate-only or insufficient

- The controlled binding builders require synthetic-only inputs.
- Dynamic Runtime Admission records are trial/controlled records and are not
  a non-fixture owner-issued production source.
- The YOLO11n Model Contract Repository entry has `source="registered_candidate"`.
- The official catalog records the YOLO11n path as a bounded FPO/provider
  supporting asset and explicitly notes that it is absent from the canonical
  `model_registry_v1.json` mapping.

