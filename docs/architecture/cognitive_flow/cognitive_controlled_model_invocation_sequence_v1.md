# Controlled Model Invocation Sequence v1

## Architecture sequence

```mermaid
sequenceDiagram
    participant B as Cognitive Brain
    participant N as Neural Governance
    participant M as Cognitive Middleware
    participant PM as Provider Management
    participant P as Provider
    participant G as Evidence Gateway

    B->>N: Cognitive Intent Candidate
    N->>M: Cognitive Work Objective
    M->>PM: Capability Requirement / Execution Candidate
    PM-->>M: Provider Candidate / resource / lifecycle status
    M-->>N: Situation / feasibility candidate
    Note over M,P: Future controlled admission only; not implemented
    M->>P: Provider Session Candidate
    P-->>G: Provider output/status candidate
    G-->>M: Evidence Candidate
    M-->>N: Middleware Report
    N-->>B: Neural Feedback / Brain Update Candidate
```

## First controlled-chain scenario

The first future validation target is intentionally narrow: “locate a designated target/sign region in an input image.”

1. Brain Intent: understand where an exit-sign region may be.
2. Neural: CWO requests target-region, text-location, and relationship evidence.
3. Middleware: resolves a `visual_region_understanding` capability requirement and Provider Candidate Set.
4. Provider: future bounded model output only.
5. Evidence Gateway: packages the output with source, confidence, uncertainty, and trace.
6. Neural: aligns coverage against CWO; Brain receives an update candidate.

No image, OCR, VLM, segmentation model, camera, or provider is connected by this phase.
