# Assembly Completion Evaluation Model v1

Assembly reports coverage, conflict, unknowns, and partial evidence only.

```mermaid
flowchart LR
    A[Assembly Evidence Package] --> N[Neural Alignment Candidate]
    N --> B[Brain Evaluation]
    B --> C[Continue / Complete Candidate]
```

Assembly, Middleware, and Provider cannot declare cognitive completion. A package with text and spatial coverage but unknown risk remains a partial cognitive output.
