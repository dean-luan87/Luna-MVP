# Capability Invocation Boundary v1

## Who may request

Attention, Observation Cycle, and Situation Requirement may submit a
Capability Requirement. Brain may provide governed Goal/authorization context,
but Brain does not directly execute or call a Model. Provider and Model cannot
submit their own request. Runtime cannot invent a Cognitive Need.

```text
Need
  ↓
Capability Requirement
  ↓
Capability Request
  ↓
Admission Candidate
  ↓
Provider Invocation Candidate
```

## What invocation means

Invocation is a future controlled boundary, not execution in this phase. It
contains request_reference, capability_id, scoped input, output Evidence
schema, resource envelope, expiry, and provenance. It never contains a direct
Goal mutation, Decision command, Action command, or full cognitive state.

## Forbidden initiators and paths

Provider cannot create a need, trigger itself, create a Field, modify Reality,
modify Goal, modify Decision, reach Brain directly, or execute Action. Model
Manager selects/validates provider candidates but does not become a cognitive
authority.

Admission failure returns `Capability Degraded Candidate`, `Capability
Unavailable Candidate`, or `Capability Failure Candidate`; it does not become
a Fact or a Decision.

No real Provider Runtime, Model call, OCR, SLAM, Camera, Hardware, or Action is
authorized.

The output Evidence schema is mandatory. No Model call is permitted.

Provider and Model cannot submit a request. The contract carries an output
Evidence schema. Capability Unavailable Candidate is a failure candidate. No
Model call, No OCR, No SLAM, No Camera, No Hardware, and No Action are
authorized.
