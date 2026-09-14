# Cognitive Workspace Go / No-Go v1

## Required readiness checks

- Workspace schema contains Active Field, Role, Relationship, Task, Goal, Attention, Unknown, Risk, Memory, Drive, and Value context.
- Workspace references Field and does not create or mutate Field.
- Attention controls admission into Workspace; Workspace does not allocate Attention.
- Memory enters through a retrieval candidate and cannot override Reality.
- Brain receives a governed Cognitive Workspace Package and retains Decision authority.
- Known, Unknown, and Conflict states are preserved.
- Lifecycle supports Created, Active, Updated, Background, and Closed.
- Multiple Workspaces remain isolated as Primary or Background contexts.
- B Route integration is a Snapshot placeholder only.

## Explicit prohibitions

No Decision, No Reasoning, No Planning, No Emotion Runtime, No B Route Runtime,
No automatic learning, No Memory modification, No Action Runtime, No model training,
and No hardware calls. Workspace cannot modify Reality, Goal,
Identity, or Decision.

The Agent performs V0 static checks only, does not run the Final Phase Verifier,
and stops at `WAITING_FOR_USER_TERMINAL_VERIFICATION`.
