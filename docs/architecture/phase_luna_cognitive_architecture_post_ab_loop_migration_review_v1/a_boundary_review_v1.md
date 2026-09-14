# A Boundary Review

## Current clean responsibilities

The A-owned bridge explicitly validates A authority for:

- Current Need selection;
- Local Sufficiency;
- Reconsideration;
- Next-step disposition.

The A→B-CR bridge adds A-owned B request and A-owned result evaluation. The A→Loop path maps supplied semantic decisions to mechanical commands without making Loop infer semantics.

## Residual duplication

`DynamicCognitiveFlowEngineV1` still calculates `current_need_ref`, sufficiency candidates, reconsideration, and next-step dispositions. The compatibility wrapper changes the authority interpretation at the boundary but does not remove internal computation.

`Cognitive State Formation` still constructs Attention, Hypothesis, Current World and state candidates. These are upstream/shared candidate computations, not automatically A ownership, but the A working-envelope handoff is not unified.

## Finding

A semantic authority is **boundary-complete for the migrated three decisions**, but not implementation-complete across all current computation sources. Classification: `COMPATIBILITY_ONLY` at the adapter; `REAL LEAKAGE` risk inside Dynamic Flow until a later controlled migration seam narrows it.
