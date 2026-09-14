# Hardware State Model v1

## Capability / State separation

Hardware Capability answers “what could this body component support?” Hardware
State answers “what is its current condition?”

```text
Hardware State
├── Available
├── Degraded
├── Limited
├── Failed
└── Unknown
```

Examples:

- Camera Capability: can provide image input; State: lens obstructed;
- GPU Capability: can contribute compute; State: thermal throttling;
- Battery Capability: can provide power; State: low charge;
- Storage Capability: can retain data; State: capacity constrained.

State is time-bound, sourced, confidence-calibrated, and reversible. State
change does not change Hardware Identity, Self Identity, Goal, or Reality.

## State transition candidate

```text
Hardware Evidence / Diagnostic
        ↓
State Update Candidate
        ↓
Reducer
        ↓
Self Capability / Self State Candidate
```

Hardware Manager reports “resource insufficient” or “vision reliability
degraded”; it does not close a Task, stop a Process, or choose a Decision.

Vision reliability degraded is a State candidate. Hardware Manager does not
stop a Process and does not choose a Decision.

The vision reliability degraded condition is explicit. Hardware Manager does
not stop a Process.

It does not stop a Process.
