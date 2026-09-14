# Ownership and Boundaries

| Concept | Owner | This phase |
|---|---|---|
| Observation Demand | Cognitive Flow Observation Demand Formation | read |
| Capability Requirement handoff | Capability Registry / Capability Governance bridge | form minimal mapping projection |
| Capability inventory / class / admission | Capability Registry / Capability Governance | read controlled snapshot |
| Capability Slot lifecycle | Capability Registry / Capability Admission Governance | read-only metadata only |
| Provider / Model binding | Model Manager / Provider Governance | deferred |
| Perception routing / execution | FPO / Observation Gateway / runtime | deferred |

`Strategy.required_capability_class_refs` 是 Acquisition Strategy 上游显式 capability
class hint/basis 的 carry-forward 字段；本阶段不会把它自动升级为本 canonical
Demand requirement。Requirement 必须来自本阶段的 explicit governed mapping。

不修改 Demand、Strategy、Coordination、Need、Branch、Requirement satisfaction、
Current World、Field 或 Memory。解析结果不激活、预留、绑定或执行 capability。
