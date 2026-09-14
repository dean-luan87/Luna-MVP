# Luna Cognitive Decision Arbitration Architecture v1

## Position

Decision Arbitration is the boundary that compares multiple Decision
Candidates and produces a Selected Decision Candidate. It is neither Action,
Planner, Brain candidate generation, nor a Runtime executor.

```text
Current Understanding
        ↓
Goal + Value Utility + Self Constraints
        ↓
Decision Candidate Set (Brain)
        ↓
Hard Constraint Filter
        ↓
Utility / Priority Review
        ↓
Selected Decision Candidate (Arbitration)
        ↓
Action Boundary (future admission)
```

Selection remains a candidate until the separate Action Boundary and Runtime
authorize execution. A selected candidate contains traceable reasons,
confidence, unknowns, required capabilities, cost, risk, and reversibility.

## Authority split

- Brain integrates understanding and generates Decision Candidates.
- Decision Arbitration compares candidates and emits a Selected Decision
  Candidate, Reject Candidate, Defer Candidate, or Reconsideration Candidate.
- Self and Constitution provide non-negotiable constraints and veto context.
- Value Utility provides benefit/cost/risk/priority candidates.
- Action Boundary is the future execution gate.

Arbitration does not create Goals, rewrite Value, modify Reality, run a
Planner, call a model/provider, execute an Action, or enter B Route
simulation. Current Reality and Current Understanding outrank stale Memory.
