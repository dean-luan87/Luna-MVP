# Action Retry / Idempotency Boundary v1

Action Governance may own execution identity, duplicate detection,
idempotency-key/reference validation, retry metadata and mechanical rejection
of a duplicate. It does not autonomously retry or schedule.

Whether a failed Action should be retried is a semantic/governance decision
owned by A, Decision, Task or Brain according to failure cause and scope.
