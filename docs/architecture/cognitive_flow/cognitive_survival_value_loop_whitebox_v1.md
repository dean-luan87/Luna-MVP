# Survival Value Loop Whitebox v1

```mermaid
flowchart TD
    SD[Survival Drive] --> SM[Self Model]
    SD --> WM[World Model]
    SM --> SU[Situated Understanding]
    WM --> SU
    SU --> ST[Survival Strategy Candidate]
    ST --> EXB[Future Execution / Outcome Boundary]
    EXB --> VF[Survival Value Feedback Candidate]
    VF --> SE[Self Evaluation Candidate]
    SE --> EC[Experience Consolidation Candidate]
    EC --> UP[Self Update Candidate]
    CON[Survival Constitution] -. constrains .-> ST
    CON -. constrains .-> VF
    RC[Reality Cognition] --> VF
    EM[Emotional Cognition] --> VF
```

## Display boundary

The future Whitebox shows candidate provenance, physical/capability/
relationship/meaning value dimensions, uncertainty, validation status, and
constitutional constraints. It cannot display a reward score as truth, offer
an execution button, or mutate Strategy, Self Model, Experience, or State.
