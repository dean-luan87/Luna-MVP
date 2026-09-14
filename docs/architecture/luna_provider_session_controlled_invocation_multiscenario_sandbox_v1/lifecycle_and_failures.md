# Lifecycle and failure boundaries

Session states include `CREATED`, `STARTED`, `COMPLETED`, `FAILED`, `STOPPED`,
`REVOKED`, and `TIMED_OUT`.

Grant revoke/expiry/staleness, binding revoke, released allocation, invalid
execution instance, and lineage mismatch all fail closed. Duplicate start is
blocked without a second invocation record. Timeout is a logical controlled
trigger; no wall-clock timer is used. Retry, provider fallback, and autonomous
provider continuation are deferred/forbidden.

Failure ownership remains separated:

- grant failure → Permission / Admission Manager;
- binding failure → Provider Governance;
- resource/allocation failure → Resource Governance / Runtime Executor;
- session or controlled invocation failure → Provider Runtime Governance;
- semantic continuation failure → FPO.
