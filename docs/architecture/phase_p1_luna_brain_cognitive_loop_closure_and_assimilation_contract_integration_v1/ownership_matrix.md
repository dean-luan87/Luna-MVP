# Ownership matrix

| Contract | Owner | This integration may do |
|---|---|---|
| Brain request and global concern | `BRAIN` responsibility domain; `OWNER_UNRESOLVED` canonical runtime owner | Form a candidate request and carry refs |
| Goal → Information Need authority | `BRAIN` responsibility domain; `OWNER_UNRESOLVED` canonical runtime owner | Bind a candidate need to Goal, Intent, Concern, and Context |
| Cognitive Loop lifecycle mechanics | Cognitive Flow Governance | Own loop identity/lifecycle references |
| Attention, Hypothesis, Current World | Existing A-Route/Cognitive State Formation owners | Produce canonical candidates |
| Sufficiency | Cognitive State Formation Governance | Produce canonical Sufficiency |
| Information Gap | Cognitive State Formation Governance | Produce canonical Gap |
| Re-observation | Field Perception Orchestrator | Produce canonical Re-observation candidate |
| Stop | Cognitive State Formation Governance | Produce canonical Stop |
| Closure acceptance | `BRAIN` responsibility domain; `OWNER_UNRESOLVED` canonical runtime owner | Represent controlled acceptance; no Decision execution |
| Assimilation candidate | `BRAIN` responsibility domain; `OWNER_UNRESOLVED` canonical runtime owner | Emit candidate-only bounded references |
| Evaluation/White-box | Evaluation / White-box owners | Not invoked by this phase |
| Memory/Experience/Knowledge | Their existing admission owners | No automatic consumption or mutation |

The repository has no separate concrete Brain runtime implementation for this
boundary.  Architectural documents describe Brain-level responsibility, but
they do not prove a concrete runtime owner/API for this integration.  Every
Brain-level field therefore separates `responsibility_domain=BRAIN` from
`canonical_owner_status=OWNER_UNRESOLVED`.  Mechanical loop lifecycle remains
owned by `Cognitive Flow Governance`; semantic cognition remains with the
existing A-Route/Cognitive State Formation owners.
