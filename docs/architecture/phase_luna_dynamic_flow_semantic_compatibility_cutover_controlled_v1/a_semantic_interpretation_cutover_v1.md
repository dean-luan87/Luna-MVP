# A semantic interpretation cutover

The existing `wrap_dynamic_flow_output()` implementation remains the canonical compatibility wrapper. The new adapter supplies its context and governed A grant, then preserves the resulting `ASemanticDecisionBundleV1`.

The four decision owners are explicitly `A_REASONING_ROLE`:

- Current Need: `SELECT_CURRENT_NEED`;
- Local Sufficiency: `JUDGE_LOCAL_SUFFICIENCY`;
- Reconsideration: `JUDGE_RECONSIDERATION`;
- Next-step: `DECIDE_LOCAL_CONTINUATION`.

The adapter does not add a second A vocabulary or alter existing Dynamic Flow logic.
