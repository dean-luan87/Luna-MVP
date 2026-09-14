# White-box/Profile Integration

The Level-1 case composes with existing:

- `CognitiveWhiteBoxTraceV1`
- `LunaCognitiveExecutionProfileV1`
- `CognitiveFailureGapRefV1`

The case stores refs for dataset, sample, environment, perturbation, and
expected observation requirement, then links to trace/profile artifacts after
an evaluation run. Existing V1 types are not duplicated or version-bumped in
this phase.

The trace/profile remain observation surfaces. They do not control Attention,
Evidence, Current World, Hypothesis, Sufficiency, Re-observation, or Decision.
