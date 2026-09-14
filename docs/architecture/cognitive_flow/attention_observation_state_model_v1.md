# Attention Observation State Model v1

## Purpose

Attention Observation State records which region, entity, attribute, or relation
is currently being observed, with coverage, freshness, source, confidence, and
observation window. It is a state record, not Attention Decision.

```text
Observation Request / Passive Signal
              ↓
       Observation State
              ↓
       Evidence Provenance
```

## Boundary

The state says what was observed and how fresh the observation is. It does not decide
what should receive attention, why an object matters, what Luna should do,
or which process wins resource competition. Attention Governance and A Route own
those interpretations.
