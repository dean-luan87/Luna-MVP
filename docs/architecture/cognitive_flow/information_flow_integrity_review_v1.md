# Information Flow Integrity Review v1

## Canonical flow

```text
External Capability → Evidence → Reality Workspace → Situation → Decision Candidate → Outcome → Experience Candidate
```

The canonical flow preserves source, provenance, timestamp, confidence,
uncertainty, capability reference, and intent reference where applicable.

## Forbidden jumps

- Model Output → Decision is forbidden.
- Model Output → Goal is forbidden.
- Model Output → Emotion or Goal is forbidden.
- Evidence → Decision without Reality Workspace and Situation is forbidden.
- Experience → Current Fact without Reality Confirmation is forbidden.
- Registry State → Self Identity is forbidden.
- Diagnostics → Action is forbidden.

## Integrity review

The reviewer checks that external capability output remains Evidence Candidate,
that Reality Workspace is the fact-layer boundary, and that A Route produces
Situation and Decision Candidate rather than executing. A high-confidence model
claim cannot bypass Fact Admission, Reducer, Brain, or Middleware governance.
