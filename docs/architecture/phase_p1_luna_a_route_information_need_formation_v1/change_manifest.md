# Change Manifest

## Added

- A-Route local request/result contract:
  `a_route_information_need_formation_types_v1.py`。
- A-Route read-only formation adapter:
  `a_route_information_need_formation_adapter_v1.py`。
- A-Route engine entry point `form_information_need(...)`。
- Controlled fixture, engine, runner and fail-closed verifier under
  `capabilities/evaluation/a_route_information_need_formation/`。
- This phase documentation set。

## Reused and unchanged

- Existing `CognitiveNeedCandidateV1` and `validate_cognitive_need`。
- Existing `GoalContextV1` and `CurrentWorldCandidateV1`。
- No canonical Need V2, Need ontology, Information Gap contract, Observation
  Demand contract, Capability contract, or provider/model path was added。

## Semantic implementation

The adapter performs:

`governed objective conditions − Current World cognitive coverage → necessary unknowns`。

It does not use scenario branching, keyword matching, opaque Context guessing, or
an Information Need lookup table. A satisfied difference returns `NO_ACTIVE_NEED`;
an unresolved difference forms the existing candidate-only Need。

## Explicit non-goals

No Attention redesign, Observation Demand, Capability Resolution, Hypothesis
generalization, Information Gap change, Re-observation, Stop change, Memory/PCN,
Identity, Meaning, Decision, Task, Action, Provider, Model, or Runtime execution。

## Verification state

User-terminal verification returned:

```text
all_checks_passed=true
check_count=99
cognitive_logic_result=PASS
operational_result=PASS
failed_checks=[]
final_decision=GO
```

`INFORMATION_NEED_FORMATION_GAP = CLOSED`。
Final phase state: `GO — VERIFIED — PHASE CLOSED`。

The closure is limited to state-sensitive Need formation. It does not close or
start Self-conditioned objective formation, minimum Self/External View, upstream
condition formation, pre-observation Attention, or Observation Demand Formation。
