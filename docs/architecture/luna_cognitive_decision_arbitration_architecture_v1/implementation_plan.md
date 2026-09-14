# Decision Arbitration Implementation Plan v1

This phase is Architecture Only.

1. Reuse Brain Decision Candidate, Brain Value Constraint, Field Decision
   Candidate, Value Utility, Self Boundary, and Action Boundary contracts.
2. Add a future adapter that receives a candidate set and emits a traceable
   Selected Decision Candidate without mutating runtime state.
3. Keep Brain as candidate-generation owner and Decision Arbitration as the
   arbitration owner; do not create a second Brain or Planner.
4. Add reconsideration as an explicit candidate path for changed Reality,
   Field, risk, capability, or Self state.
5. Defer execution, scheduling, B Route, Emotion, and Action Outcome Runtime
   to later phases.

No existing code or architecture asset is moved or changed in this phase.
