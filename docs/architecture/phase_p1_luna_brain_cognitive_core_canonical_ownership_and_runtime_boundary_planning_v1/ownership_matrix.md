# Ownership matrix

`OWN` means Brain is the established semantic and mutation owner. `COORDINATE`
means Brain may coordinate references without owning source state. `REQUEST`
means Brain may submit a bounded request. `CONSUME` means Brain may read a
candidate/result. `REFERENCE_ONLY` means no Brain semantic or mutation
authority is implied. `FORBIDDEN` means Brain must not perform the operation.
`OWNER_UNRESOLVED` records a missing canonical runtime authority.

| Item | Semantic owner | Mutation owner | Brain relationship |
|---|---|---|---|
| Goal | Brain responsibility domain; runtime owner unresolved | OWNER_UNRESOLVED | COORDINATE / OWNER_UNRESOLVED |
| Intent | Intent Governance | Intent Governance | REFERENCE_ONLY |
| Concern | Brain architectural concern; active cognition owned by A/CState boundary | OWNER_UNRESOLVED for global Brain concern | COORDINATE |
| Context | Context Foundation | Context Foundation | REFERENCE_ONLY |
| Role | OWNER_UNRESOLVED | OWNER_UNRESOLVED | REFERENCE_ONLY |
| Field | Field State Reducer / Field Event Admission | Field State Reducer | REFERENCE_ONLY / FORBIDDEN mutation |
| Attention | Cognitive State Formation Governance | Cognitive State Formation Governance | REQUEST / CONSUME |
| Information Need | Canonical cognition for active need; Brain acceptance owner unresolved | Existing producing owner; no Brain mutation | REQUEST / CONSUME |
| Observation Demand | Cognitive State Formation produces need/gap; FPO admits demand | Field Perception Orchestrator | REQUEST |
| Capability Requirement | Capability Registry / Capability Governance | Capability Governance | REQUEST |
| Evidence | Source producer and Observation Gateway admission | Source/admission owners | CONSUME / REFERENCE_ONLY |
| Hypothesis | Cognitive State Formation Governance | Cognitive State Formation Governance | CONSUME |
| Current World Candidate | Cognitive State Formation Governance | Cognitive State Formation Governance | CONSUME |
| Sufficiency | Cognitive State Formation Governance | Cognitive State Formation Governance | CONSUME |
| Information Gap | Cognitive State Formation Governance | Cognitive State Formation Governance | CONSUME / REQUEST |
| Re-observation | Field Perception Orchestrator | Field Perception Orchestrator | REQUEST |
| Stop | Cognitive State Formation Governance | Cognitive State Formation Governance | CONSUME |
| Cognitive Loop lifecycle | Cognitive Flow Governance | Cognitive Flow Governance | COORDINATE |
| Closure Candidate | A/Cognitive outcome candidate boundary | Candidate-only; lifecycle mechanics remain Flow-owned | CONSUME |
| Closure Acceptance | Brain responsibility domain; runtime owner unresolved | OWNER_UNRESOLVED; no mutation in this phase | OWNER_UNRESOLVED |
| Assimilation Candidate | Brain responsibility domain; runtime owner unresolved | No automatic mutation | CONSUME / OWNER_UNRESOLVED |
| Decision | Decision Governance | Decision Governance | REFERENCE_ONLY / FORBIDDEN execution |
| Task | Task Manager | Task Manager | REFERENCE_ONLY / FORBIDDEN execution |
| Memory | Cognitive Memory & Experience Governance | Cognitive Memory & Experience Governance | REQUEST / FORBIDDEN mutation |
| Experience | Cognitive Memory & Experience Governance | Cognitive Memory & Experience Governance | REQUEST / FORBIDDEN promotion |
| Emotion | Emotion integration boundary / unresolved canonical mutation owner | Emotion owner, if admitted by its contract | REFERENCE_ONLY |
| Self / Identity | Self Governance | Self Governance | REFERENCE_ONLY |
| Learning | Cognitive Learning Governance | Cognitive Learning Governance | REQUEST / FORBIDDEN mutation |

Semantic ownership and mutation ownership are intentionally not collapsed.
