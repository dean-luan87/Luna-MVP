# Action Execution Boundary Model v1

## Purpose

Action Execution Boundary defines the information handoff from a Brain-reviewed
Decision Candidate to a future execution system. It does not implement an
Action, device control, scheduler, provider invocation, or State mutation.
It does not implement an Action.

```text
Decision Candidate
        ↓
Execution Request Candidate
        ↓
Future Capability Execution Boundary
        ↓
Execution Status Candidate
        ↓
Outcome Evidence Candidate
```

## Contract fields

| Candidate | Required meaning |
|---|---|
| Execution Request Candidate | decision reference, intended effect, constraints, required capability, trace reference |
| Execution Status Candidate | accepted/rejected/prepared/partial/unknown status; never a success verdict |
| Outcome Evidence Candidate | observed post-boundary evidence, provenance, uncertainty, temporal reference |

Brain does not directly execute. Neural may organize future cognitive process
candidates but cannot control a device. Middleware may report capability and
resource feasibility, but cannot decide the desired effect. Any future Action
system remains a separately admitted architecture.
