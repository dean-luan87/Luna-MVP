# Reality–Reflection Dual Loop Whitebox v1

```mermaid
flowchart TD
    SD[Survival Drive] --> SM[Self Model]
    SD --> A[A Reality Cognition]
    WS[Current World State] --> A
    SM --> A
    A --> SU[Situated Understanding]
    SU --> DB[Brain Decision Candidate Boundary]
    SU --> EX[Experience / Outcome Reference]
    EX --> VF[Value Feedback Candidate]
    VF --> B[B Reflective Cognition]
    SM --> B
    B --> RS[Reflective Resource Budget Candidate]
    RS --> CS[Counterfactual / Hypothetical Reflection]
    CS --> RC[Strategy / Self Understanding Candidate]
    RC --> VA[Validation + Reality Feasibility]
    VA --> AD[Adoption Candidate]
    AD -. future governed influence only .-> A
```

The Whitebox must show whether each node is Reality-bound or hypothetical,
its trace reference, uncertainty, depth/budget, validation/adoption status,
and the absence of a direct B-to-A control path. It is read-only and cannot
serve as a Sandbox, action console, or State mutation interface.
