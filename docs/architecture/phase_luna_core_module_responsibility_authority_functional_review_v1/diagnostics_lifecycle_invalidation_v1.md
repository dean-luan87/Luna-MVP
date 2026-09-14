# Diagnostics Lifecycle and Invalidation v1

Conceptual lifecycle: source/probe available → evidence collected → finding or
classification → versioned snapshot → consumer handoff → stale, superseded,
or expired. An incident candidate correlates findings and is resolved or
superseded externally.

Invalidation triggers include time expiry, runtime restart, dependency/model
change, Provider instance change, device reconnect, protocol/config update,
and environment change. Relevant consumers must re-evaluate admission; no
direct cross-owner mutation is implied.
