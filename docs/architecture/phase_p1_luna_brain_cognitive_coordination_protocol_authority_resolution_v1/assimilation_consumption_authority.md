# Assimilation Candidate Consumption Authority

| Responsibility | Producer | Routing owner | Downstream consumer/mutation owner | Brain relation | Decision |
|---|---|---|---|---|---|
| Assimilation Candidate formation | controlled closure/outcome boundary | none established | none implied | CONSUME / OWNER_UNRESOLVED | `OWNER_UNRESOLVED` as authority |
| Candidate routing | candidate producer or future protocol dispatcher | `OWNER_UNRESOLVED` | per-target governance only | REQUEST | `OWNER_UNRESOLVED` |
| Memory admission/mutation | routed candidate | Cognitive Memory & Experience Governance | Cognitive Memory & Experience Governance | FORBIDDEN mutation | downstream owner resolved |
| Experience admission/mutation | routed candidate | Cognitive Memory & Experience Governance | Cognitive Memory & Experience Governance | FORBIDDEN promotion | downstream owner resolved |
| Learning admission/mutation | explicitly routed learning candidate | Cognitive Learning Governance | Cognitive Learning Governance | FORBIDDEN mutation | downstream owner resolved |
| Decision/Task/Action | explicitly routed domain candidate | Decision Governance / Task Manager / Action Boundary | respective owner | FORBIDDEN execution | downstream owners resolved |

`BrainAssimilationCandidateV1` is a governed, candidate-only handoff. Its
fields explicitly guard against World Truth, Decision, Action, Intent,
Memory, Experience, Learning, automatic loops, and automatic Tasks. No
canonical generic consumer or routing/admission API was found. Existing
Memory/Experience and Learning registries prove downstream mutation authority,
not that they currently consume this specific Brain candidate automatically.

Accordingly, this phase resolves downstream mutation ownership but leaves
Assimilation Candidate routing and consumption `OWNER_UNRESOLVED`.
