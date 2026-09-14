# Cognitive Runtime Life Process Whitebox v1

```text
Tick / Wake-up Sources
          ↓
Lifecycle Manager → Process Scheduler
          ↓                 ↓
Workspace Manager ← Attention Scheduler
          ↓                 ↓
State Synchronization → Brain Invocation Candidate
          ↓
Diagnostics / Fallback / Escalation
```

## Control questions

- Who advances time? Tick Manager as a logical tick candidate.
- Who wakes processes? Wake-up Manager from governed signals.
- Who schedules processes? Process Scheduler; no Goal or Decision authority.
- Who maintains Workspaces? Workspace Manager; it only refreshes context.
- Who allocates scarce resources? Attention and Resource Governance.
- Who maintains Memory and Learning? Maintenance/Scheduler candidates only.
- Who monitors Reflex? Reflex Monitor; it emits candidates.
- Who invokes Brain? Brain Invocation Boundary on escalation conditions.
- Who owns final judgment? Brain.
- Who owns Reality mutation? Reality Reducer after Evidence Gateway.

## Isolation invariants

Runtime → State Update Candidate, Runtime → Wake-up Candidate, Runtime → Allocation Candidate, and Runtime → Brain Invocation Candidate are allowed.
Runtime → Goal Mutation, Runtime → Decision, Runtime → Action, Runtime → Model Call, Runtime → Hardware Call, Runtime → Automatic Learning, and Scheduler → Value Resolution are forbidden.

This is a Planning Only artifact; no real Scheduler or Runtime loop is
implemented.
