# Temporal Evidence Boundary v1

## Purpose

Temporal Evidence is the governed input boundary for recognizing that a
represented condition may be stable or changing. It does not preserve every
observation and does not enter Decision, Action, or Memory directly.

## Allowed inputs

- timestamp or ordering reference;
- governed state change evidence;
- continuous observation reference;
- external event reference;
- environment change evidence.

## Output

```text
Temporal Evidence
        ↓
Temporal Candidate
```

Temporal Candidate must retain `source_reference`, `time_or_order_reference`,
`observed_delta_candidate`, `coverage_candidate`, `uncertainty`, and
`trace_ref`.

## Boundary

- Timestamp alone is not temporal understanding.
- Raw continuous observation is not Temporal Memory.
- Temporal Evidence does not directly enter Decision, Action, Experience,
  Memory, State mutation, or Provider control.
- Evidence remains Evidence until a governed Reality/Temporal representation
  process forms a candidate.

