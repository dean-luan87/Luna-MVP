# Entity Local Autonomy Boundary v1

## Purpose

Entity local autonomy is limited to protecting the local embodiment and preserving its ability to participate safely in future cognitive work. It is not local cognition, independent agency, or a second Brain.

## Allowed local autonomy

| Allowed boundary | Meaning |
|---|---|
| Reflex protection | Bounded local protection response to declared safety/health constraints. |
| Health management | Detect/report local health degradation and protocol condition. |
| Resource protection | Preserve local power, compute, storage, and connection within approved limits. |
| Network recovery | Attempt bounded channel recovery and report state. |
| Local cache | Retain short-lived, scope-bound operational data for trace/session continuity. |

## Prohibited local autonomy

- Create, modify, prioritize, or abandon a Brain Goal;
- modify Value, Identity, Personality, or long-term Memory;
- form an independent Decision or Action;
- execute world-affecting behavior beyond separately authorized body/reflex safety boundaries;
- self-assign a CWO;
- convert local evidence into Truth;
- mutate Brain/Reducer state.

```mermaid
flowchart LR
    L[Entity local health / resource event] --> R[Local protection candidate]
    R --> F[Entity Feedback Candidate]
    F --> N[Neural Governance]
    N --> B[Brain Update Candidate]
```

Local reflex/protection does not create a general action pathway. It remains a future, separately governed embodiment safety boundary and is not implemented in this phase.
