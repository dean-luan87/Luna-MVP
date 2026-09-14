# Phase Contract

Prove, for exactly two controlled positive cases:

```text
admitted planned Task
  → Action Governance
  → permission/safety validation
  → execution eligibility candidate
  → candidate-only Runtime Executor handoff
```

The phase also exercises exactly one permission rejection and one safety
rejection. It stops before Runtime Executor, Action execution, device control,
and external side effects.

Operational correctness and cognitive logic conformance remain separate
results. This narrow phase may report
`cognitive_logic_result=NOT_INDEPENDENTLY_EXERCISED` because it does not run
the Role/Task/Field contrast suite.

