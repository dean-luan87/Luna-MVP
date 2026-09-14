# Verification Contract

Runner marker:

`CONTROLLED_A_ROUTE_MINIMUM_RELEVANT_COGNITIVE_VIEW_TEST`

The user terminal must run the controlled runner and then the verifier. This
phase does not claim live Provider or Model execution.

## Required behavior

- Same information with different governed Goal conditions selects different
  minimum views.
- Relevant Self and External changes alter the selected view.
- Irrelevant Self, External, and opaque Context changes do not alter it.
- One case selects both Self and External information.
- A previously excluded item is reactivated by a different Goal condition.
- Exclusions are recoverable, not deleted.
- Selected refs become the read-only cognitive coverage projection.

## Required negative guards

- non-candidate requests are rejected;
- duplicate information refs are rejected;
- no governed conditions produce no active view;
- no Goal, Self, Field, World, Memory, or PCN mutation;
- no Truth, Decision, Task, Action, Observation, or Capability execution;
- no Provider or Model invocation;
- no scenario-driven selection;
- opaque Context refs are not interpreted as semantic conditions;
- no static Goal-to-selected-ref lookup is used.

## Final user-terminal result

The user terminal reported:

```text
all_checks_passed=true
cognitive_logic_result=PASS
operational_result=PASS
failed_checks=[]
final_decision=GO
validation_errors_empty=true
```

Verified behavior included Goal changes, relevant Self/External changes,
irrelevant Self/External/opaque Context stability, Role conditioning,
Self/External use of the same algorithm, selected refs equal to current
cognitive coverage, and recoverable exclusions.

Governance checks confirmed candidate-only, read-only, non-Truth behavior with
no Self/Field/Memory/PCN mutation, Provider/Model invocation, Observation or
Observation Demand execution, Decision, Task, or Action execution.

The phase is now `GO — VERIFIED — PHASE CLOSED`.

The verified algorithm remains only `declared governed condition
intersection`. It must not be described as generalized semantic relevance,
autonomous semantic Attention, or generalized meaning understanding.

## User-terminal commands

From the repository root, run:

```text
python -m capabilities.evaluation.a_route_minimum_relevant_cognitive_view.runner_v1
python -m capabilities.evaluation.a_route_minimum_relevant_cognitive_view.verifier_v1
```

The runner is controlled-only and does not invoke a Provider, Model, live
observation, or downstream Observation Demand path.
