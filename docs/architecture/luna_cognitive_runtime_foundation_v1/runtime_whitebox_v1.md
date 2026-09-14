# Luna Runtime Foundation Whitebox v1

## Questions the foundation must answer

1. What woke the system?
2. Which pending event was admitted and why?
3. Which Tick and Flow Candidate were selected?
4. Which State Proposal was produced, and who owns the State?
5. What trace records the transition?
6. What is persisted, and why is it allowed?
7. If interrupted, where can processing safely resume?

## Explicit non-authority

Runtime Foundation is not a Scheduler implementation, Brain, Decision owner,
Reality Reducer, Provider, Model Manager, Hardware Manager, or Action Runtime.
It may produce lifecycle, event, state-sync, trace, snapshot, and recovery
candidates only.

