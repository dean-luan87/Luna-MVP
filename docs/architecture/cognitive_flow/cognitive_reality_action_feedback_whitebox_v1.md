# Reality Action Feedback Loop Whitebox v1

```mermaid
flowchart TD
    E[Evidence] --> R[Reality Representation]
    R --> W[World State]
    SM[Self Model] --> S[Situation Understanding]
    W --> S
    S --> D[Decision Candidate]
    D --> ER[Execution Request Candidate]
    ER --> XB[Future Action Execution Boundary]
    XB --> ES[Execution Status Candidate]
    ES --> OE[Outcome Evidence / Observation Candidate]
    D --> EO[Expected Outcome Candidate]
    EO --> PA[Prediction–Outcome Alignment]
    OE --> PA
    PA --> FA[Failure Analysis Candidate]
    OE --> VF[Survival Value Feedback Candidate]
    FA --> AC[Adaptive Correction Candidate]
    VF --> EX[Experience Consolidation Candidate]
    AC --> EX
    EX -. governed future reflection only .-> B[B Reflection]
```

The Whitebox shows the Decision/Action/Outcome/Evaluation separation,
provenance, expected-versus-observed difference, failure-class uncertainty,
and every candidate's future-only status. It cannot expose an execution
control, auto-correct an Action, or mutate State.
