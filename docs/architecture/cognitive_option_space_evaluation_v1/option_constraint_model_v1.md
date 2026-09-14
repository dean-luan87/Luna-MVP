# Option Constraint Model v1

## Option dimensions

```text
Option
├── Expected Benefit Candidate
├── Resource Cost
├── Risk Candidate
├── Capability Requirement
├── Unknown
└── Dependency
```

Each option is evaluated against current Self Capability, Self State, Resource
State, Goal Context, authority boundaries, temporal constraints, Field Context,
and Unknown. Resource State is required. Constraint evaluation produces a candidate status such as
feasible candidate, limited candidate, blocked-by-capability candidate, or
needs-more-information candidate.

Constraint Fit is not a final value judgment. High benefit cannot erase a
non-negotiable safety or authority constraint. Unknown remains visible and
affects Option Confidence. Resource Cost is an explicit evaluation field.

The constraint model does not execute, select, rank a final option, modify
Reality, modify Reality, modify Goal, modify Decision, or issue Action. Brain retains final
evaluation authority.
