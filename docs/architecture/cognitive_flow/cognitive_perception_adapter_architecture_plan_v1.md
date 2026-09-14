# Cognitive Perception Adapter Architecture Plan v1

## Phase

`Phase-Cognitive-Foundation-Real-Input-Adapter-Planning-v1-001`

## Stage and execution mode

- Stage: Architecture Planning.
- Execution Mode: `Planning Only`.
- Previous Phase: `Phase-Cognitive-State-Transition-Architecture-Planning-v1-001`.
- Previous Phase Decision: `COGNITIVE_STATE_TRANSITION_ARCHITECTURE_PLANNING_READY_WITH_NOTES`.
- Verification Authority: V0 agent only; V1/V2/V3 are not authorized by this planning phase.

## Objective and position

Define the boundary by which a future external capability may submit Evidence Candidates to the Luna A-route Cognitive Foundation.

```text
External Capability
  -> Capability Adapter Candidate
  -> Evidence Candidate
  -> Evidence Admission Candidate
  -> Cognitive Information Field Candidate
  -> Cognitive Foundation
```

External Model != Brain. The adapter carries context, source, uncertainty, provenance, and permission constraints; it does not invoke an external capability in this phase.

## Inputs and outputs

Permitted future input families: visual, audio, and user-language capability outputs, each as an untrusted source candidate.

Permitted outputs: Evidence Candidate, Evidence Admission Candidate, uncertainty candidates, and references for Cognitive Information Field processing.

## Out of scope

No camera/OCR/ASR/VLM/SLAM integration, model invocation, actual input ingestion, Runtime, Decision, Action, Memory, Hive, Emotion, B Route, World Model, automatic Learning, or State mutation.

## Required final files

The eleven `cognitive_*adapter*`, `cognitive_*evidence*`, and `cognitive_real_input_*` assets named by this phase instruction under `docs/architecture/cognitive_flow/`.

## Required checks and authority

V0 only: file existence and static boundary/forbidden-coupling checks. No final phase verifier is created or run.

## Stop condition

`final_candidate_decision: COGNITIVE_FOUNDATION_REAL_INPUT_ADAPTER_PLANNING_READY_WITH_NOTES`

`status: WAITING_FOR_USER_TERMINAL_VERIFICATION`
