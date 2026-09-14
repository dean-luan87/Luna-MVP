# Loop continuity full audit

| Current behavior | Type | Target owner/disposition |
|---|---|---|
| `LoopIdentityCandidateV1` refs and lifecycle label | MECHANICAL | KEEP in Loop |
| `LoopLocalStateCandidateV1` storage of Need/hypothesis/state refs | MECHANICAL storage | KEEP; refs are not authoritative copies |
| `_local_disposition` derives `SUFFICIENT/RECONSIDER/DEFER/INSUFFICIENT` | SEMANTIC | MOVE_TO_A; Loop receives disposition ref |
| Continuity signal comparison | MIXED | source comparison can remain; A decides material impact |
| Resume decision `KEEP/SUPERSEDE/REPLAN/COMPLETE/WAITING` | SEMANTIC | MOVE_TO_A/Brain; Loop stores command |
| Stale Requirement detection and path blocking | MIXED | Capability/A reassess; Loop mechanical block remains |
| Growth guards: duplicate, diminishing value, resource envelope | MIXED | Resource/Capability governance and A decide; Loop records bounded result |
| Branch reservation refs | MECHANICAL reservation | KEEP; Brain governs materialization |
| Closure assessment reason | SEMANTIC suggestion | A/Brain owns suggestion/acceptance; Loop stores candidate |
| Closure decision acceptance | GOVERNANCE | Brain/Cognitive Flow, not Loop |
| Final freeze and history boundary | MECHANICAL | KEEP in Loop surface |
| Cognitive Outcome / Loop Package refs | MECHANICAL handoff | KEEP; Brain assimilates |

The main real leakage is semantic inference in the continuity engine, not the existence of local reference fields.

