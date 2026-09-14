# Fail-closed matrix

| Condition | Result | Responsibility |
|---|---|---|
| Capability Resolution/Slot missing or mismatched | blocked, no executable | Capability Governance |
| Capability↔Model binding stale or wrong owner | blocked | Capability Governance |
| Model identity/version/weights missing or stale | blocked | Model Governance |
| Model↔Provider binding missing/stale/mismatched | blocked | Provider Governance |
| Grant stale/revoked | blocked | Brain Governance |
| Permission/Safety/Resource blocked | blocked | corresponding policy owner |
| Working Envelope incompatible | blocked | Working Envelope |
| dependency/runtime readiness unavailable | blocked | Runtime Admission / evidence source |
| provenance/version missing | blocked | source owner / integration translation |
| invalidation/supersession present | blocked | owning lifecycle boundary |

No failure path constructs a success record, refreshes a record, retries,
loads a model, or invokes a Provider.
