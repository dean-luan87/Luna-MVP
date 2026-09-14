# Cognitive Intent Preservation Contract v1

## Purpose

Intent Preservation prevents a Brain-originated cognitive purpose from being
silently expanded, narrowed, substituted, or converted into a model-local
optimization while it moves through Neural, Attention, Middleware, Capability,
Evidence, and feedback boundaries.

```text
Intent Contract Candidate
├── Original Purpose
├── Non-Negotiable Objective
├── Allowed Interpretation Range
├── Forbidden Transformation
├── Required Evidence
├── Success Evaluation
└── trace_ref
```

| Field | Meaning |
|---|---|
| Original Purpose | Brain-originated reason the information is needed |
| Non-Negotiable Objective | minimum cognitive outcome that may not be removed during translation |
| Allowed Interpretation Range | bounded alternative decompositions that still serve the purpose |
| Forbidden Transformation | known narrowing, expansion, substitution, or action conversion violations |
| Required Evidence | evidence categories required to support the purpose |
| Success Evaluation | candidate criteria for whether returned evidence supports the purpose |
| trace_ref | immutable lineage reference across translation steps |

## Example

For “determine whether the path ahead is suitable for passage,” allowed evidence
may include obstacle, road-boundary, height-difference, and relation evidence.
Forbidden Transformation includes “inspect vehicles only,” “inspect colour
only,” or “scan the whole city” when these no longer meet the original bounded
purpose.

## Boundary

Intent Contract Candidate does not create a Goal, Decision, Action, Truth,
Provider mandate, device command, actual allocation, or State mutation.

