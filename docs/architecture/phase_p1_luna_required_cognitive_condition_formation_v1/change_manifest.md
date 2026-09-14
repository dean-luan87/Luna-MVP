# Change Manifest

## Added

- `a_route_required_cognitive_condition_formation_types_v1.py`
  - thin governed rule, current situation, request, candidate and result
    contracts;
- `a_route_required_cognitive_condition_formation_engine_v1.py`
  - exact-reference, state-sensitive formation and minimum-set selection;
- `capabilities/evaluation/a_route_required_cognitive_condition_formation/`
  - controlled fixtures, evaluation wrapper, user-terminal runner and
    fail-closed verifier;
- this Phase documentation。

## Modified

- `ARouteOrchestrationEngineV1` exposes the local formation boundary;
- A-Route orchestration exports the new thin types/engine;
- formation evaluation now keeps applicable required conditions in the active
  required set when coverage marks them `SATISFIED`; satisfaction is reported
  separately for downstream Need subtraction;
- `GovernedObjectiveConditionRuleV1` now accepts the optional governed
  `alternative_satisfaction_basis_refs` set. Any covered alternative satisfies
  the semantic requirement, while rules without alternatives retain exact
  legacy coverage semantics;
- canonical Goal/Condition and cognitive conformance documentation records
  that governed objective semantics can form current required conditions before
  Minimum View and Information Need。

## Explicitly unchanged

Information Need core algorithm, Minimum Relevant Cognitive View algorithm,
Field/Entity/Relation owners, Evidence Sufficiency, Observation Demand,
Capability Resolution, Field/World Truth, Identity, Memory, PCN, Decision,
Task, Action, Provider/Model execution and `POLICY_TRACE_COMPATIBILITY_GAP`。

No Runtime was executed by the Agent. Final Phase status is
`WAITING_FOR_USER_TERMINAL_VERIFICATION` pending user terminal execution。
