# Diagnostics Freshness and Snapshot v1

Every runtime-relevant diagnostic should carry `observed_at`, source identity
and version, environment/runtime version, validity window or TTL where
applicable, provenance, and stale status. A stale PASS cannot remain
indefinitely authoritative.

Live telemetry is current source evidence; a Diagnostic Snapshot is a bounded,
versioned health picture. Consumers must distinguish current, recent, stale,
unknown, and unavailable. No continuous monitor or scheduler is created here.
