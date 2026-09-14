# Diagnostics Governance Model v1

Diagnostics is an observability and classification plane, not a control plane.

## It detects

- anomaly and health degradation;
- state, permission, protocol, and resource drift;
- latency, timeout, invalid output, and provider errors;
- Registry inconsistency and lifecycle violations;
- Evidence quality and Capability confidence decline.

## It emits

Diagnostics emits Diagnostic Candidate, Failure Classification Candidate,
Fallback Candidate, Capability Update Candidate, and Governance Blocker
Candidate. It does not emit Action, Goal, Decision, Reality Write, or automatic
repair.

## Failure flow

```text
Failure → Diagnostics → Classification → Fallback Candidate
       → Capability / Resource / Protocol Update Candidate
```

Diagnostics preserves provenance, timestamp, confidence, unknowns, and
correlation. It cannot hide a failure, delete a check, weaken Constitution, or
become a second Brain.

Diagnostics handles protocol errors. It may emit a Governance Blocker Candidate,
not Action, not Goal, not Decision, and not Reality Write. Automatic repair is
not permitted. Diagnostics cannot weaken Constitution.

Automatic repair is not permitted.

No automatic repair is permitted.
