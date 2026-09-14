# Action Boundary Whitebox v1

## Candidate-only flow

```text
Decision Candidate
       ↓
Action Intent
       ↓
Action Request
       ↓
Permission / Risk / Capability Validation
       ↓
Execution Boundary Candidate
       ↓
Outcome Evidence
       ↓
Reality Update Candidate → Reducer
```

The trace preserves Decision Reference, Intent, Target, Constraints,
Confidence, Required Capability, Authorization Level, Risk Classification,
Unknowns, Permission Candidate, Provenance, and Feedback. It contains no
Action Command, no real execution, and no direct Reality mutation.

Action Failure is routed to Outcome Evidence and Cause Attribution Candidate;
it is not automatically classified as Decision Failure. Neural Safety Action
Candidate remains a candidate-only fast path. The Reducer remains the sole
State mutation authority.

No real Action Runtime, No hardware control, No robot movement, No payment, No
external system operation, No automatic execution, No Emotion Runtime, No Role
Runtime, No Social Runtime, and No B Runtime are included.

Neural Safety Action Candidate remains candidate-only.
The Reducer remains the sole State mutation authority.
No external system operation is included.
No Role Runtime is included.
