# Integration Mapping

The implementation reuses the following canonical owners:

1. `RealProviderExecutionEngineV1` performs the one real YOLO11n provider
   invocation and produces the existing runtime result/observation path.
2. `ProviderNativeDetectionRecordV1` is the native visual source record.
3. `RealVisualSituatedStateSourceV1` is an evaluation projection only.
4. `SituatedStatePerceptionRequestV1` and `derive()` produce the four existing
   `SituatedConditionStateCandidateV1` records.
5. `SituatedCapabilityPreconditionRequestV1` and `evaluate()` consume those
   condition candidates and produce canonical feasibility, gaps,
   adjustments, opportunity and eligibility.

The new layer does not replace or fork Provider Runtime, RuntimeObservation,
Observation Gateway, Evidence, A-Route, or Cognitive State Formation.
Historical runtime output is not used as a substitute for the new terminal
execution.
