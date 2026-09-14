# Canonical Edge Authority Contract v1

| Edge | Producer → output | Class | Admission/mutation authority | Consumer / failure return |
|---|---|---|---|---|
| Brain→Envelope | Brain refs → Envelope Candidate | BINDING/ADMISSION | Working Envelope under Brain Concern/Grant | Semantic/State Formation/A; stale→A/Brain |
| Envelope→Outline | Envelope → Outline | FORMATION | Semantic Module lifecycle | A; malformed→Semantic Module |
| Envelope→Snapshot | Envelope → Snapshot Candidate | FORMATION/VALIDATION | Cognitive State Formation | A; invalid→State Formation/A |
| A→Attention | Requirement → focus candidate | BINDING | Attention allocation | Observation/Capability; budget conflict→A/Brain |
| A→Capability | Requirement → Capability Requirement | FORMATION/BINDING | Capability Governance | Runtime Admission; invalid→A |
| Capability→Runtime | resolution/binding → executable candidate | ADMISSION | Runtime Admission | Provider/Observation/Action; block→A/Task |
| Runtime→Observation | executable ref → Observation Request | BINDING/ADMISSION | Observation | Provider; invalid→A/Task |
| Observation→Provider | request → Provider Admission input | BINDING | Provider Governance | invocation; block→Observation/A |
| Provider→Evidence | Result → Evidence Candidate | FORMATION/MAPPING | Gateway | Evidence Admission; malformed→Provider/Gateway |
| Evidence→Field/World | admitted evidence → candidates | FORMATION/BINDING | Field admission for Field; Current World representation for World candidate | A; stale→A/refresh |
| A→Decision | local disposition → DecisionCandidate | FORMATION | Decision Governance | Task/Action; rejected→A/Brain |
| Decision→Task | approved Decision → Task | ADMISSION/BINDING | Task | Action; blocked→A/Decision |
| Task→Action | Task → ActionCandidate | FORMATION | Action Governance | Provider; invalid→Task/A |
| Action→Provider | admitted Action → invocation | ADMISSION/EXECUTION | Action then Provider | result; fail→Task/A/Outcome |
| Result→Outcome | results → OutcomeCandidate | FORMATION/EVALUATION | Outcome Evaluation | Brain; uncertain→A/Brain |
| Outcome→Brain | candidate → adjudication | ADMISSION/EVALUATION | Brain | Goal/Concern/Assimilation |
| Brain→Loop | authorized refs → close/freeze/archive | MECHANICAL_PERSISTENCE | Loop mechanics | history; no semantic inference |

Every edge requires source versions, trace identity, provenance, and invalidation behavior. No edge grants the consumer mutation authority over producer state.

