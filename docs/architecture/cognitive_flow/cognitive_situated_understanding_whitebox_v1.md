# Situated Understanding Whitebox v1

```mermaid
flowchart TD
    P[Provider Evidence] --> G[Evidence Gateway]
    G --> R[Reality Representation]
    R --> W[World State Candidate / State Reference]
    W --> S[Situation Assessment]
    SM[Self Model / Self Capability Context] --> S
    GC[Goal Context] --> S
    RC[Resource Context] --> S
    EX[Experience Candidate] -. optional, validated .-> S
    S --> SC[Situation Candidate]
    SC --> BC[Brain Context]
```

The future local Whitebox must expose provenance and uncertainty at each
transition: `evidence_ref`, representation reference, relevant Self Capability
boundary, goal/resource context, unresolved unknowns, and `trace_ref`. It must
show a Situation Candidate, not a Decision or Action.

The presentation is observational only: it is not a runtime control surface,
provider console, or State mutation path.
