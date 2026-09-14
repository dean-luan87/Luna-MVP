# Proposed Contract Revision

## Replace the primary profile

Previous planning emphasis on `EvaluationExecutionProfileV1` and
`ModelFitProfileV1` is revised:

- `LunaCognitiveExecutionProfileV1` becomes primary;
- `CognitiveWhiteBoxTraceV1` becomes the joined machine-readable trace;
- `CognitiveFailureGapRefV1` becomes the primary P0 failure reference;
- `CognitiveBurdenMetricsV1` measures Luna system cost;
- `ExternalCapabilityFitnessProfileV1` becomes supporting L3/L4 evidence.

## Preserve Dataset contracts

`DatasetRegistryEntryV1`, `DatasetSampleManifestV1`,
`AnnotationGroundTruthRefV1`, and `BenchmarkSpecV1` remain valid, but serve
world/observation corpus construction for Cognitive Evaluation.

## Reuse instead of duplication

The revision references existing Model Test Case/Result/Trace, TestBoard,
Observation, Evidence, Current World, Hypothesis, Sufficiency, and governance
contracts. It does not create parallel canonical types in this phase.

## Required invariants

- L0/L1 Luna cognition outranks L3/L4 model metrics;
- external capability failure is not automatically Luna cognition failure;
- evaluation result is not World Truth;
- unavailable trace nodes stay unavailable;
- no automatic binding/model/provider selection;
- versions and provenance remain separate and traceable.
