# Cognitive Attention Lifecycle Architecture Plan v1

## Phase and governance

- Phase: `Phase-Cognitive-Attention-Lifecycle-Architecture-Planning-v1-001`.
- Stage: Architecture Planning.
- Execution Mode: `Planning Only`.
- Previous Phase: `Phase-Cognitive-Attention-Architecture-Extension-Planning-v1-001`.
- Previous Phase Decision: `COGNITIVE_ATTENTION_ARCHITECTURE_EXTENSION_PLANNING_READY_WITH_NOTES`.
- Verification Authority: V0 agent only; V1/V2/V3 are not authorized by this phase.

## Objective and position

Define the candidate lifecycle by which an attention request begins, is active/maintained/reduced/suspended/closed, and may later contribute to an experience-pattern candidate.

```text
Attention Source -> Attention Candidate -> Admission Candidate -> Active Attention
  -> Maintained / Background / Dormant / Reduced Candidates
  -> Suspended or Closed Candidate -> Attention Pattern Candidate
```

Lifecycle labels are candidate interpretations, not a persistent State Machine. Attention remains separate from Memory, Experience, Goal, Decision, Truth, and State mutation.

## Scope

Define lifecycle state, activation, maintenance, decay, suspension, closure, pattern extraction, experience alignment, and evolution interface candidates.

## Out of scope

No attention runtime, TTL implementation, scheduler, memory store/write, experience/evolution runtime, Decision, Action, Permission, B Route runtime, external device/model invocation, or State mutation.

## Required checks and stop condition

V0 only: required-file and boundary checks. No Final Phase Verifier is created or run.

`final_candidate_decision: COGNITIVE_ATTENTION_LIFECYCLE_ARCHITECTURE_PLANNING_READY_WITH_NOTES`

`status: WAITING_FOR_USER_TERMINAL_VERIFICATION`
