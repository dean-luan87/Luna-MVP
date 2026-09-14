# Luna Cognitive Action Boundary Architecture v1

## Position

Action Boundary is the governed exit from L2 Cognitive Core toward the
external world. It converts a Decision Commitment into an Action Request
Candidate, validates risk and permission, and emits an Approved Candidate. It
does not execute an Action.

```text
Decision Commitment
        ↓
Action Request Candidate
        ↓
Candidate Management
        ↓
Risk Evaluation
        ↓
Permission Check
        ↓
Context Validation
        ↓
Action Approved Candidate
        ↓
Execution System (future)
        ↓
Outcome Evidence
        ↓
Experience / Learning
```

## Boundary principles

- Decision is not Action; an Action Candidate is not an Action.
- Brain cannot directly call Hardware, Provider, or an Action Executor.
- Risk covers Physical, Social, Privacy, and Resource dimensions.
- High-risk cases may require Human Override; override is an authority record,
  not an automatic action.
- Execution results return as Outcome Evidence and re-enter cognition through
  the Evidence/Experience boundary.
- Action Boundary owns authorization and validation only. It cannot redefine
  Goal, Value, Decision, Constitution, or Runtime policy.

No Action Runtime, hardware control, robot movement, API execution, Provider
execution, or external side effect is enabled in this phase.

