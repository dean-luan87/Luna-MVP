# Ownership and canonical order

| Boundary | Owner | Responsibility |
|---|---|---|
| Provider Binding Decision | Provider Governance | provider binding-domain decision and failure |
| Runtime Grant | Permission / Admission Manager | execution authorization decision |
| Resource feasibility | Resource Governance | satisfiability/status, not allocation identity |
| Runtime Allocation | Runtime Executor | authoritative allocation record and allocation failure |
| Execution Instance | Runtime Executor | execution identity and instance lifecycle |
| Provider Session | Provider Runtime / Runtime Executor | future session start/failure |
| Gateway ingress | Observation Gateway | future Runtime Observation ingress admission |

实际顺序是 `Candidate → Grant → Binding Decision → Allocation → Execution Instance`。
当前 grant contract 以 Binding Candidate 为输入，因此不存在 Binding/Grant 循环。
`RESOURCE_FEASIBLE` 不等于 `ALLOCATED`；`CREATED` 不等于 `STARTED`。
