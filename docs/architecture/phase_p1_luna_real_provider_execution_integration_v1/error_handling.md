# Error Handling

The bridge remains fail-closed. Missing model/dependency, missing source,
invalid canonical admission, provider exception, and malformed provider
output produce an explicit non-success result and no fabricated Observation or
Evidence. A successful provider call with zero detections is represented as
`EMPTY_SUCCESS`; it is distinct from `ERROR` or `UNAVAILABLE` and produces no
manufactured positive detection output. Any downstream empty-observation
handling remains governed by the existing Gateway contract.

This phase does not add a fallback provider, network download, dependency
installation, or retry loop. LIVE_RUNTIME still remains inside the controlled
Gateway boundary: `controlled_integration_only` must be true. Source-frame
dimensions are taken from actual image metadata when available, rather than
using a generic 640x480 label.
