# End-to-End Authority Graph

| Edge | Producer | Consumer | Semantic owner | Mutation owner | Candidate-only | Status |
|---|---|---|---|---|---|---|
| Goal/Intent/Concern → Cognitive Request | Brain responsibility domain; Intent Governance supplies Intent | request protocol | Brain semantic owner unresolved; Intent Governance owns Intent | source owners | yes | `OWNER_UNRESOLVED` for Brain request |
| Cognitive Request → Request Admission | Brain-domain producer | future admission boundary | unresolved | none | yes | `OWNER_UNRESOLVED` |
| Admitted request → Loop lifecycle | protocol caller | Cognitive Flow Governance | CFlow mechanics | CFlow candidate state | yes | `RESOLVED_TO_EXISTING_OWNER` for mechanics |
| Goal/Concern → Information Need | A/B or future semantic boundary | Need protocol | unresolved | unresolved | yes | `OWNER_UNRESOLVED` |
| Information Need → Need lifecycle | Need producer | Cognitive Flow tracking | CFlow mechanics | CFlow candidate state | yes | `RESOLVED_TO_EXISTING_OWNER` for tracking |
| Need → Observation Demand | Cognitive State Formation / Gap | Field Perception Orchestrator | CState identifies missing information; FPO controls observation demand | FPO | yes | existing split owners |
| Evidence → A-Route cognition | Observation Gateway | A-Route/CState | A-Route/CState owners | no source mutation | yes | existing canonical path |
| Cognition → Sufficiency/Stop | Cognitive State Formation Governance | Brain/CFlow consumers | Cognitive State Formation Governance | same owner | yes | resolved production |
| Sufficiency/Stop → Closure Candidate | CState proof and closure boundary | closure protocol | closure eligibility unresolved | candidate-only | yes | candidate surface only |
| Closure Candidate → Closure Acceptance | candidate closure boundary | future authorized consumer | unresolved | unresolved | yes | `OWNER_UNRESOLVED` |
| Accepted closure → lifecycle closure | authorized acceptance ref | Cognitive Flow Governance | acceptance remains external | CFlow mechanics | yes | `RESOLVED_TO_EXISTING_OWNER` for mechanics |
| Lifecycle closure → Assimilation Candidate | closure/outcome boundary | Brain-domain consumer | unresolved | none | yes | `OWNER_UNRESOLVED` |
| Assimilation Candidate → candidate routing | candidate producer | future dispatcher | unresolved | downstream owners only | yes | `OWNER_UNRESOLVED` |
| Candidate route → Memory/Experience | explicit admitted target | Memory/Experience Governance | downstream governance | Memory/Experience Governance | yes until admission | resolved downstream only |
| Candidate route → Learning | explicit admitted target | Cognitive Learning Governance | downstream governance | Cognitive Learning Governance | yes until admission | resolved downstream only |

No edge grants Brain a mutation path into an existing owner’s state.
