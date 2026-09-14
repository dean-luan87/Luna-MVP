# Change manifest

## Added

- `capabilities/midplatform/core/cognitive_flow/strategy_coordination_v1.py`;
- exports in `capabilities/midplatform/core/cognitive_flow/__init__.py`;
- `capabilities/evaluation/strategy_coordination_controlled/` with fixtures,
  evaluation engine, Runner and Verifier;
- this documentation set.

## Reused

- `InformationAcquisitionStrategyCandidateV1`;
- `CognitiveBranchGovernanceDecisionV1`;
- existing Branch / Need / Gap / basis / dependency / lineage / provenance refs.

## Not modified

Required Cognitive Condition Formation, Information Need, Branch Formation, Branch
Governance, Acquisition Strategy Formation, Hypothesis, Current World, Sufficiency,
Stop, Observation and execution owners remain unchanged.

## Deferred

Strategy Execution, Observation Demand, Capability Resolution/Scheduling, Resource
Optimization/Merge, cost/priority/utility/confidence ranking, winner selection,
Evidence Fusion, Conflict Resolution, runtime concurrency, real acquisition,
Provider/Model invocation, Branch lifecycle and B Route runtime.

Sandbox integration is deferred: the independent coordinator and its controlled
verifier are sufficient for this boundary without changing the existing 12-scenario
Sandbox behavior.

Status: `WAITING_FOR_USER_TERMINAL_VERIFICATION`.
