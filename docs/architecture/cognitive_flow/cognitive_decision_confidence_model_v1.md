# Decision Confidence Model v1

## Purpose

Decision Confidence expresses how well a Decision Candidate is supported; it
does not say that a choice is true or guaranteed to succeed.

```text
Evidence + Experience Reference + Capability Fit + Unknowns
                             ↓
              Decision Confidence Candidate
```

| Factor | Effect on confidence candidate |
|---|---|
| Evidence coverage/provenance | establishes support quality, never truth |
| Experience relevance | contributes only when context is comparable and validated |
| Capability feasibility | exposes whether the option is presently supportable |
| Unknown/risk/conflict | reduces confidence and remains visible |

Low confidence creates a candidate to seek more information, reduce risk,
defer, or request user confirmation. It cannot force a decision, disguise
unknown as negative evidence, or directly invoke a Provider.
