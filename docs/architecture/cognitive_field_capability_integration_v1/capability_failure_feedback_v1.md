# Capability Failure Feedback v1

## Failure taxonomy

Capability failures are returned as structured diagnostics, not as a change
to Reality or a silent success:

- Provider unavailable;
- capability unavailable;
- low-quality Evidence;
- confidence below boundary;
- capability protocol error;
- resource unavailable;
- timeout candidate;
- unsupported input;
- unknown failure.

## Feedback chain

```text
Capability Failure
    ↓
Diagnostics
    ↓
Self Capability Candidate
    ↓
Brain / A Route awareness
```

The chain reports which capability was unavailable, why, its provenance,
confidence, and affected Observation Requirement. It does not assert that the
world changed and does not directly change the Self Model, Goal, Field, or
Decision Policy.

## Human and provider failures

Human Feedback and Provider output both pass through the Evidence Gateway.
Missing human feedback is an Unknown candidate, not a fabricated Fact. A
Provider failure is not a Decision failure unless a later situated evaluation
establishes that relationship.

## Safety boundary

No automatic retry policy, automatic model switching, automatic learning,
automatic Action, or automatic Reality mutation is implemented here. Failure
feedback remains a candidate for governance and later Brain evaluation.
