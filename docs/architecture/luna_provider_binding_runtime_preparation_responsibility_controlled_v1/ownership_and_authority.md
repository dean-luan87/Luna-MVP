# Ownership and authority

- Provider identity/inventory：Model Manager Provider Registry 与 Provider Runtime Governance boundary。
- Provider admission/lifecycle/health：Provider Runtime Governance。
- Provider Binding：Provider Governance；现有 contract 记录 provider-facing binding，但不替 Model Governance 维护 Model identity。
- Model Binding：Model Governance / Model Manager binding contract。
- Runtime Allocation、Execution Instance、Provider Session：Runtime / resource / provider runtime owner。
- Active-observation semantic control：FPO。
- Runtime ingress admission proof：Observation Gateway。

FPO 不选择 Provider，Gateway 不选择 Provider，Provider Target Preparation 也不产生需求。Adapter 只转换 shape、carry refs、保持 lineage，不获得新的 Requirement、Provider、Runtime 或 Gateway authority。
