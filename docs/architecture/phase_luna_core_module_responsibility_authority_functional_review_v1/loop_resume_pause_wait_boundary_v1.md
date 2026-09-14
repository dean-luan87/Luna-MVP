# Loop Resume / Pause / Wait Boundary

A/Brain decide why a process should KEEP, REPLAN, SUPERSEDE, COMPLETE or WAITING. Loop records/restores the specified mechanical state.

- `KEEP` → resume recorded state
- `REPLAN` → record supplied new state/Need refs, then resume mechanics
- `SUPERSEDE` → supersede supplied recorded refs
- `COMPLETE` → close/freeze supplied state
- `WAITING` → mechanical WAIT

Loop must not infer any of these from missing evidence, resource state, stale refs or lifecycle signals. The legacy continuity engine's resume interpretation is semantic leakage and a retirement candidate.
