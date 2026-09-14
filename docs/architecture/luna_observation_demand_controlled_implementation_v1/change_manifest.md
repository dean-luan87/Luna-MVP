# Change Manifest

## Added

- `capabilities/midplatform/core/cognitive_flow/observation_demand_formation_v1.py`
- `capabilities/evaluation/observation_demand_controlled/` canonical controlled
  fixtures, evaluation engine, runner and verifier。
- 本目录中的 Observation Demand architecture documentation。

## Modified

- `capabilities/midplatform/core/cognitive_flow/__init__.py` exports the new
  candidate-only contract and formation function。
- `docs/architecture/README.md` adds the current phase index entry。

## Reused

- `InformationAcquisitionStrategyCandidateV1`；
- `StrategyCoordinationResultV1` 与 `StrategyCoordinationDecisionV1`；
- existing branch/need/gap/basis lineage and provenance fields；
- existing controlled evaluation and `_eval_out` conventions。

## Not modified

- Information Need、Branch Formation、Branch Governance、Strategy Coordination；
- FPO、Observation Gateway、Provider/Model、Capability、Sandbox runtime。

## Deferred

Capability Resolution、Capability Requirement Formation、Perception Routing、Provider
或 Model selection、Camera/OCR/SLAM runtime、Observation execution、Resource
Scheduling、Attention Scheduling、Evidence Fusion、Conflict Resolution、Decision、
Task、Action 与 real-world acquisition。

当前状态：`WAITING_FOR_USER_TERMINAL_VERIFICATION`。
