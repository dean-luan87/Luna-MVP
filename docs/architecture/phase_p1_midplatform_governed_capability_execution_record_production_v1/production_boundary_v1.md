# Production Boundary

The integration seam is composition and translation only.

It may inspect repository-backed declarations and compose owner-issued
records into a generic `GovernedExecutionRecordBundleV1`.  It may not:

- create Capability identity or Slot lifecycle;
- register Model identity or weights;
- approve Capability↔Model compatibility;
- register Provider identity or Provider lifecycle;
- create Runtime Admission;
- select a Model or Provider;
- load a model or invoke a Provider;
- refresh stale records;
- mutate source state.

The generic bundle is translated to
`CanonicalYOLO11nUpstreamRecordsV1` only after all required records exist.
The current implementation never reaches that translation because the
canonical declarations are incomplete.

