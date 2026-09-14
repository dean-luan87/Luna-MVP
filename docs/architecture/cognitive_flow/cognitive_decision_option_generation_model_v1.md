# Decision Option Generation Model v1

## Purpose

Option Generation forms a non-ranked set of possible paths from the current
Situation Candidate. An option is not a recommendation, Decision, Action, or
execution plan.

```text
Situation + Self Capability + Experience Reference + Rules + Survival Strategy
                                      ↓
                        Option Generation Candidate Set
```

| Source | Contribution | Restriction |
|---|---|---|
| Situation Candidate | current constraints, opportunities, unknowns | cannot preselect an option |
| Self Capability | capability fit and boundary | no imaginary current capability |
| Experience | comparable pattern reference | no direct strategy override |
| Rules / Constitution | permitted and prohibited option space | no automatic decision |
| Survival Strategy | long-term continuity consideration | not an independent goal source |

Example: for a road closure, candidates may include rerouting, waiting,
requesting user clarification, or reframing the current goal. They carry
assumptions, requirements, unknowns, and `trace_ref`; no option is preferred
until evaluation.
