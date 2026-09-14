# Cognitive Middleware Design Principles v1

## Frozen principles

### 1. The Brain does not call hardware directly

Context, Goal, Attention, Workspace, Simulation, Evaluation, and Feedback may create Cognitive Request Candidates only. A camera, IMU, ToF sensor, microphone, or compute provider can be reached only through the Cognitive Neural Protocol and a future approved middleware admission boundary.

### 2. Middleware has no cognitive decision authority

Middleware may assess feasibility, provider availability, lifecycle health, and resource constraints. It cannot choose Luna's goal, decide what is true, select an action, or replace Brain Evaluation.

### 3. A model is only a Capability Provider

OCR, VLM, detection, segmentation, SLAM, ASR, TTS, or any future model provides a bounded capability result. A model result has source, scope, confidence, uncertainty, and provenance; it is not a fact, decision, or command.

### 4. Hardware is only Embodiment

Hardware supplies physical observation, availability, and limits. It does not interpret the world, own task priority, create goals, or authorize action.

### 5. Evidence is the only return form to the Cognitive Brain

Middleware returns Evidence Candidate, capability availability, reliability state, resource state, and failure candidates. It may not return implicit truth, a direct decision, an action request, or State mutation.

### 6. Every capability path passes through the protocol

No direct links are permitted from Brain to model/hardware, or from model/hardware to decision/action. CNP preserves request context, evidence requirements, resource constraints, provenance, trace, and failure visibility.

### 7. Capability growth cannot break the Brain boundary

New sensors, models, providers, or capability bundles may extend the Middleware only by adding controlled capability/evidence forms. They must not gain Goal, Attention, Truth, Decision, Action, Permission, or State-mutation authority.

## Complementary constraints

- Capability availability ≠ capability execution.
- Evidence confidence ≠ truth.
- Resource limitation ≠ goal override.
- Diagnostics ≠ Cognitive Evaluation.
- Middleware fallback ≠ autonomous decision.
- Attention Request ≠ hardware command.
- Reducer remains the only State Mutation Authority.

## Status

`COGNITIVE_MIDDLEWARE_DESIGN_PRINCIPLES_READY_WITH_NOTES`

`WAITING_FOR_USER_TERMINAL_VERIFICATION`
