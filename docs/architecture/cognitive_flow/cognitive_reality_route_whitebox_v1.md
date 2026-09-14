# A-Route Reality Cognition Foundation Whitebox v1

```mermaid
flowchart TD
    SD[Survival Drive] --> SM[Self Model]
    E[Evidence] --> RR[Reality Representation]
    RR --> WS[World State]
    SM --> SU[Situation Understanding]
    WS --> SU
    SU --> DF[Decision Formation]
    DF --> XB[Execution Boundary]
    XB --> OE[Outcome Observation Candidate]
    OE --> VE[Value Feedback Candidate]
    VE --> EC[Experience Consolidation Candidate]
    EC --> FI[Future Improvement Candidate]
    FC[Failure / Health Candidates] -. locate gaps .-> DF
    OE --> FC
    EC -. A-to-B governed interface .-> B[B Reflection]
```

The future Whitebox must display layer reference, candidate status, evidence
provenance, self-capability/resource context, uncertainty, failure locality,
and A/B interface status. It must not display an action control, claim runtime
completion, hide a boundary, or mutate State.
