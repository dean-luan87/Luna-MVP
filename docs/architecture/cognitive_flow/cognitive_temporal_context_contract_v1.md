# Temporal Context Contract v1

## Purpose

Temporal Context is the candidate-only input that lets the A-route describe
reality as a continuing process rather than an isolated state snapshot. It
supports Situation enhancement and Decision support; it does not establish a
future fact.

## Contract shape

```text
Temporal Context Candidate
├── Past Reference
├── Current State Reference
├── Change Evidence
├── Transition Pattern Candidate
├── Trend Candidate
├── Future Possibility Candidate
├── Temporal Uncertainty
└── trace_ref
```

| Field | Meaning | Boundary |
|---|---|---|
| Past Reference | governed reference to an earlier represented state | not an immutable history claim |
| Current State Reference | link to the current World State | does not overwrite the World State |
| Change Evidence | evidence of transition, duration, order, recurrence, or discontinuity | evidence remains evidence |
| Transition Pattern Candidate | increasing, decreasing, moving, recovering, or worsening | not causal proof |
| Trend Candidate | directional interpretation of observed transitions | not a prediction truth |
| Future Possibility Candidate | bounded possible continuation or risk window | never written into Reality as fact |
| Temporal Uncertainty | gaps in cadence, coverage, duration, or interpretation | must remain visible downstream |
| trace_ref | provenance to evidence, state references, and evaluation | required for review and replay |

## Required rules

- `Reality State != Reality Process`: a current state is one temporal slice.
- `Prediction != Reality`: a Future Possibility Candidate cannot substitute for
  observation, Current State, or Reality Representation.
- Temporal Context is not a scheduler instruction, frequency command, action,
  decision, provider call, or State mutation request.
- A missing past reference produces Temporal Uncertainty; it must not be
  fabricated from a single observation.

## Permitted attachment path

```text
Temporal Evidence
        ↓
Temporal Context Candidate
        ↓
Temporal World State Candidate
        ↓
Situation Enhancement Candidate
        ↓
Decision Support Candidate
        ↓
Outcome / Experience Extension Candidate
```

