# Luna Cognitive Operating System Architecture v1

## Position

L1 Cognitive Operating System (Cognitive OS) is the operating substrate for
Luna. It governs how modules are registered, admitted, connected, observed,
interrupted, recovered, and traced. It does not understand the world, own
Goals, make Decisions, or execute Actions.

```text
L0 Constitution
        ↓ constraints
L1 Cognitive Operating System
        ↓ lifecycle / state / event / contract governance
L2 Cognitive Core
        ↓ context and candidates
L3 Social & Emotion Boundary
        ↓ context candidates
L4 Capability & Execution Boundary
```

## Subsystems

1. Module Lifecycle System
2. Cognitive Flow Controller
3. State Management System
4. Event System
5. Trace System
6. Recovery System
7. Contract Enforcement System
8. Admission System
9. Health Monitoring System

These subsystems are contracts and governance surfaces in this phase. No
production loop, Scheduler, provider, hardware, or Action Runtime is enabled.

## Boundary principles

- L0 defines what cannot be violated; L1 enforces those constraints.
- L1 controls process and state transitions, not cognitive meaning.
- Events produce processing candidates and never directly trigger Action.
- Every State has one writer and explicit readers.
- Recovery degrades, recovers, and resumes where safe; it does not silently
  rewrite Reality or Goal.
- Admission is required before a module becomes Active.

