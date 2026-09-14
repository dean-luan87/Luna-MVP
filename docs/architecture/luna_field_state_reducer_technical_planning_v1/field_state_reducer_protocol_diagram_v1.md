# Field State Reducer Protocol Diagram v1

## Event -> Reducer -> State 主链
```mermaid
flowchart LR
    E[Admitted Field Events] --> R[Field State Reducer]
    R --> S[Field State]
```

## Input Admission Boundary
```mermaid
flowchart TD
    A[Raw Observation] --> X[BLOCKED]
    B[Provider Response] --> X
    C[Admitted Event] --> D[Reducer Input Contract]
    D --> R[Reducer]
```

## Temporal Reduction Flow
```mermaid
flowchart TD
    T1[Temporal Snapshot] --> T2[Temporal Gating]
    T2 --> T3[Exclude revoked/expired]
    T3 --> T4[Eligible Event Set]
```

## Conflict Preservation Flow
```mermaid
flowchart TD
    C1[Contradictory Events] --> C2[Conflict Matrix]
    C2 --> C3[Preserve Conflict]
    C3 --> C4[state_status conflicted/unresolved]
```

## Replay Flow
```mermaid
flowchart LR
    R1[Event Set Snapshot] --> R2[Ordering Snapshot]
    R2 --> R3[Reducer Version Snapshot]
    R3 --> R4[Deterministic Replay]
    R4 --> R5[Same State + Same Trace]
```

## State Supersession Flow
```mermaid
flowchart LR
    S1[Old Active State] --> S2[New Eligible Events]
    S2 --> S3[Reducer Decision]
    S3 --> S4[New Active State]
    S4 --> S5[Old State Superseded]
```

## Illegal Direct Mutation Blocking
```mermaid
flowchart TD
    V[Vision] --> B[Mutation Block Gate]
    O[OCR] --> B
    N[Navigation] --> B
    M[Memory] --> B
    B --> R[Reducer Only Mutation Path]
```
