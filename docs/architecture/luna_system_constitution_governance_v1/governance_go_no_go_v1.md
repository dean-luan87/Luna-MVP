# System Constitution Governance Go / No-Go v1

## Readiness condition

`LUNA_SYSTEM_CONSTITUTION_GOVERNANCE_READY` is a structural readiness signal.
It requires principles, authority hierarchy, permissions, conflict policy,
change control, ownership, invariants, safety, and future boundaries to parse
and remain internally consistent.

## Blockers

- Missing or invalid contract;
- Non-unique authority or state owner;
- Permission conflict that grants lower layers L0 authority;
- Missing conflict resolution or change-control lifecycle;
- Invariant coverage gap;
- Runtime, model, provider, hardware, Emotion, Social, or automatic
  self-modification introduced in this Planning Only phase.

## Authority

Agent may run V0 static checks only. The user terminal runs the final phase
verifier (V2). ChatGPT performs the V3 audit and final decision. The Agent
stops at `WAITING_FOR_USER_TERMINAL_VERIFICATION`.
