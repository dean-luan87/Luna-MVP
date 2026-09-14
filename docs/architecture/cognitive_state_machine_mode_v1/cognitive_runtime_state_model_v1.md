# Cognitive Runtime State Model v1

## Runtime states

```text
Cognitive Runtime State
├── Idle
├── Observe
├── Engage
├── Analyze
├── Escalated
├── Recover
└── Maintain
```

These are runtime states, not Tasks, Goals, Decisions, or Actions. These are not
Goals. These are not Goals. These are not Decisions. These are not Actions. Idle means
no active foreground demand. Observe organizes incoming Reality candidates.
Engage binds an active process context. Analyze represents a higher processing
candidate. Escalated requests Brain evaluation. Recover protects resources and
continuity. Maintain supports background organization.

## State candidate boundary

State Evaluation produces a Runtime State Candidate. It must include trigger,
current state, target state, Field, resource context, confidence, provenance,
and exit condition. A candidate is not an automatic state change and cannot
modify Reality, Goal, Decision, Self Identity, or Action. The state machine
does not modify Reality, does not modify Goal, and does not modify Decision.

## Stability

Every state has entry, maintenance, exit, timeout, and recovery conditions.
State transitions preserve Identity and do not create a second subject. The
Reducer remains the sole State mutation authority.
