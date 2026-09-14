# Failure Recovery Model v1

## Failure classes

The integration model distinguishes Model Unavailable, Hardware Degraded,
Network Disconnected, Information Conflict, Invalid Evidence, Timeout,
Resource Denied, Protocol Error, and Unknown Failure.

## Recovery flow

```text
Failure
  ↓
Diagnostics
  ↓
Classification
  ↓
Fallback Candidate
  ↓
Capability Update
```

Failure does not directly change Goal, Decision, Reality, Identity, or Action.
Diagnostics preserves source, provenance, timestamp, Unknown, and failure
namespace. A fallback remains a candidate; automatic model switching is not
enabled.

## Boundary examples

- Model Unavailable produces Capability Degradation Candidate and may request
  an alternative Capability, but it does not choose a Goal.
- Hardware Degraded updates Self Capability and Self State candidates; it does
  not rewrite Reality.
- Network Disconnected changes resource/availability context and may suspend
  a Capability Process; it does not complete or abandon a Task.
- Information Conflict returns competing Evidence and Conflict Candidate to the
  Reducer; it does not silently select the newest claim.
- Invalid Evidence is rejected by the Evidence Gateway and cannot become
  Situation, Decision, or Reality.

No real recovery Runtime, Scheduler, Provider, Camera, OCR, SLAM, Hardware,
Action, Emotion, Social, or B implementation is included.

Failure does not directly change Decision, does not directly change Reality,
and does not directly change Identity. No Scheduler, No Provider, No Camera, No
OCR, No SLAM, No Hardware, No Action, No Emotion, No Social, and No B are
included.

No OCR.
