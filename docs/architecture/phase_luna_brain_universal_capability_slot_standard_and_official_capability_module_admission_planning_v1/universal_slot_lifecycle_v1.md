# Universal Slot lifecycle

The Slot lifecycle is capability-neutral:

`EMPTY -> AVAILABLE -> BINDING_CANDIDATE -> BOUND -> ACTIVE`

with governed candidates for `SUSPENDED`, `DEGRADED`, `UNBINDING_CANDIDATE`,
`REBINDING_CANDIDATE`, `RECOVERY_CANDIDATE`, and `RETIRED`.

Slot lifecycle does not authorize Module installation or runtime execution.
Each transition requires the appropriate Capability Governance, permission,
resource, compatibility, safety, and admission checks. Existing capability
lifecycle vocabulary remains a referenced predecessor, not silently rewritten.
