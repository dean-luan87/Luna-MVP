# Self Awareness Loop Review v1

## Closed loop

```text
Hardware State
      ↓
Capability State
      ↓
Self Capability Candidate
      ↓
A Route Evaluation
      ↓
Decision Constraint
```

The loop must preserve cause, confidence, provenance, limitation, and Unknown.
Hardware State is an observation of the body; it is not a Decision or a Goal.

## Camera degradation review case

```text
Camera health degraded
      ↓
Vision capability confidence decreases
      ↓
Self Capability Candidate: visual reliability limited
      ↓
A Route requests other evidence / lowers confidence
      ↓
Brain evaluates constrained options
```

The failure must not directly rewrite World State. It must not become “Luna
cannot see”, a new identity, an Emotion, or a permanent Goal. Registry,
Diagnostics, Neural, and Middleware supply candidates; Self Model and Brain use
their governed abstractions.

## Continuity checks

Identity remains stable while Capability, Resource, Health, and Limitation may
change. Adoption remains Candidate → Validation → Adoption. Reducer remains the sole State mutation authority.
