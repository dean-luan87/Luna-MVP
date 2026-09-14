# Cognitive Runtime Life Process Go / No-Go v1

## Required readiness checks

- Cognitive Runtime is defined as a lifecycle plane, not Brain or Decision. It is not Decision authority.
- Tick, Wake-up, Process Scheduler, Workspace Manager, Attention Scheduler, Maintenance, Reflex Monitor, and Brain Invocation Boundary are separated.
- Wake-up sources include Reality Change, Field Change, Attention Trigger, Reflex Signal, and Task Deadline.
- Process lifecycle includes Created, Activated, Running, Background, Suspended, Completed, and Archived.
- Resource constraints and State Synchronization preserve module boundaries.
- Brain escalation conditions include Unknown, Conflict, Risk, and high cost.
- Failure flow is Diagnostics → Fallback Candidate → Escalation.

## Explicit prohibitions

No real Scheduler, No Runtime loop, No model call, No Hardware Runtime, No Action Runtime, No B Simulation, and No automatic Learning execution. Runtime
cannot modify Goal, Decision, Value, Reality, Identity, or Action.

The Agent performs V0 static checks only, does not run the Final Phase Verifier,
and stops at `WAITING_FOR_USER_TERMINAL_VERIFICATION`.
