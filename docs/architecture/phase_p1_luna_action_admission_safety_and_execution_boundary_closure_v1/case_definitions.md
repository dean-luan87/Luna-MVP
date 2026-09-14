# Case Definitions

## Case A

`CASE_A_SUFFICIENT_STOP` reuses the verified one-cycle path:

```text
Sufficiency/Stop → Decision Candidate → admitted planned Task
→ Action Candidate → permission/safety validation
→ READY_CANDIDATE → Runtime Executor handoff candidate → stop
```

Exactly one final Action handoff is expected.

## Case B

`CASE_B_GAP_REOBSERVE_REVISE_STOP` reuses the verified two-cycle path. Cycle 1
has insufficiency, Gap, Re-observation, and no Decision/Task/Action handoff.
Cycle 2 supplies the revised sufficient cognition, Decision Candidate, and
admitted Task before the single final Action handoff.

The adapter validates the final Task and cognition provenance without
reconstructing upstream candidates.

