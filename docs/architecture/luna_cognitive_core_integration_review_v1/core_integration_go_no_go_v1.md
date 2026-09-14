# Cognitive Core Integration Go / No-Go v1

## Readiness condition

`LUNA_COGNITIVE_CORE_BASELINE_READY` is a structural readiness signal only.
It requires all phase assets to parse, the master flow to be continuous, each
reviewed concept to have one owner, and the dependency graph to be acyclic.

## Blockers

- Missing or invalid phase assets;
- Broken master-flow link;
- Duplicate owner for a core concept;
- Permission conflict or forbidden provider path;
- Dependency cycle;
- Runtime/model/provider/hardware/action/emotion/social/automatic-learning
  implementation introduced in this Planning Only phase.

## Authority

V0 static checks are Agent-authorized and do not grant GO. The user terminal
must run the final phase verifier (V2). ChatGPT performs the V3 audit and final
decision. The Agent stops at `WAITING_FOR_USER_TERMINAL_VERIFICATION`.
