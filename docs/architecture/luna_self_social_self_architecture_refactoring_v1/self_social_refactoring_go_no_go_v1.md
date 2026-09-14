# Self / Social Self Refactoring Go / No-Go v1

## Readiness condition

`LUNA_SELF_SOCIAL_SELF_ARCHITECTURE_READY` is a structural refactoring signal.
It requires Self Layer and Social Self Layer to have distinct owners,
Integration to be candidate-only, Emotion to remain a boundary placeholder,
and migration mappings to remain conceptual only.

## Blockers

- Self and Social Self share a protected owner without an explicit boundary;
- Role or Relationship can rewrite Core Identity or Constitution;
- Integration directly mutates Self, Social Self, Brain, or Action;
- Emotion is treated as a runtime or authority;
- Any code refactor, file move, deletion, Memory migration, or Runtime behavior
  is introduced in this Planning Only phase.

## Authority

Agent may run V0 static checks only. The user terminal runs the final verifier
(V2). ChatGPT performs the V3 audit and final decision. The Agent stops at
`WAITING_FOR_USER_TERMINAL_VERIFICATION`.
