# Transition Audit

Transitions are checked for unique IDs, execution ref, cycle/order, source and
target semantics, and absence of orphan or duplicate transitions.

Case B must expose the equivalent ordered edges:

`current-world-to-sufficiency` → `sufficiency-to-information-gap` →
`information-gap-to-reobservation` → `reobservation-to-next-cycle`, then
Cycle 2 revision → final sufficiency → stop.

String existence alone is insufficient; the audit also compares execution and
cycle context from the canonical proof and archived route metadata.
