# Cognitive Process Lifecycle Model v1

```mermaid
stateDiagram-v2
    Dormant --> Triggered: signal / context / CWO candidate
    Triggered --> Active: governance admission candidate
    Active --> Maintained: continuing relevance candidate
    Maintained --> Reduced: lower value or resource constraint candidate
    Reduced --> Suspended: no current relevance candidate
    Suspended --> Triggered: renewed evidence or context candidate
    Active --> Closed: bounded closure candidate
    Reduced --> Closed: invalidation or closure candidate
```

Every transition is a candidate and remains Reducer-free. Time is not a sole expiration rule: Goal relevance, risk, unknown impact, expected value, and resource cost are considered. No Process may become permanently active by default.
