# Task Runtime Gap v1

## Existing assets

The repository contains Task types, lifecycle and dependency helpers,
decomposition, capability-routing candidates, observation request contracts,
result aggregation, state snapshots, static validators, and a Task Manager
module facade. Candidate flags preserve non-execution in the reviewed
orchestration contracts.

## Gap classification

| Gap | Classification | Finding |
|---|---|---|
| canonical Task identity/lifecycle contract | NO_GAP at contract level | types and lifecycle helpers exist |
| Decision → Task admission bridge | ADAPTER_GAP / CONTRACT_GAP | `source_decision_ref` exists but integration is broad |
| Task → Capability Requirement bridge | ADAPTER_GAP | current router is too module-oriented |
| Runtime Admission handoff | ADAPTER_GAP | Task must consume executable candidate refs only |
| Task → Action handoff | ADAPTER_GAP | Action remains separately governed |
| Task/Observation/A separation | LEGACY_OVERLAP | task-driven request assets need narrowing |
| independent Task owner | NO_GAP | Task Manager is established |
| global Planner/Scheduler | OWNER_GAP not justified | no new owner should be created |

Current implementation is candidate/planning-oriented rather than a complete
runtime contract. That is a runtime maturity gap, not permission to expand
Task authority.
