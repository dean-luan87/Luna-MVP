# Luna Cognitive Closed Loop Integration Architecture v1

## Position

This phase integrates the already-defined L0–L4 contracts into one explainable
cognitive cycle. It defines the cycle and its interfaces; it does not run a
loop, Scheduler, model, hardware, Action, or online learning.

```text
Observe
  ↓ Context Formation
  ↓ Attention Allocation
  ↓ Situation Understanding
  ↓ Hypothesis / Belief Update
  ↓ Expectation Comparison
  ↓ Brain Evaluation
  ↓ Decision Commitment
  ↓ Action Boundary
  ↓ Action Runtime Foundation (future)
  ↓ Outcome Collection
  ↓ Learning Update
  ↓ Memory Consolidation
  ↺ Next Cycle
```

## Integration principles

- Runtime Foundation supplies Tick, Wake-up, Process, State, Trace, and
  Recovery; Closed Loop defines one cognitive cycle within that substrate.
- Global State composes module state but owns none of it.
- Capability supplies Evidence; it does not own the loop or initiate cognition.
- Action Outcome returns through Expectation Difference, Learning, and Memory.
- Social and Emotion provide context candidates only; they cannot directly
  execute Action or override Decision.
- Every transition is traceable, permission-bound, and candidate-preserving.

