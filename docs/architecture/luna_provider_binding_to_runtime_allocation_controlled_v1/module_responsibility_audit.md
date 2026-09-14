# Module responsibility audit

| Module | Requester | Owns | Does not own |
|---|---|---|---|
| Observation Demand | Cognitive Requirement / Need | WHAT information is needed | provider/resource internals |
| Capability Resolution | Observation Demand | capability compatibility | cognitive reinterpretation |
| Perception Routing / FPO compatibility | Capability Resolution / Routing | perception handoff shape | provider binding |
| Provider Target Preparation | FPO compatibility | explicit provider target eligibility | model inference, binding, allocation |
| Provider Binding | Provider Target Preparation | provider binding candidate boundary | runtime/resource allocation |
| Runtime Allocation | Provider Binding | runtime/resource preparation | semantic requirement |
| Execution Instance | Runtime Allocation | concrete execution identity lifecycle | provider choice, observation meaning |
| Observation Gateway | Runtime Observation Envelope | runtime ingress/admission proof | provider selection, cognition |

责权原则：`Requester owns requirement complexity; Executor owns execution complexity.` 本阶段未新增 Provider、Runtime 或 Governance super-owner。
