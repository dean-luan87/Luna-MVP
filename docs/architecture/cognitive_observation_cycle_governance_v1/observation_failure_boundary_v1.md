# Observation Failure Boundary v1

## Failure path

```text
Capability Failure
      ↓
Evidence Quality Decline
      ↓
Observation Retry Candidate
      ↓
Alternative Capability Candidate
```

The path is a governance candidate. It does not automatically execute a
retry, switch a Provider, open a Camera, call OCR, call SLAM, change Reality,
or trigger Action.

## Failure classes

- Capability unavailable;
- Provider unavailable;
- OCR/SLAM/text or spatial quality below boundary;
- protocol error;
- resource budget unavailable;
- timeout or stale Evidence;
- incomplete coverage;
- conflicting Evidence;
- environment limitation;
- Unknown.

Failure returns to Diagnostics with provenance and request reference. It may
produce a Self Capability Candidate, but it does not directly modify the Self
Model, Goal, Field, or Decision Policy. Missing information remains Unknown.
The governance layer does not directly modify the Self Model and does not
automatically execute a retry.

This boundary does not automatically execute a retry.

## Stop boundary

Repeated failure does not become automatic learning. Escalation, alternative
capability selection, and Brain review remain candidates governed by their
respective layers.
