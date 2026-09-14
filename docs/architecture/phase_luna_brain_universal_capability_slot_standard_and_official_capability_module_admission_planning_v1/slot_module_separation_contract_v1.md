# Slot versus Capability Module separation

`Capability Slot != Capability Module`.

The Slot is a stable binding surface. The Module describes what Luna may be
able to do. A Slot may be empty, bound, unbound, rebound, degraded, or
recoverable. Unbinding a Module does not erase Slot identity or historical
binding records.

`Capability Module != Model`, `Capability Module != Provider`, and
`Capability Module != Knowledge`. A Module may remain the same capability
across compatible implementation/model/provider replacement.

Binding, unbinding, rebinding, replacement, and restoration are separate
governed candidates. Compatibility and admission must be re-evaluated before
rebinding or activation.
