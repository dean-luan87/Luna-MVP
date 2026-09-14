# Asset Inventory

Reused canonical assets:

- `ActionGovernanceInputV1` and `ActionGovernanceOutputV1`.
- `ActionGovernanceEngineV1`.
- Action candidate, trace, transition, readiness, precondition, dependency,
  and candidate-only handoff types.
- Action static validators and ownership guards.
- The verified Decision-to-Task Manager controlled integration.

The only missing surface was a narrow adapter that maps an admitted planned
Task result into `ActionGovernanceInputV1`. No Action Manager or parallel
runtime was created.
