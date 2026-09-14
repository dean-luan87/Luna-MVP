# Attention Dynamic Flow / A Route Overlap v1

| Existing pattern | Target classification |
|---|---|
| Cognitive State Formation builds/ranks AttentionCandidateV1 | COMPATIBILITY_ONLY candidate computation; future allocation authority should be clarified |
| Observation Attention Layer region priority | KEEP as candidate focus/route input; not execution |
| Attention Allocation L0→value→budget | KEEP/NARROW; goal input must be admitted relevance/Need/policy, not raw semantic authority |
| Task-aware visual focus policy | NARROW/COMPATIBILITY_ONLY; Task supplies constraints, not Attention ownership |
| Dynamic Flow reobserve/follow-up/priority | COMPATIBILITY_ONLY; semantic Next-step remains A, acquisition remains Observation |
| A Route/Product Loop focus stages | LEGACY orchestration; split into A Need, Attention candidate and Observation handoff |
| Prompt policy or route selection | CANDIDATE/COMPATIBILITY_ONLY; no Provider selection authority |

Repository conflict: existing cognitive-state code calls `_select_attention()`
and creates an `AttentionSelectionCandidateV1`, while the canonical Cognitive
State boundary says State Formation carries/assembles candidate refs rather than
owning Attention ranking. This is a future adapter/cutover issue, not a runtime
change in this phase.
