# Runtime Integration Mapping

The integration reuses:

- `situated_state_perception_engine_v1.derive`;
- existing Situated Capability Preconditions evaluation;
- `RealOCRProviderExecutionEngineV1`;
- existing ProviderRuntimeRequest/Result contracts;
- existing RuntimeObservation, Observation Gateway, A-Route, and CState
  handoffs.

The ineligible branch has no Provider Runtime result, observation, Gateway, or
Evidence because the real OCR call site is never entered.  The eligible branch
passes a canonical `ProviderObservationIngressCaseV1` to the existing real OCR
engine and preserves its native result, runtime result, observation, Gateway,
Evidence, A-Route, and cognition outputs.

The source is the existing local OCR asset:
`capabilities/test_assets/p1/ocr/ocr_real_image_subway_station_longtan_temple_v1_001.png`.
