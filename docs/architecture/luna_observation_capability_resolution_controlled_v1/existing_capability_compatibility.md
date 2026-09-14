# Existing Capability Compatibility

Repository 已有：

- `CapabilityRequirementV1` 与 Need→Capability Requirement bridge；
- `CapabilityModuleV1`、`UniversalCapabilitySlotV1` 与既有 readiness/scope resolver；
- Capability Registry / Capability Governance 与 Capability Admission Governance；
- Model Manager 的 model/provider admission boundary。

既有 `CapabilityRequirementV1` 以 purpose、operation、input/output contract、scope
与 slot readiness 为中心，不能直接承载本阶段 Demand lineage 及“一个显式 class
对应多个 controlled candidates”的最小 handoff。因此本阶段增加窄的
`ObservationDemandCapabilityRequirementAdapterV1` 与 read-only inventory projection，
仍位于既有 `universal_capability_slot` owner namespace，不创建第二套 registry。

Capability Slot 仍由 Capability Registry/Governance 管理。本阶段只读取 opaque
`slot_ref`，不 bind、reserve、activate 或改变 slot state。未来由 Capability
Governance / Model Manager 负责 concrete Provider/Model binding。
