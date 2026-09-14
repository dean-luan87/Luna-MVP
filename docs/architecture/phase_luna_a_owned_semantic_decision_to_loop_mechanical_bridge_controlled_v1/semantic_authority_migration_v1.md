# Semantic Authority Migration

## Current implementation source

`DynamicCognitiveFlowEngineV1.run_case()` currently selects the next Need,
constructs goal sufficiency candidates, constructs reconsideration candidates,
and emits next-step disposition. Its registry owner remains
`Cognitive Flow Governance`.

## Controlled target boundary

At this phase boundary, the three decisions are represented as A-owned
candidate decisions:

| Decision | A authority | Loop residual |
| --- | --- | --- |
| Current Need | `SELECT_CURRENT_NEED` | `RECORD_NEED_REF` |
| Local sufficiency | `JUDGE_LOCAL_SUFFICIENCY` | record supplied ref / mechanical command |
| Reconsideration / next step | `JUDGE_RECONSIDERATION`, `DECIDE_LOCAL_CONTINUATION` | record, wait, pause, close or freeze |

This is a compatibility migration seam, not a claim that Dynamic Flow no
longer computes semantic values internally.
