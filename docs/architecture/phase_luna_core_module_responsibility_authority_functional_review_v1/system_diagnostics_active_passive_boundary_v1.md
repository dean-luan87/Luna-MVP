# System Diagnostics Active / Passive Boundary v1

Passive diagnostics consumes existing status, telemetry, and runtime events.
Active diagnostics performs a bounded check. Both produce evidence with
observed_at, source/version, environment version, provenance, and validity
information.

Active probes cannot bypass Permission, Safety, or Resource Governance and may
not become an always-on watchdog by implication. A failed or unavailable probe
means unknown/unavailable evidence unless the contract establishes a narrower
classification. Consumers decide whether that evidence blocks admission or
changes operation.
