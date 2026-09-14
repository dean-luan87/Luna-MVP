# Evidence Feedback Loop v1

## Governed loop

```text
Observation
    ↓
Evidence
    ↓
Evidence Validation
    ↓
Reality Update Candidate
    ↓
Reality Workspace / Reducer
    ↓
Field Reassessment
```

Observation does not directly change the Field. Evidence must carry
provenance, timestamp, confidence, uncertainty, capability reference, request
reference, and coverage/missing-information status. The Reality Workspace
decides whether a state update candidate is admissible; Reducer remains the
sole State mutation authority. Reducer remains the sole State mutation authority.

## Feedback outcomes

Feedback may indicate sufficient coverage, missing information, low confidence,
conflict, stale evidence, or capability failure. The Field may receive a
Reassessment Candidate, but no automatic Decision or Action is created.

Human Feedback and Provider output enter through the same Evidence Gateway.
Evidence is not Reality by source alone, and absence of Evidence is not proof
of absence.

## No hidden loop

There is no direct Observation → Field mutation path, no direct Observation →
Decision path, no automatic retry, no automatic model switch, and no online
learning in this phase. This phase has no online learning.
