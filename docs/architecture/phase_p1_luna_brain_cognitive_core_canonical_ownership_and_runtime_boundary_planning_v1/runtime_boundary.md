# Runtime boundary plan

This is a future API plan, not an implementation. Every Brain-facing object
must preserve source refs, execution identity, provenance, candidate status,
and explicit owner status.

| Surface | Producer | Consumer | Owner status | Candidate-only rule |
|---|---|---|---|---|
| `BrainCognitiveRequest` | Brain-domain caller; concrete owner unresolved | Future Brain protocol boundary / Cognitive Flow | `BRAIN / OWNER_UNRESOLVED` | Request only; no cognition or mutation |
| `BrainCognitiveLoopStart` | Future Brain coordinator after authorization | Cognitive Flow Governance and A-Route ingress | Brain coordinator unresolved; Flow owns mechanics | References only; no direct observation |
| `BrainCognitiveLoopUpdate` | A-Route/CState/FPO result adapters | Brain coordination boundary | Source owners remain authoritative | Carries canonical refs; does not rewrite them |
| `BrainCognitiveLoopClosureRequest` | Closure Candidate producer | Future closure authority and Flow mechanics | Brain closure authority unresolved | Candidate request; requires canonical Sufficiency and Stop |
| `BrainAssimilationCandidate` | Existing outcome/closure candidate bridge | Future Brain consumer and independent admission owners | Brain assimilation owner unresolved | Candidate only; no Memory/Experience/Knowledge mutation |

## Required refs

Future surfaces should carry, where applicable:

`brain_request_ref`, `cognitive_loop_ref`, `goal_ref`, `intent_ref`,
`concern_ref`, `context_ref`, `information_need_ref`, `execution_ref`,
`a_route_execution_ref`, `sufficiency_ref`, `information_gap_ref`,
`reobservation_ref`, `stop_ref`, closure refs, provenance refs, and version
refs.

## Boundary rule

The Brain boundary may coordinate and route canonical references. It may not
construct or mutate A-Route cognition, Field state, Decision, Task, Action,
Memory, Experience, Knowledge, or World Truth.
