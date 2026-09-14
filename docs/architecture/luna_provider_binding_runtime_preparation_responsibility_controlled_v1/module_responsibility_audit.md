# Module responsibility audit

| Module | Requester | Requirement complexity owned by | Module decision | Forbidden complexity |
|---|---|---|---|---|
| Cognitive Requirement | Problem/context | Cognitive Requirement owner | 必要的 semantic requirement | provider/model/runtime |
| Observation Demand | Requirement/Need | Observation Demand owner | WHAT information to observe | provider selection/allocation |
| Capability Resolution | Observation Demand | Capability Governance | matching capability candidates | cognitive goal reinterpretation |
| Perception Routing | Capability Resolution | Perception control boundary | Demand×Capability handoff | Provider/Model choice |
| FPO Compatibility | Perception Routing | FPO compatibility boundary | FPO-compatible handoff shape | provider binding/execution |
| Provider Target Preparation | FPO Compatibility | Provider Governance | explicit Provider target candidates | new Demand/Model inference |
| Provider Binding | Provider Target | Provider Governance | whether a Provider binding can be formed | new Need/target rewrite |
| Runtime Allocation | Provider Binding | Runtime/Resource owner | resource preparation/allocation | cognition reinterpretation |
| Execution Instance | Runtime Allocation | Runtime owner | concrete execution identity | provider choice/meaning |
| Observation Gateway Runtime Admission | Runtime Observation Envelope | Observation Gateway | runtime ingress proof/admission | strategy/provider selection |

每一层只承担一次必要转换。下游不得用模糊文本再次猜测上游 intent。
