# A-Route Loop Completeness Review v1

## Required candidate path

```text
Reality Evidence
        ↓
Reality Representation
        ↓
World State
        +
Self Model / Goal / Resource
        ↓
Situation Candidate
        ↓
Decision Candidate
        ↓
Execution Boundary Candidate
        ↓
Outcome Reference
        ↓
Value Feedback Candidate
        ↓
Experience Candidate
```

## Completeness criteria

Each node must specify an input contract, output candidate, trace/provenance
reference, uncertainty representation, and an authority boundary. A node may
remain a future execution boundary, but it must not be silently omitted or
replaced by an Action/Outcome assumption.

Completeness does not mean correctness, intelligence, model quality, or real
execution. It means a future controlled simulation can test every transition
without crossing an undefined architecture gap.
