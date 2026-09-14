# Negative integration cases

The focused cases are:

- stale Capability↔Model binding;
- blocked Runtime Admission;
- stale Executable Capability;
- Model↔Provider model mismatch;
- invalidation propagation;
- revoked Grant represented by invalidation;
- source/model version mismatch.

Each case must stop at bundle translation or context validation. No invalid
upstream record may produce a current/executable Provider Admission candidate.
