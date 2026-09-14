# Cognitive Loop Integration Go/No-Go

## Readiness criterion

`LUNA_COGNITIVE_RUNTIME_LOOP_INTEGRATION_READY` is a user V2 verifier result after the static contracts and fixture trace pass.

## No-go conditions

- Runtime Tick and Cognitive Tick are coupled into one decision-producing function;
- context fields or unknowns are dropped;
- Brain boundary returns an Action Command or mutates Reality/Memory/Goal;
- state writes bypass the State Update Boundary;
- cognitive stages are absent from Trace;
- any model, provider, hardware, Action, Learning, Emotion, Social, or Memory Consolidation integration appears.

The agent performs V0 only and stops at `WAITING_FOR_USER_TERMINAL_VERIFICATION`.
