# Field / Context / Current World Version Domains v1

These domains are distinct and must not be collapsed into one global state
version.

| Domain | Meaning | Invalidation trigger |
|---|---|---|
| Evidence/Observation version | evidence acquisition/admission lineage | new, revoked, duplicate, stale or conflicting evidence |
| Field version | governed Field transition lineage | admitted Field event, revocation, expiration, correction |
| Context version | assembled situation-frame lineage | changed source ref, temporal scope, validity or applicability |
| Current World version | candidate world-view lineage for a cognition cycle | new evidence, source conflict, stale or superseded candidate |
| Perspective projection version | derived Role/Perspective projection lineage | Role/Perspective/source change; carried as ref only |
| Working Envelope version | admitted cognitive-work envelope composition | governance/source constraint change |
| Cognitive Snapshot version | version-aligned candidate snapshot | any included source/version change |

## Propagation

`source change → new source/version or invalidation ref → new Context/Current
World candidate and/or snapshot → Working Envelope refresh → A impact
assessment`. This propagation does not directly issue REPLAN, change Intent,
mutate Task or change Brain governance.

## Version responsibility

Field owns Field lineage; Context owns envelope assembly lineage; Current World
formation owns candidate lineage; State Formation owns snapshot assembly
lineage. Consumers must retain the source versions rather than replacing them
with a single local timestamp.
