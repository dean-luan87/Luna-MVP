# Intent Requirement Boundary Model v1

## Requirement boundary

```text
Intent Contract Candidate
        ↓
Interpretation Candidate
        ↓
Attention Requirement Candidate
        ↓
Capability Observation Request Candidate
```

Requirement Boundary protects the meaning between purpose and capability.
It limits both unnecessary expansion and unsafe narrowing.

| Boundary question | Required answer |
|---|---|
| What information is minimally required? | Required Evidence categories and unknowns |
| What interpretation is allowed? | bounded scope, region/entity/relation candidates |
| What is forbidden? | transformations that omit non-negotiable objective or substitute a proxy |
| What can constrain the request? | resource, capability, safety, and availability limits |
| How is incompleteness represented? | coverage gap and unknown candidates |

## Example

“Confirm safe passage” must not expand into exhaustive city scanning or narrow
to vehicle-only detection. Capability can state that some evidence is
unavailable; it cannot redefine success as a high local model score.

