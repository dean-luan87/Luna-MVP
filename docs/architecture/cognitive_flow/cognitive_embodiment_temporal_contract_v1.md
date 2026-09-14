# Cognitive–Embodiment Temporal Contract v1

```mermaid
flowchart LR
    CR[Cognitive Requirement] --> TR[Temporal Requirement Candidate]
    TR --> CAP[Capability Requirement Candidate]
    CAP --> HC[Hardware Capability Candidate]
    HC --> HP[Hardware Protocol Boundary]
```

Example: `visual_observation` may propose latency <100ms, high frequency, and 10s duration; it never says “open camera.” Middleware matches capability/resource candidates; Hardware Protocol alone governs device operations.
