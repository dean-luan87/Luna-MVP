# Reality Cognition System Whitebox v1

```mermaid
flowchart TD
    RE[Reality Evidence] --> RR[Reality Representation]
    RR --> WS[World State]
    SS[Self State / Capability Context] --> SU[Situation Understanding]
    WS --> SU
    GC[Goal / Resource / Experience References] --> SU
    SU --> DF[Decision Formation]
    DF --> XB[Execution Boundary]
    XB --> OO[Outcome Observation Candidate]
    OO --> VF[Value Feedback Candidate]
    VF --> EC[Experience Candidate]
    EC --> FI[Future Improvement Candidate]
    EC -. external A-to-B interface only .-> B[B Reflection]
```

The Whitebox presents system inputs, internal candidate transitions, external
outputs, trace references, uncertainty, and the delayed A-to-B interface. It
does not expose internal modules as controls, provide execution buttons, or
claim that an Action Runtime exists.
