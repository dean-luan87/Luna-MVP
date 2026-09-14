# Diagnostics Health and Failure Semantics v1

`HEALTHY`/`AVAILABLE` indicate an observed condition; `VERIFIED` indicates a
stronger contract check; `DEGRADED` is impaired but not necessarily blocked;
`UNAVAILABLE` is not currently usable; `BLOCKED` is a governance/admission
consequence; `UNKNOWN` lacks sufficient evidence; `STALE` has expired validity;
`FAILED` is a condition/event requiring source context.

Health is ongoing state, failure is a specific event/result. Repeated failure
may support a candidate degraded-health classification, but Diagnostics
preserves uncertainty and does not overclaim root cause.
