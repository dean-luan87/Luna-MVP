# Failure ownership

| Failure | Owner |
|---|---|
| incomplete preparation/request | requester or preparation owner |
| provider binding denied | Provider Governance |
| permission denied | Permission / Admission Manager |
| safety / constitution blocked | corresponding Safety Governance / Protocol Manager |
| runtime grant denied | Permission / Admission Manager |
| resource unavailable | Resource Governance / Runtime owner |
| execution instance creation failure | Runtime Executor |
| provider session start failure | Provider Runtime / Runtime Executor |
| Gateway ingress rejection | Observation Gateway Governance |
| evidence insufficient | FPO / cognitive semantic owner |

The controlled evaluator checks that a failure is not laundered as an upstream
invalid request when the input is complete and the denying owner made the
decision. It also checks that an adapter cannot acquire decision authority by
renaming a decision field as a recommendation or helper result.
