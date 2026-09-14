# Dynamic Flow Post-Migration Disposition

| Current responsibility in `DynamicCognitiveFlowEngineV1` | Disposition | Finding |
|---|---|---|
| input candidate validation and candidate-only guards | KEEP_AS_SHARED_COMPUTATION | useful generic boundary validation |
| state-version advancement and lineage construction | KEEP_AS_SHARED_COMPUTATION | deterministic reference/history machinery |
| evidence acceptance/ignored evidence bookkeeping | KEEP_AS_SHARED_COMPUTATION | transport/computation, subject to source-owner refs |
| requirement/resolution/invocation reference collection | KEEP_AS_SHARED_COMPUTATION | no provider invocation; preserves stale filtering |
| stale requirement calculation | CONVERT_TO_LOOP_MECHANICAL only for recording; MOVE_TO_A for semantic invalidation | stale fact can be computed, but invocation eligibility/adoption is governed |
| `_select_next_need` | MOVE_TO_A | Need selection is A-owned |
| `_reconsideration` | MOVE_TO_A | Reconsideration judgment is A-owned |
| capability unavailable/degraded interpretation | MOVE_TO_A | A decides alternative evidence/reconsideration |
| execution SUCCESS + requirement UNSATISFIED interpretation | MOVE_TO_A | outcome relationship is semantic cognition, not generic Loop authority |
| goal sufficiency decision construction | MOVE_TO_A | A local sufficiency; Brain global adjudication |
| `STOP_SUFFICIENT` semantic next step | MOVE_TO_A | A emits semantic decision; Loop receives CLOSE/FREEZE |
| provisional plan non-materialization bookkeeping | KEEP_AS_COMPATIBILITY_ONLY | useful candidate-only plan boundary; no queue |
| final disposition / next-step output fields | KEEP_AS_COMPATIBILITY_ONLY, then DEPRECATE_LATER | preserve verified fixtures while A wrapper is migration seam |

## Conclusion

Do not delete Dynamic Flow. Retain generic state/evidence/reference computation and the verified compatibility source. Narrow semantic decision production behind A-owned adapters in a later controlled cut line.
