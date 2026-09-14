# Cognitive Assembly Coordination Model v1

```mermaid
flowchart TD
    AC[Assembly Coordinator] --> MA[Member A]
    AC --> MB[Member B]
    AC --> MC[Member C]
    MA --> EB[Assembly Evidence Bus]
    MB --> EB
    MC --> EB
    EB --> AC
    AC --> NF[Assembly Feedback Package]
```

Members do not privately negotiate. All member contribution, relation metadata, and feedback pass through the Coordinator/Evidence Bus structure. The Coordinator is a routing and structure-maintenance contract only: not an Agent, Goal holder, Decision Maker, Scheduler, Provider caller, or State mutation authority.
