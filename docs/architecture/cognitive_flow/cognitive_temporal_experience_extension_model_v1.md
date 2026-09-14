# Temporal Experience Extension Model v1

## Purpose

Temporal experience preserves the process surrounding an outcome so that a
future governed Experience Candidate can distinguish a static condition from a
changing one. It is not Memory adoption, online learning, or automatic Self
update.

## Extension shape

```text
Outcome Reference
        +
Temporal Context Candidate
        ↓
Temporal Experience Extension Candidate
├── context_window_reference
├── observed_transition_candidate
├── turning_point_candidate
├── outcome_reference
├── temporal_difference_candidate
├── failure_context_candidate
├── uncertainty
└── trace_ref
```

## Example

Do not reduce an outcome to “navigation failed at night.” Preserve the
candidate sequence: continuous low illumination, extended operation, declining
visual-quality candidate, then navigation reliability reduction. The sequence
does not prove a universal causal rule; validation is required before any
Experience adoption or future strategy change.

## Boundary

- A single sequence cannot modify Self Model, Strategy, Decision, or capability
  policy.
- Temporal Experience Extension Candidate enters only the governed Experience
  interface and may later be validated.
- It does not enter B Reflection during this phase.

