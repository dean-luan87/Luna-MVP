# A / Dynamic Flow Cutover Map v1

| Dynamic Flow behavior | Current source | Target classification | Future cutover |
|---|---|---|---|
| `_select_next_need()` | `cognitive_dynamic_loop_engine_v1.py` | MUST_EVENTUALLY_RETIRE as authority; COMPUTATION_SOURCE only if useful | compatibility output → A Current Need decision |
| `_reconsideration()` | same engine | COMPATIBILITY_ONLY | output candidate → A Reconsideration |
| sufficiency candidate/status construction | same engine | COMPUTATION_SOURCE / COMPATIBILITY_ONLY | A judges SUFFICIENT/INSUFFICIENT/RECONSIDER |
| next-step disposition construction | same engine | COMPUTATION_SOURCE / COMPATIBILITY_ONLY | A `DECIDE_LOCAL_CONTINUATION` |
| active hypothesis refs and invalidated refs | Dynamic Flow state transition | COMPUTATION_SOURCE | A owns active hypothesis judgment |
| state-version advancement | Dynamic Flow | COMPUTATION_SOURCE | retain deterministic lineage; A supplies semantic interpretation |
| evidence acceptance/bookkeeping | Dynamic Flow | COMPUTATION_SOURCE | A judges relevance/consequence |
| stale requirement refs | Dynamic Flow | COMPUTATION_SOURCE | Capability/A assess semantic consequence; Loop records refs |
| provisional non-binding plan refs | Dynamic Flow | COMPUTATION_SOURCE | no semantic authority |
| trace/provenance | Dynamic Flow | KEEP_AS_SHARED_COMPUTATION | preserve lineage |

Active callers and fixtures still consume legacy fields. Removal requires compatibility callers migrated, Runner/Verifier assertions moved to A-owned refs, and consolidated regression coverage.
