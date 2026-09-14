# Failure ownership

| Failure | Owner |
|---|---|
| Requirement incomplete | Requester / semantic requirement owner |
| Capability mismatch | Capability Governance |
| Provider unavailable | Provider Governance |
| Binding rejection | Provider Binding authority |
| Resource unavailable | Runtime / Resource owner |
| Execution failure | Runtime owner |
| Gateway ingress rejected | Observation Gateway |
| Evidence insufficient | FPO / Cognitive semantic owner |

拥有 authority 的 owner 必须承担相应 failure responsibility；没有 authority 的 requester 不承接下游 operational failure。
