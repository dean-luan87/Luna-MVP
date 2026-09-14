# Task Capability Router Full Audit v1

| Current asset | Current behavior | Target owner | Retained Task role | Disposition |
|---|---|---|---|---|
| `build_capability_routes_v1` | registry lookup and request candidates | Capability Governance | preserve requirement refs/order | NARROW |
| `TaskManagerModuleV1` capability-routing step | marks blocked capabilities and adds candidates | Capability Governance + Task | aggregate dependency/blocker refs | WRAP |
| `task_manager_task_decomposition_v1` capability fields | attaches capability IDs to subtasks | Task/Capability bridge | carry requirement refs only | KEEP_AS_CANDIDATE |
| orchestration route builder | produces route/module handoff candidate | governed adapter | preserve trace/handoff refs | COMPATIBILITY_ONLY |

No inspected Task router should select a model, Provider, Runtime Admission,
or executable capability. A future cutover should replace module-selection
semantics with a Capability Requirement → Scope → Logical Resolution handoff.

Retirement readiness: R1 for direct module routing; R2 after an explicit
Capability bridge exists; R0 for any proposed Provider/runtime behavior.
