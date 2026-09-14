# Cognitive Process Model v1

## Cognitive Process

A Cognitive Process is a governed thread, not a simple task and not a Runtime
job. Its contract contains:

```text
Cognitive Process {
  intent,
  context,
  state,
  resource,
  priority,
  authority,
  lifecycle
}
```

One user request may contain multiple threads: Navigation, Time Risk,
Environment Monitoring, User State Attention, and Preparation Reminder. These
threads share a parent intent reference but retain distinct scopes and authority.

## Creation sources

Process creation may be proposed by Brain, Neural, User, or External Event. The
source creates a Process Candidate; creation does not grant Goal, Decision, or
Action authority.

## Governance fields

Each process declares owner, purpose, parent reference, allowed inputs, resource
budget candidate, priority candidate, escalation path, lifecycle, and termination
condition. It cannot bypass Brain, Reality Workspace, Middleware, or the Reducer.
