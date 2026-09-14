# Diagnostics Protocol Drift v1

Diagnostics may detect protocol version mismatch, missing/incompatible
contract refs, deprecated usage, fingerprint mismatch, or stale binding. The
result is a source-linked drift finding. Protocol Manager owns protocol
identity, lifecycle, compatibility policy, and change control. Diagnostics does
not rewrite, migrate, or approve a new protocol.
