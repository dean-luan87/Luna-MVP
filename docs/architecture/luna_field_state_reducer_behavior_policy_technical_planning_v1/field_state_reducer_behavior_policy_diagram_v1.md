# Field State Reducer Behavior Policy Diagram v1

本文件仅用于 Technical Planning，可视化策略选择与约束，不表示 Runtime 已实现。

## 1) Policy Eligibility Flow

```mermaid
flowchart TD
    A[Input Candidate Policies] --> B{Admitted Only?}
    B -- No --> C[Reject Policy]
    B -- Yes --> D{Runtime Callable?}
    D -- Yes --> C
    D -- No --> E{State Write Allowed?}
    E -- Yes --> C
    E -- No --> F[Eligible Policy Set]
```

## 2) Precedence Resolution Flow

```mermaid
flowchart TD
    A[Eligible Policies] --> B{Revocation Present?}
    B -- Yes --> C[Apply revocation_override]
    B -- No --> D{Hard Contradiction?}
    D -- Yes --> E[Apply conflict_preservation]
    D -- No --> F{Evidence Sufficient?}
    F -- No --> G[Apply insufficient_evidence_unresolved]
    F -- Yes --> H[Continue to composition]
```

## 3) Composition Contract Flow

```mermaid
flowchart LR
    A[Policy Sequence Start] --> B[revocation_override]
    B --> C[conflict_preservation]
    C --> D[expiration_degrade]
    D --> E[temporary_overlay_separation]
    E --> F[multi_event_consensus]
    F --> G[highest_confidence_valid_event]
    G --> H[latest_valid_event]
    H --> I[explicit_owner_override_candidate]
    I --> J[insufficient_evidence_unresolved]
    J --> K[negative_event_override]
    K --> L[no_state_change]
```

## 4) Temporal Gate Flow

```mermaid
flowchart TD
    A[Temporal Status] --> B{active or expiring}
    B -- Yes --> C[Support Eligible]
    B -- No --> D{expired/revoked/suspended/superseded/unknown}
    D -- Yes --> E[Support Ineligible]
    E --> F[Degrade or unresolved path]
    D -- No --> G[Refresh required]
```

## 5) Confidence Handling Flow

```mermaid
flowchart TD
    A[State Type] --> B[Select confidence policy]
    B --> C[Apply threshold and caps]
    C --> D{Hard contradiction present?}
    D -- Yes --> E[Apply penalty]
    D -- No --> F[Keep weighted score]
    E --> G{Safe winner exists?}
    F --> G
    G -- Yes --> H[Candidate support]
    G -- No --> I[Conflict or unresolved]
```

## 6) Conflict Preservation Flow

```mermaid
flowchart TD
    A[Contradicting Evidence] --> B{Resolution safe?}
    B -- No --> C[Preserve conflict]
    C --> D[Status = conflicted/unresolved]
    D --> E[No fact promotion]
    E --> F[No direct state write]
    B -- Yes --> G[Proceed with governed candidate]
```

## 7) Owner Correction Governance Flow

```mermaid
flowchart TD
    A[Owner Correction Event] --> B{Provenance complete?}
    B -- No --> C[Reject candidate]
    B -- Yes --> D{Supporting evidence present?}
    D -- No --> C
    D -- Yes --> E[Create provisional candidate]
    E --> F{Contradiction with confirmed fact?}
    F -- Yes --> G[Require review]
    F -- No --> H[Keep candidate state]
```

## 8) Overlay Separation Flow

```mermaid
flowchart TD
    A[Overlay Event] --> B{Overlay active?}
    B -- Yes --> C[Create overlay layer candidate]
    C --> D[Do not mutate substrate]
    D --> E{Overlay expired?}
    E -- Yes --> F[Require substrate refresh evidence]
    E -- No --> G[Keep overlay candidate]
```

## 9) Replay Determinism Flow

```mermaid
flowchart LR
    A[Replay Input] --> B[Load policy registry snapshot]
    B --> C[Load eligibility snapshot]
    C --> D[Load precedence snapshot]
    D --> E[Load composition snapshot]
    E --> F[Compute deterministic replay key]
    F --> G[Produce same decision candidate]
```
