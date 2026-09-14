# Workspace–Neural Interaction Contract v1

## Normal loop contract

```text
Capability → Evidence → Reality Workspace → Neural Processing → Workspace Update
```

Workspace exposes a bounded projection containing current state, validity,
confidence, Unknown, conflict, temporal change, and resource references. Neural
returns a Monitoring Observation Candidate, State Refresh Candidate, Attention
Maintenance Candidate, Resource Allocation Candidate, or Escalation Candidate.

## Abnormal loop contract

```text
Unknown ↑ / Risk ↑ / Conflict ↑
          ↓
Escalation Candidate
          ↓
Situation Candidate
          ↓
Brain Evaluation
```

Neural cannot turn a candidate into a Decision or Action. Reality Workspace does
not receive a Goal change from Neural. Reducer remains the sole State mutation authority.

## Driver separation

Brain Driven Observation expresses what information is needed for a cognitive
purpose. Neural Driven Monitoring detects passive changes that deserve review.
Both paths preserve provenance and intent references where applicable.
