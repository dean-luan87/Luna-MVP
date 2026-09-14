# Integration Mapping

The integration reuses:

1. `RealProviderExecutionEngineV1` for both bounded local YOLO invocations;
2. `ProviderNativeDetectionRecordV1` for native detection, bbox, dimensions,
   frame and provider trace;
3. existing `ProviderRuntimeResultV1` and RuntimeObservation references;
4. existing Situated State Perception and Situated Capability Preconditions;
5. existing minimum condition resolution for the primary sign-text need.

The new evaluation layer adds only cross-frame candidate contracts and metric
projection. It does not fork Provider Runtime, Observation Gateway, A-Route,
Cognitive State Formation, or condition ownership. OCR is not invoked.
