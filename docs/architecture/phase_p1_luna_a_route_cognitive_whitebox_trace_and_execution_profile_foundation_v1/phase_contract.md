# Phase Contract

## In scope

- evaluation-only CognitiveWhiteBoxTraceV1;
- evaluation-only LunaCognitiveExecutionProfileV1;
- minimum CognitiveFailureGapRefV1;
- existing cognitive candidate/event ref mapping;
- synthetic candidate-only traces;
- structural Runner and Verifier preparation.

## Out of scope

- runtime cognition mutation;
- model/provider/Roboflow invocation;
- Dataset Registry or dataset download;
- White-box UI;
- Cognitive Burden scoring;
- Model comparison;
- Memory, Capability Slot deepening, B-Route, Learning, Emotion;
- Task/Action execution.

## Stop condition

Stop at this foundation once the three contracts, existing-ref mapping,
observation-cycle/revision/sufficiency/gap linkage, synthetic cases, and
negative guards are present. User terminal verification is required before any
next phase.
