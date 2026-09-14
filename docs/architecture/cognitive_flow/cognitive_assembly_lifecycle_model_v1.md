# Cognitive Assembly Lifecycle Model v1

```mermaid
stateDiagram-v2
    Candidate --> Created: governance admission candidate
    Created --> Initializing: binding candidates prepared
    Initializing --> Active: bounded activation candidate
    Active --> Maintained: relevance remains
    Maintained --> Reduced: lower value or constrained resources
    Reduced --> Suspended: no current cognitive need
    Suspended --> Active: renewed trigger candidate
    Active --> Archived: experience-validation candidate
    Archived --> Released: retention/reuse boundary complete
    Suspended --> Released: closure candidate
```

Goal completion, timeout, resource reclamation, and failure replacement are closure/replacement signals only. They do not auto-mutate State or create a replacement Assembly.
