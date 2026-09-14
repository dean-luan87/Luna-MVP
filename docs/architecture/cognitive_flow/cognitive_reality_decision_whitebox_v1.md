# Reality Decision Formation Whitebox v1

```mermaid
flowchart TD
    E[Evidence] --> WS[World State]
    SM[Self Model] --> SU[Situation Understanding]
    WS --> SU
    GC[Goal / Resource Context] --> SU
    SU --> OG[Option Generation Candidate Set]
    OG --> DE[Decision Evaluation Candidates]
    DE --> DC[Decision Candidate]
    DC --> BE[Brain Evaluation / Approval Candidate]
    BE --> NO[Neural Organization Candidate]
    NO --> XB[Future Capability Execution Boundary]
    EX[Experience Reference] -. candidate-only .-> OG
    SV[Survival Value Alignment] -. candidate-only .-> DE
```

The future Whitebox shows option assumptions, priority conflicts, evidence and
experience references, capability/resource constraints, confidence/unknowns,
and path class (Fast/Normal/Deep). It must never expose an action control,
automatically choose an option, or hide the Decision/Action boundary.
