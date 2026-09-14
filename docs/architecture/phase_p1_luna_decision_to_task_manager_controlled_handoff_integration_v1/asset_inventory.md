# Asset Inventory

| Asset | Classification | Use |
|---|---|---|
| `DecisionGovernanceOutputV1` and `DecisionToActionTaskHandoffCandidateV1` | Canonical contract | Source Decision Candidate, selection, trace, and downstream candidate handoff |
| `TaskManagerModuleV1` / `run_task_manager_module_v1` | Canonical controlled implementation | Task admission, decomposition, lifecycle, state snapshot, and aggregation |
| `TaskManagerModuleRequestV1` shape | Canonical input contract | Mapping fields supplied to the module API |
| `task_manager_module_input_adapter_v1` | Canonical adapter/validator | Input admission and boundary checks |
| Task lifecycle/status resolver | Canonical implementation | Controlled Task state |
| Decision-to-Task adapter | New narrow integration surface | Propagates existing Decision refs into Task Manager input |

The legacy Task candidate helpers were inspected but are not used to replace
the canonical Task Manager module consumer in this phase.

