# A-Route Final Whitebox v1

```mermaid
flowchart TD
    RE[Reality Evidence] --> RR[Reality Representation]
    RR --> WS[World State]
    SS[Self State] --> SU[Situation Understanding]
    WS --> SU
    SU --> DC[Decision Candidate]
    DC --> XB[Execution Boundary]
    XB --> OE[Outcome Evidence]
    OE --> VF[Value Feedback]
    VF --> EC[Experience Candidate]
    EC --> RI[Reflection Interface]
    RI -. delayed future candidate only .-> B[B Reflection]
```

The final Whitebox exposes provenance, uncertainty, authority boundary, baseline status, and handoff status.
It does not expose action controls, B-to-current-A control, or State mutation controls.
