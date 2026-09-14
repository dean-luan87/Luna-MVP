# Change Manifest

## Added

- `capabilities/midplatform/core/cognitive_flow/information_acquisition_strategy_candidate_formation_v1.py`
  - governed basis, formation input/result and strategy candidate contracts
  - candidate-only formation function
- `capabilities/evaluation/information_acquisition_strategy_candidate_formation/`
  - controlled fixtures
  - evaluation engine
  - user-terminal Runner
  - Verifier
- this phase documentation set。

## Modified

- `capabilities/midplatform/core/cognitive_flow/__init__.py`
  - exports the new candidate-only formation contract and function。
- `docs/architecture/README.md`
  - records this Phase as waiting for user terminal verification。
- Cognitive Flow growth-boundary documentation
  - records the strategy-candidate boundary; later Strategy Coordination is a
    separate controlled owner, while execution remains deferred。

## Semantic boundary

This implementation only normalizes explicit governed acquisition bases for admitted
Branches. It does not change Branch Formation, Branch Governance, Information Need,
Hypothesis, Sufficiency, Stop, Current World, Field, Capability, Observation, Decision,
Task, Action, Provider, Model, Memory or PCN ownership.

The implementation does not create an Acquisition Strategy ontology or a second
Cognitive Loop. It does not infer strategies from Goal, Question, Need text, scenario,
case or fixture names.

## Status

`WAITING_FOR_USER_TERMINAL_VERIFICATION`

## User terminal commands

```text
python -m capabilities.evaluation.information_acquisition_strategy_candidate_formation.runner_v1
python -m capabilities.evaluation.information_acquisition_strategy_candidate_formation.verifier_v1
```
