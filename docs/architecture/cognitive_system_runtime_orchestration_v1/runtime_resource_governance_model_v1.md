# Runtime Resource Governance Model v1

## Resource dimensions

Runtime governance accounts for compute, battery/energy, time, storage,
attention, sensor/capability access, network, and memory. It compares process
demand with Information Value, Survival Impact, Goal Relevance, and Resource
Cost.

```text
Process Request
      ↓
Attention Priority
      ↓
Resource Allocation Candidate
      ↓
Execution Candidate
```

## Boundary

Resource Governance can defer, compress, background, suspend, or escalate a
process candidate. It cannot decide what is valuable in place of Brain, call a
model directly, control Hardware, execute Action, or mutate Reality. It is not
a Scheduler and does not implement a Scheduler.

Low resource produces a Resource Constraint Candidate and preserves Unknown;
it does not fake Evidence or silently drop a safety requirement. It is not a Scheduler. It does not call a model,
does not control Hardware, and does not execute Action.
