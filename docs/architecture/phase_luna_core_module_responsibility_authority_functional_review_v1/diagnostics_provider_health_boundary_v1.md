# Diagnostics Provider Health Boundary v1

Diagnostics may report provider instance/adapter availability, capacity,
latency, recent failures, degraded/unavailable state, and stale health records.
Provider Governance owns provider admission, invocation identity, execution
contract, and provider-specific enforcement. A provider health PASS does not
authorize invocation and a failed invocation does not by itself prove ongoing
provider unhealthiness.

Circuit-breaker or health-store assets are runtime evidence/compatibility
mechanisms, not a new semantic owner. Diagnostics preserves uncertainty and
time lineage.
