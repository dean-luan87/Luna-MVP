# Change manifest

## Added

- `capabilities/evaluation/cognitive_requirement_alternative_satisfaction_basis/`
  - controlled direct fixtures, evaluation engine, user-terminal runner and
    fail-closed verifier;
- this architecture documentation set.

## Modified

- `GovernedObjectiveConditionRuleV1` with the single optional
  `alternative_satisfaction_basis_refs` field;
- Required Cognitive Condition formation evaluation so any explicit alternative
  basis can satisfy one semantic requirement while actual coverage refs remain
  precise;
- controlled Sandbox fixtures for the exit-direction semantic requirement and
  its Scenario 12 downstream coverage projection;
- canonical Required Cognitive Condition documentation with the compatibility
  semantics.

## Reused / unchanged owners

- A-Route Required Cognitive Condition formation remains the satisfaction
  evaluation owner;
- Information Need remains the `required - coverage` owner;
- Branch Formation, Branch Governance and Acquisition Strategy remain their
  existing owners;
- Minimum View, Current World, Sufficiency and Stop ownership are unchanged.

## Deferred

- Multiple Sufficient Condition Sets;
- Boolean sufficiency expressions;
- many-to-many basis mapping;
- basis invalidation and Need reopen lifecycle;
- conflict resolution, evidence fusion and confidence algebra;
- Strategy Coordination, Observation Demand and real acquisition runtime;
- capability execution, Provider/Model integration, Decision, Task and Action.

No user-terminal Runner/Verifier result has been supplied for this phase. Status
remains `IMPLEMENTATION_READY_FOR_USER_EXECUTION`.
