# A-Route Reality Cognition Final Architecture Map v1

```mermaid
flowchart TD
    SD[Survival Drive] --> RCS[Reality Cognition System]
    RCS --> W[World Understanding]
    RCS --> S[Self Understanding]
    W --> U[Situation Understanding]
    S --> U
    U --> D[Decision Formation]
    D --> A[Action Feedback]
    A --> F[Adaptation Feedback]
    F --> EI[Experience Interface]
    EI --> B[Reflection System B]
```

This map is architectural only.
Action Feedback contains an execution boundary, not an Action Runtime.
Experience Interface exports candidates, not memory writes or live B control signals.
