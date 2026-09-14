# Action Governance — Existence Test v1

| Architecture | Finding |
|---|---|
| Embedded in Task | task organization becomes side-effect authorization and execution |
| Embedded in Provider | provider can execute without a stable policy/target/idempotency boundary |
| Embedded in Decision | commitment becomes execution and cannot own runtime failure cleanly |
| Independent Action Governance | separates concrete side-effect admission, audit and result from capability/provider |
| Generic adapter only | lacks a canonical owner for permission, safety, duplicate and external-effect semantics |

An independent boundary is justified, but it is a narrow governance seam and
does not imply a new Action Manager or scheduler.
