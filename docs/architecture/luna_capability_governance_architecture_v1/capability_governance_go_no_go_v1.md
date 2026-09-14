# Capability Governance Go / No-Go v1

## Readiness condition

`LUNA_CAPABILITY_GOVERNANCE_ARCHITECTURE_READY` is a structural readiness
signal. It requires all contracts to parse, Capability Registry to remain the
unique capability owner, Model Manager and Provider boundaries to be explicit,
admission hierarchy to be capability-first, and Brain/Self boundaries to hold.

## Blockers

- Missing or invalid required asset;
- Duplicate Capability owner;
- Model Manager presented as cognitive authority;
- Provider direct access to Brain, Reality, State, Goal, or Memory;
- Admission hierarchy that allows implementation assets to self-admit;
- Runtime, model, provider, hardware, scheduler, upgrade, recovery, or action
  implementation introduced in this Planning Only phase.

## Authority

Agent may run V0 static checks only. The user terminal must run the final phase
verifier (V2). ChatGPT performs the V3 audit and final decision. The Agent
stops at `WAITING_FOR_USER_TERMINAL_VERIFICATION`.
