# Diagnostics Failure Responsibility v1

Diagnostics owns wrong probe interpretation, incorrect health classification,
stale current publication, provenance loss, cross-component contamination,
invalid drift/aggregation, and failure to expose unknown or conflict. It does
not own Brain policy, A reasoning, Capability Scope, Runtime Admission,
Provider execution, Action outcome, or remediation unless an incorrect
diagnostic output caused the downstream error.

The consumer owns its use of supplied evidence: Runtime Admission owns the
admission result, Provider owns invocation, and Maintenance owns remediation.
