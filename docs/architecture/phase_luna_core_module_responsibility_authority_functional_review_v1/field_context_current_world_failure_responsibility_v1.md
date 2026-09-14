# Field / Context / Current World Failure Responsibility v1

| Failure | Field | Context | Current World |
|---|---|---|---|
| incorrect state transition | owns | no | no |
| incorrect source assembly/binding | no | owns | owns candidate binding |
| stale acceptance | Field transition lineage | context validity | candidate validity |
| provenance loss | Field event/state lineage | assembly lineage | candidate lineage |
| cross-entity/Field contamination | owns within Field | owns cross-source frame contamination | owns cross-candidate contamination |
| invalid Context binding | no | owns | reports carried invalid ref |
| invalid Current World candidate | no | no | owns |
| unauthorized mutation | rejects Field bypass | rejects source mutation | must remain immutable/candidate |

## Common degradation rule

Missing, stale, mixed-version, conflicted or provenance-broken input produces a
rejected, partial, stale, conflicted or invalidated candidate with diagnostics
and trace refs. None of the three invents missing reality or issues semantic
recovery advice.

## Downstream ownership

A decides whether a source/candidate issue changes Need, Hypothesis,
Sufficiency, Reconsideration or Next-step. Brain owns global safety, permission,
resource and Concern/Grant consequences. Loop records refs only.
