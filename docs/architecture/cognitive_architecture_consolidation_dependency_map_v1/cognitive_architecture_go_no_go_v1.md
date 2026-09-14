# Cognitive Architecture Consolidation Go / No-Go v1

## Readiness checks

- Canonical model and module inventory are present.
- Required, Optional, Candidate, and Future Interface dependencies are
  classified.
- Information-flow matrix distinguishes permitted candidate flow from
  prohibited authority paths.
- Authority ownership matrix identifies Reality, Attention, Goal, Decision,
  Action, Experience, Learning, Capability, and Governance owners.
- State ownership map records Owner, Writer, and Reader for each state.
- Canonical loop is `Observe → Represent → Understand → Hypothesize → Evaluate
  → Commit → Prepare Action → Feedback → Learn → Adapt`.
- Migration map is candidate-based and does not mutate runtime or prior assets.
- Boundary audit preserves Reality, Reducer, Brain, Attention, Action Boundary,
  and Governance authority.
- Unknown and Provenance remain first-class fields.

## Required negative guards

No new cognitive module; no Runtime implementation; no model integration; no
hardware integration; no Action execution; no automatic Learning; no B
Simulation; no Emotion Runtime; no `Learning → Reality`; no `Emotion → Decision
Override`; no `Capability → Goal Creation`; no `Provider → Brain Direct Access`;
no direct Reality mutation; no ownership drift; no hardcoded pass; no deleted
checks; no renamed failure hiding.

Contract keywords: no hardware integration; no B Simulation; Emotion → Decision
Override; no deleted checks.
Exact guard: Emotion → Decision Override.

## Verification authority and stop point

V0 static checks, JSON parsing, AST checks, and `py_compile` are Agent-allowed.
V1 is not authorized in Planning Only mode. V2 Final Phase Verification is
User Terminal Only. V3 Final Audit and Decision are ChatGPT Only. V0 does not
grant GO. The Agent stop status is
`WAITING_FOR_USER_TERMINAL_VERIFICATION`.

## No-go conditions

Block if a matrix grants a reader write authority, if a forbidden path is
listed as allowed, if a state has no Owner/Writer, if a migration silently
changes active assets, or if any runtime/model/hardware/action behavior is
implemented in this phase.
