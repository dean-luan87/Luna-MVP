# Decision Selection Model v1

Arbitration follows a non-executing sequence:

```text
Candidate Set
      ↓
Hard Constraint Filter
      ↓
Utility Evaluation Candidate
      ↓
Priority Ranking Candidate
      ↓
Selected Decision Candidate
```

Hard constraints are non-compensatory. A candidate that violates Safety,
Constitution, Self Preservation, capability feasibility, or an irreversible
impact boundary is rejected even if its utility is high. Remaining candidates
may be ranked using Value Utility outputs, but the rank is not a Decision
commitment and not an Action command.

When Reality, Understanding, Self State, Capability State, or risk changes,
the current candidate may become Invalidated and produce a Reconsideration
Candidate. This is a boundary contract, not an automatic state machine.
