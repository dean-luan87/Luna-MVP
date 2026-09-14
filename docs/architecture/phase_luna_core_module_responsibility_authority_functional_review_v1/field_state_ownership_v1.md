# Field State Ownership v1

| State | Owner | Representation elsewhere | Status |
|---|---|---|---|
| Field identity | Field boundary | refs in Context/Current World | authoritative source identity |
| Field version/transition lineage | Field Reducer/governed persistence | source-version refs | authoritative mechanical lineage |
| Entity/relation/environment state admitted to Field | Field boundary | read projections/refs | authoritative operational state, not Truth |
| Raw observation/evidence | Observation/Evidence owner | event/evidence refs | external source |
| Field event admission result | Field Event Admission | reducer input candidate | candidate/decision evidence |
| Current World payload | Current World/State Formation boundary | Field refs | derived candidate |
| Context payload | Context Foundation | Field projection refs | derived reference envelope |
| Role/Perspective overlay | Role/Perspective source/derived boundary | refs only | external/derived, never Field mutation |
| Memory/Experience | Memory/Experience governance | historical refs | external |

The primary duplication prohibition is: no Current World, Context, Working
Envelope, Semantic Outline or Cognitive Snapshot may silently copy Field payload
into a second mutable owner. They carry `field_ref`, `field_version`,
projection/candidate metadata and provenance instead.

Field accepts only the contractually admitted transition path. It must reject
wrong Field/work scope, stale transition lineage, malformed event identity,
duplicate/replayed event identity and revoked/expired event input according to
the existing admission vocabulary.
