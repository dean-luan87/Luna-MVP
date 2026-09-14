# Diagnostics Resource Fact Boundary v1

Diagnostics observes resource facts: memory, GPU/CPU availability/load,
battery, temperature, network, latency, storage, bandwidth, and runtime
capacity. Resource Governance owns ceilings, reserves, budgets, allocation
rules, and protected resources. Attention, Task, Decision, Runtime Admission,
Provider, and Action consume the appropriate governed refs; none may treat a
raw measurement as a global policy.

`RESOURCE_PRESSURE` is evidence/classification. `RESOURCE_BLOCKED`,
`RESOURCE_DEGRADED`, and reservation decisions belong to Resource Governance
or the relevant admission owner.
