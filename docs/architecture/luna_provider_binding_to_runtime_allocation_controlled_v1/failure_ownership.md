# Failure ownership

| Failure | Owner |
|---|---|
| Requirement incomplete | upstream requester / requirement owner |
| Capability mismatch | Capability Governance |
| Provider unavailable or ineligible | Provider Governance |
| Binding rejected | Provider Binding authority |
| Resource unavailable / allocation denied | Runtime / Resource owner |
| Execution instance creation failure | Runtime / Execution owner |
| Gateway ingress rejected | Observation Gateway |
| Evidence insufficient | FPO / cognitive semantic control |

本阶段只验证责任映射，不触发任何上述 runtime 动作。`validate_failure_ownership` 会阻止无 authority、owner mismatch 或将下游失败伪装为 upstream failure。
