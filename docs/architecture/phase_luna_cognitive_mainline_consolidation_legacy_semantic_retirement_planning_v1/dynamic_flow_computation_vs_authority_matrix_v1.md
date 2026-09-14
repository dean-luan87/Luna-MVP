# Computation versus authority

| Behavior | Computation present? | Semantic interpretation? | Authority target | State persistence |
|---|---:|---:|---|---|
| State version increment | Yes | No, if treated as lineage construction | Shared Flow / Loop mechanical surface | Loop records supplied version |
| Need map lookup | Yes | No | A selects | Loop records selected ref |
| Select next Need | Yes | Yes | A | Loop records A decision |
| Sufficiency candidate construction | Yes | Yes when status is interpreted | A | Loop records supplied sufficiency ref |
| Evidence state-version match | Yes | Boundary check only | Shared computation; A decides relevance | Loop/state lineage |
| Hypothesis invalidation refs | Yes | Yes when invalidation is judged | A | state version stores refs |
| Reconsideration candidate formatting | Yes | Yes if Flow chooses reason/target | A/B | Loop stores candidate ref |
| STOP_SUFFICIENT bookkeeping | Yes | A decides stop; Flow can calculate consequences | A → Loop command | Loop closes/freezes |
| Stale Requirement comparison | Yes | A/Capability decides supersession | Capability/A; Loop blocks stale use | Loop records disposition |
| Trace/provenance lists | Yes | No | Existing source owners | Trace remains history |

The retirement rule is `computation may remain; semantic interpretation must move to its owner`. The existing compatibility wrapper is a migration seam, not proof that the engine has lost semantic computation.

