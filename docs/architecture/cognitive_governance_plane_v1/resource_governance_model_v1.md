# Resource Governance Model v1

Resource Governance manages finite compute, energy, memory, time, network,
storage, and sensor budgets. It coordinates with Attention and Runtime
Governance but does not own cognition or schedule a Goal.

## Resource flow

```text
Need / Capability Request
        ↓
Resource Requirement
        ↓
Budget Review
        ↓
Allocation Candidate / Denial Candidate
        ↓
Diagnostics and Self State Candidate
```

Resource Governance records Information Value, Resource Cost, risk, urgency,
quota, reservation, health, and expiry. It may recommend throttling,
deferment, release, or fallback. It cannot directly execute, change Goal,
change Decision, mutate Reality, or select a Provider as a cognitive choice.

Resource denial must be explicit and may produce Capability Degraded Candidate
or Attention Adjustment Candidate. The Reducer remains the sole State mutation
authority.

Resource Governance cannot change Goal. The Reducer remains the sole State mutation authority.

Runtime Governance is a separate boundary. Resource Governance cannot change
Goal, cannot change Decision, and the Reducer remains the sole State mutation
authority.
