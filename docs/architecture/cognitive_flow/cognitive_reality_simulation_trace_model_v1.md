# Reality Cognition Simulation Trace Model v1

```text
Simulation Trace
├── Input
├── Self State
├── World State
├── Situation Candidate
├── Decision Candidate
├── Expected Outcome Candidate
├── Simulated Outcome Reference
├── Difference / Prediction Error Candidate
├── Failure Classification Candidate
├── Survival Value Feedback Candidate
└── Experience Candidate
```

The trace is deterministic and candidate-only. It preserves scenario source,
links between adjacent candidates, confidence/unknowns, and authority checks.
It does not record a real Action, Provider result, hardware event, State
mutation, B Reflection, or automatic self update.

Replay must produce an identical trace signature for the same fixture.
