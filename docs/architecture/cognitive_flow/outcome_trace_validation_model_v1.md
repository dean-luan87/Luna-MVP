# Outcome Trace Validation Model v1

## Structured outcome trace contract

```json
{
  "intent_reference": {},
  "situation_reference": {},
  "decision_candidate": {},
  "execution_boundary": {},
  "expected_outcome": {},
  "actual_outcome": {},
  "difference": {},
  "cause_attribution": {},
  "adaptation_candidate": {}
}
```

The trace is structured provenance and candidate relation data only. It is not
private chain-of-thought, a real Action record, device telemetry authority,
Outcome truth, a Memory write, or a State mutation request.

## Trace assertions

- Decision Candidate, Execution Boundary, and Outcome Evidence remain distinct references.
- difference compares Expected Outcome against actual governed Outcome Evidence.
- cause attribution retains competing factors and Unknown without responsibility or blame.
- adaptation candidate preserves validation and adoption boundaries.
- past decision review uses Past Available Context rather than later evidence.
