# Temporal Reality State Model v1

## Purpose

Temporal State maintains continuity of observed reality, not a forecast. It
records current state, previous reference, change delta, transition evidence,
validity window, and temporal uncertainty.

```text
Previous State
      ↓
Change Evidence
      ↓
Current Temporal State
```

Examples include a closed door becoming a changed-state candidate, a vehicle's
position changing, or a resource validity window expiring.

## Boundary

Temporal State is not a Prediction, future fact, plan, schedule, or Decision. It is not a Decision.
does not answer why a person moved or what Luna should do. It supplies temporal
context to A Route and preserves current/previous evidence for the Reducer.
