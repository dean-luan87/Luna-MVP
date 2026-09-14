# YOLO11n repository-backed path

The first consumer reads:

- `capability_registry_v1.json` for `object_detection` and its Slot;
- `model_registry_v1.json` for `model-asset:yolo11n:weights-v1`;
- `provider_registry_v1.json` for the YOLO local Provider declaration;
- the Capability↔Model binding registry;
- the Model↔Provider binding registry.

The generic source translates these declarations into candidate/reference
records, assesses them, and composes the existing
`GovernedExecutionRecordBundleV1`. The existing YOLO translation can then
consume the bundle and build `CanonicalYOLO11nUpstreamRecordsV1`.

This proves record composition only. It does not prove model availability,
Provider health, Provider Admission, or execution readiness in the physical
runtime.
