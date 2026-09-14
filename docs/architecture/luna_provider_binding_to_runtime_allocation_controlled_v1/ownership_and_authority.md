# Ownership and authority

- Provider identity、provider target 与 Provider Binding candidate：Provider Governance。
- Provider Binding authoritative decision：本阶段不形成；未来仍由 Provider Governance owner 决定。
- Runtime allocation preparation、execution identity lifecycle：Runtime Executor / Resource boundary。
- `execution_instance_ref` 是实际执行身份；本阶段不生成。
- `BoundedProviderSessionCandidateV1` 属于 FPO 的语义/session candidate；实际 session 不在本阶段启动。
- Observation Gateway 仍只负责 runtime observation ingress/admission proof，不参与本阶段。

Candidate preparation 不拥有 Provider Binding Decision、Runtime Authority、Truth Authority 或 Gateway Authority。
