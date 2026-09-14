# Brain–Neural–Middleware Interaction Model v1

## Airport navigation case

Goal: find the airport boarding gate.

```mermaid
sequenceDiagram
    participant B as Brain
    participant N as Neural Layer
    participant M as Middleware
    participant P as OCR / Vision Provider
    participant E as Evidence Gateway

    B->>B: Goal + Context + Unknown<br/>gate signage not confirmed
    B->>N: Attention Signal Candidate<br/>target=gate sign; priority=high
    N->>M: Capability Signal Candidate<br/>text/visual evidence needed
    M->>M: capability/resource feasibility candidate
    M->>P: future admitted OCR/Vision capability operation
    P->>E: raw visual/text result + provider health
    E->>N: Evidence Signal Candidate
    N->>B: evidence + reliability/resource/failure candidates
    B->>B: Workspace / Context Update Candidate<br/>evaluate sufficiency
```

## Responsibility progression

| Stage | Owner | Result | Prohibition |
|---|---|---|---|
| Goal/unknown formation | Brain | Goal, Context, Attention candidates | Middleware cannot originate this task. |
| Signal transport/classification | Neural Layer | validated Attention/Capability/Evidence signal path | Neural Layer cannot change semantics into fact/decision. |
| Capability resolution | Middleware | feasible capability/resource/provider candidate | Middleware cannot decide what the gate is. |
| Capability activity | Provider/Hardware | raw OCR/vision output or health signal | Provider cannot update context/goal. |
| Evidence packaging | Evidence Gateway | Evidence Candidate | Gateway cannot confirm gate truth. |
| Cognitive update | Brain | Context/Workspace/Evaluation/Sufficiency candidate | Does not authorize action. |

## Feedback example

If the camera lens becomes obstructed during the session:

`Body State Signal → Reflex/State Neural Path → Middleware diagnostics/resource candidate → Neural feedback → Self State Candidate → Attention adjustment candidate`

The active goal remains a Brain candidate. The feedback changes available evidence strategy, not the truth of the airport situation.

## Status

`COGNITIVE_BRAIN_NEURAL_MIDDLEWARE_INTERACTION_MODEL_READY_WITH_NOTES`

`WAITING_FOR_USER_TERMINAL_VERIFICATION`
