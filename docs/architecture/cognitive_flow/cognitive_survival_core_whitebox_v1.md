# Cognitive Survival Core Whitebox v1

```mermaid
flowchart TD
    SD[Survival Drive] --> SM[Self Model]
    SD --> WM[World Model]
    SM --> DW[Dual World Cognition]
    WM --> DW
    DW --> SU[Situation Understanding]
    SU --> NR[Neural Regulation Candidate]
    NR --> CG[Capability Governance Candidate]
    CG --> EX[Experience Candidate]
    EX --> UP[Self Update Candidate]
    CON[Survival Constitution] -. constrains all candidates .-> SD
    CON -. constrains all candidates .-> DW
    CON -. constrains all candidates .-> CG
```

## Display contract

The future Whitebox displays sources, candidate type, trace reference,
uncertainty, constitutional constraints, and boundary status. It must not show
a fabricated inner state as fact, expose an action control, or provide a
direct State-mutation path.
