# Task — Canonical Module Contract v1

## Canonical purpose

Task is Luna's governed execution-organization module: it structures
decision-backed work into bounded executable units, dependency and readiness
relations, completion conditions, progress references, and execution-state
relationships without owning Goal, Intent, Concern-local reasoning,
Capability resolution, Runtime Admission, or Action semantics.

## Irreducible responsibility

Removing Task would remove the owner for organizing approved work: identity,
dependency graph, readiness aggregation, completion conditions, bounded
progress/lifecycle, and execution handoffs. Intent cannot absorb this without
becoming an execution planner; Decision chooses what should be done; Action
executes it; Loop persists cognitive work rather than task lifecycle.

## Core / supporting / out of scope

| Responsibility | Class | Boundary |
|---|---|---|
| Task identity/version and lifecycle | CORE | Task Manager |
| dependency graph and readiness aggregation | CORE | source status remains external |
| completion conditions/status | CORE | Task contract, not Goal success |
| behavior/execution constraints | CORE | carries constraints, does not execute |
| progress/subtask relationships | SUPPORTING | only where governed decomposition exists |
| capability requirement routing | SUPPORTING/NARROW | produce request candidate; Capability resolves |
| observation dependency declaration | SUPPORTING | does not create Need or schedule observation |
| Goal, Intent, Concern governance | OUT_OF_SCOPE | Brain/Intent owners |
| Need, Sufficiency, Reconsideration, B | OUT_OF_SCOPE | A/B owners |
| Provider/model/Action execution | OUT_OF_SCOPE | Capability/Provider/Action owners |
| cognitive Loop control | OUT_OF_SCOPE | Loop |

## Evidence and status

`TaskCandidate` requires `source_decision_ref` and marks execution as false;
readiness, blocker, plan, step, and handoff candidates are present. The
current `TaskManagerModuleV1` also performs input adaptation, dependency
resolution, decomposition, capability candidate routing, lifecycle/recovery
candidate construction, and state snapshot assembly. These are candidate
assets, not permission to make Task a global scheduler or Capability owner.

## Disposition

**NARROW.** Keep execution organization; move historical cognitive routing,
Capability resolution, Provider selection, Attention scheduling, and broad
orchestration semantics to their canonical owners. Timing:
`CONTRACT_ONLY / DEFER_RUNTIME_CONSOLIDATION`.
