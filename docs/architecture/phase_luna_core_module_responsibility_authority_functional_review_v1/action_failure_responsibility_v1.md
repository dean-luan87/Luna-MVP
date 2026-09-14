# Action Failure Responsibility v1

| Failure | Primary owner |
|---|---|
| invalid/stale/duplicate Action, bad precondition, missing permission/safety/resource | Action Governance / supplied policy owner |
| logical capability unsupported or runtime admission unavailable | Capability Governance / Runtime Admission |
| Provider/device execution failure | Provider/Runtime Executor |
| target/world state becomes stale | Field/Observation admission plus A consequence assessment |
| Task completion/failure interpretation | Task |
| semantic recovery/replan | A/Decision/Brain according to scope |
| final Outcome | Brain |

Action returns explicit blocked, failed, partial or uncertain references and
never fabricates success or semantic recovery.
